import logging
from collections import Mapping
from textwrap import dedent
import copy
import collections
import numpy as np
from mdt.configuration import get_active_post_processing
from mdt.lib.deferred_mappings import DeferredFunctionDict
from mdt.lib.exceptions import DoubleModelNameException
from mdt.model_building.model_functions import WeightType
from mdt.model_building.parameter_functions.dependencies import SimpleAssignment, AbstractParameterDependency
from mdt.model_building.utils import ParameterCodec

from mot.lib.cl_function import SimpleCLFunction, SimpleCLFunctionParameter
from mot.cl_routines import compute_log_likelihood, estimate_hessian
from mdt.model_building.parameters import ProtocolParameter, FreeParameter, CurrentObservationParam, \
    DataCacheParameter, CurrentModelSignalParam, NoiseStdFreeParameter, NoiseStdInputParameter, PolarAngleParameter, \
    AzimuthAngleParameter, RotationalAngleParameter, AllObservationsParam, ObservationIndexParam, NmrObservationsParam
from mot.configuration import CLRuntimeInfo
from mot.lib.utils import all_elements_equal, get_single_value
from mot.lib.kernel_data import Array, Zeros, Scalar, LocalMemory, Struct, CompositeArray, PrivateMemory

from mdt.models.base import MissingProtocolInput
from mdt.models.base import EstimableModel
from mdt.utils import calculate_point_estimate_information_criterions, is_scalar, split_array_to_dict, \
    create_covariance_matrix
from mot.library_functions import pseudo_inverse_real_symmetric_matrix_upper_triangular
from mot.mcmc_diagnostics import multivariate_ess, univariate_ess
from mot.optimize.base import SimpleConstraintFunction

__author__ = 'Robbert Harms'
__date__ = "2014-10-26"
__license__ = "LGPL v3"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


