import collections
import logging
import logging.config as logging_config
import os
from contextlib import contextmanager
import numpy as np

import mot
from mot.configuration import CLRuntimeInfo, CLRuntimeAction
from .__version__ import VERSION, VERSION_STATUS, __version__

from mdt.configuration import get_logging_configuration_dict, get_optimizer_for_model, get_general_sampling_settings

try:
    logging_config.dictConfig(get_logging_configuration_dict())
except ValueError:
    print('Logging disabled')

from mdt.component_templates.parameters import FreeParameterTemplate, ProtocolParameterTemplate
from mdt.component_templates.batch_profiles import BatchProfileTemplate
from mdt.component_templates.compartment_models import CompartmentTemplate, WeightCompartmentTemplate
from mdt.component_templates.composite_models import CompositeModelTemplate
from mdt.component_templates.library_functions import LibraryFunctionTemplate

from mdt.lib.processing.model_fitting import get_batch_fitting_function
from mdt.utils import estimate_noise_std, get_cl_devices, create_blank_mask, create_index_matrix, \
    volume_index_to_roi_index, roi_index_to_volume_index, load_brain_mask, init_user_settings, restore_volumes, \
    apply_mask, create_roi, volume_merge, protocol_merge, create_median_otsu_brain_mask, create_brain_mask, \
    load_samples, load_sample, load_nifti, write_slice_roi, apply_mask_to_file, extract_volumes, \
    get_slice_in_dimension, per_model_logging_context, \
    get_temporary_results_dir, get_example_data, SimpleInitializationData, InitializationData, load_volume_maps, \
    covariance_to_correlation, check_user_components, unzip_nifti, zip_nifti, combine_dict_to_array, \
    compute_noddi_dti
from mdt.lib.input_data import load_input_data
from mdt.lib.sorting import sort_orientations, create_4d_sort_matrix, sort_volumes_per_voxel
from mdt.simulations import create_signal_estimates, simulate_signals, add_rician_noise
from mdt.lib.batch_utils import run_function_on_batch_fit_output, batch_apply, \
    batch_profile_factory, get_subject_selection
from mdt.protocols import load_bvec_bval, load_protocol, auto_load_protocol, write_protocol, write_bvec_bval, \
    create_protocol
from mdt.configuration import config_context, get_processing_strategy, get_config_option, set_config_option
from mdt.lib.exceptions import InsufficientProtocolError
from mdt.lib.nifti import write_nifti, get_all_nifti_data
from mdt.lib.components import get_model, get_batch_profile, get_component, get_template


__author__ = 'Robbert Harms'
__date__ = "2015-03-10"
__license__ = "LGPL v3"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


def get_optimization_inits(model_name, input_data, output_folder, cl_device_ind=None,
                           method=None, optimizer_options=None, double_precision=False):
    """Get better optimization starting points for the given model.

    Since initialization can make quite a difference in optimization results, this function can generate
    a good initialization starting point for the given model. The idea is that before you call the :func:`fit_model`
    function, you call this function to get a better starting point. An usage example would be::

        input_data = mdt.load_input_data(..)

        init_data = get_optimization_inits('BallStick_r1', input_data, '/my/folder')

        fit_model('BallStick_r1', input_data, '/my/folder',
                  initialization_data={'inits': init_data})

    Where the init data returned by this function can directly be used as input to the ``initialization_data``
    argument of the :func`fit_model` function.

    Please note that his function only supports models shipped by default with MDT.

    Args:
        model_name (str):
            The name of a model for which we want the optimization starting points.
        input_data (:class:`~mdt.lib.input_data.MRIInputData`): the input data object containing all
            the info needed for model fitting of intermediate models.
        output_folder (string): The path to the folder where to place the output, we will make a subdir with the
            model name in it.
        cl_device_ind (int or list): the index of the CL device to use. The index is from the list from the function
            utils.get_cl_devices(). This can also be a list of device indices.
        method (str): The optimization method to use, one of:
            - 'Levenberg-Marquardt'
            - 'Nelder-Mead'
            - 'Powell'
            - 'Subplex'

            If not given, defaults to 'Powell'.
        optimizer_options (dict): extra options passed to the optimization routines.
        double_precision (boolean): if we would like to do the calculations in double precision

    Returns:
        dict: a dictionary with initialization points for the selected model
    """
    from mdt.lib.processing.model_fitting import get_optimization_inits
    return get_optimization_inits(model_name, input_data, output_folder, cl_device_ind=cl_device_ind,
                                  method=method, optimizer_options=optimizer_options,
                                  double_precision=double_precision)


