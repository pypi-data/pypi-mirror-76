import re
from copy import deepcopy, copy
import numpy as np
from mdt.component_templates.base import ComponentBuilder, ComponentTemplate
from mdt.lib.components import get_component, has_component
from mdt.models.compartments import DMRICompartmentModelFunction, WeightCompartment, CacheInfo
from mdt.utils import spherical_to_cartesian
from mot.lib.cl_function import CLFunction, SimpleCLFunction, SimpleCLFunctionParameter, SimpleCLCodeObject
from mdt.model_building.parameters import CurrentObservationParam, DataCacheParameter, NoiseStdInputParameter, \
    FreeParameter, ProtocolParameter, AllObservationsParam, ObservationIndexParam, NmrObservationsParam
from mot.optimize.base import SimpleConstraintFunction

__author__ = 'Robbert Harms'
__date__ = "2017-02-14"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


class CompartmentBuilder(ComponentBuilder):

    def _create_class(self, template):
        """Creates classes with as base class CompartmentBuildingBase

        Args:
            template (CompartmentTemplate): the compartment config template to use for
                creating the class with the right init settings.
        """
        builder = self

        class AutoCreatedDMRICompartmentModel(DMRICompartmentModelFunction):

            def __init__(self, nickname=None):
                parameters = _resolve_parameters(template.parameters, template.name)
                dependencies = _resolve_dependencies(template.dependencies)

                if template.cl_extra:
                    extra_code = '''
                        #ifndef {inclusion_guard_name}
                        #define {inclusion_guard_name}
                        {cl_extra}
                        #endif // {inclusion_guard_name}
                    '''.format(inclusion_guard_name='INCLUDE_GUARD_CL_EXTRA_{}'.format(template.name),
                               cl_extra=template.cl_extra)
                    dependencies.append(SimpleCLCodeObject(extra_code))

                super().__init__(
                    template.return_type,
                    template.name,
                    parameters,
                    template.cl_code,
                    dependencies=dependencies,
                    constraints_func=_resolve_constraints(template.constraints, template.name,
                                                          parameters, dependencies),
                    model_function_priors=_resolve_prior(template.prior, template.name,
                                                         [p.name for p in parameters]),
                    extra_optimization_maps_funcs=builder._get_extra_optimization_map_funcs(template, parameters),
                    extra_sampling_maps_funcs= builder._get_extra_sampling_map_funcs(template, parameters),
                    nickname=nickname,
                    cache_info=builder._get_cache_info(template))

        for name, method in template.bound_methods.items():
            setattr(AutoCreatedDMRICompartmentModel, name, method)

        return AutoCreatedDMRICompartmentModel

    def _get_extra_optimization_map_funcs(self, template, parameter_list):
        extra_optimization_maps = copy(template.extra_optimization_maps)
        if all(map(lambda name: name in [p.name for p in parameter_list], ('theta', 'phi'))):
            extra_optimization_maps.append(lambda results: {
                'vec0': spherical_to_cartesian(np.squeeze(results['theta']), np.squeeze(results['phi']))})
        return extra_optimization_maps

    def _get_extra_sampling_map_funcs(self, template, parameter_list):
        extra_sampling_maps = copy(template.extra_sampling_maps)

        def compute(results):
            cartesian = spherical_to_cartesian(np.squeeze(results['theta']), np.squeeze(results['phi']))

            if len(cartesian.shape) == 3:
                return {'vec0': np.mean(cartesian, axis=1), 'vec0.std': np.std(cartesian, axis=1)}
            else:
                return {'vec0': np.mean(cartesian, axis=0)[None, :], 'vec0.std': np.std(cartesian, axis=0)[None, :]}

        if all(map(lambda name: name in [p.name for p in parameter_list], ('theta', 'phi'))):
            extra_sampling_maps.append(compute)
        return extra_sampling_maps

    def _get_cache_info(self, template):
        if template.cache_info is None:
            return None

        fields = []
        for field in template.cache_info['fields']:
            if isinstance(field, str):
                param = SimpleCLFunctionParameter(field)

                ctype = param.ctype
                name = param.name
                nmr_elements = 1
                if param.is_array_type:
                    nmr_elements = np.prod(param.array_sizes)
            else:
                ctype, name = field[:2]
                nmr_elements = 1
                if len(field) == 3:
                    nmr_elements = field[2]

            fields.append((ctype, name, nmr_elements))

        if template.cache_info.get('use_local_reduction', True):
            cl_code = '''
                if(get_local_id(0) == 0){{
                    {}
                }}
                barrier(CLK_LOCAL_MEM_FENCE);
            '''.format(template.cache_info['cl_code'])
        else:
            cl_code = template.cache_info['cl_code']

        return CacheInfo(fields, cl_code)


