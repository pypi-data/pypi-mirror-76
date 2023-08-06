"""
@Title   : Stochastic nonparametric envelopment of data (StoNED): Residuals decomposition
@Author  : Sheng Dai, Timo Kuosmanen
@Mail    : sheng.dai@aalto.fi (S. Dai); timo.kuosmanen@aalto.fi (T. Kuosmanen)  
@Date    : 2020-04-12 
"""

from . import qle
import numpy as np
import math
from scipy.stats import norm
import scipy.optimize as opt


def stoned(y, eps, fun, method, cet):
    # fun     = "prod": production frontier;
    #         = "cost": cost frontier
    # method  = "MOM" : Method of moments
    #         = "QLE" : Quasi-likelihood estimation
    # cet     = "addi": Additive composite error term
    #         = "mult": Multiplicative composite error term

    if method == "MoM":

        # Average of residuals (approximately zero)
        mresid = np.mean(eps)

        # Calculate the 2nd/3rd central moments for each DMU (sample variance/skewness)
        M2 = (eps - mresid) * (eps - mresid)
        M3 = (eps - mresid) * (eps - mresid) * (eps - mresid)

        # Average of 2nd/ 3rd moments
        mM2 = np.mean(M2, axis=0)
        mM3 = np.mean(M3, axis=0)

        if fun == "prod":
            if mM3 > 0:
                mM3 = 0.0

            # standard deviation sigma_u, sigma_v
            sigmau = (mM3 / ((2 / math.pi) ** (1 / 2) * (1 - 4 / math.pi))) ** (1 / 3)
            sigmav = (mM2 - ((math.pi - 2) / math.pi) * sigmau ** 2) ** (1 / 2)

            # calculate bias correction
            # (unconditional) mean (mu)
            mu = (sigmau ** 2 * 2 / math.pi) ** (1 / 2)

            # bias adjusted residuals
            epsilon = eps - mu

        if fun == "cost":
            if mM3 < 0:
                mM3 = 0.00001

            # standard deviation sigma_u, sigma_v
            sigmau = (-mM3 / ((2 / math.pi) ** (1 / 2) * (1 - 4 / math.pi))) ** (1 / 3)
            sigmav = (mM2 - ((math.pi - 2) / math.pi) * sigmau ** 2) ** (1 / 2)

            # calculate bias correction
            # (unconditional) mean (mu)
            mu = (sigmau ** 2 * 2 / math.pi) ** (1 / 2)

            # bias adjusted residuals
            epsilon = eps + mu

    if method == "QLE":

        # initial parameter lambda
        lamda = 1.0

        if fun == "prod":

            # optimization
            llres = opt.minimize(qle.qlep, lamda, eps, method='BFGS')

            lamda = llres.x[0]

            # use estimate of lambda to calculate sigma Eq. (3.26) in Johnson and Kuosmanen (2015)
            sigma = math.sqrt((np.mean(eps) ** 2) / (1 - (2 * lamda ** 2) / (math.pi * (1 + lamda**2))))

            # calculate bias correction
            # (unconditional) mean
            mu = math.sqrt(2) * sigma * lamda / math.sqrt(math.pi * (1 + lamda ** 2))

            # calculate sigma.u and sigma.v
            sigmav = (sigma ** 2 / (1 + lamda**2)) ** (1/2)
            sigmau = sigmav * lamda

            # adj. res.
            epsilon = eps - mu

        if fun == "cost":

            # optimization
            llres = opt.minimize(qle.qlec, lamda, eps, method='BFGS')

            lamda = llres.x[0]

            # use estimate of lambda to calculate sigma
            sigma = math.sqrt((np.mean(eps) ** 2) / (1 - (2 * lamda ** 2) / (math.pi * (1 + lamda**2))))

            # calculate bias correction
            # (unconditional) mean
            mu = math.sqrt(2) * sigma * lamda / math.sqrt(math.pi * (1 + lamda ** 2))

            # calculate sigma.u and sigma.v
            sigmav = (sigma ** 2 / (1 + lamda**2)) ** (1/2)
            sigmau = sigmav * lamda

            # adj. res.
            epsilon = eps + mu

    # expected value of the inefficiency term u
    sigmart = sigmau * sigmav / math.sqrt(sigmau ** 2 + sigmav ** 2)
    mus = epsilon * sigmau / (sigmav * math.sqrt(sigmau ** 2 + sigmav ** 2))
    norpdf = 1 / math.sqrt(2 * math.pi) * np.exp(-mus ** 2 / 2)

    if cet == "addi":

        if fun == "prod":

            # Conditional mean
            Eu = sigmart * ((norpdf / (1 - norm.cdf(mus) + 0.000001)) - mus)
            # technical inefficiency
            TE = ((y - eps + mu) - Eu) / (y - eps + mu)

        if fun == "cost":

            # Conditional mean
            Eu = sigmart * ((norpdf / (1 - norm.cdf(-mus) + 0.000001)) + mus)
            # technical inefficiency
            TE = ((y - eps - mu) + Eu) / (y - eps - mu)
            TE = 1/TE

    if cet == "mult":

        if fun == "prod":

            # Conditional mean
            Eu = sigmart * ((norpdf / (1 - norm.cdf(mus) + 0.000001)) - mus)
            # technical inefficiency
            TE = np.exp(-Eu)

        if fun == "cost":

            # Conditional mean
            Eu = sigmart * ((norpdf / (1 - norm.cdf(-mus) + 0.000001)) + mus)
            # technical inefficiency
            TE = np.exp(Eu)
            TE = 1/TE

    return TE