class DMRICompositeModel(EstimableModel):

    def __init__(self, model_name, model_tree, likelihood_function, signal_noise_model=None, input_data=None,
                 enforce_weights_sum_to_one=True, volume_selection=True):
        """A model builder for a composite dMRI sample and optimization model.

        It implements some protocol check functions. These are used by the fit_model functions in MDT
        to check if the protocol is correct for the model we try to fit.

        Args:
            model_name (str): the name of the model
            model_tree (mdt.model_building.trees.CompartmentModelTree): the model tree object
            likelihood_function (mdt.model_building.likelihood_functions.LikelihoodFunction): the likelihood function to
                use for the resulting complete model.
            signal_noise_model (mdt.model_building.signal_noise_models.SignalNoiseModel): the optional signal
                noise model to use to add noise to the model prediction
            input_data (mdt.lib.input_data.MRIInputData): the input data container
            enforce_weights_sum_to_one (boolean): if we want to enforce that weights sum to one. This does the
                following things; it fixes the first weight to the sum of the others and it adds a transformation
                that ensures that those other weights sum to at most one.
            volume_selection (boolean): if we should do volume selection or not, set this before
                calling ``set_input_data``.

        Attributes:
            _constraints (List[mot.optimize.base.ConstraintFunction]): the constraint functions
            _model_priors (List[mot.lib.cl_function.CLFunction]): the list of model priors this class
                will also use (next to the priors defined in the parameters).
            _proposal_callbacks (Iterable[Tuple[Tuple[CompartmentFunction, CLFunctionParameter], CLFunction]]):
                the list of proposal callbacks. Each element in the list consists of a tuple with two elements,
                first a reference to the used compartments (as a list of (compartment, parameter) tuples),
                second the CL function to call (using those parameters).

                Proposals generated during sample may sometimes require transformations to transform the proposal
                vector. For example, in the case of sample a spherical coordinate system, this callback can be used
                to transform both the inclination and the azimuth at the same time to an antipodal point.
        """
        super().__init__(model_name, model_tree, likelihood_function, signal_noise_model,
                         input_data=input_data, enforce_weights_sum_to_one=enforce_weights_sum_to_one)
        self._name = model_name
        self._model_tree = model_tree
        self._likelihood_function = likelihood_function
        self._signal_noise_model = signal_noise_model
        self.volume_selection = volume_selection

        self._enforce_weights_sum_to_one = enforce_weights_sum_to_one

        self._model_functions_info = ModelFunctionsInformation(model_tree, likelihood_function, signal_noise_model,
                                                               enable_prior_parameters=True)

        self._lower_bounds = {'{}.{}'.format(m.name, p.name): p.lower_bound for m, p in
                              self._model_functions_info.get_free_parameters_list()}

        self._upper_bounds = {'{}.{}'.format(m.name, p.name): p.upper_bound for m, p in
                              self._model_functions_info.get_free_parameters_list()}

        self._input_data = None
        if input_data:
            self.set_input_data(input_data)

        self._set_default_dependencies()

        self._constraints = []
        self._model_priors = []

        if self._enforce_weights_sum_to_one:
            weight_prior = self._get_weight_prior()
            if weight_prior:
                self._model_priors.append(weight_prior)

        for compartment in self._model_functions_info.get_model_list():
            priors = compartment.get_model_function_priors()
            if priors:
                for prior in priors:
                    self._model_priors.append(_ModelFunctionPriorToCompositeModelPrior(prior, compartment.name))

        self._logger = logging.getLogger(__name__)
        self._original_input_data = None

        self._extra_optimization_maps_funcs = []
        self._extra_sampling_maps_funcs = []

        if self._enforce_weights_sum_to_one:
            self._extra_optimization_maps_funcs.append(self._get_propagate_weights_uncertainty)

        self.nmr_parameters_for_bic_calculation = self.get_nmr_parameters()
        self._post_processing = get_active_post_processing()

    @property
    def name(self):
        return self._name

    def get_composite_model_function(self):
        """Get the composite model function for the current model tree.

        The output model function of this class is a subclass of :class:`~mot.lib.cl_function.CLFunction` meaning it can
        be used to evaluate the model given some input parameters.

        This function does not incorporate the likelihood function (Gaussian, Rician, etc.), but does incorporate the
        signal noise model (JohnsonNoise for example).

        Returns:
            CompositeModelFunction: the model function for the composite model
        """
        return CompositeModelFunction(self._model_tree, signal_noise_model=self._signal_noise_model)

    def get_kernel_data(self):
        """Get the kernel data this model needs for evaluation in OpenCL.

        This is needed for evaluating the priors, likelihoods and other functions.

        Returns:
            mot.lib.kernel_data.KernelData: the kernel data used by this model
        """
        data_items = {
            'local_tmp': LocalMemory('double'),
            'bounds': self._get_bounds_as_var_data(),
            'protocol': self._get_protocol_data_as_var_data(),
            'protocol_update_cbs': self._get_protocol_update_callbacks_kernel_inputs(),
            'cache': self._get_cache_struct()
        }
        data_items.update(self._get_observations_data())
        data_items.update(self._get_fixed_parameters_as_var_data())

        if self._input_data.volume_weights is not None:
            data_items.update({'volume_weights': Array(self._input_data.volume_weights.astype(np.float16))})

        return Struct(data_items, '_mdt_model_data')

    def get_objective_function(self):
        """For minimization, get the negative of the log-likelihood function."""
        return self._get_log_likelihood_function(True, True)

    def get_constraints_function(self):
        """The function for the (inequality) constraints."""
        return self._get_constraints_function()

    def get_log_likelihood_function(self):
        """For sampling, get the log-likelihood function."""
        return self._get_log_likelihood_function(False, False)

    def get_log_prior_function(self):
        """Get the prior function used during sampling."""
        return self._get_log_prior_function()

    def get_finalize_proposal_function(self):
        """Get the function used to finalize the proposal.

        This function is used to finalize the proposals during sampling.

        Returns:
            mot.lib.cl_function.CLFunction: the CL function used to finalize a proposal during sampling.
        """
        return SimpleCLFunction.from_string('''
            void finalizeProposal(void* data, local mot_float_type* x){
                _mdt_model_data* model_data = (_mdt_model_data*)data;
                ''' + '\n'.join(self._get_spherical_transformations()) + '''
                ''' + '\n'.join(self._get_rotational_transformations()) + '''
            }
        ''', dependencies=[self._get_spherical_transformation_func()])

    def get_initial_parameters(self):
        """Get the initial parameters for all the voxels in the input data.

        Returns:
            ndarray: 2d array with for every problem (first dimension) the initial parameters (second dimension).
        """
        np_dtype = np.float32

        def prepare_value(value):
            if is_scalar(value):
                if self._get_nmr_problems() == 0:
                    value = np.full((1, 1), value, dtype=np_dtype)
                else:
                    value = np.full((self._get_nmr_problems(), 1), value, dtype=np_dtype)
            else:
                if len(value.shape) < 2:
                    value = np.transpose(np.asarray([value]))
                elif value.shape[1] > value.shape[0]:
                    value = np.transpose(value)
                else:
                    value = value
            return value

        starting_points = []
        for ind, (m, p) in enumerate(self._model_functions_info.get_estimable_parameters_list()):
            param_name = '{}.{}'.format(m.name, p.name)
            value = prepare_value(self._model_functions_info.get_parameter_value(param_name))
            starting_points.append(value)

        return np.concatenate([np.transpose(np.array([s]))
                               if len(s.shape) < 2 else s for s in starting_points], axis=1)

    def get_post_optimization_output(self, optimized_parameters, roi_indices=None, parameters_dict=None):
        """Get the output after optimization.

        This is called by the processing strategy to finalize the optimization of a batch of voxels.

        Returns:
            dict: dictionary with results maps, can be nested which should translate to sub-directories.
        """
        if not parameters_dict:
            parameters_dict = split_array_to_dict(optimized_parameters, self.get_free_param_names())
        parameters_dict = self._post_process_optimization_maps(optimized_parameters, roi_indices,
                                                               parameters_dict=parameters_dict)
        return parameters_dict

    def get_rwm_proposal_stds(self):
        """Get the Random Walk Metropolis proposal standard deviations for every parameter and every problem instance.

        These proposal standard deviations are used in Random Walk Metropolis MCMC sample.

        Returns:
            ndarray: the proposal standard deviations of each free parameter, for each problem instance
        """
        return self._get_rwm_proposal_stds()

    def get_rwm_epsilons(self):
        """Get per parameter a value small relative to the parameter's standard deviation.

        This is used in, for example, the SCAM Random Walk Metropolis sampling routine to add to the new proposal
        standard deviation to ensure it does not collapse to zero.

        Returns:
            list: per parameter an epsilon, relative to the proposal standard deviation
        """
        return self._get_rwm_epsilons()

    def get_random_parameter_positions(self, nmr_positions=1):
        """Get one or more random parameter positions centered around the initial parameters.

        This can be used to generate random starting points for sampling routines with multiple walkers.

        Per position requested, this function generates a normal distribution around the initial parameters (using
        :meth:`get_initial_parameters`) with the standard deviation derived from the random walk metropolis std.

        Returns:
            ndarray: a 3d matrix for (voxels, parameters, nmr_positions).
        """
        initial_params = self.get_initial_parameters()
        results = np.zeros((initial_params.shape[:2]) + (nmr_positions,), dtype=initial_params.dtype)
        stds = np.squeeze(self.get_rwm_proposal_stds()) * 2

        for position_ind in range(nmr_positions):
            position = np.random.normal(initial_params, stds)
            position = self.get_mle_codec().encode_decode(position, kernel_data=self.get_kernel_data())

            d = {'{}.{}'.format(m.name, p.name): position[:, ind]
                 for ind, (m, p) in enumerate(self._model_functions_info.get_estimable_parameters_list())}

            d.update(self._get_dependent_map_calculator()(self, d))
            d.update(self._get_fixed_parameter_maps())

            results[..., position_ind] = self._param_dict_to_array(d)
        return results

    def _post_process_optimization_maps(self, parameters_array, roi_indices, parameters_dict=None,
                                        log_likelihoods=None):
        """Create post processing optimization maps.

        The current steps in this function:

            1) Add the maps for the dependent and fixed parameters
            2) Add the fixed maps to the results
            3) Add information criteria maps
            4) Calculate the covariance matrix according to the Fisher Information Matrix theory
            5) Add the additional results from the ``additional_result_funcs``

        Args:
            parameters_array (ndarray): the optimization results
            parameters_dict (dict): A dictionary with as keys the names of the parameters and as values the 1d maps with
                for each voxel the optimized parameter value. If not given, we create it from the
                ``optimized_parameters`` array.
            log_likelihoods (ndarray): for every set of parameters the corresponding log likelihoods.
                If not provided they will be calculated from the parameters.
            roi_indices (Iterable): if set, the problem instances optimized in this batch

        Returns:
            dict: The results dictionary.
        """
        results_dict = {}
        if not parameters_dict:
            parameters_dict = split_array_to_dict(parameters_array, self.get_free_param_names())
        results_dict.update(parameters_dict)

        results_dict.update(self._get_dependent_map_calculator()(self, results_dict, roi_indices=roi_indices))
        results_dict.update(self._get_fixed_parameter_maps(roi_indices))

        if self._post_processing['optimization']['ll_and_ic']:
            results_dict.update(self._get_post_optimization_information_criterion_maps(
                parameters_array, roi_indices, log_likelihoods=log_likelihoods))

        if self._post_processing['optimization']['uncertainties']:
            fim = self._compute_fisher_information_matrix(parameters_array, roi_indices)
            results_dict.update(fim['stds'])
            results_dict['covariances'] = fim['covariances']

        routine_input = ExtraOptimizationMapsInfo(self, results_dict, self._input_data, roi_indices)
        for routine in self._extra_optimization_maps_funcs:
            try:
                results_dict.update(routine(routine_input))
            except KeyError as exc:
                if not exc.args[0].endswith('.std'):
                    raise exc

        if not self._post_processing['optimization']['store_covariances']:
            del results_dict['covariances']

        return results_dict

    def compute_covariance_matrix(self, parameters, roi_indices=None):
        """Calculate the covariance and correlation matrix by taking the inverse of the Hessian.

        This first calculates/approximates the Hessian at each of the points using numerical differentiation.
        Afterwards we inverse the Hessian to return the covariance matrix.

        This function only returns the upper triangular data of the covariance matrix.

        Args:
            parameters (ndarray): for each voxel, the optimized parameters
            roi_indices (Iterable or None): if set, the problem instances optimized in this batch.

        Returns:
            ndarray: for each voxel (first dimension ) a covariance matrix (second dimension)
        """
        return self._compute_covariance_matrix(parameters, roi_indices=roi_indices)

    def get_covariance_output_names(self):
        """Get pretty names for each of the covariance matrix outputs.

        This corresponds to the output array from :meth:`compute_covariance_matrix`.

        Returns:
            List[str]: for each elements in the upper triangular covariance vector, a pretty name
        """
        nmr_params = self.get_nmr_parameters()
        param_names = ['{}.{}'.format(m.name, p.name)
                       for m, p in self._model_functions_info.get_estimable_parameters_list()]

        covariance_names = {}
        ind_counter = 0
        for x_ind in range(nmr_params):
            covariance_names[ind_counter] = param_names[x_ind] + '.std'
            ind_counter += 1

            for y_ind in range(x_ind + 1, nmr_params):
                covariance_names[ind_counter] = '{}_to_{}'.format(param_names[x_ind], param_names[y_ind])
                ind_counter += 1
        return [covariance_names[ind] for ind in range(len(covariance_names))]

    def get_post_sampling_maps(self, sampling_output, roi_indices=None):
        """Get the post sample volume maps.

        This will return a dictionary mapping folder names to dictionaries with volumes to write.

        Args:
            sampling_output (mot.sample.base.SamplingOutput): the output of the sampler
            roi_indices (Iterable or None): if set, the problem instances optimized in this batch

        Returns:
            dict: a dictionary with for every subdirectory the maps to save
        """
        samples = sampling_output.get_samples()

        items = {}

        if self._post_processing['sampling']['model_defined_maps']:
            items.update({'model_defined_maps': lambda: self._post_sampling_extra_model_defined_maps(
                samples, roi_indices)})
        if self._post_processing['sampling']['univariate_normal']:
            items.update({'univariate_normal': lambda: self._get_univariate_normal(samples)})
        if self._post_processing['sampling']['univariate_ess']:
            items.update({'univariate_ess': lambda: self._get_univariate_ess(samples)})
        if self._post_processing['sampling']['multivariate_ess']:
            items.update({'multivariate_ess': lambda: self._get_multivariate_ess(samples)})
        if self._post_processing['sampling']['average_acceptance_rate']:
            items.update({'average_acceptance_rate': lambda: self._get_average_acceptance_rate(samples)})
        if self._post_processing['sampling']['maximum_likelihood'] \
            or self._post_processing['sampling']['maximum_a_posteriori']:
            mle_maps_cb, map_maps_cb = self._get_mle_map_statistics(sampling_output, roi_indices=roi_indices)
            if self._post_processing['sampling']['maximum_likelihood']:
                items.update({'maximum_likelihood': mle_maps_cb})
            if self._post_processing['sampling']['maximum_a_posteriori']:
                items.update({'maximum_a_posteriori': map_maps_cb})

        return DeferredFunctionDict(items, cache=False)

    def get_model_eval_function(self):
        return self._get_model_eval_function(include_cache_init_func=True)

    def update_active_post_processing(self, processing_type, settings):
        """Update the active post-processing semaphores.

        It is possible to control which post-processing routines get run by overwriting them using this method.
        For a list of post-processors, please see the default mdt configuration file under ``active_post_processing``.

        Args:
            processing_type (str): one of ``sample`` or ``optimization``.
            settings (dict): the items to set in the post-processing information
        """
        self._post_processing[processing_type].update(settings)

    def get_active_post_processing(self):
        """Get a dictionary with the active post processing.

        This returns a dictionary with as first level the processing type and as second level the post-processing
        options.

        Returns:
            dict: the dictionary with the post-processing options for both sample and optimization.
        """
        return copy.deepcopy(self._post_processing)

    def get_mle_codec(self):
        """Get a parameter codec that can be used to transform the parameters to and from optimization and model space.

        This does two things:
        - It applies the transformation of each of the parameters
        - For compartments with both a :class:`mdt.model_building.parameters.PolarAngleParameter` and
          :class:`mdt.model_building.parameters.AzimuthAngleParameter`, we apply the right spherical transformation
          to put the spherical coordinates in the right spherical hemisphere.

        Returns:
            mdt.model_building.utils.ParameterCodec: an instance of a parameter codec
        """
        def get_parameter_transformations():
            """Get the encode and decode transformations for each of the parameters. """
            dec_func_list = []
            enc_func_list = []
            for m, p in self._model_functions_info.get_estimable_parameters_list():
                parameter = p
                ind = self._model_functions_info.get_parameter_estimable_index(m, p)
                transform = parameter.parameter_transform

                s = '{0}[' + str(ind) + '] = ' + transform.get_cl_decode().create_assignment(
                    '{0}[' + str(ind) + ']',
                    'model_data->bounds->lower_bounds[' + str(ind) + ']',
                    'model_data->bounds->upper_bounds[' + str(ind) + ']') + ';'

                dec_func_list.append(s)

                s = '{0}[' + str(ind) + '] = ' + transform.get_cl_encode().create_assignment(
                    '{0}[' + str(ind) + ']',
                    'model_data->bounds->lower_bounds[' + str(ind) + ']',
                    'model_data->bounds->upper_bounds[' + str(ind) + ']') + ';'

                enc_func_list.append(s)

            return tuple(reversed(enc_func_list)), dec_func_list

        def get_encode_function():
            func = '''
                void parameter_encode(void* data, local mot_float_type* x){
                    _mdt_model_data* model_data = (_mdt_model_data*)data;
            '''
            if self._enforce_weights_sum_to_one:
                func += self._get_weight_sum_to_one_transformation()

            for transformation in self._get_spherical_transformations():
                func += '\n' + '\t' * 4 + transformation

            for transformation in self._get_rotational_transformations():
                func += '\n' + '\t' * 4 + transformation

            for d in get_parameter_transformations()[0]:
                func += "\n" + "\t" * 4 + d.format('x')

            func += '''
                }
            '''
            return SimpleCLFunction.from_string(func, dependencies=[self._get_spherical_transformation_func()])

        def get_decode_function():
            func = '''
                void parameter_decode(void* data, local mot_float_type* x){
                    _mdt_model_data* model_data = (_mdt_model_data*)data;
            '''
            for d in get_parameter_transformations()[1]:
                func += "\n" + "\t" * 4 + d.format('x')

            for transformation in self._get_spherical_transformations():
                func += '\n' + '\t' * 4 + transformation

            for transformation in self._get_rotational_transformations():
                func += '\n' + '\t' * 4 + transformation

            if self._enforce_weights_sum_to_one:
                func += self._get_weight_sum_to_one_transformation()

            func += '''
                }
            '''
            return SimpleCLFunction.from_string(func, dependencies=[self._get_spherical_transformation_func()])

        def encode_bounds_func(lower_bounds, upper_bounds):
            encoded_lbs = []
            encoded_ubs = []
            for m, p in self._model_functions_info.get_estimable_parameters_list():
                ind = self._model_functions_info.get_parameter_estimable_index(m, p)
                lb, ub = p.parameter_transform.encode_bounds(lower_bounds[ind], upper_bounds[ind])
                encoded_lbs.append(lb)
                encoded_ubs.append(ub)
            return encoded_lbs, encoded_ubs

        return ParameterCodec(get_encode_function(), get_decode_function(), encode_bounds_func=encode_bounds_func)

    def fix(self, model_param_name, value):
        """Fix the given model.param to the given value.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'
            value (scalar or vector or string or AbstractParameterDependency): The value or dependency
                to fix the given parameter to.

        Returns:
            Returns self for chainability
        """
        if isinstance(value, str):
            value = SimpleAssignment(value)
        self._model_functions_info.fix_parameter(model_param_name, value)
        return self

    def unfix(self, model_param_name):
        """Unfix the given model.param

        Args:
            model_param_name (string): A model.param name like 'Ball.d'

        Returns:
            Returns self for chainability
        """
        self._model_functions_info.unfix(model_param_name)
        return self

    def init(self, model_param_name, value):
        """Init the given model.param to the given value.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'
            value (scalar or vector): The value to initialize the given parameter to

        Returns:
            Returns self for chainability
        """
        if not self._model_functions_info.is_fixed(model_param_name):
            self._model_functions_info.set_parameter_value(model_param_name, value)
        return self

    def set_initial_parameters(self, initial_params):
        """Update the initial parameters for this model by the given values.

        This only affects free parameters.

        Args:
            initial_params (dict): a dictionary containing as keys full parameter names (<model>.<param>) and as values
                numbers or arrays to be used as starting point
        """
        for m, p in self._model_functions_info.get_model_parameter_list():
            param_name = '{}.{}'.format(m.name, p.name)

            if param_name in initial_params:
                self.init(param_name, initial_params[param_name])

        return self

    def set_lower_bound(self, model_param_name, value):
        """Set the lower bound for the given parameter to the given value.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'
            value (scalar or vector): The value to set the lower bounds to, either a single value for
                every voxel or a value per voxel.

        Returns:
            Returns self for chainability
        """
        self._lower_bounds[model_param_name] = value
        return self

    def set_lower_bounds(self, lower_bounds):
        """Apply multiple lower bounds from a dictionary.

        Args:
            lower_bounds (dict): per parameter a lower bound

        Returns:
            Returns self for chainability
        """
        for param, value in lower_bounds.items():
            self.set_lower_bound(param, value)
        return self

    def set_upper_bound(self, model_param_name, value):
        """Set the upper bound for the given parameter to the given value.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'
            value (scalar or vector): The value to set the upper bounds to, either a single value for
                every voxel or a value per voxel.

        Returns:
            Returns self for chainability
        """
        self._upper_bounds[model_param_name] = value
        return self

    def set_upper_bounds(self, upper_bounds):
        """Apply multiple upper bounds from a dictionary.

        Args:
            upper_bounds (dict): per parameter a upper bound

        Returns:
            Returns self for chainability
        """
        for param, value in upper_bounds.items():
            self.set_upper_bound(param, value)
        return self

    def has_parameter(self, model_param_name):
        """Check to see if the given parameter is defined in this model.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'

        Returns:
            boolean: true if the parameter is defined in this model, false otherwise.
        """
        return self._model_functions_info.has_parameter(model_param_name)

    def set_input_data(self, input_data, suppress_warnings=False):
        """Set the input data this model will deal with.

        Args:
            input_data (mdt.lib.input_data.MRIInputData):
                The container for the data we will use for this model.
            suppress_warnings (boolean): set to suppress all warnings

        Returns:
            Returns self for chainability
        """
        if not suppress_warnings:
            self._check_data_consistency(input_data)

        self._original_input_data = input_data

        input_data = self._prepare_input_data(input_data, suppress_warnings=suppress_warnings)

        if not suppress_warnings:
            if input_data.gradient_deviations is not None and self._model_functions_info.has_protocol_parameter('g'):
                self._logger.info('Using the gradient deviations in the model optimization.')

        self._input_data = input_data
        if self._input_data.noise_std is not None:
            std_param = self._model_functions_info.get_noise_std_param()
            self._model_functions_info.set_parameter_value(
                '{}.{}'.format(self._likelihood_function.name, std_param.name),
                self._input_data.noise_std)
        return self

    def get_input_data(self):
        """Get the input data actually being used by this model.

        Returns:
            mdt.lib.input_data.MRIInputData: the input data being used by this model
        """
        return self._input_data

    def get_nmr_observations(self):
        return self._input_data.nmr_observations

    def get_nmr_parameters(self):
        return len(self._model_functions_info.get_estimable_parameters_list())

    def get_lower_bounds(self):
        return [self._lower_bounds['{}.{}'.format(m.name, p.name)] for m, p in
                self._model_functions_info.get_estimable_parameters_list()]

    def get_upper_bounds(self):
        return [self._upper_bounds['{}.{}'.format(m.name, p.name)] for m, p in
                self._model_functions_info.get_estimable_parameters_list()]

    def get_free_param_names(self):
        """Get the names of the free parameters"""
        return ['{}.{}'.format(m.name, p.name) for m, p in self._model_functions_info.get_estimable_parameters_list()]

    def get_required_protocol_names(self):
        """Get a list with the constant data names that are needed for this model to work.

        For example, an implementing diffusion MRI model might require the presence of the protocol parameter
        'g' and 'b'. This function should then return ('g', 'b').

        Returns:
            list: A list of columns names that need to be present in the protocol
        """
        return list(set([p.name for m, p in self._model_functions_info.get_model_parameter_list() if
                         isinstance(p, ProtocolParameter)]))

    def is_input_data_sufficient(self, input_data=None):
        """Check if the input data has enough information for this model to work.

        Args:
            input_data (mdt.lib.input_data.MRIInputData): The input data we intend on using with this model.

        Returns:
            boolean: True if there is enough information in the input data, false otherwise.
        """
        return not self.get_input_data_problems(input_data=input_data)

    def get_input_data_problems(self, input_data=None):
        """Get all the problems with the protocol.

        Args:
            input_data (mdt.lib.input_data.MRIInputData): The input data we intend on using with this model.

        Returns:
            list of InputDataProblem: A list of
                InputDataProblem instances or subclasses of that baseclass.
                These objects indicate the problems with the protocol and this model.
        """
        if input_data is None:
            input_data = self._input_data

        problems = []

        missing_columns = []
        for name in self.get_required_protocol_names():
            if not input_data.has_input_data(name):
                for p in self._model_functions_info.get_unique_protocol_parameters():
                    if p.name == name and p.value is None:
                        missing_columns.append(name)

        if missing_columns:
            problems.append(MissingProtocolInput(missing_columns))

        return problems

    def param_dict_to_array(self, volume_dict):
        params = [volume_dict['{}.{}'.format(m.name, p.name)] for m, p
                  in self._model_functions_info.get_estimable_parameters_list()]
        elements = [np.transpose(np.atleast_2d([s])) if len(np.array(s).shape) < 2
                    else np.atleast_2d(s) for s in params]
        return np.concatenate(elements, axis=1)

    def _post_sampling_extra_model_defined_maps(self, samples, roi_indices):
        """Compute the extra post-sample maps defined in the models.

        Args:
            samples (ndarray): the array with the samples
            roi_indices (Iterable or None): the indices of the voxels we processed

        Returns:
            dict: some additional statistic maps we want to output as part of the samping results
        """
        post_processing_data = SamplingPostProcessingData(samples, self.get_free_param_names(),
                                                          self._get_fixed_parameter_maps(roi_indices))
        results_dict = {}
        for routine in self._extra_sampling_maps_funcs:
            try:
                results_dict.update(routine(post_processing_data))
            except KeyError:
                pass
        return results_dict

    def _get_mle_map_statistics(self, sampling_output, roi_indices=None):
        """Get the maximum and corresponding volume maps of the MLE and MAP estimators.

        This computes the Maximum Likelihood Estimator and the Maximum A Posteriori in one run and computes from that
        the corresponding parameter and global post-optimization maps.

        Args:
            sampling_output (mot.cl_routines.sample.base.SimpleSampleOutput): the output of the sampler
            roi_indices (Iterable): if set, the problem instances sampled in this batch

        Returns:
            tuple(Func, Func): the function that generates the maps for the MLE and for the MAP estimators.
        """
        log_likelihoods = sampling_output.get_log_likelihoods()
        posteriors = log_likelihoods + sampling_output.get_log_priors()

        mle_indices = np.argmax(log_likelihoods, axis=1)
        map_indices = np.argmax(posteriors, axis=1)

        mle_values = log_likelihoods[range(log_likelihoods.shape[0]), mle_indices]
        map_values = posteriors[range(posteriors.shape[0]), map_indices]
        map_lls = log_likelihoods[range(log_likelihoods.shape[0]), map_indices]

        samples = sampling_output.get_samples()

        mle_samples = samples[range(samples.shape[0]), :, mle_indices]
        map_samples = samples[range(samples.shape[0]), :, map_indices]

        def mle_maps():
            maps = self._post_process_optimization_maps(mle_samples, roi_indices, log_likelihoods=mle_values)
            maps.update({'MaximumLikelihoodEstimator.indices': mle_indices})
            return maps

        def map_maps():
            maps = self._post_process_optimization_maps(map_samples, roi_indices, log_likelihoods=map_lls)
            maps.update({'MaximumAPosteriori': map_values,
                         'MaximumAPosteriori.indices': map_indices})
            return maps

        return mle_maps, map_maps

    def _get_univariate_normal(self, samples):
        """Fit a univariate normal distribution to the parameters, i.e. calculate the mean and std. of each parameter.

        Args:
            samples (ndarray): an (d, p, n) matrix for d problems, p parameters and n samples.

        Returns:
            dict: the volume maps with the univariate normal distribution fits (mean and std.)
        """
        results = {}
        for ind, param_name in enumerate(self.get_free_param_names()):
            results['{}'.format(param_name)] = np.mean(samples[:, ind, :], axis=1)
            results['{}.std'.format(param_name)] = np.std(samples[:, ind, :], axis=1)
        return results

    def _get_univariate_ess(self, samples):
        """Get the univariate Effective Sample Size statistics for the given set of samples.

        Args:
            samples (ndarray): an (d, p, n) matrix for d problems, p parameters and n samples.

        Returns:
            dict: the volume maps with the univariate ESS statistics
        """
        ess = univariate_ess(samples, method='standard_error')
        ess[np.isinf(ess)] = 0
        ess = np.nan_to_num(ess)
        return split_array_to_dict(ess, [a + '.UnivariateESS' for a in self.get_free_param_names()])

    def _get_multivariate_ess(self, samples):
        """Get the multivariate Effective Sample Size statistics for the given set of samples.

        Args:
            samples (ndarray): an (d, p, n) matrix for d problems, p parameters and n samples.

        Returns:
            dict: the volume maps with the ESS statistics
        """
        ess = multivariate_ess(samples)
        ess[np.isinf(ess)] = 0
        ess = np.nan_to_num(ess)
        return {'MultivariateESS': ess}

    def _get_average_acceptance_rate(self, samples):
        """Get the multivariate Effective Sample Size statistics for the given set of samples.

        This computes the acceptance rate on basis of the obtained samples, not taking into account any thinning
        during the generation of the samples.

        Args:
            samples (ndarray): an (d, p, n) matrix for d problems, p parameters and n samples.

        Returns:
            dict: the volume maps with the average acceptance rates
        """
        results = {}
        for ind, param_name in enumerate(self.get_free_param_names()):
            results['{}'.format(param_name)] = np.count_nonzero(samples[:, ind, 1:] - samples[:, ind, :-1], axis=1) \
                                               / samples.shape[2]
        return results

    def _compute_fisher_information_matrix(self, results_array, roi_indices):
        """Calculate the covariance and correlation matrix by taking the inverse of the Hessian.

        This first calculates/approximates the Hessian at each of the points using numerical differentiation.
        Afterwards we inverse the Hessian and compute a correlation matrix.

        Args:
            results_array (ndarray): the list with the optimized points for each parameter
            roi_indices (Iterable or None): if set, the problem instances optimized in this batch
        """
        covars = self._compute_covariance_matrix(results_array, roi_indices)
        names = self.get_covariance_output_names()

        stds = {}
        covariances = {}
        for ind, name in enumerate(names):
            if name.endswith('.std'):
                stds[name] = np.nan_to_num(np.sqrt(covars[..., ind]))
            else:
                covariances[name] = covars[..., ind]

        return {'stds': stds, 'covariances': covariances}

    def _compute_covariance_matrix(self, results_array, roi_indices=None):
        """Calculate the covariance and correlation matrix by taking the inverse of the Hessian.

        This first calculates/approximates the Hessian at each of the points using numerical differentiation.
        Afterwards we inverse the Hessian to return the covariance matrix.

        This function only returns the upper triangular data of the covariance matrix.

        Args:
            results_array (ndarray): the list with the optimized points for each parameter
            roi_indices (Iterable or None): if set, the problem instances optimized in this batch

        Returns:
            ndarray: for each voxel (first dimension ) a covariance matrix (second dimension)
        """
        nmr_params = self.get_nmr_parameters()
        scales = self._get_numdiff_scaling_factors()

        wrapped_objective = SimpleCLFunction.from_string('''
            double wrapped_''' + self.get_objective_function().get_cl_function_name() + '''(
                    local mot_float_type* x,
                    void* data){

                local mot_float_type* x_tmp = ((hessian_function_wrapper_data*)data)->x_tmp;

                if(get_local_id(0) == 0){
                    ''' + '\n'.join('x_tmp[{0}] = x[{0}] / {1};'.format(i, s) for i, s in enumerate(scales)) + '''
                    ''' + '\n'.join(tr for tr in self._get_spherical_transformations(vector_name='x_tmp')) + '''
                    ''' + '\n'.join(tr for tr in self._get_rotational_transformations(vector_name='x_tmp')) + '''
                    ''' + (self._get_weight_sum_to_one_transformation(vector_name='x_tmp')
                           if self._enforce_weights_sum_to_one else '') + '''
                }
                barrier(CLK_LOCAL_MEM_FENCE);

                return ''' + self.get_objective_function().get_cl_function_name() + '''(
                    x_tmp, ((hessian_function_wrapper_data*)data)->data, 0);
            }
        ''', dependencies=[self.get_objective_function(), self._get_spherical_transformation_func()])

        wrapped_input_data = Struct({
            'data': self.get_kernel_data().get_subset(roi_indices),
            'x_tmp': LocalMemory('mot_float_type', nmr_items=nmr_params)
        }, 'hessian_function_wrapper_data')

        lower_bounds = self.get_lower_bounds()
        for ind in range(len(lower_bounds)):
            if not self._get_numdiff_use_bounds()[ind] or not self._get_numdiff_use_lower_bounds()[ind]:
                lower_bounds[ind] = -np.inf
            lower_bounds[ind] *= scales[ind]
            if not is_scalar(lower_bounds[ind]) and roi_indices is not None:
                lower_bounds[ind] = lower_bounds[ind][roi_indices]

        upper_bounds = self.get_upper_bounds()
        for ind in range(len(upper_bounds)):
            if not self._get_numdiff_use_bounds()[ind] or not self._get_numdiff_use_upper_bounds()[ind]:
                upper_bounds[ind] = np.inf
            upper_bounds[ind] *= scales[ind]
            if not is_scalar(upper_bounds[ind]) and roi_indices is not None:
                upper_bounds[ind] = upper_bounds[ind][roi_indices]

        hessian = estimate_hessian(
            wrapped_objective,
            results_array * scales,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            step_ratio=2,
            nmr_steps=5,
            max_step_sizes=self._get_numdiff_max_step_sizes(),
            data=wrapped_input_data,
            cl_runtime_info=CLRuntimeInfo(double_precision=True)
        )

        hessian = np.nan_to_num(hessian)

        data = Array(hessian, ctype='double', mode='rw')
        pseudo_inverse_real_symmetric_matrix_upper_triangular().evaluate((
            Scalar(nmr_params, ctype='uint'),
            data,
            PrivateMemory(2 * nmr_params + 2 * nmr_params ** 2, 'double')
        ), nmr_instances=hessian.shape[0], use_local_reduction=False)

        covars = data.get_data()
        covars /= np.outer(scales, scales)[np.triu_indices(nmr_params)]
        return covars

    def _get_post_optimization_information_criterion_maps(self, results_array, roi_indices, log_likelihoods=None):
        """Add some final results maps to the results dictionary.

        This called by the function post_process_optimization_maps() as last call to add more maps.

        Args:
            results_array (ndarray): the results from model optimization.
            roi_indices (ndarray): limit the analysis to these voxels.
            log_likelihoods (ndarray): for every set of parameters the corresponding log likelihoods.
                If not provided they will be calculated from the parameters.

        Returns:
            dict: the calculated information criterion maps
        """
        if log_likelihoods is None:
            log_likelihoods = compute_log_likelihood(self.get_log_likelihood_function(),
                                                     results_array, data=self.get_kernel_data().get_subset(roi_indices))
            log_likelihoods[np.isinf(log_likelihoods)] = 0
            log_likelihoods = np.nan_to_num(log_likelihoods)

        k = self.nmr_parameters_for_bic_calculation
        n = self.get_nmr_observations()

        result = {'LogLikelihood': log_likelihoods}
        result.update(calculate_point_estimate_information_criterions(log_likelihoods, k, n))

        return result

    def _param_dict_to_array(self, volume_dict):
        params = [volume_dict['{}.{}'.format(m.name, p.name)]
                  for m, p in self._model_functions_info.get_estimable_parameters_list()]
        return np.concatenate([np.transpose(np.array([s]))
                               if len(s.shape) < 2 else s for s in params], axis=1)

    def _get_propagate_weights_uncertainty(self, results):
        weight_names = ['{}.{}'.format(m.name, p.name) for (m, p) in self._model_functions_info.get_weights()]
        if len(weight_names) > 1:
            nmr_voxels = results[weight_names[1]].shape[0]
            covar_matrix = create_covariance_matrix(nmr_voxels, results, weight_names[1:],
                                                    results.get('covariances', None))
            covar_sum = np.sum(np.sum(covar_matrix, axis=1), axis=1)
            covar_sum[np.isinf(covar_sum) | np.isnan(covar_sum) | (covar_sum < 0)] = 0
            std = np.sqrt(covar_sum)
            return {weight_names[0] + '.std': std}
        return {}

    def _get_gradient_deviation_proposal_callback(self):
        """Get the proposal callback for the gradient deformations.

        Returns:
            ProtocolAdaptionCallbacks: the protocol adaption callback for the gradient deformations.
        """
        if self._input_data.gradient_deviations is None:
            return None

        if not self._model_functions_info.has_protocol_parameter('g'):
            return None

        def flatten_deviations_matrix(deviations):
            """Converts a deviation matrix of shape (n, 3, 3) into (n, 9) and (n, m, 3, 3) into (n, m, 9)."""
            if len(deviations.shape) > 3:
                return deviations.reshape(-1, deviations.shape[1], 9)
            else:
                return deviations.reshape(-1, 9)

        def compress_zeros(deviations):
            """Find array indices that hold zeros throughout.

            In some cases, the user only knows the diagonal of the deviations matrix, but still had to provide the
            full matrix. In those cases we are wasting 2/3th of the memory on zeros. This method reduces the size
            by removing the all-zero components from the deviations matrix.

            Args:
                deviations (ndarray): either an (n, 9) of an (n, m, 9) matrix

            Returns:
                 tuple: the compressed deviations matrix and a tuple of length 9 indicating the positions of the
                    zero elements.
            """
            zero_locations = [np.all(gradient_deviations[..., ind] == 0) for ind in range(9)]

            if any(zero_locations):
                compressed_deviations = np.delete(deviations, [ind for ind in range(9) if zero_locations[ind]], axis=-1)
                return compressed_deviations, zero_locations

            return deviations, zero_locations

        def get_observation_multiplier(deviations):
            """Get the multiplier for correctly indexing the matrix in the case of per volume deformation matrices.

            If the user provide a deviation matrix per volume, we have to correctly index the matrices by
            multiplying the number of non-compressed deviations with the observation index.

            Args:
                deviations (ndarray): either an (n, X) or an (n, m, X) matrix.

            Returns:
                int: if an (n, X) matrix is provided we will return 0 because we don't need to index based on
                    volumes. If an (n, m, X) matrix is provided, we will return X.
            """
            if len(deviations.shape) > 2:
                return deviations.shape[-1]
            return 0

        def get_cl_deviations_computation_code(zero_locations):
            """Get the CL computation code for the new non-normalized gradient vector.

            This method takes into account the locations of the removed elements.
            """
            index_counter = 0
            elements = []
            for ind in range(9):
                if zero_locations[ind]:
                    elements.append('0')
                else:
                    elements.append('gradient_deviations[{} + matrix_index]'.format(index_counter))
                    index_counter += 1

            return '''
                float4 new_g_non_normalized = (float4)(
                ''' + elements[0] + ''' * (*g).x +
                ''' + elements[1] + ''' * (*g).y +
                ''' + elements[2] + ''' * (*g).z,

                ''' + elements[3] + ''' * (*g).x +
                ''' + elements[4] + ''' * (*g).y +
                ''' + elements[5] + ''' * (*g).z,

                ''' + elements[6] + ''' * (*g).x +
                ''' + elements[7] + ''' * (*g).y +
                ''' + elements[8] + ''' * (*g).z,
                0);
            '''

        gradient_deviations = flatten_deviations_matrix(self._input_data.gradient_deviations)
        gradient_deviations, zero_locations = compress_zeros(gradient_deviations)

        parameters_needed = [p for p in ['g', 'b', 'G'] if self._model_functions_info.has_protocol_parameter(p)]

        function_arguments = [self._model_functions_info.get_protocol_parameter_by_name(p).ctype
                              + '* ' + p for p in parameters_needed]
        function_arguments.append('global float* gradient_deviations')
        function_arguments.append('uint observation_index')

        body = '''
            const uint matrix_index = ''' + str(get_observation_multiplier(gradient_deviations)) + '''
                                        * observation_index;

            ''' + get_cl_deviations_computation_code(zero_locations) + '''

            float new_g_length = length(new_g_non_normalized);
            *g = new_g_non_normalized / new_g_length;
        '''
        if 'b' in parameters_needed:
            body += '*b *= new_g_length * new_g_length;' + "\n"
        if 'G' in parameters_needed:
            body += '*G *= new_g_length;' + "\n"

        class GradientDeviationProtocolUpdate(ProtocolAdaptionCallbacks):

            def get_protocol_parameter_names(self):
                return parameters_needed

            def get_callback_function(self):
                return SimpleCLFunction('void', 'gradient_deformations_protocol_callback', function_arguments, body)

            def get_kernel_input_data(self):
                return {'gradient_deviations': Array(gradient_deviations, ctype='float')}

        return GradientDeviationProtocolUpdate()

    def get_used_volumes(self, input_data=None):
        input_data = input_data or self._input_data
        return self._get_suitable_volume_indices(input_data)

    def _prepare_input_data(self, input_data, suppress_warnings=False):
        """Update the input data to make it suitable for this model.

        Some of the models in diffusion MRI can only handle a subset of all volumes. For example, the S0 model
        can only work with the unweighted signals, or the Tensor model that can only handle a b-value up to 1.5e9 s/m^2.

        Overwrite this function to limit the input data to a suitable range.

        Args:
            input_data (mdt.lib.input_data.MRIInputData): the input data set by the user

        Returns:
            mdt.lib.input_data.MRIInputData: either the same input data or a changed copy.
        """
        if not self.volume_selection:
            if not suppress_warnings:
                self._logger.info('Disabled volume selection, '
                                  'using all {} volumes.'.format(input_data.nmr_observations))
            return input_data

        indices = self._get_suitable_volume_indices(input_data)

        if len(indices) != input_data.nmr_observations:
            if not suppress_warnings:
                self._logger.info('For this model, {}, we will use a subset of the volumes.'.format(self._name))
                self._logger.info('Using {} out of {} volumes, indices: {}'.format(
                    len(indices), input_data.nmr_observations, str(indices).replace('\n', '').replace('[  ', '[')))
            return input_data.get_subset(volumes_to_keep=indices)
        else:
            if not suppress_warnings:
                self._logger.info('No volume options to apply, '
                                  'using all {} volumes.'.format(input_data.nmr_observations))
        return input_data

    def _check_data_consistency(self, input_data):
        """Check the input data for any anomalies.

        We do this here so that implementing models can add additional consistency checks, or skip the checks.
        Also, by doing this here instead of in the Protocol class we ensure that the warnings end up in the log file.
        The final argument for putting this here is that I do not want any log output in the protocol tab.

        Args:
            input_data (mdt.lib.input_data.MRIInputData): the input data to analyze.
        """

        def warn(warning):
            self._logger.warning('{}, proceeding with seemingly inconsistent values.'.format(warning))

        def convert_to_total_map(value):
            if is_scalar(value):
                return np.ones((input_data.nmr_voxels, input_data.nmr_observations)) * value
            if value.shape[0] == input_data.nmr_observations:
                return np.tile(np.squeeze(value)[None, :], (input_data.nmr_voxels, 1))
            if value.shape[0] == input_data.nmr_voxels and value.shape[1] != input_data.nmr_observations:
                return np.tile(np.squeeze(value)[:, None], (1, input_data.nmr_observations))
            return value

        def any_greater(a, b):
            return np.any(np.greater(convert_to_total_map(a), convert_to_total_map(b)))

        if input_data.has_input_data('TE') and input_data.has_input_data('TR'):
            if any_greater(input_data.get_input_data('TE'), input_data.get_input_data('TR')):
                warn('Volumes detected where TE > TR')

        if input_data.has_input_data('TE'):
            if any_greater(input_data.get_input_data('TE'), 1):
                warn('Volumes detected where TE >= 1 second')

        if input_data.has_input_data('TR'):
            if any_greater(input_data.get_input_data('TR'), 50):
                warn('Volumes detected where TR >= 50 seconds')

        if input_data.has_input_data('delta') and input_data.has_input_data('Delta'):
            if any_greater(input_data.get_input_data('delta'), input_data.get_input_data('Delta')):
                warn('Volumes detected where (small) delta >= (big) Delta')

        if input_data.has_input_data('Delta') and input_data.has_input_data('TE'):
            if any_greater(input_data.get_input_data('Delta'), input_data.get_input_data('TE')):
                warn('Volumes detected where (big) Delta >= TE')

    def _get_suitable_volume_indices(self, input_data):
        """Usable in combination with _prepare_input_data, return the suitable volume indices.

        Get a list of volume indices that the model can use. Can be overloaded by a sub-class.

        Args:
            input_data (mdt.lib.input_data.MRIInputData): the input data set by the user

        Returns:
            list: the list of indices we want to use for this model.
        """
        return list(range(input_data.nmr_observations))

    def _get_dependent_map_calculator(self):
        """Get the calculation function to compute the maps for the dependent parameters."""
        estimable_parameters = self._model_functions_info.get_estimable_parameters_list(exclude_priors=True)
        dependent_parameters = self._model_functions_info.get_dependency_fixed_parameters_list(exclude_priors=True)

        if len(dependent_parameters):
            func = ''
            func += self._get_fixed_parameters_listing()
            func += self._get_estimable_parameters_listing()
            func += self._get_dependent_parameters_listing()

            dependent_parameter_names = [('{}.{}'.format(m.name, p.name).replace('.', '_'),
                                          '{}.{}'.format(m.name, p.name))
                                         for m, p in dependent_parameters]

            estimable_parameter_names = ['{}.{}'.format(m.name, p.name) for m, p in estimable_parameters]

            def calculator(model, results_dict, roi_indices=None):
                estimated_parameters = [results_dict[k] for k in estimable_parameter_names]

                vals = calculate_dependent_parameters(model.get_kernel_data().get_subset(roi_indices),
                                                      estimated_parameters, func, dependent_parameter_names)
                return split_array_to_dict(vals, [n[1] for n in dependent_parameter_names])
        else:
            def calculator(model, results_dict, roi_indices=None):
                return {}

        return calculator

    def _get_fixed_parameter_maps(self, roi_indices=None):
        """In place add complete maps for the fixed parameters."""
        fixed_params = self._model_functions_info.get_value_fixed_parameters_list(exclude_priors=True)

        result = {}

        for (m, p) in fixed_params:
            name = '{}.{}'.format(m.name, p.name)
            value = self._model_functions_info.get_parameter_value(name)

            if is_scalar(value):
                result.update({name: np.tile(np.array([value]), (self._get_nmr_problems(roi_indices),))})
            else:
                if roi_indices is not None:
                    value = value[roi_indices, ...]
                result.update({name: value})

        return result

    def _get_rwm_proposal_stds(self):
        proposal_stds = []
        for m, p in self._model_functions_info.get_estimable_parameters_list():
            proposal_std = p.sampling_proposal_std

            if is_scalar(proposal_std):
                if self._get_nmr_problems() == 0:
                    proposal_stds.append(np.full((1, 1), proposal_std))
                else:
                    proposal_stds.append(np.full((self._get_nmr_problems(), 1), proposal_std))
            else:
                if len(proposal_std.shape) < 2:
                    proposal_std = np.transpose(np.asarray([proposal_std]))
                elif proposal_std.shape[1] > proposal_std.shape[0]:
                    proposal_std = np.transpose(proposal_std)
                proposal_stds.append(proposal_std)

        return np.concatenate([np.transpose(np.array([s])) if len(s.shape) < 2 else s for s in proposal_stds], axis=1)

    def _get_rwm_epsilons(self):
        """Get per parameter a value small relative to the parameter's standard deviation.

        This is used in, for example, the SCAM MCMC sampling routine to add to the new proposal standard deviation to
        ensure it does not collapse to zero.
        """
        scaling_factor = 1e-5
        epsilons = []
        for m, p in self._model_functions_info.get_estimable_parameters_list():
            proposal_std = p.sampling_proposal_std
            if is_scalar(proposal_std):
                epsilons.append(proposal_std * scaling_factor)
            else:
                epsilons.append(np.mean(proposal_std) * scaling_factor)
        return epsilons

    def _get_weight_sum_to_one_transformation(self, vector_name='x'):
        """Returns a snippet of CL for the encode and decode functions to force the sum of the weights to 1.

        Args:
            vector_name (str): the name of the vector on which to operate
        """
        weight_indices = []
        for (m, p) in self._model_functions_info.get_estimable_weights():
            weight_indices.append(self._model_functions_info.get_parameter_estimable_index(m, p))

        if len(weight_indices) > 1:
            return '''
                mot_float_type _weight_sum = ''' + \
                   ' + '.join(vector_name + '[{}]'.format(index) for index in weight_indices) + ''';
                if(_weight_sum > 1.0){
                    ''' + '\n'.join(vector_name + '[{}] /= _weight_sum;'.format(index)
                                    for index in weight_indices) + '''
                }
            '''
        return ''

    def _set_default_dependencies(self):
        """Initialize the default dependencies.

        By default this adds dependencies for the fixed data that is used in multiple parameters.
        Additionally, if enforce weights sum to one is set, this adds the dependency on the first weight.
        """
        self._init_fixed_duplicates_dependencies()
        if self._enforce_weights_sum_to_one:
            names = ['{}.{}'.format(m.name, p.name) for (m, p) in self._model_functions_info.get_weights()]
            if len(names) > 1:
                self.fix(names[0], SimpleAssignment('max((double)1 - ({}), (double)0)'.format(' + '.join(names[1:]))))

    def _get_protocol_data_as_var_data(self):
        """Get the value for the given protocol parameter.

        The resolution order is as follows, with a latter stage taking preference over an earlier stage

        1. the value defined in the parameter definition
        2. the <param_name> in the input data

        Returns:
            dict: the value for the given parameter.
        """
        return_data = {}

        for p in self._model_functions_info.get_unique_protocol_parameters():
            value = self._get_protocol_value(p)

            if value is None:
                raise ValueError('Could not find a suitable value for the protocol parameter "{}".'.format(p.name))

            if all_elements_equal(value):
                const_d = {p.name: Scalar(get_single_value(value), ctype=p.ctype)}
            else:
                if value.shape[0] == self._input_data.nmr_voxels:
                    const_d = {p.name: Array(value, ctype=p.ctype)}
                else:
                    const_d = {p.name: Array(value, ctype=p.ctype, parallelize_over_first_dimension=False)}
            return_data.update(const_d)
        return return_data

    def _get_protocol_value(self, parameter):
        if isinstance(parameter, ProtocolParameter):
            value = parameter.value

            if self._input_data.has_input_data(parameter.name):
                value = self._input_data.get_input_data(parameter.name)
            return value

    def _get_observations_data(self):
        """Get the observations to use in the kernel.

        Can return None if there are no observations.
        """
        observations = self._input_data.observations
        if observations is not None:
            observations = self._transform_observations(observations).astype(np.float32)
            return {'observations': Array(observations)}
        return {}

    def _convert_parameters_dot_to_bar(self, string):
        """Convert a string containing parameters with . to parameter names with _"""
        for m, p in self._model_functions_info.get_model_parameter_list():
            dname = '{}.{}'.format(m.name, p.name)
            bname = '{}.{}'.format(m.name, p.name).replace('.', '_')
            string = string.replace(dname, bname)
        return string

    def _init_fixed_duplicates_dependencies(self):
        """Find duplicate fixed parameters, and make dependencies of them. This saves data transfer in CL."""
        var_data_dict = {}
        for m, p in self._model_functions_info.get_free_parameters_list():
            param_name = '{}.{}'.format(m.name, p.name)
            if self._model_functions_info.is_fixed_to_value(param_name):
                value = self._model_functions_info.get_parameter_value(param_name)

                if not is_scalar(value):
                    duplicate_found = False
                    duplicate_key = None

                    for key, data in var_data_dict.items():
                        if np.array_equal(data, value):
                            duplicate_found = True
                            duplicate_key = key
                            break

                    if duplicate_found:
                        self.fix(param_name, SimpleAssignment(duplicate_key))
                    else:
                        var_data_dict.update({param_name: value})

    def _get_free_parameter_assignment_value(self, m, p):
        """Get the assignment value for one of the free parameters.

        Since the free parameters can be fixed we need an auxiliary routine to get the assignment value.

        Args:
            m: model
            p: parameter
        """
        data_type = p.basic_ctype

        if self._model_functions_info.is_fixed_to_value('{}.{}'.format(m.name, p.name)):
            param_name = '{}.{}'.format(m.name, p.name).replace('.', '_')
            return '(' + data_type + ') model_data->{}'.format(param_name)
        elif self._model_functions_info.is_fixed_to_dependency(m, p):
            dependency = self._model_functions_info.get_parameter_value('{}.{}'.format(m.name, p.name))
            return self._convert_parameters_dot_to_bar(dependency.assignment_code)

        ind = self._model_functions_info.get_parameter_estimable_index(m, p)
        return 'x[' + str(ind) + ']'

    def _get_param_listing_for_param(self, m, p):
        """Get the param listing for one specific parameter. This can be used for example for the noise model params.
        """
        data_type = p.basic_ctype
        name = '{}.{}'.format(m.name, p.name).replace('.', '_')
        assignment = ''

        if isinstance(p, ProtocolParameter):
            assignment = 'model_data->' + p.name + '[observation_index]'
        elif isinstance(p, FreeParameter):
            assignment = self._get_free_parameter_assignment_value(m, p)

        return data_type + ' ' + name + ' = ' + assignment + ';' + "\n"

    def _get_parameters_listing(self):
        """Get the CL code for the parameter listing, this goes on top of the evaluate function.

        Args:
            exclude_list: an optional list containing parameters to exclude from the listing.
             This should contain full parameter names like: <model_name>_<param_name>

        Returns:
            An CL string that contains all the parameters as primitive data types.
        """
        func = ''
        func += self._get_protocol_parameters_listing()
        func += self._get_fixed_parameters_listing()
        func += self._get_estimable_parameters_listing()
        func += self._get_dependent_parameters_listing()
        return str(func)

    def _get_estimable_parameters_listing(self):
        """Get the parameter listing for the free parameters.
        """
        param_list = self._model_functions_info.get_estimable_parameters_list(exclude_priors=True)

        func = ''
        estimable_param_counter = 0
        for m, p in param_list:
            name = '{}.{}'.format(m.name, p.name).replace('.', '_')
            data_type = p.ctype
            assignment = 'x[' + str(estimable_param_counter) + ']'
            func += "\t" * 4 + data_type + ' ' + name + ' = ' + assignment + ';' + "\n"
            estimable_param_counter += 1
        return func

    def _get_protocol_parameters_listing(self):
        """Get the parameter listing for the protocol parameters.
        """
        param_list = self._model_functions_info.get_all_protocol_parameters()
        protocol_params_seen = []
        func = ''
        for m, p in param_list:
            if p.name not in protocol_params_seen:
                assignment = self._get_protocol_parameter_assignment(p)
                func += "\t" * 4 + p.ctype + ' ' + p.name + ' = ' + assignment + ';' + "\n"
                protocol_params_seen.append(p.name)
        return func

    def _get_protocol_parameter_assignment(self, parameter):
        """Get the assignment value for the given protocol parameter."""
        value = self._get_protocol_value(parameter)

        if all_elements_equal(value):
            assignment = 'model_data->protocol->' + parameter.name
        elif len(value.shape) > 1 and value.shape[0] == self._input_data.nmr_voxels and \
            value.shape[1] != self._input_data.nmr_observations:
            assignment = 'model_data->protocol->' + parameter.name + '[0]'
        else:
            assignment = 'model_data->protocol->' + parameter.name + '[observation_index]'
        return assignment

    def _get_fixed_parameters_listing(self):
        """Get the parameter listing for the fixed parameters.
        """
        param_list = self._model_functions_info.get_value_fixed_parameters_list(exclude_priors=True)

        func = ''
        for m, p in param_list:
            name = '{}.{}'.format(m.name, p.name).replace('.', '_')
            data_type = p.basic_ctype
            param_name = '{}.{}'.format(m.name, p.name).replace('.', '_')
            assignment = 'model_data->{}'.format(param_name)
            func += "\t" * 4 + data_type + ' ' + name + ' = ' + assignment + ';' + "\n"
        return func

    def _get_dependent_parameters_listing(self, dependent_param_list=None):
        """Get the parameter listing for the dependent parameters.

        Args:
            dependent_param_list: the list list of dependent params
            exclude_list: a list of parameters to exclude from this listing, note that this will only exclude the
                definition of the parameter, not the dependency code.
        """
        if dependent_param_list is None:
            dependent_param_list = self._model_functions_info.get_dependency_fixed_parameters_list(exclude_priors=True)

        func = ''
        for m, p in dependent_param_list:
            dependency = self._model_functions_info.get_parameter_value('{}.{}'.format(m.name, p.name))

            if dependency.pre_transform_code:
                func += "\t" * 4 + self._convert_parameters_dot_to_bar(dependency.pre_transform_code)

            assignment = self._convert_parameters_dot_to_bar(dependency.assignment_code)
            name = '{}.{}'.format(m.name, p.name).replace('.', '_')
            data_type = p.basic_ctype
            func += "\t" * 4 + data_type + ' ' + name + ' = ' + assignment + ';' + "\n"
        return func

    def _get_fixed_parameters_as_var_data(self):
        var_data_dict = {}
        for m, p in self._model_functions_info.get_value_fixed_parameters_list():
            value = self._model_functions_info.get_parameter_value('{}.{}'.format(m.name, p.name))
            param_name = '{}.{}'.format(m.name, p.name).replace('.', '_')

            if all_elements_equal(value):
                var_data_dict[param_name] = Scalar(get_single_value(value), ctype=p.ctype)
            else:
                var_data_dict[param_name] = Array(value, ctype=p.ctype, as_scalar=True)
        return var_data_dict

    def _get_bounds_as_var_data(self):
        lower_bounds = []
        upper_bounds = []

        for m, p in self._model_functions_info.get_estimable_parameters_list():
            lower_bound = self._lower_bounds['{}.{}'.format(m.name, p.name)]
            upper_bound = self._upper_bounds['{}.{}'.format(m.name, p.name)]

            for elements, value in zip((lower_bounds, upper_bounds), (lower_bound, upper_bound)):
                data = value

                if all_elements_equal(value):
                    elements.append(Scalar(get_single_value(data), ctype=p.ctype))
                else:
                    elements.append(Array(data, ctype='float', as_scalar=True))

        return {'lower_bounds': CompositeArray(lower_bounds, 'float', address_space='local'),
                'upper_bounds': CompositeArray(upper_bounds, 'float', address_space='local')}

    def _get_spherical_parameters(self):
        """Get the spherical parameter pairs for each of the compartments.

        Returns:
            List[tuple]: (compartment, (spherical parameters)) nested tuple for each compartment that has
                the spherical coordinate parameters.
        """
        spherical_params = []
        for compartment in self._model_functions_info.get_compartment_models():
            polar = list(filter(lambda p: isinstance(p, PolarAngleParameter), compartment.get_parameters()))
            azimuth = list(filter(lambda p: isinstance(p, AzimuthAngleParameter), compartment.get_parameters()))

            if polar and azimuth:
                spherical_params.append((compartment, (polar[0], azimuth[0])))
        return spherical_params

    def _get_spherical_transformation_func(self):
        """The transformation function for restraining the spherical coordinates with the right spherical hemisphere."""
        return SimpleCLFunction.from_string('''
            void _ensure_right_spherical_hemisphere(local mot_float_type* theta, local mot_float_type* phi){
                if(*phi > M_PI_F){
                    *phi -= M_PI_F;
                    *theta = M_PI_F - *theta;
                }
                else if(*phi < 0){
                    *phi += M_PI_F;
                    *theta = M_PI_F - *theta;
                }
                *theta = *theta - floor(*theta / M_PI_F) * M_PI_F;
                *phi = *phi - floor(*phi / M_PI_F) * M_PI_F;
            }
        ''')

    def _get_spherical_transformations(self, vector_name='x'):
        """Get the spherical transformations as a list of CL functions on the parameter vector.

        Args:
            vector_name (str): the name of the vector on which to operate
        """
        spherical_transformations = []
        for compartment, params in self._get_spherical_parameters():
            polar_is_free = self._model_functions_info.is_parameter_estimable(compartment, params[0])
            azimuth_is_free = self._model_functions_info.is_parameter_estimable(compartment, params[1])

            if polar_is_free and azimuth_is_free:
                polar_ind = self._model_functions_info.get_parameter_estimable_index(compartment, params[0])
                azimuth_ind = self._model_functions_info.get_parameter_estimable_index(compartment, params[1])
                spherical_transformations.append(
                    '_ensure_right_spherical_hemisphere({vn} + {pind}, {vn} + {aind});'.format(
                        vn=vector_name, pind=polar_ind, aind=azimuth_ind)
                )
            elif polar_is_free:
                polar_ind = self._model_functions_info.get_parameter_estimable_index(compartment, params[0])
                spherical_transformations.append(
                    '{vn}[{pind}] = x[{pind}] - floor({vn}[{pind}] / M_PI_F) * M_PI_F;'.format(
                        vn=vector_name, pind=polar_ind))
            elif azimuth_is_free:
                azimuth_ind = self._model_functions_info.get_parameter_estimable_index(compartment, params[1])
                spherical_transformations.append(
                    '{vn}[{aind}] = {vn}[{aind}] - floor({vn}[{aind}] / M_PI_F) * M_PI_F;'.format(
                        vn=vector_name, aind=azimuth_ind))
        return spherical_transformations

    def _get_rotational_transformations(self, vector_name='x'):
        """Get the transformations for the rotational parameters.

        Args:
            vector_name (str): the name of the vector on which to operate
        """
        rotational_transformations = []
        for m, p in self._model_functions_info.get_estimable_parameters_list():
            if isinstance(p, RotationalAngleParameter):
                param_ind = self._model_functions_info.get_parameter_estimable_index(m, p)
                modulus = p.modulus

                if modulus is np.pi:
                    modulus = 'M_PI'

                rotational_transformations.append(
                    '{vn}[{pind}] = {vn}[{pind}] - floor(x[{pind}] / {mod}) * {mod};'.format(
                        vn=vector_name, pind=param_ind, mod=modulus))
        return rotational_transformations

    def _transform_observations(self, observations):
        """Apply a transformation on the observations before fitting.

        This function is called by get_problems_var_data() just before the observations are handed over to the
        CL routine.

        To implement any behaviour here, you can override this function and add behaviour that changes the observations.

        Args:
            observations (ndarray): the 2d matrix with the observations.

        Returns:
            observations (ndarray): a 2d matrix of the same shape as the input. This should hold the transformed data.
        """
        return observations

    def _get_numdiff_max_step_sizes(self):
        """Get the numerical differentiation step for each parameter.

        Returns:
            list[float]: for each free parameter the numerical differentiation step size to use
        """
        return [p.numdiff_info.max_step for _, p in self._model_functions_info.get_estimable_parameters_list()]

    def _get_numdiff_scaling_factors(self):
        """Get the parameter scaling factor for each parameter.

        Returns:
            list[float]: for each parameter the scaling factor to use.
        """
        return [p.numdiff_info.scaling_factor for _, p in self._model_functions_info.get_estimable_parameters_list()]

    def _get_numdiff_use_bounds(self):
        """Get the boolean array indicating the use the of the bounds when taking the numerical derivative.

        Returns:
            list[bool]: a list with booleans, with True if we should use the bounds for that parameter, and False
                if we don't have to.
        """
        return [p.numdiff_info.use_bounds for _, p in self._model_functions_info.get_estimable_parameters_list()]

    def _get_numdiff_use_upper_bounds(self):
        """Check for each parameter if we should be using the upper bounds when taking the derivative.

        This is only used if use_bounds is True for a parameter.

        Returns:
            list[bool]: per parameter a boolean to identify if we should use the upper bounds for that parameter.
        """
        return [p.numdiff_info.use_upper_bound for _, p in self._model_functions_info.get_estimable_parameters_list()]

    def _get_numdiff_use_lower_bounds(self):
        """Check for each parameter if we should be using the lower bounds when taking the derivative.

        This is only used if use_bounds is True for a parameter.

        Returns:
            list[bool]: per parameter a boolean to identify if we should use the lower bounds for that parameter.
        """
        return [p.numdiff_info.use_lower_bound for _, p in self._model_functions_info.get_estimable_parameters_list()]

    def _get_log_likelihood_function(self, support_for_objective_list, negative_ll):
        eval_function_info = self._get_model_eval_function(include_cache_init_func=False)
        eval_model_func = self._likelihood_function
        cache_init_func = self._get_cache_init_function()

        eval_call_args = []
        param_listing = ''
        for p in eval_model_func.get_parameters():
            if isinstance(p, CurrentObservationParam):
                eval_call_args.append('model_data->observations[observation_ind]')
            elif isinstance(p, AllObservationsParam):
                eval_call_args.append('model_data->observations')
            elif isinstance(p, ObservationIndexParam):
                eval_call_args.append('observation_ind')
            elif isinstance(p, NmrObservationsParam):
                eval_call_args.append('nmr_observations')
            elif isinstance(p, CurrentModelSignalParam):
                eval_call_args.append(eval_function_info.get_cl_function_name() + '(data, x, observation_ind)')
            else:
                param_listing += self._get_param_listing_for_param(eval_model_func, p)
                eval_call_args.append('{}.{}'.format(eval_model_func.name, p.name).replace('.', '_'))

        cache_init = self._get_cache_init_function().get_cl_function_name() + '(data, x);'

        cl_body = '''
            double getObjectiveInstanceValue(
                    local const mot_float_type* const x,
                    void* data
                    ''' + (', local mot_float_type* objective_list' if support_for_objective_list else '') + '''){

                _mdt_model_data* model_data = (_mdt_model_data*)data;

                ''' + param_listing + '''
                ''' + cache_init + '''

                const uint nmr_observations = ''' + str(self.get_nmr_observations()) + ''';
                uint local_id = get_local_id(0);
                uint workgroup_size = get_local_size(0);

                double eval;
                uint observation_ind;
                model_data->local_tmp[local_id] = 0;

                uint batch_range;
                uint offset = get_workitem_batch(nmr_observations, &batch_range);

                for(uint i = offset; i < offset + batch_range; i++){
                    observation_ind = i;

                    eval = ''' + ('-' if negative_ll else '') + ''' ''' + \
                            eval_model_func.get_cl_function_name() + '(' + ', '.join(eval_call_args) + ''');

                    ''' + ('eval *= model_data->volume_weights[observation_ind];'
                    if self._input_data.volume_weights is not None else '') + '''

                    model_data->local_tmp[local_id] += eval;

                    ''' + ('''
                    if(objective_list){
                        // used by the nonlinear least-squares routines, which square the observations
                        objective_list[observation_ind] = sqrt(fabs(eval));
                    }
                    ''' if support_for_objective_list else '') + '''
                }
                barrier(CLK_LOCAL_MEM_FENCE);

                double sum = 0;
                for(uint i = 0; i < min(nmr_observations, workgroup_size); i++){
                    sum += model_data->local_tmp[i];
                }
                return sum;
            }
        '''
        return SimpleCLFunction.from_string(cl_body, dependencies=[cache_init_func, eval_function_info,
                                                                   eval_model_func])

    def _get_cache_init_function(self):
        """Get the function to initialize all the caches of all the compartments in this composite model.

        This does not include the cache typedefinitions.

        Returns:
            CLFunction: the CL function for initializing the data caches.
        """

        def include_cache_init_calls():
            calls = []
            for compartment in self._model_functions_info.get_compartment_models():
                if compartment.get_cache_init_function():
                    func = compartment.get_cache_init_function()

                    param_list = []
                    for param in func.get_parameters():
                        if isinstance(param, FreeParameter):
                            param_list.append('{}.{}'.format(compartment.name, param.name).replace('.', '_'))
                        elif isinstance(param, NoiseStdInputParameter):
                            std_param = self._model_functions_info.get_noise_std_param()
                            param_list.append(
                                '{}.{}'.format(self._likelihood_function.name, std_param.name).replace('.', '_'))
                        elif isinstance(param, DataCacheParameter):
                            param_list.append('model_data->cache->' + compartment.name)

                    calls.append('{}({});'.format(func.get_cl_function_name(), ', '.join(param_list)))
            return '\n'.join(calls)

        def get_function_body():
            param_listing = ''
            param_listing += self._get_fixed_parameters_listing()
            param_listing += self._get_estimable_parameters_listing()
            param_listing += self._get_dependent_parameters_listing()

            body = '_mdt_model_data* model_data = (_mdt_model_data*)data;'
            body += dedent(param_listing.replace('\t', ' ' * 4)) + '\n'

            body += include_cache_init_calls()

            body += '\n'
            return body

        dependencies = []
        for compartment in self._model_functions_info.get_compartment_models():
            if compartment.get_cache_init_function():
                dependencies.extend(compartment.get_dependencies())
                dependencies.append(compartment.get_cache_init_function())

        parameters = ['void* data',
                      'local const mot_float_type* const x']

        return SimpleCLFunction(
            'void', '_initCaches', parameters, get_function_body(), dependencies=dependencies)

    def _get_model_eval_function(self, include_cache_init_func=False):
        """Get the evaluation function that evaluates the model at the given parameters.

        The returned function should not do any error calculations, it should merely return the result of
        evaluating the model for the given parameters.

        Returns:
            mot.lib.cl_function.CLFunction: a named CL function with the following signature:

                .. code-block:: c

                    double <func_name>(void* data, mot_float_type* x, uint observation_index);
        """
        protocol_cbs = self._get_protocol_update_callbacks()
        composite_model_function = self.get_composite_model_function()

        def get_composite_model_function_signature(composite_model):
            """Create the parameter call code for the composite model.

            Args:
                composite_model (CompositeModelFunction): the composite model function
            """
            param_list = []
            for model, param in composite_model.get_model_parameter_list():
                if isinstance(param, ProtocolParameter):
                    param_list.append(param.name)
                elif isinstance(param, CurrentObservationParam):
                    if self._input_data.observations is not None:
                        param_list.append('model_data->observations[observation_index]')
                    else:
                        param_list.append('0.0')
                elif isinstance(param, AllObservationsParam):
                    if self._input_data.observations is not None:
                        param_list.append('model_data->observations')
                    else:
                        param_list.append('null')
                elif isinstance(param, ObservationIndexParam):
                    if self._input_data.observations is not None:
                        param_list.append('observation_index')
                    else:
                        param_list.append('0')
                elif isinstance(param, NmrObservationsParam):
                    if self._input_data.observations is not None:
                        param_list.append(str(self.get_nmr_observations()))
                    else:
                        param_list.append('0')
                elif isinstance(param, NoiseStdInputParameter):
                    std_param = self._model_functions_info.get_noise_std_param()
                    param_list.append('{}.{}'.format(self._likelihood_function.name, std_param.name).replace('.', '_'))
                elif isinstance(param, FreeParameter):
                    param_list.append('{}.{}'.format(model.name, param.name).replace('.', '_'))
                elif isinstance(param, DataCacheParameter):
                    param_list.append('model_data->cache->' + model.name)

            return composite_model.get_cl_function_name() + '(' + ', '.join(param_list) + ')'

        def get_protocol_cb_call(callback, callback_index):
            call_args = []
            for protocol_parameter_name in callback.get_protocol_parameter_names():
                call_args.append('&{}'.format(protocol_parameter_name))

            for key, value in callback.get_kernel_input_data().items():
                call_args.append('model_data->protocol_update_cbs->cb{}_{}'.format(str(callback_index), key))

            call_args.append('observation_index')

            func_name = callback.get_callback_function().get_cl_function_name()
            return '{}({});'.format(func_name, ', '.join(call_args))

        def get_function_body():
            param_listing = self._get_parameters_listing()

            body = '_mdt_model_data* model_data = (_mdt_model_data*)data;'
            body += dedent(param_listing.replace('\t', ' ' * 4)) + '\n'

            for ind, cb in enumerate(protocol_cbs):
                body += get_protocol_cb_call(cb, ind) + '\n'

            if include_cache_init_func:
                body += self._get_cache_init_function().get_cl_function_name() + '(data, x);'

            body += '\n'
            body += 'return ' + get_composite_model_function_signature(composite_model_function) + ';'
            return body

        def get_dependencies():
            deps = []
            if include_cache_init_func:
                deps.append(self._get_cache_init_function())
            deps.append(composite_model_function)
            deps.extend([cb.get_callback_function() for cb in protocol_cbs])
            return deps

        def get_function_parameters():
            parameters = ['void* data',
                          'local const mot_float_type* const x',
                          'uint observation_index']
            return parameters

        return SimpleCLFunction(
            'double', '_evaluateModel', get_function_parameters(), get_function_body(), dependencies=get_dependencies())

    def _get_protocol_update_callbacks(self):
        """Get a list of all protocol update callbacks"""
        protocol_update_callbacks = []

        grad_dev_cb = self._get_gradient_deviation_proposal_callback()
        if grad_dev_cb is not None:
            protocol_update_callbacks.append(grad_dev_cb)

        return protocol_update_callbacks

    def _get_protocol_update_callbacks_kernel_inputs(self):
        """Get the kernel input data needed by the proposal update methods.

        Returns:
            Dict[str, KernelData]: the kernel data elements to load for the protocol callback functions.
        """
        return_items = {}
        for ind, cb in enumerate(self._get_protocol_update_callbacks()):
            for key, value in cb.get_kernel_input_data().items():
                return_items['cb{}_{}'.format(str(ind), key)] = value
        return return_items

    def _get_nmr_problems(self, roi_indices=None):
        if roi_indices is None:
            if self._input_data:
                return self._input_data.nmr_voxels
            return 0
        return len(roi_indices)

    def _get_cache_struct(self):
        """Get all cache Structs for this composite model.

        This prepares the cache in the local memory address space.
        """
        elements = {}
        for compartment in self._model_functions_info.get_compartment_models():
            if compartment.get_cache_struct('local'):
                elements.update(compartment.get_cache_struct('local'))
        return elements

    def _get_constraints_function(self):
        constraint_ind = 0
        func_calls = []
        for constraint_func in self._constraints:
            func_call_params = []
            for param in constraint_func.get_parameters():
                if isinstance(param, FreeParameter):
                    func_call_params.append(param.name)
                elif isinstance(param, ProtocolParameter):
                    func_call_params.append(self._get_protocol_parameter_assignment(param))

            func_calls.append('{func}({params}, constraints + {ind});'.format(
                func=constraint_func.get_cl_function_name(),
                params=', '.join(func_call_params),
                ind=constraint_ind
            ))
            constraint_ind += constraint_func.get_nmr_constraints()

        params_listing = ''
        params_listing += self._get_fixed_parameters_listing()
        params_listing += self._get_estimable_parameters_listing()
        params_listing += self._get_dependent_parameters_listing()

        nmr_constraints = sum([c.get_nmr_constraints() for c in self._constraints])

        return SimpleConstraintFunction.from_string('''
                void modeling_constraints(
                        local const mot_float_type* const x,
                        void* data,
                        local mot_float_type* constraints){

                    if(get_local_id(0) == 0){
                        for(uint i = 0; i < ''' + str(nmr_constraints) + '''; i++){
                            constraints[i] = 0;
                        }
                    }
                    barrier(CLK_LOCAL_MEM_FENCE);

                    _mdt_model_data* model_data = (_mdt_model_data*)data;
                    ''' + params_listing + '''

                    uint observation_index;
                    uint batch_range;
                    uint offset = get_workitem_batch(''' + str(self.get_nmr_observations()) + ''', &batch_range);
                    for(int i = offset; i < offset + batch_range; i++){
                        observation_index = i;
                        ''' + '\n'.join(func_calls) + '''
                    }
                    barrier(CLK_LOCAL_MEM_FENCE);
            }
        ''', dependencies=self._constraints,
             nmr_constraints=nmr_constraints)

    def _get_log_prior_function(self):
        def get_dependencies():
            dependencies = []
            for i, (m, p) in enumerate(self._model_functions_info.get_estimable_parameters_list()):
                dependencies.append(p.sampling_prior)

            for model_prior in self._model_priors:
                dependencies.append(model_prior)
            return dependencies

        def get_body():
            cl_str = '_mdt_model_data* model_data = (_mdt_model_data*)data;\n' \
                     'mot_float_type prior = 1.0;\n'
            for i, (m, p) in enumerate(self._model_functions_info.get_estimable_parameters_list()):
                name = '{}.{}'.format(m.name, p.name)

                function_name = p.sampling_prior.get_cl_function_name()

                if m.get_prior_parameters(p):
                    prior_params = []
                    for prior_param in m.get_prior_parameters(p):
                        if self._model_functions_info.is_parameter_estimable(m, prior_param):
                            estimable_index = self._model_functions_info.get_parameter_estimable_index(m, prior_param)
                            prior_params.append('x[{}]'.format(estimable_index))
                        else:
                            prior_params.append('model_data->{}.{}'.format(m.name, prior_param.name).replace('.', '_'))

                    cl_str += 'prior *= {}(x[{}], {}, {}, {});\n'.format(
                        function_name,
                        i,
                        'model_data->bounds->lower_bounds[' + str(i) + ']',
                        'model_data->bounds->upper_bounds[' + str(i) + ']',
                        ', '.join(prior_params))
                else:
                    cl_str += 'prior *= {}(x[{}], {}, {});\n'.format(
                        function_name,
                        i,
                        'model_data->bounds->lower_bounds[' + str(i) + ']',
                        'model_data->bounds->upper_bounds[' + str(i) + ']')

            for model_prior in self._model_priors:
                function_name = model_prior.get_cl_function_name()
                parameters = []

                for param in model_prior.get_parameters():
                    assignment_value = self._get_free_parameter_assignment_value(
                        *self._model_functions_info.get_model_parameter_by_name(param.name))
                    parameters.append(assignment_value)

                cl_str += '\tprior *= {}({});\n'.format(function_name, ', '.join(parameters))

            cl_str += '\n\treturn log(prior);'
            return cl_str

        return SimpleCLFunction(
            'mot_float_type', 'getLogPrior',
            ['local const mot_float_type* const x', 'void* data'],
            get_body(), dependencies=get_dependencies())

    def _get_weight_prior(self):
        """Get the prior limiting the weights between 0 and 1"""
        weights = []
        for (m, p) in self._model_functions_info.get_estimable_weights():
            weights.append(('mot_float_type', '{}.{}'.format(m.name, p.name)))

        if len(weights) > 1:
            return SimpleCLFunction(
                'mot_float_type', 'prior_estimable_weights_sum_to_one',
                ['{} {}'.format(el[0], el[1]) for el in weights],
                'return (' + ' + '.join(el[1].replace('.', '_') for el in weights) + ') <= 1;')
        return None