def fit_model(model, input_data, output_folder,
              method=None, optimizer_options=None, recalculate=False,
              cl_device_ind=None, cl_load_balancer=None,
              double_precision=False, tmp_results_dir=True,
              initialization_data=None, use_cascaded_inits=True,
              post_processing=None):
    """Run the optimizer on the given model.

    Args:
        model (str or :class:`~mdt.models.base.EstimableModel`):
            The name of a composite model or an implementation of a composite model.
        input_data (:class:`~mdt.lib.input_data.MRIInputData`): the input data object containing all
            the info needed for the model fitting.
        output_folder (string): The path to the folder where to place the output, we will make a subdir with the
            model name in it.
        method (str): The optimization method to use, one of:
            - 'Levenberg-Marquardt'
            - 'Nelder-Mead'
            - 'Powell'
            - 'Subplex'

            If not given, defaults to 'Powell'.
        optimizer_options (dict): extra options passed to the optimization routines.
        recalculate (boolean): If we want to recalculate the results if they are already present.
        cl_device_ind (List[Union[mot.lib.cl_environments.CLEnvironment, int]]
                             or mot.lib.cl_environments.CLEnvironment or int): the CL devices to use.
            Either provide MOT CLEnvironment's or indices from into the list from the function mdt.get_cl_devices().
        cl_load_balancer (mot.lib.load_balancers.LoadBalancer or Tuple[float]): the load balancer to use. Can also
            be an array of fractions (summing to 1) with one fraction per device. For example, for two devices one
            can specify ``cl_load_balancer = [0.3, 0.7]`` to let one device to more work than another.
        double_precision (boolean): if we would like to do the calculations in double precision
        tmp_results_dir (str, True or None): The temporary dir for the calculations. Set to a string to use
            that path directly, set to True to use the config value, set to None to disable.
        initialization_data (dict): provides (extra) initialization data to
            use during model fitting. This dictionary can contain the following elements:

            * ``inits``: dictionary with per parameter an initialization point
            * ``fixes``: dictionary with per parameter a fixed point, this will remove that parameter from the fitting
            * ``lower_bounds``: dictionary with per parameter a lower bound
            * ``upper_bounds``: dictionary with per parameter a upper bound
            * ``unfix``: a list of parameters to unfix

            For example::

                initialization_data = {
                    'fixes': {'Stick0.theta: np.array(...), ...},
                    'inits': {...}
                }

        use_cascaded_inits (boolean): if set, we initialize the model parameters using :func:`get_optimization_inits`.
            You can also overrule the default initializations using the ``initialization_data`` attribute.
        post_processing (dict): a dictionary with flags for post-processing options to enable or disable.
            For valid elements, please see the configuration file settings for ``optimization``
            under ``post_processing``. Valid input for this parameter is for example: {'covariance': False}
            to disable automatic calculation of the covariance from the Hessian.

    Returns:
        dict: The result maps for the given composite model or the last model in the cascade.
            This returns the results as 3d/4d volumes for every output map.
    """
    initialization_data = initialization_data or {}
    logger = logging.getLogger(__name__)

    if not check_user_components():
        init_user_settings(pass_if_exists=True)

    cl_runtime_info = CLRuntimeInfo(cl_environments=cl_device_ind,
                                    double_precision=double_precision,
                                    load_balancer=cl_load_balancer)

    if isinstance(model, str):
        model_name = model
        model_instance = get_model(model)()
    else:
        model_name = model.name
        model_instance = model

    if not model_instance.is_input_data_sufficient(input_data):
        raise InsufficientProtocolError(
            'The provided protocol is insufficient for this model. '
            'The reported errors where: {}'.format(model_instance.get_input_data_problems(input_data)))

    if post_processing:
        model_instance.update_active_post_processing('optimization', post_processing)

    if use_cascaded_inits:
        initialization_data['inits'] = initialization_data.get('inits', {})
        inits = get_optimization_inits(model_name, input_data, output_folder, cl_device_ind=cl_device_ind,
                                       method=method, optimizer_options=optimizer_options,
                                       double_precision=double_precision)
        inits.update(initialization_data['inits'])
        initialization_data['inits'] = inits
        logger.info('Preparing {0} with the cascaded initializations.'.format(model_name))

    initialization_data = SimpleInitializationData(**initialization_data)
    initialization_data.apply_to_model(model_instance, input_data)

    if method is None:
        method, optimizer_options = get_optimizer_for_model(model_name)

    with mot.configuration.config_context(CLRuntimeAction(cl_runtime_info)):
        from mdt.lib.processing.model_fitting import fit_composite_model
        fit_composite_model(model_instance, input_data, output_folder, method,
                            get_temporary_results_dir(tmp_results_dir), recalculate=recalculate,
                            optimizer_options=optimizer_options)

    return get_all_nifti_data(os.path.join(output_folder, model_name))