class WeightBuilder(ComponentBuilder):
    def _create_class(self, template):
        """Creates the weight compartments

        Args:
            template (WeightCompartmentTemplate): the compartment config template
        """
        class AutoCreatedWeightModel(WeightCompartment):

            def __init__(self, nickname=None):
                dependencies = _resolve_dependencies(template.dependencies)

                if template.cl_extra:
                    extra_code = '''
                        #ifndef {inclusion_guard_name}
                        #define {inclusion_guard_name}
                        {cl_extra}
                        #endif // {inclusion_guard_name}
                    '''.format(inclusion_guard_name='INCLUDE_GUARD_CL_EXTRA_{}'.format(template.name),
                               cl_extra=template.cl_extra)
                    dependencies.append(SimpleCLCodeObject(extra_code))

                super().__init__(
                    template.return_type, template.name,
                    _resolve_parameters(template.parameters, template.name), template.cl_code,
                    dependencies=dependencies,
                    nickname=nickname)

        for name, method in template.bound_methods.items():
            setattr(AutoCreatedWeightModel, name, method)

        return AutoCreatedWeightModel


class CompartmentTemplate(ComponentTemplate):
    """The compartment config to inherit from.

    These configs are loaded on the fly by the CompartmentBuilder.

    Attributes:
        name (str): the name of the model, defaults to the class name

        description (str): model description

        return_type (str): the return type of this compartment, defaults to double.

        parameters (list): the list of parameters to use. A few options are possible per item, that is, if given:

            * a string, we will look for a corresponding parameter with the given name
            * an instance of a CLFunctionParameter subclass, this will then be used directly
            * the literal ``@observation``, this injects the current volume/observation into this function
                of type ``mot_float_type`` and name ``observation``.
            * the literal ``@observations``, this injects a pointer to all the observations into this function.
                of type ``float`` and name ``observations``.
            * the literal ``@observation_ind``, the index of the current observation we are computing the signal for,
                of type ``uint`` and name ``observation_ind``.
            * the literal ``@nmr_observation``, injects the total number of observations,
                of type ``uint`` and name ``nmr_observation``.
            * the literal ``@cache``, this injects the data cache into this function, with the name ``cache``
                and a struct as datatype. The struct type name is provided by this compartment name appended with
                ``_DataCache``.
            * the literal ``@noise_std``, this injects the current value of the noise standard sigma parameter value
                 of the likelihood function in this parameter.

        dependencies (list): the list of functions this function depends on, can contain string which will be
            resolved as library functions.

        cl_code (str): the CL code definition to use, please provide here the body of your CL function.

        cl_extra (str): additional CL code for your model. This will be prepended to the body of your CL function.

        constraints (str or None): additional inequality constraints for this model. Each constraint needs to be
            implemented as ``g(x)`` where we assume that ``g(x) <= 0``. For example, to implement a simple inequality
            constraint like ``d >= dperp0``, we first write it as ``dperp0 - d <= 0``. We can then implement it as::

                constraints = '''
                    constraints[0] = dperp0 - d;
                '''

            To add more constraint, add another entry to the ``constraints`` array. MDT parses the given text and
            automatically recognizes the model parameter names and the number of constraints.

        prior (str or None): an extra MCMC sample prior for this compartment. This is additional to the priors
            defined in the parameters. This should be an instance of a CLFunction or a string with a CL function body.
            If the latter, the CLFunction is automatically constructed based on the content of the string.

        cache_info (dict): the data cache information. This works in combination with specifying the ``@cache``
            parameter for this compartment. The cache info should have two elements, ``fields`` and ``cl_code``.
            The fields specify the items we need to store in the structure, the syntax per field is either a string
            like ``double alpha`` or a tuple like ``('double', 'alpha')``. Specifying a tuple also allows for specifying
            arrays like: ``('double', 'beta', 10)``. The CL code given by ``cl_code`` is supposed to fill the cache.
            This cl_code will be wrapped in a function with as arguments all free parameters of the compartments,
            and the cache. The fields in the cache are accessible using ``*cache->alpha``, i.e. dereferencing a pointer
            to a variable using the cache. An optional element in the cache info is "use_local_reduction"
            which specifies that for this compartment we use all workitems in the workgroup. If not set, or if False,
            we will execute the cache CL code only for the first work item. The default is True.

        extra_optimization_maps (list): a list of functions to return extra information maps based on a point estimate.
            This is called after the model calculated uncertainties based on the Fisher Information Matrix.
            Therefore, these routines can propagate uncertainties in the estimates.

            These functions should accept as single argument an object of type
            :class:`mdt.models.composite.ExtraOptimizationMapsInfo`.

            Examples:

            .. code-block:: python

                extra_optimization_maps_funcs = [lambda d: {'FS': 1 - d['w']},
                                                 lambda d: {'Kurtosis.MK': <...>},
                                                 lambda d: {'Power2': d['foo']**2, 'Power3': d['foo']**3},
                                                 ...]

        extra_sampling_maps (list): a list of functions to return additional maps as results from sample.
            This is called after sample with as argument a dictionary containing the sample results and
            the values of the fixed parameters.

            Examples::

                extra_sampling_maps = [lambda s: {'MD': np.mean((s['d'] + s['dperp0'] + s['dperp1'])/3., axis=1)}
                                      ...]
    """
    _component_type = 'compartment_models'
    _builder = CompartmentBuilder()

    name = ''
    description = ''
    parameters = []
    cl_code = None
    cl_extra = None
    dependencies = []
    return_type = 'double'
    prior = None
    extra_optimization_maps = []
    extra_sampling_maps = []
    cache_info = None
    constraints = None