class SamplingPostProcessingData(collections.Mapping):

    def __init__(self, samples, param_names, fixed_parameters):
        """Stores the sample output for use in the model defined post-processing routines.

        In general, this class acts as a dictionary with as keys the parameter names (as ``<compartment>.<parameter>``).
        Each value may be a scalar, a 1d map or a 2d set of samples. Additional object attributes can also be used
        by the post-processing routines.

        Args:
            samples (ndarray): a matrix of shape (d, p, n) with d problems, p parameters and n samples
            param_names (list of str): the list containing the names of the parameters in the samples array
            fixed_parameters (dict): for every fixed parameter the fixed values (either a scalar or a map).
        """
        self._samples = samples
        self._param_names = param_names
        self._fixed_parameters = fixed_parameters

    @property
    def samples(self):
        """Get the array of samples as returned by the sample routine.

        For the names of the corresponding parameters, please see :py:attr:`~sampled_parameter_names`.

        Returns:
            ndarray: a matrix of shape (d, p, n) with d problems, p parameters and n samples.
        """
        return self._samples

    @property
    def sampled_parameter_names(self):
        """Get the names of the parameters that have been sampled.

        Returns:
            list of str: the names of the parameters in the samples.
        """
        return self._param_names

    @property
    def fixed_parameters(self):
        """Get the dictionary with all the fixed parameter values.

        Returns:
            dict: the names and values of the fixed parameters
        """
        return self._fixed_parameters

    def __getitem__(self, key):
        if key in self._param_names:
            return self._samples[:, self._param_names.index(key), :]
        return self._fixed_parameters[key]

    def __iter__(self):
        for key in self._param_names:
            yield key
        for key in self._fixed_parameters:
            yield key

    def __len__(self):
        return len(self._param_names) + len(self._fixed_parameters)


