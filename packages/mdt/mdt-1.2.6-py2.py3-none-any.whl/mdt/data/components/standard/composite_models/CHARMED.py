import numpy as np
from mdt import CompositeModelTemplate

__author__ = 'Robbert Harms'
__date__ = "2015-06-22"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


class CHARMED_r1(CompositeModelTemplate):
    """The CHARMED model with 1 restricted compartments"""

    model_expression = '''
        S0 * ( (Weight(w_hin0) * Tensor) +
               (Weight(w_res0) * CHARMEDRestricted(CHARMEDRestricted0))
               )
    '''

    inits = {'Tensor.d': 2e-9,
             'Tensor.dperp0': 1e-9,
             'Tensor.dperp1': 1e-9,
             'CHARMEDRestricted0.d': 1e-9}

    extra_optimization_maps = [
        lambda results: {'FR': results['w_res0.w']},
        lambda results: {'FR.std': results['w_res0.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {'FR': np.mean(samples['w_res0.w'], axis=1),
                         'FR.std': np.std(samples['w_res0.w'], axis=1)}
    ]


class CHARMED_r2(CompositeModelTemplate):
    """The CHARMED model with 2 restricted compartments."""

    model_expression = '''
        S0 * ( (Weight(w_hin0) * Tensor) +
               (Weight(w_res0) * CHARMEDRestricted(CHARMEDRestricted0)) +
               (Weight(w_res1) * CHARMEDRestricted(CHARMEDRestricted1)) )
    '''

    inits = {'Tensor.d': 2e-9,
             'Tensor.dperp0': 1e-9,
             'Tensor.dperp1': 1e-9,
             'CHARMEDRestricted0.d': 1e-9,
             'CHARMEDRestricted1.d': 1e-9,
             'w_res0.w': 0.1,
             'w_res1.w': 0.1}

    constraints = '''
        constraints[0] = w_res1.w - w_res0.w;
    '''

    extra_optimization_maps = [
        lambda results: {'FR': 1 - results['w_hin0.w']},
        lambda results: {'FR.std': results['w_hin0.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {'FR': np.mean(samples['w_res0.w'] + samples['w_res1.w'], axis=1),
                         'FR.std': np.std(samples['w_res0.w'] + samples['w_res1.w'], axis=1)}
    ]

    prior = 'return w_res1.w < w_res0.w;'


class CHARMED_r3(CompositeModelTemplate):
    """The standard CHARMED model with 3 restricted compartments"""

    model_expression = '''
        S0 * ( (Weight(w_hin0) * Tensor) +
               (Weight(w_res0) * CHARMEDRestricted(CHARMEDRestricted0)) +
               (Weight(w_res1) * CHARMEDRestricted(CHARMEDRestricted1)) +
               (Weight(w_res2) * CHARMEDRestricted(CHARMEDRestricted2)) )
    '''

    inits = {'Tensor.d': 2e-9,
             'Tensor.dperp0': 1e-9,
             'Tensor.dperp1': 1e-9,
             'CHARMEDRestricted0.d': 1e-9,
             'CHARMEDRestricted1.d': 1e-9,
             'CHARMEDRestricted2.d': 1e-9,
             'w_res0.w': 0.1,
             'w_res1.w': 0.1,
             'w_res2.w': 0.1}

    constraints = '''
        constraints[0] = w_res1.w - w_res0.w;
        constraints[1] = w_res2.w - w_res1.w;
    '''

    extra_optimization_maps = [
        lambda results: {'FR': 1 - results['w_hin0.w']},
        lambda results: {'FR.std': results['w_hin0.w.std']}
    ]
    extra_sampling_maps = [
        lambda samples: {'FR': np.mean(samples['w_res0.w'] + samples['w_res1.w'] + samples['w_res2.w'], axis=1),
                         'FR.std': np.std(samples['w_res0.w'] + samples['w_res1.w'] + samples['w_res2.w'], axis=1)}
    ]

    prior = 'return w_res2.w < w_res1.w && w_res1.w < w_res0.w;'