def sample_model(model, input_data, output_folder, nmr_samples=None, burnin=None, thinning=None,
                 method=None, recalculate=False, cl_device_ind=None, cl_load_balancer=None, double_precision=False,
                 store_samples=True, sample_items_to_save=None, tmp_results_dir=True,
                 initialization_data=None, post_processing=None, post_sampling_cb=None,
                 sampler_options=None):
    """Sample a composite model using Markov Chain Monte Carlo sampling.

    Args:
        model (str or :class:`~mdt.models.base.EstimableModel`): the model to sample
        input_data (:class:`~mdt.lib.input_data.MRIInputData`): the input data object containing all
            the info needed for the model fitting.
        output_folder (string): The path to the folder where to place the output, we will make a subdir with the
            model name in it (for the optimization results) and then a subdir with the samples output.
        nmr_samples (int): the number of samples we would like to return.
        burnin (int): the number of samples to burn-in, that is, to discard before returning the desired
            number of samples
        thinning (int): how many sample we wait before storing a new one. This will draw extra samples such that
                the total number of samples generated is ``nmr_samples * (thinning)`` and the number of samples stored
                is ``nmr_samples``. If set to one or lower we store every sample after the burn in.
        method (str): The sampling method to use, one of:
            - 'AMWG', for the Adaptive Metropolis-Within-Gibbs
            - 'SCAM', for the Single Component Adaptive Metropolis
            - 'FSL', for the sampling method used in the FSL toolbox
            - 'MWG', for the Metropolis-Within-Gibbs (simple random walk metropolis without updates)

            If not given, defaults to 'AMWG'.

        recalculate (boolean): If we want to recalculate the results if they are already present.
        cl_device_ind (List[Union[mot.lib.cl_environments.CLEnvironment, int]]
                             or mot.lib.cl_environments.CLEnvironment or int): the CL devices to use.
            Either provide MOT CLEnvironment's or indices from into the list from the function mdt.get_cl_devices().
        cl_load_balancer (mot.lib.load_balancers.LoadBalancer or Tuple[float]): the load balancer to use. Can also
            be an array of fractions (summing to 1) with one fraction per device. For example, for two devices one
            can specify ``cl_load_balancer = [0.3, 0.7]`` to let one device to more work than another.
        double_precision (boolean): if we would like to do the calculations in double precision
        store_samples (boolean): determines if we store any of the samples. If set to False we will store none
            of the samples.
        sample_items_to_save (list): list of output names we want to store the samples of. If given, we only
            store the items specified in this list. Valid items are the free parameter names of the model and the
            items 'LogLikelihood' and 'LogPrior'.
        tmp_results_dir (str, True or None): The temporary dir for the calculations. Set to a string to use
                that path directly, set to True to use the config value, set to None to disable.
        initialization_data (dict): provides (extra) initialization data to
            use during model fitting. This dictionary can contain the following elements:

            * ``inits``: dictionary with per parameter an initialization point
            * ``fixes``: dictionary with per parameter a fixed point, this will remove that parameter from the fitting
            * ``lower_bounds``: dictionary with per parameter a lower bound
            * ``upper_bounds``: dictionary with per parameter a upper bound
            * ``unfix``: a list of parameters to unfix

            For example::

                initialization_data = {
                    'fixes': {'Stick0.theta: np.array(...), ...},
                    'inits': {...}
                }

        post_processing (dict): a dictionary with flags for post-processing options to enable or disable.
            For valid elements, please see the configuration file settings for ``sample`` under ``post_processing``.
            Valid input for this parameter is for example: {'univariate_normal': True} to enable automatic calculation
            of the univariate normal distribution for the model parameters.
        post_sampling_cb (Callable[
            [mot.sample.base.SamplingOutput, mdt.models.composite.DMRICompositeModel], Optional[Dict]]):
                additional post-processing called after sampling. This function can optionally return a (nested)
                dictionary with as keys dir-/file-names and as values maps to be stored in the results directory.
        sampler_options (dict): specific options for the MCMC routine. These will be provided to the sampling routine
            as additional keyword arguments to the constructor.

    Returns:
        dict: if store_samples is True then we return the samples per parameter as a numpy memmap. If store_samples
            is False we return None
    """
    initialization_data = initialization_data or {}

    if not check_user_components():
        init_user_settings(pass_if_exists=True)

    cl_runtime_info = CLRuntimeInfo(cl_environments=cl_device_ind,
                                    double_precision=double_precision,
                                    load_balancer=cl_load_balancer)

    settings = get_general_sampling_settings()
    if nmr_samples is None:
        nmr_samples = settings['nmr_samples']
    if burnin is None:
        burnin = settings['burnin']
    if thinning is None:
        thinning = settings['thinning']

    if isinstance(model, str):
        model_instance = get_model(model)()
    else:
        model_instance = model

    initialization_data = SimpleInitializationData(**initialization_data)
    initialization_data.apply_to_model(model_instance, input_data)

    if post_processing:
        model_instance.update_active_post_processing('sampling', post_processing)

    with mot.configuration.config_context(CLRuntimeAction(cl_runtime_info)):
        from mdt.lib.processing.model_sampling import sample_composite_model
        return sample_composite_model(model_instance, input_data, output_folder, nmr_samples, thinning, burnin,
                                      get_temporary_results_dir(tmp_results_dir),
                                      method=method, recalculate=recalculate,
                                      store_samples=store_samples,
                                      sample_items_to_save=sample_items_to_save,
                                      post_sampling_cb=post_sampling_cb,
                                      sampler_options=sampler_options)