class CompositeModelFunction(SimpleCLFunction):

    def __init__(self, model_tree, signal_noise_model=None):
        """The model function for the total constructed model.

        This combines all the functions in the model tree into one big function and exposes that function and
        its parameters.

        Args:
            model_tree (mdt.model_building.trees.CompartmentModelTree): the model tree object
            signal_noise_model (mdt.model_building.signal_noise_models.SignalNoiseModel): the optional signal
                noise model to use to add noise to the model prediction
        """
        self._model_tree = model_tree
        self._signal_noise_model = signal_noise_model
        self._models = list(self._model_tree.get_compartment_models())
        if self._signal_noise_model:
            self._models.append(self._signal_noise_model)
        self._parameter_model_list = list((m, p) for m in self._models for p in m.get_parameters())

        cl_function_name = '_composite_model_function'

        super().__init__(
            'double', cl_function_name,
            [p.get_renamed(external_name.replace('.', '_'))
             for m, p, external_name in self.get_model_function_parameters()],
            self._get_model_function_body(),
            dependencies=self._models)

    def evaluate(self, inputs, nmr_instances, **kwargs):
        inputs = {k.replace('.', '_'): v for k,v in inputs.items()}
        return super().evaluate(inputs, nmr_instances, **kwargs)

    def get_model_parameter_list(self):
        """Get the model and parameter tuples that constructed this composite model.

        This is used by the model builder, to construct the model function call.

        Returns:
            list of tuple: the list of (model, parameter) tuples for each of the models and parameters.
        """
        return [(m, p) for m, p, ext_name in self.get_model_function_parameters()]

    def get_model_function_parameters(self):
        """Get the parameters to use in the model function.

        Returns:
            list of tuples: per parameter a tuple with (model, parameter, cl_name, external_name)
                where the cl_name is how we reference the parameter in the CL code and the external_name is
                how we reference the parameter in a call to for example 'evaluate'.
        """
        seen_shared_params = []

        shared_params = []
        other_params = []

        shareable_param_types = (ProtocolParameter, CurrentObservationParam, NoiseStdInputParameter,
                                 AllObservationsParam, ObservationIndexParam, NmrObservationsParam)

        for m, p in self._parameter_model_list:
            if isinstance(p, shareable_param_types):
                if p.name not in seen_shared_params:
                    shared_params.append((m, p, p.name))
                    seen_shared_params.append(p.name)
            elif isinstance(p, (FreeParameter, DataCacheParameter)):
                other_params.append((m, p, '{}.{}'.format(m.name, p.name)))
        return shared_params + other_params

    def _get_model_function_body(self):
        """Get the CL code for the body of the model function as build by this model.

        Returns:
            str: the CL code for the body of this code
        """

        def build_model_expression():
            tree = self._build_model_from_tree(self._model_tree, 0)

            model_expression = ''
            if self._signal_noise_model:
                inputs = []
                for p in self._signal_noise_model.get_parameters():
                    if isinstance(p, CurrentModelSignalParam):
                        inputs.append('(' + tree + ')')
                    else:
                        inputs.append('{}.{}'.format(self._signal_noise_model.name, p.name).replace('.', '_'))

                model_expression += '{}({});'.format(self._signal_noise_model.get_cl_function_name(), ', '.join(inputs))
            else:
                model_expression += '(' + tree + ');'
            return model_expression

        return_str = 'return ' + build_model_expression()
        return dedent(return_str.replace('\t', '    '))

    def _build_model_from_tree(self, node, depth):
        """Construct the model equation from the provided model tree.

        Args:
            node: the next to to process
            depth (int): the current tree depth

        Returns:
            str: model (sub-)equation
        """
        shareable_param_types = (ProtocolParameter, CurrentObservationParam, NoiseStdInputParameter,
                                 AllObservationsParam, ObservationIndexParam, NmrObservationsParam)

        def model_to_string(model):
            """Convert a model to CL string."""
            param_list = []
            for param in model.get_parameters():
                if isinstance(param, shareable_param_types):
                    param_list.append(param.name)
                else:
                    param_list.append('{}.{}'.format(model.name, param.name).replace('.', '_'))
            return model.get_cl_function_name() + '(' + ', '.join(param_list) + ')'

        if not node.children:
            return model_to_string(node.data)
        else:
            subfuncs = []
            for child in node.children:
                if child.children:
                    subfuncs.append(self._build_model_from_tree(child, depth + 1))
                else:
                    subfuncs.append(model_to_string(child.data))

            operator = node.data
            func = (' ' + operator + ' ').join(subfuncs)

        if func[0] == '(':
            return '(' + func + ')'
        return '(' + "\n" + ("\t" * int((depth / 2) + 5)) + func + "\n" + ("\t" * int((depth / 2) + 4)) + ')'