class WeightCompartmentTemplate(ComponentTemplate):
    """Special compartment template for representing a Weight.

    Defining a compartment as a Weight enables automatic volume fraction weighting, and ensures that all weights sum
    to one during optimization and sample.
    """
    _component_type = 'compartment_models'
    _builder = WeightBuilder()

    name = ''
    description = ''
    parameters = []
    cl_code = None
    cl_extra = None
    dependencies = []
    return_type = 'double'


def _resolve_dependencies(dependencies):
    """Resolve the dependency list such that the result contains all functions.

    Args:
        dependencies (list): the list of dependencies as given by the user. Elements can either include actual
            instances of :class:`~mot.library_functions.CLLibrary` or strings with the name of libraries or
            other compartments to load.

    Returns:
        list: a new list with the string elements resolved as :class:`~mot.library_functions.CLLibrary`.
    """
    if not len(dependencies):
        return []

    result = []
    for dependency in dependencies:
        if isinstance(dependency, str):
            if has_component('library_functions', dependency):
                result.append(get_component('library_functions', dependency)())
            else:
                result.append(get_component('compartment_models', dependency)())
        else:
            result.append(dependency)

    return result


def _resolve_prior(prior, compartment_name, compartment_parameters):
    """Create a proper prior out of the given prior information.

    Args:
        prior (str or mot.lib.cl_function.CLFunction or None):
            The prior from which to construct a prior.
        compartment_name (str): the name of the compartment
        compartment_parameters (list of str): the list of parameters of this compartment, used
            for looking up the used parameters in a string prior

    Returns:
        List[mdt.models.compartments.CompartmentPrior]: the list of extra priors for this compartment
    """
    if prior is None:
        return []

    if isinstance(prior, CLFunction):
        return [prior]

    parameters = ['mot_float_type ' + p for p in compartment_parameters if p in prior]
    return [SimpleCLFunction('mot_float_type', 'prior_' + compartment_name, parameters, prior)]


def _resolve_constraints(constraint, compartment_name, compartment_parameters, dependencies):
    """Create a constraint function out of the given constraint information.

    Args:
        constraint (str or None): The string containing the constraints
        compartment_name (str): the name of the compartment
        compartment_parameters (list of parameters): the list of parameters of this compartment
            We only use the free and protocol parameters in the constraint functions.

    Returns:
        mot.optimize.base.ConstraintFunction: the constraint function for this compartment model
    """
    if constraint is None:
        return None

    constraint_refs = re.findall(r'constraints\[(\d+)\]', constraint)

    if not constraint_refs:
        return None

    nmr_constraints = max(map(int, constraint_refs)) + 1

    parameters = []
    for param in compartment_parameters:
        if isinstance(param, (FreeParameter, ProtocolParameter)):
            parameters.append(param)

    return SimpleConstraintFunction('void', compartment_name + '_constraints',
                                    parameters + ['local mot_float_type* constraints'],
                                    constraint, dependencies=dependencies, nmr_constraints=nmr_constraints)


def _resolve_parameters(parameter_list, compartment_name):
    """Convert all the parameters in the given parameter list to actual parameter objects.

    Args:
        parameter_list (list): a list containing a mix of either parameter objects, strings or tuples. If it is a
            parameter we add a copy of it to the return list. If it is a string we will autoload it. It is possible to
            specify a nickname for that parameter in this compartment using the syntax: ``<param>(<nickname>)``.

    Returns:
        list: the list of actual parameter objects
    """
    if not parameter_list:
        return []

    parameters = []
    for item in parameter_list:
        if isinstance(item, str):
            if item == '@observation':
                parameters.append(CurrentObservationParam(name='observation'))
            elif item == '@observations':
                parameters.append(AllObservationsParam(name='observations'))
            elif item == '@observation_ind':
                parameters.append(ObservationIndexParam(name='observation_ind'))
            elif item == '@nmr_observations':
                parameters.append(NmrObservationsParam(name='nmr_observations'))
            elif item == '@cache':
                parameters.append(DataCacheParameter(compartment_name, 'cache'))
            elif item == '@noise_std':
                parameters.append(NoiseStdInputParameter(name='noise_std'))
            else:
                if '(' in item:
                    param_name = item[:item.index('(')].strip()
                    nickname = item[item.index('(')+1:item.index(')')].strip()
                else:
                    param_name = item
                    nickname = None
                parameters.append(get_component('parameters', param_name)(nickname=nickname))
        elif isinstance(item, (tuple, list)):
            parameters.append(SimpleCLFunctionParameter(item[0] + ' ' + item[1]))
        else:
            parameters.append(deepcopy(item))
    return parameters