def compute_fim(model, input_data, optimization_results, output_folder=None, cl_device_ind=None, cl_load_balancer=None,
                initialization_data=None):
    """Compute the Fisher Information Matrix (FIM).

    This is typically done as post-processing step during the model fitting process, but can also be performed
    separately after optimization.

    Since the FIM depends on which parameters were optimized, results will change if different parameters are fixed.
    That is, this function will compute the FIM for every estimable parameter (free-non-fixed parameters). If you want
    to have the exact same FIM results as when you computed the FIM as optimization post-processing it is important
    to have exactly the same maps fixed.

    Contrary to the post-processing of the optimization maps, all FIM results are written to a single sub-folder in the
    provided output folder.

    Args:
        model (str or :class:`~mdt.models.base.EstimableModel`):
            The name of a composite model or an implementation of a composite model.
        input_data (:class:`~mdt.lib.input_data.MRIInputData`): the input data object containing all
            the info needed for the model fitting.
        optimization_results (dict or str): the optimization results, either a dictionary with results or the
            path to a folder.
        output_folder (string): Optionally, the path to the folder where to place the output
        cl_device_ind (List[Union[mot.lib.cl_environments.CLEnvironment, int]]
                             or mot.lib.cl_environments.CLEnvironment or int): the CL devices to use.
            Either provide MOT CLEnvironment's or indices from into the list from the function mdt.get_cl_devices().
        cl_load_balancer (mot.lib.load_balancers.LoadBalancer or Tuple[float]): the load balancer to use. Can also
            be an array of fractions (summing to 1) with one fraction per device. For example, for two devices one
            can specify ``cl_load_balancer = [0.3, 0.7]`` to let one device to more work than another.
        initialization_data (dict): provides (extra) initialization data to
            use during model fitting. This dictionary can contain the following elements:

            * ``inits``: dictionary with per parameter an initialization point
            * ``fixes``: dictionary with per parameter a fixed point, this will remove that parameter from the fitting
            * ``lower_bounds``: dictionary with per parameter a lower bound
            * ``upper_bounds``: dictionary with per parameter a upper bound
            * ``unfix``: a list of parameters to unfix

            For example::

                initialization_data = {
                    'fixes': {'Stick0.theta: np.array(...), ...},
                    'inits': {...}
                }

    Returns:
        dict: all the computed FIM maps in a flattened dictionary.
    """
    initialization_data = initialization_data or {}

    if isinstance(optimization_results, str):
        optimization_results = get_all_nifti_data(optimization_results)

    if not check_user_components():
        init_user_settings(pass_if_exists=True)

    cl_runtime_info = CLRuntimeInfo(cl_environments=cl_device_ind,
                                    double_precision=True,
                                    load_balancer=cl_load_balancer)

    if isinstance(model, str):
        model_name = model
        model_instance = get_model(model)()
    else:
        model_name = model.name
        model_instance = model

    model_instance.set_input_data(input_data)

    initialization_data = SimpleInitializationData(**initialization_data)
    initialization_data.apply_to_model(model_instance, input_data)

    with mot.configuration.config_context(CLRuntimeAction(cl_runtime_info)):
        opt_points = create_roi(optimization_results, input_data.mask)
        opt_array = combine_dict_to_array(opt_points, model_instance.get_free_param_names())

        covars = model_instance.compute_covariance_matrix(opt_array)
        covariance_names = model_instance.get_covariance_output_names()

        return_results = {}
        for ind, name in enumerate(covariance_names):
            if name.endswith('.std'):
                return_results[name] = np.nan_to_num(np.sqrt(covars[..., ind]))
            else:
                return_results[name] = covars[..., ind]

        return_results = restore_volumes(return_results, input_data.mask)
        write_volume_maps(return_results, os.path.join(output_folder, model_name, 'FIM'))

        return return_results