class _ModelFunctionPriorToCompositeModelPrior(SimpleCLFunction):

    def __init__(self, model_function_prior, compartment_name):
        """Simple prior class for easily converting the compartment priors to composite model priors."""
        parameters = [SimpleCLFunctionParameter('mot_float_type {}.{}'.format(compartment_name, p.name))
                      for p in model_function_prior.get_parameters()]
        self._old_params = model_function_prior.get_parameters()

        super().__init__(
            model_function_prior.get_return_type(),
            model_function_prior.get_cl_function_name(),
            parameters,
            model_function_prior.get_cl_body(),
            dependencies=model_function_prior.get_dependencies()
        )

    def _get_parameter_signatures(self):
        declarations = []
        for p in self._old_params:
            new_p = p.get_renamed(p.name.replace('.', '_'))
            declarations.append(new_p.get_declaration())
        return declarations


class ModelFunctionsInformation:

    def __init__(self, model_tree, likelihood_function, signal_noise_model=None, enable_prior_parameters=False):
        """Contains centralized information about the model functions in the model builder parent.

        Args:
            model_tree (mdt.model_building.trees.CompartmentModelTree): the model tree object
            likelihood_function (mdt.model_building.likelihood_functions.LikelihoodFunction): the likelihood function to
                use for the resulting complete model
            signal_noise_model (mdt.model_building.signal_noise_models.SignalNoiseModel): the signal
                noise model to use to add noise to the model prediction
            enable_prior_parameters (boolean): adds possible prior parameters to the list of parameters in the model
        """
        self._model_tree = model_tree
        self._likelihood_function = likelihood_function
        self._signal_noise_model = signal_noise_model
        self._enable_prior_parameters = enable_prior_parameters

        self._model_list = self._get_model_list()
        self._model_parameter_list = self._get_model_parameter_list()
        self._prior_parameters_info = self._get_prior_parameters_info()

        self._check_for_double_model_names()

        self._fixed_parameters = {'{}.{}'.format(m.name, p.name): p.fixed for m, p in
                                  self.get_model_parameter_list() if isinstance(p, FreeParameter)}
        self._fixed_values = {'{}.{}'.format(m.name, p.name): p.value for m, p in self.get_free_parameters_list()}

        self._parameter_values = {'{}.{}'.format(m.name, p.name): p.value for m, p in self.get_model_parameter_list()
                                  if hasattr(p, 'value')}

        self._original_parameter_values = copy.deepcopy(self._parameter_values)

    def set_parameter_value(self, parameter_name, value):
        """Set the value we will use for the given parameter.

        If the parameter is a fixed free parameter we will set the fixed value to the given value.

        Args:
            parameter_name (string): A model.param name like 'Ball.d'
            value (scalar or vector or string or AbstractParameterDependency): The value or dependency
                to fix the given parameter to. Dependency objects and strings are only value for fixed free parameters.
        """
        if parameter_name in self._fixed_parameters and self._fixed_parameters[parameter_name]:
            self._fixed_values[parameter_name] = value
        else:
            self._parameter_values[parameter_name] = value

    def get_parameter_value(self, parameter_name):
        """Get the parameter value for the given parameter. This is regardless of model fixation.

        Returns:
            float or ndarray: the value for the given parameter
        """
        if parameter_name in self._fixed_parameters and self._fixed_parameters[parameter_name]:
            return self._fixed_values[parameter_name]
        return self._parameter_values[parameter_name]

    def get_default_parameter_value(self, parameter_name):
        """Get the default parameter value for the given parameter. This is regardless of model fixation.

        The default parameter value is the parameter value as originally defined in the model parameter.

        Returns:
            float or ndarray: the value for the given parameter
        """
        return self._original_parameter_values[parameter_name]

    def fix_parameter(self, parameter_name, value):
        """Fix the indicated free parameter to the given value.

        Args:
            parameter_name (string): A model.param name like 'Ball.d'
            value (scalar or vector or string or AbstractParameterDependency): The value or dependency
                to fix the given parameter to.
        """
        self._fixed_parameters[parameter_name] = True
        self._fixed_values[parameter_name] = value

    def unfix(self, parameter_name):
        """Unfix the indicated parameter

        Args:
            parameter_name (str): the name of the parameter to fix or unfix
        """
        self._fixed_parameters[parameter_name] = False

    def get_model_list(self):
        """Get the list of all the applicable model functions

        Returns:
            list of mdt.model_building.model_functions.ModelCLFunction: the list of model functions.
        """
        return self._model_list

    def get_compartment_models(self):
        """Get a list of all the compartment models in the model.

        Returns:
            list of mdt.models.compartments.CompartmentModel: the compartment models in this composite model
        """
        return self._model_tree.get_compartment_models()

    def get_model_parameter_list(self):
        """Get a list of all model, parameter tuples.

        Returns:
            list of tuple: the list of tuples containing (model, parameters)
        """
        param_list = copy.copy(self._model_parameter_list)

        if self._enable_prior_parameters:
            for prior_info in self._prior_parameters_info.values():
                if prior_info:
                    param_list.extend(prior_info)

        return param_list

    def get_free_parameters_list(self, exclude_priors=False):
        """Gets the free parameters as (model, parameter) tuples from the model listing.
        This does not incorporate checking for fixed parameters.

        Args:
            exclude_priors (boolean): if we want to exclude the parameters for the priors

        Returns:
            list of tuple: the list of tuples containing (model, parameters)
        """
        free_params = list((m, p) for m, p in self._model_parameter_list if isinstance(p, FreeParameter))

        if not exclude_priors:
            if self._enable_prior_parameters:
                prior_params = []
                for m, p in free_params:
                    prior_params.extend((m, prior_p) for prior_p in m.get_prior_parameters(p)
                                        if self.is_parameter_estimable(m, p) and isinstance(prior_p, FreeParameter))
                free_params.extend(prior_params)

        return free_params

    def get_estimable_parameters_list(self, exclude_priors=False):
        """Gets a list (as model, parameter tuples) of all parameters that are estimable.

        Args:
            exclude_priors (boolean): if we want to exclude the parameters for the priors

        Returns:
            list of tuple: the list of estimable parameters
        """
        estimable_parameters = [(m, p) for m, p in self._model_parameter_list if self.is_parameter_estimable(m, p)]

        if not exclude_priors:
            if self._enable_prior_parameters:
                prior_params = []
                for m, p in estimable_parameters:
                    prior_params.extend((m, prior_p) for prior_p in m.get_prior_parameters(p) if not prior_p.fixed)
                estimable_parameters.extend(prior_params)

        return estimable_parameters

    def get_all_protocol_parameters(self):
        """Gets the protocol parameters (as model, parameter tuples) from the model listing."""
        return list((m, p) for m, p in self.get_model_parameter_list() if isinstance(p, ProtocolParameter))

    def get_unique_protocol_parameters(self):
        """Gets the unique protocol parameters from the model listing.

        This does not return the corresponding compartment model, only the parameters.

        Returns:
            List[ProtocolParameter]: the list of protocol parameters
        """
        return list(set(p for _, p in self.get_model_parameter_list() if isinstance(p, ProtocolParameter)))

    def get_value_fixed_parameters_list(self, exclude_priors=False):
        """Gets a list (as model, parameter tuples) of all parameters that are fixed to a value.

        Args:
            exclude_priors (boolean): if we want to exclude the parameters for the priors

        Returns:
            list of tuple: the list of value fixed parameters
        """
        value_fixed_parameters = []
        for m, p in self.get_free_parameters_list(exclude_priors=exclude_priors):
            if self.is_fixed_to_value('{}.{}'.format(m.name, p.name)):
                value_fixed_parameters.append((m, p))
        return value_fixed_parameters

    def get_dependency_fixed_parameters_list(self, exclude_priors=False):
        """Gets a list (as model, parameter tuples) of all parameters that are fixed to a dependency.

        Args:
            exclude_priors (boolean): if we want to exclude the parameters for the priors

        Returns:
            list of tuple: the list of value fixed parameters
        """
        dependency_fixed_parameters = []
        for m, p in self.get_free_parameters_list(exclude_priors=exclude_priors):
            if self.is_fixed_to_dependency(m, p):
                dependency_fixed_parameters.append((m, p))
        return dependency_fixed_parameters

    def get_protocol_parameter_by_name(self, protocol_name):
        """Get the first instance of a protocol parameter that matches the given name.

        Args:
            protocol_name (str): the protocol parameter name for which we want the corresponding parameter object.

        Returns:
            ProtocolParameter: the parameter matching the protocol name
        """
        for p in self.get_unique_protocol_parameters():
            if p.name == protocol_name:
                return p
        raise ValueError('Could not find a protocol parameter with the name "{}".'.format(protocol_name))

    def get_model_parameter_by_name(self, parameter_name):
        """Get the parameter object of the given full parameter name in dot format.

        Args:
            parameter_name (string): the parameter name in dot format ``<model>.<param>``, or in bar format
                ``<model>_<param>``. If the bar format leads to ambiguous results, an exception will be raised.

        Returns:
            tuple: containing the (model, parameter) pair for the given parameter name
        """
        matches = []
        for m, p in self.get_model_parameter_list():
            if '{}.{}'.format(m.name, p.name) == parameter_name:
                matches.append((m, p))
            elif '{}_{}'.format(m.name, p.name) == parameter_name:
                matches.append((m, p))

        if not matches:
            raise ValueError('The parameter with the name "{}" could not be '
                             'found in this model.'.format(parameter_name))
        elif len(matches) > 1:
            raise ValueError('Two parameters with the same name have been found in this model for the search key "{}", '
                             'namely: {}'.format(parameter_name,
                                                 ', '.join('{}.{}'.format(m.name, p.name) for m, p in matches)))
        return matches[0]

    def is_fixed(self, parameter_name):
        """Check if the given (free) parameter is fixed or not (either to a value or to a dependency).

        Args:
            parameter_name (str): the name of the parameter to check if it is fixed, in dot format.

        Returns:
            boolean: if the parameter is fixed or not (can be fixed to a value or dependency).
        """
        return parameter_name in self._fixed_parameters and self._fixed_parameters[parameter_name]

    def is_fixed_to_value(self, parameter_name):
        """Check if the given (free) parameter is fixed to a value.

        Args:
            parameter_name (str): the name of the parameter to check if it is fixed, in dot format.

        Returns:
            boolean: if the parameter is fixed to a value or not
        """
        if self.is_fixed(parameter_name):
            return not isinstance(self._fixed_values[parameter_name], AbstractParameterDependency)
        return False

    def is_fixed_to_dependency(self, model, param):
        """Check if the given model and parameter name combo has a dependency.

        Args:
            model (mdt.model_building.model_functions.ModelCLFunction): the model function
            param (mot.cl_parameter.CLFunctionParameter): the parameter

        Returns:
            boolean: if the given parameter has a dependency
        """
        model_param_name = '{}.{}'.format(model.name, param.name)
        if self.is_fixed(model_param_name):
            return isinstance(self._fixed_values[model_param_name], AbstractParameterDependency)
        return False

    def is_parameter_estimable(self, model, param):
        """Check if the given model parameter is estimable.

        A parameter is estimable if it is of the Free parameter type and is not fixed.

        Args:
            model (mdt.model_building.model_functions.ModelCLFunction): the model function
            param (mot.cl_parameter.CLFunctionParameter): the parameter

        Returns:
            boolean: true if the parameter is estimable, false otherwise
        """
        return isinstance(param, FreeParameter) and not self.is_fixed('{}.{}'.format(model.name, param.name))

    def get_weights(self):
        """Get all the model functions/parameter tuples of the models that are a subclass of WeightType

        Returns:
            list: the list of compartment models that are a subclass of WeightType as (model, parameter) tuples.
        """
        weight_models = [m for m in self._model_tree.get_compartment_models() if isinstance(m, WeightType)]
        weights = []
        for m in weight_models:
            for p in m.get_free_parameters():
                weights.append((m, p))
        return weights

    def get_estimable_weights(self):
        """Get all the estimable weights.

        Returns:
            list of tuples: the list of compartment models/parameter pairs for models that are a subclass of WeightType
        """
        return [(m, p) for m, p in self.get_weights() if self.is_parameter_estimable(m, p)]

    def get_parameter_estimable_index(self, model, param):
        """Get the index of this parameter in the parameters list

        This returns the position of this parameter in the 'x', parameter vector in the CL kernels.

        Args:
            model (mdt.model_building.model_functions.ModelCLFunction): the model function
            param (mot.cl_parameter.CLFunctionParameter): the parameter

        Returns:
            int: the index of the requested parameter in the list of optimized parameters

        Raises:
            ValueError: if the given parameter could not be found as an estimable parameter.
        """
        ind = 0
        for m, p in self.get_estimable_parameters_list():
            if m.name == model.name and p.name == param.name:
                return ind
            ind += 1
        raise ValueError('The given estimable parameter "{}" could not be found in this model'.format(
            '{}.{}'.format(model.name, param.name)))

    def get_parameter_estimable_index_by_name(self, model_param_name):
        """Get the index of this parameter in the parameters list

        This returns the position of this parameter in the 'x', parameter vector in the CL kernels.

        Args:
            model_param_name (str): the model parameter name

        Returns:
            int: the index of the requested parameter in the list of optimized parameters

        Raises:
            ValueError: if the given parameter could not be found as an estimable parameter.
        """
        ind = 0
        for m, p in self.get_estimable_parameters_list():
            if '{}.{}'.format(m.name, p.name) == model_param_name:
                return ind
            ind += 1
        raise ValueError('The given estimable parameter "{}" could not be found in this model'.format(model_param_name))

    def has_parameter(self, model_param_name):
        """Check to see if the given parameter is defined in this model.

        Args:
            model_param_name (string): A model.param name like 'Ball.d'

        Returns:
            boolean: true if the parameter is defined in this model, false otherwise.
        """
        for m, p in self.get_model_parameter_list():
            if '{}.{}'.format(m.name, p.name) == model_param_name:
                return True
        return False

    def has_protocol_parameter(self, parameter_name):
        """Check if the model has the given protocol parameter defined.

        Args:
            parameter_name (str): the protocol parameter name.

        Returns:
            boolean: true if the given protocol parameter is defined in the model.
        """
        return parameter_name in list(p.name for p in self.get_unique_protocol_parameters())

    def get_noise_std_param(self):
        """Get a reference to the noise standard deviation parameter in the likelihood model.

        Returns:
            parameter: the reference to the NoiseStdFreeParam of the likelihood model
        """
        for p in self._likelihood_function.get_parameters():
            if isinstance(p, NoiseStdFreeParameter):
                return p

    def _get_model_parameter_list(self):
        """Get a list of all model, parameter tuples.

        Returns:
            list of tuple: the list of tuples containing (model, parameters)
        """
        return list((m, p) for m in self._model_list for p in m.get_parameters())

    def _get_prior_parameters_info(self):
        """Get a dictionary with the prior parameters for each of the model parameters.

        Returns:
            dict: lookup dictionary matching model names to parameter lists
        """
        prior_lookup_dict = {}
        for model in self._model_list:
            for param in model.get_free_parameters():
                prior_lookup_dict.update({
                    '{}.{}'.format(model.name, param.name): list((model, p) for p in model.get_prior_parameters(param))
                })
        return prior_lookup_dict

    def _get_model_list(self):
        """Get the list of all the applicable model functions"""
        models = list(self._model_tree.get_compartment_models())
        models.append(self._likelihood_function)
        if self._signal_noise_model:
            models.append(self._signal_noise_model)
        return models

    def _check_for_double_model_names(self):
        models = self._model_list
        model_names = []
        for m in models:
            if m.name in model_names:
                raise DoubleModelNameException("Double model name detected in the model tree.", m.name)
            model_names.append(m.name)


