from mdt import CompartmentTemplate
from mdt.lib.post_processing import DTIMeasures

__author__ = 'Robbert Harms'
__date__ = "2015-06-21"
__maintainer__ = "Robbert Harms"
__email__ = "robbert@xkls.nl"


class Tensor(CompartmentTemplate):

    parameters = ('g', 'b', 'd', 'dperp0', 'dperp1', 'theta', 'phi', 'psi')
    dependencies = ['TensorApparentDiffusion']
    cl_code = '''
        double adc = TensorApparentDiffusion(theta, phi, psi, d, dperp0, dperp1, g);
        return exp(-b * adc);
    '''
    constraints = '''
        constraints[0] = dperp0 - d;
        constraints[1] = dperp1 - dperp0;
    '''
    prior = 'return dperp1 < dperp0 && dperp0 < d;'
    extra_optimization_maps = [DTIMeasures.extra_optimization_maps]
    extra_sampling_maps = [DTIMeasures.extra_sampling_maps]