def bootstrap_model(model, input_data, optimization_results, output_folder, bootstrap_method=None,
                    bootstrap_options=None, nmr_samples=None, optimization_method=None, optimizer_options=None,
                    recalculate=False, cl_device_ind=None, double_precision=False, keep_samples=True,
                    tmp_results_dir=True, initialization_data=None):
    """Resample the model using residual bootstrapping.

    This is typically used to construct confidence intervals on the optimized parameters.

    Args:
        model (str or :class:`~mdt.models.base.EstimableModel`): the model to sample
        input_data (:class:`~mdt.lib.input_data.MRIInputData`): the input data object containing all
            the info needed for the model fitting.
        optimization_results (dict or str): the optimization results, either a dictionary with results or the
            path to a folder.
        output_folder (string): The path to the folder where to place the output, we will make a subdir with the
            model name in it (for the optimization results) and then a subdir with the samples output.
        bootstrap_method (str): the bootstrap method we want to use, 'residual', or 'wild'. Defaults to 'wild'.
        bootstrap_options (dict): bootstrapping options specific for the bootstrap method in use
        nmr_samples (int): the number of samples we would like to compute. Defaults to 1000.
        optimization_method (str): The optimization method to use, one of:
            - 'Levenberg-Marquardt'
            - 'Nelder-Mead'
            - 'Powell'
            - 'Subplex'

            If not given, defaults to 'Powell'.
        optimizer_options (dict): extra options passed to the optimization routines.
        recalculate (boolean): If we want to recalculate the results if they are already present.
        cl_device_ind (int): the index of the CL device to use. The index is from the list from the function
            utils.get_cl_devices().
        double_precision (boolean): if we would like to do the calculations in double precision
        keep_samples (boolean): determines if we keep any of the chains. If set to False, the chains will
            be discarded after generating the mean and standard deviations.
        tmp_results_dir (str, True or None): The temporary dir for the calculations. Set to a string to use
                that path directly, set to True to use the config value, set to None to disable.
        initialization_data (dict): provides (extra) initialization data to
            use during model fitting. This dictionary can contain the following elements:

            * ``inits``: dictionary with per parameter an initialization point
            * ``fixes``: dictionary with per parameter a fixed point, this will remove that parameter from the fitting
            * ``lower_bounds``: dictionary with per parameter a lower bound
            * ``upper_bounds``: dictionary with per parameter a upper bound
            * ``unfix``: a list of parameters to unfix

            For example::

                initialization_data = {
                    'fixes': {'Stick0.theta: np.array(...), ...},
                    'inits': {...}
                }

    Returns:
        dict: if keep_samples is True we return the samples per parameter as a numpy memmap.
            If store_samples is False we return None
    """
    initialization_data = initialization_data or {}
    nmr_samples = nmr_samples or 1000
    bootstrap_method = bootstrap_method or 'wild'

    if not check_user_components():
        init_user_settings(pass_if_exists=True)

    if cl_device_ind is None:
        cl_context_action = mot.configuration.VoidConfigurationAction()
    else:
        cl_context_action = mot.configuration.RuntimeConfigurationAction(
            cl_environments=get_cl_devices(cl_device_ind),
            double_precision=double_precision)

    if isinstance(model, str):
        model_name = model
        model_instance = get_model(model)()
    else:
        model_name = model.name
        model_instance = model

    model_instance.update_active_post_processing('optimization', {'uncertainties': False, 'll_and_ic': False})

    initialization_data = SimpleInitializationData(**initialization_data)
    initialization_data.apply_to_model(model_instance, input_data)

    if optimization_method is None:
        optimization_method, optimizer_options = get_optimizer_for_model(model_name)

    with mot.configuration.config_context(cl_context_action):
        from mdt.lib.processing.model_bootstrapping import compute_bootstrap
        return compute_bootstrap(model_instance, input_data, optimization_results,
                                 output_folder, bootstrap_method, optimization_method, nmr_samples,
                                 get_temporary_results_dir(tmp_results_dir),
                                 recalculate=recalculate,
                                 keep_samples=keep_samples,
                                 optimizer_options=optimizer_options,
                                 bootstrap_options=bootstrap_options)