class ProtocolAdaptionCallbacks:
    """Information container for the protocol adaption callbacks.

    During model evaluation, it may be necessary to apply a transformation on some or all of the protocol
    inputs. For example, this allows loading the gradient deviations as a matrix that transforms the gradient
    vector just prior to model evaluation. The alternative would be to load the transformed protocol
    parameters directly as protocol values, which can be costly, hence these callback functions.
    """

    def get_protocol_parameter_names(self):
        """Get the names of the protocol parameters need for this proposal adaption callback.

        Returns:
            List[str]: the list of protocol parameters needed
        """
        raise NotImplementedError()

    def get_callback_function(self):
        """Get the CL callback function we will execute just prior model evaluation.

        The parameters of this callback function should be as follows. First the list of protocol parameter names,
        second the list of kernel input data elements and finally an uint for the current observation index.

        Returns:
            CLFunction: the CL function we will use
        """
        raise NotImplementedError()

    def get_kernel_input_data(self):
        """Get the additional kernel input data needed for this proposal callback to work.

        Returns:
            Dict[str, KernelData]: additional kernel input data
        """
        raise NotImplementedError()


def calculate_dependent_parameters(kernel_data, estimated_parameters_list,
                                   parameters_listing, dependent_parameter_names, cl_runtime_info=None):
    """Calculate the dependent parameters

    Some of the models may contain parameter dependencies. We would like to return the maps for these parameters
    as well as all the other maps. Since the dependencies are specified in CL, we have to recourse to CL to
    calculate these maps.

    This uses the calculated parameters in the results dictionary to run the parameters_listing in CL to obtain
    the maps for the dependent parameters.

    Args:
        kernel_data (dict[str: mot.lib.utils.KernelData]): the list of additional data to load
        estimated_parameters_list (list of ndarray): The list with the one-dimensional
            ndarray of estimated parameters
        parameters_listing (str): The parameters listing in CL
        dependent_parameter_names (list of list of str): Per parameter we would like to obtain the CL name and the
            result map name. For example: (('Wball_w', 'Wball.w'),)
        cl_runtime_info (mot.configuration.CLRuntimeInfo): the runtime information

    Returns:
        dict: A dictionary with the calculated maps for the dependent parameters.
    """

    def get_cl_function():
        parameter_write_out = ''
        for i, p in enumerate([el[0] for el in dependent_parameter_names]):
            parameter_write_out += 'results[' + str(i) + '] = ' + p + ";\n"

        return SimpleCLFunction.from_string('''
            void transform(private mot_float_type* x, global mot_float_type* results, void* data){
                _mdt_model_data* model_data = (_mdt_model_data*)data;

                ''' + parameters_listing + '''
                ''' + parameter_write_out + '''
            }
        ''')

    data_struct = {
        'data': kernel_data,
        'x': Array(np.dstack(estimated_parameters_list)[0, ...], ctype='mot_float_type'),
        'results': Zeros((estimated_parameters_list[0].shape[0], len(dependent_parameter_names)), 'mot_float_type')
    }

    get_cl_function().evaluate(data_struct, estimated_parameters_list[0].shape[0], cl_runtime_info=cl_runtime_info)
    return data_struct['results'].get_data()


