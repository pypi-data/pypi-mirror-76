from mdt import CompartmentTemplate

__author__ = 'Robbert Harms'
__date__ = '2018-09-07'
__maintainer__ = 'Robbert Harms'
__email__ = 'robbert@xkls.nl'
__licence__ = 'LGPL v3'


class NODDI_EC(CompartmentTemplate):
    """The Extra-Cellular compartment of the NODDI-Watson model.

    This is the compartment as described in Gary Zhang's papers, with the exponent model outside the integral.
    """
    parameters = ('g', 'b', 'd', 'dperp0', 'theta', 'phi', 'kappa')
    dependencies = ('NODDI_WatsonHinderedDiffusionCoeff', 'Zeppelin')
    cl_code = '''
        double d_ = d;
        double dperp0_ = d;

        NODDI_WatsonHinderedDiffusionCoeff(&d_, &dperp0_, kappa);
        return Zeppelin(g, b, d_, dperp0_, theta, phi);
    '''


class NODDI_EC_Integration(CompartmentTemplate):
    """Extra-Cellular NODDI with the compartment inside the integration instead of outside."""
    parameters = ('g', 'b', 'd', 'dperp0', 'theta', 'phi', 'kappa')
    dependencies = ('NODDI_SphericalHarmonicsIntegral', 'SphericalToCartesian')
    cl_code = '''
        return exp(-b * dperp0) * NODDI_SphericalHarmonicsIntegral(dot(g, SphericalToCartesian(theta, phi)),
                                                                   -b * (d - dperp0), kappa);
    '''


class NODDI_IC(CompartmentTemplate):
    """Generate the compartment model signal for the NODDI Intra Cellular (Stick with dispersion) compartment."""
    parameters = ('g', 'b', 'd', 'theta', 'phi', 'kappa')
    dependencies = ('NODDI_SphericalHarmonicsIntegral', 'SphericalToCartesian')
    cl_code = '''
        return NODDI_SphericalHarmonicsIntegral(dot(g, SphericalToCartesian(theta, phi)), -b*d, kappa);
    '''


class BinghamNODDI_EN(CompartmentTemplate):
    """The Extra-Neurite tissue model of Bingham NODDI."""
    parameters = ('g', 'b', 'd', 'dperp0', 'theta', 'phi', 'psi', 'k1', 'kw', '@cache')
    dependencies = ['ConfluentHyperGeometricFirstKind', 'SphericalToCartesian', 'Tensor']
    cl_code = '''
        double d_mu_1 = dperp0 + (d - dperp0) * *cache->diff_kappa;
        double d_mu_2 = dperp0 + (d - dperp0) * *cache->diff_beta;
        double d_mu_3 = d + 2*dperp0 - d_mu_1 - d_mu_2;

        return Tensor(g, b, d_mu_1, d_mu_2, d_mu_3, theta, phi, psi);
    '''
    cache_info = {
        'fields': ['double diff_kappa',
                   'double diff_beta'],
        'cl_code': '''
            double kappa = k1;
            double beta = k1 / kw;

            double DELTA = 1e-4;
            double normalization_constant = ConfluentHyperGeometricFirstKind(-kappa, -beta, 0);

            *cache->diff_kappa = (ConfluentHyperGeometricFirstKind(-(kappa+DELTA), -beta, 0) -
                                  ConfluentHyperGeometricFirstKind(-(kappa-DELTA), -beta, 0))
                                  / (2*DELTA) / normalization_constant;

            *cache->diff_beta = (ConfluentHyperGeometricFirstKind(-kappa, -(beta+DELTA), 0) -
                                 ConfluentHyperGeometricFirstKind(-kappa, -(beta-DELTA), 0))
                                 / (2*DELTA) / normalization_constant;
        '''
    }


class BinghamNODDI_IN(CompartmentTemplate):
    """The Intra-Neurite tissue model of Bingham NODDI."""
    parameters = ('g', 'b', 'd', 'theta', 'phi', 'psi', 'k1', 'kw', '@cache')
    dependencies = ['eigenvalues_3x3_symmetric', 'ConfluentHyperGeometricFirstKind', 'TensorSphericalToCartesian']
    cl_code = '''
        double kappa = k1;
        double beta = k1 / kw;

        float4 v1, v2, v3;
        TensorSphericalToCartesian(theta, phi, psi, &v1, &v2, &v3);

        double Q[6]; // upper triangular
        Q[0] = pown(dot(g, v3), 2) * (-b * d);
        Q[1] = dot(g, v3) * dot(g, v2) * (-b * d);
        Q[2] = dot(g, v3) * dot(g, v1) * (-b * d);
        Q[3] = pown(dot(g, v2), 2) * (-b * d);
        Q[4] = dot(g, v2) * dot(g, v1) * (-b * d);
        Q[5] = pown(dot(g, v1), 2) * (-b * d);

        Q[3] += beta;
        Q[5] += kappa;

        double e[3];
        eigenvalues_3x3_symmetric(Q,e);

        return ConfluentHyperGeometricFirstKind(-e[0], -e[1], -e[2]) / *cache->denom;
    '''
    cache_info = {
        'fields': ['double denom'],
        'cl_code': '''
            *cache->denom = ConfluentHyperGeometricFirstKind(-k1, -(k1 / kw), 0);
        '''
    }