def batch_fit(data_folder, models_to_fit, output_folder=None, batch_profile=None,
              subjects_selection=None, recalculate=False,
              cl_device_ind=None, dry_run=False,
              double_precision=False, tmp_results_dir=True,
              use_gradient_deviations=False):
    """Run all the available and applicable models on the data in the given folder.

    The idea is that a single folder is enough to fit_model the computations. One can optionally give it the
    batch_profile to use for the fitting. If not given, this class will attempt to use the
    batch_profile that fits the data folder best.

    Args:
        data_folder (str): The data folder to process
        models_to_fit (list of str): A list of models to fit to the data.
        output_folder (str): the folder in which to place the output, if not given we per default put an output folder
            next to the data_folder.
        batch_profile (:class:`~mdt.lib.batch_utils.BatchProfile` or str): the batch profile to use,
            or the name of a batch profile to use. If not given it is auto detected.
        subjects_selection (:class:`~mdt.lib.batch_utils.BatchSubjectSelection` or iterable): the subjects to \
            use for processing. If None, all subjects are processed. If a list is given instead of a
            :class:`~mdt.lib.batch_utils.BatchSubjectSelection` instance, we apply the following. If the elements in that
            list are string we use it as subject ids, if they are integers we use it as subject indices.
        recalculate (boolean): If we want to recalculate the results if they are already present.
        cl_device_ind (int or list of int): the index of the CL device to use.
            The index is from the list from the function get_cl_devices().
        dry_run (boolean): a dry run will do no computations, but will list all the subjects found in the
            given directory.
        double_precision (boolean): if we would like to do the calculations in double precision
        tmp_results_dir (str, True or None): The temporary dir for the calculations. Set to a string to use
                that path directly, set to True to use the config value, set to None to disable.
        use_gradient_deviations (boolean): if you want to use the gradient deviations if present
    Returns:
        The list of subjects we will calculate / have calculated.
    """
    logger = logging.getLogger(__name__)

    if not check_user_components():
        init_user_settings(pass_if_exists=True)

    if output_folder is None:
        output_folder = os.path.join(data_folder + '/', '..', os.path.dirname(data_folder + '/') + '_output')

    batch_profile = batch_profile_factory(batch_profile, data_folder)
    if batch_profile is None:
        raise RuntimeError('No suitable batch profile could be '
                           'found for the directory {0}'.format(os.path.abspath(data_folder)))
    subjects_selection = get_subject_selection(subjects_selection)

    logger.info('Using MDT version {}'.format(__version__))
    logger.info('Using batch profile: {0}'.format(batch_profile))

    if dry_run:
        logger.info('Dry run enabled')

    all_subjects = batch_profile.get_subjects(data_folder)
    subjects = subjects_selection.get_subjects(batch_profile.get_subjects(data_folder))
    logger.info('Fitting models: {}'.format(models_to_fit))
    logger.info('Subjects found: {0}'.format(len(all_subjects)))
    logger.info('Subjects to process: {0}'.format(len(subjects)))

    if dry_run:
        logger.info('Subjects found: {0}'.format(list(subject.subject_id for subject in subjects)))
        return

    batch_fit_func = get_batch_fitting_function(
        len(subjects), models_to_fit, output_folder, recalculate=recalculate,
        cl_device_ind=cl_device_ind, double_precision=double_precision,
        tmp_results_dir=tmp_results_dir, use_gradient_deviations=use_gradient_deviations)

    return batch_apply(data_folder, batch_fit_func, batch_profile=batch_profile, subjects_selection=subjects_selection)