class ExtraOptimizationMapsInfo(Mapping):

    def __init__(self, model, results, input_data, roi_indices):
        """Container holding information usable for computing extra optimization maps, after optimization.

        For backwards compatibility, this class functions both as a dictionary as well as a data container. That is,
        one can index this object with map names and it will forward those indices to the results container.
        Additionally, it provides some auxiliary data and functions for getting protocol information.

        Args:
            model (DMRICompositeModel): the model used to compute the results
            results (dict): the dictionary with all the optimization results
            input_data (mdt.lib.input_data.MRIInputData): the input data used during the optimization
            roi_indices (ndarray): a one dimensional array with indices in the region of interest
                This holds the voxels we are currently optimizing.
        """
        self.model = model
        self.results = results
        self.input_data = input_data
        self.roi_indices = roi_indices

    def copy_with_different_results(self, new_results):
        """Create a copy of this optimization maps info but then with different result maps.

        Args:
            results (dict): the dictionary with the new set of optimization results

        Returns:
            ExtraOptimizationMapsInfo: same as the current class but then with updated results
        """
        return ExtraOptimizationMapsInfo(self.model, new_results, self.input_data, self.roi_indices)

    def get_input_data(self, parameter_name):
        """Get the input data for the given parameter.

        This gets the input data from the protocol and for maps it only returns the voxels within the voxel roi indices
        we optimized.

        Args:
             parameter_name (str): the name of the parameter for which we want to get input data

        Returns:
            float, ndarray or None: either a scalar, a vector or a matrix with values for the given parameter.

        Raises:
            ValueError: if no suitable value can be found.
        """
        value = self.input_data.get_input_data(parameter_name)
        if value.shape[0] == np.count_nonzero(self.input_data.mask) and self.roi_indices is not None:
            return value[self.roi_indices]
        return value

    def __getitem__(self, item):
        return self.results[item]

    def __iter__(self):
        return self.results.__iter__()

    def __len__(self):
        return len(self.results)