def view_maps(data, config=None, figure_options=None,
              block=True, show_maximized=False, use_qt=True,
              window_title=None, save_filename=None):
    """View a number of maps using the MDT Maps Visualizer.

    Args:
        data (str, dict, :class:`~mdt.visualization.maps.base.DataInfo`, list, tuple): the data we are showing,
            either a dictionary with result maps, a string with a path name, a DataInfo object or a list
            with filenames and/or directories.
        config (str, dict, :class:`~mdt.visualization.maps.base import MapPlotConfig`): either a Yaml string or a
            dictionary with configuration settings or a ValidatedMapPlotConfig object to use directly
        figure_options (dict): Used when ``use_qt`` is False or when ``write_figure`` is used.
            Sets the figure options for the matplotlib Figure.
            If figsizes is not given you can also specify two ints, width and height, to indicate the pixel size of
            the resulting figure, together with the dpi they are used to calculate the figsize.
        block (boolean): if we block the plots or not
        show_maximized (boolean): if we show the window maximized or not
        window_title (str): the title for the window
        use_qt (boolean): if we want to use the Qt GUI, or show the results directly in matplotlib
        save_filename (str): save the figure to file. If set, we will not display the viewer.
    """
    from mdt.gui.maps_visualizer.main import start_gui
    from mdt.visualization.maps.base import MapPlotConfig
    from mdt.visualization.maps.matplotlib_renderer import MapsVisualizer
    from mdt.visualization.maps.base import SimpleDataInfo
    import matplotlib.pyplot as plt
    from mdt.gui.maps_visualizer.actions import NewDataAction
    from mdt.gui.maps_visualizer.base import SimpleDataConfigModel

    if isinstance(data, str):
        data = SimpleDataInfo.from_paths([data])
    elif isinstance(data, collections.MutableMapping):
        data = SimpleDataInfo(data)
    elif isinstance(data, collections.Sequence):
        if all(isinstance(el, str) for el in data):
            data = SimpleDataInfo.from_paths(data)
        else:
            data = SimpleDataInfo({str(ind): v for ind, v in enumerate(data)})
    elif data is None:
        data = SimpleDataInfo({})

    if config is None:
        config = MapPlotConfig()
    elif isinstance(config, str):
        if config.strip():
            config = MapPlotConfig.from_yaml(config)
        else:
            config = MapPlotConfig()
    elif isinstance(config, dict):
        config = MapPlotConfig.from_dict(config)

    config = config.create_valid(data)

    if not use_qt or save_filename:
        settings = {'dpi': 100, 'width': 1800, 'height': 1600}
        if save_filename:
            settings = {'dpi': 80, 'width': 800, 'height': 600}

        settings.update(figure_options or {})
        if 'figsize' not in settings:
            settings['figsize'] = (settings['width'] / settings['dpi'],
                                   settings['height'] / settings['dpi'])

        del settings['width']
        del settings['height']

        figure = plt.figure(**settings)
        viz = MapsVisualizer(data, figure)

        if save_filename:
            viz.to_file(save_filename, config, dpi=settings['dpi'])
        else:
            viz.show(config, block=block, maximize=show_maximized)
    else:
        start_gui(data, config, app_exec=block, show_maximized=show_maximized, window_title=window_title)


def block_plots(use_qt=True):
    """A small function to block matplotlib plots and Qt GUI instances.

    This basically calls either ``plt.show()`` and ``QtApplication.exec_()`` depending on ``use_qt``.

    Args:
        use_qt (boolean): if True we block Qt windows, if False we block matplotlib windows
    """
    if use_qt:
        from mdt.gui.utils import QtManager
        QtManager.exec_()
    else:
        import matplotlib.pyplot as plt
        plt.show()


def view_result_samples(data, **kwargs):
    """View the samples from the given results set.

    Args:
        data (string or dict): The location of the maps to use the samples from, or the samples themselves.
        kwargs (kwargs): see SampleVisualizer for all the supported keywords
    """
    from mdt.visualization.samples import SampleVisualizer

    if isinstance(data, str):
        data = load_samples(data)

    if not data:
        raise ValueError('No samples provided.')

    if kwargs.get('voxel_ind') is None:
        kwargs.update({'voxel_ind': data[list(data.keys())[0]].shape[0] / 2})
    SampleVisualizer(data).show(**kwargs)


def make_path_joiner(*args, make_dirs=False):
    """Generates and returns an instance of utils.PathJoiner to quickly join path names.

    Args:
        *args: the initial directory or list of directories to concatenate
        make_dirs (boolean): if we should make the referenced directory if it does not yet exist

    Returns:
         mdt.utils.PathJoiner: easy path manipulation path joiner
    """
    from mdt.utils import PathJoiner
    return PathJoiner(*args, make_dirs=make_dirs)


def sort_maps(input_maps, reversed_sort=False, sort_index_matrix=None):
    """Sort the values of the given maps voxel by voxel.

    This first creates a sort matrix to index the maps in sorted order per voxel. Next, it creates the output
    maps for the maps we sort on.

    Args:
        input_maps (:class:`list`): a list of string (filenames) or ndarrays we will sort
        reversed_sort (boolean): if we want to sort from large to small instead of small to large.
            This is not used if a sort index matrix is provided.
        sort_index_matrix (ndarray): if given we use this sort index map instead of generating one by sorting the
            maps_to_sort_on. Supposed to be a integer matrix.

    Returns:
        list: the list of sorted volumes
    """
    if sort_index_matrix is None:
        sort_index_matrix = create_4d_sort_matrix(input_maps, reversed_sort=reversed_sort)
    elif isinstance(sort_index_matrix, str):
        sort_index_matrix = np.round(load_nifti(sort_index_matrix).get_data()).astype(np.int64)
    return sort_volumes_per_voxel(input_maps, sort_index_matrix)


def get_volume_names(directory):
    """Get the names of the Nifti volume maps in the given directory.

    Args:
        directory: the directory to get the names of the available maps from.

    Returns:
        :class:`list`: A list with the names of the volumes.
    """
    from mdt.lib.nifti import yield_nifti_info
    return list(sorted(el[1] for el in yield_nifti_info(directory)))


def write_volume_maps(maps, directory, header=None, overwrite_volumes=True, gzip=True):
    """Write a dictionary with maps to the given directory using the given header.

    Args:
        maps (dict): The maps with as keys the map names and as values 3d or 4d maps
        directory (str): The dir to write to
        header: The Nibabel Image Header
        overwrite_volumes (boolean): If we want to overwrite the volumes if they are present.
        gzip (boolean): if we want to write the results gzipped
    """
    from mdt.lib.nifti import write_all_as_nifti
    write_all_as_nifti(maps, directory, nifti_header=header, overwrite_volumes=overwrite_volumes, gzip=gzip)


def get_models_list():
    """Get a list of all available composite models

    Returns:
        list of str: A list of available model names.
    """
    from mdt.lib.components import get_component_list
    return list(sorted(get_component_list('composite_models')))


def get_models_meta_info():
    """Get the meta information tags for all the models returned by get_models_list()

    Returns:
        dict of dict: The first dictionary indexes the model names to the meta tags, the second holds the meta
            information.
    """
    from mdt.lib.components import get_meta_info, get_component_list
    return {model: get_meta_info('composite_models', model) for model in get_component_list('composite_models')}


def start_gui(base_dir=None, app_exec=True):
    """Start the model fitting GUI.

    Args:
        base_dir (str): the starting directory for the file opening actions
        app_exec (boolean): if true we execute the Qt application, set to false to disable.
            This is only important if you want to start this GUI from within an existing Qt application. If you
            leave this at true in that case, this will try to start a new Qt application which may create problems.
    """
    from mdt.gui.model_fit.qt_main import start_gui
    return start_gui(base_dir=base_dir, app_exec=app_exec)


def reset_logging():
    """Reset the logging to reflect the current configuration.

    This is commonly called after updating the logging configuration to let the changes take affect.
    """
    logging_config.dictConfig(get_logging_configuration_dict())


@contextmanager
def with_logging_to_debug():
    """A context in which the logging is temporarily set to WARNING.

    Example of usage::

        with mdt.with_logging_to_debug():
            your_computations()

    During the function ``your_computations`` only WARNING level logging will show up.
    """
    handlers = logging.getLogger('mot').handlers
    previous_levels = [handler.level for handler in handlers]
    for handler in handlers:
        handler.setLevel(logging.WARNING)
    yield
    for handler, previous_level in zip(handlers, previous_levels):
        handler.setLevel(previous_level)


def reload_components():
    """Reload all the dynamic components.

    This can be useful after changing some of the dynamically loadable modules. This function will remove all cached
    components and reload the directories.
    """
    from mdt.lib.components import reload
    try:
        reload()
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.error('Failed to load the default components. Try removing your MDT home folder and reload.')


if 'MDT.LOAD_COMPONENTS' in os.environ and os.environ['MDT.LOAD_COMPONENTS'] != '1':
    pass
else:
    reload_components()
