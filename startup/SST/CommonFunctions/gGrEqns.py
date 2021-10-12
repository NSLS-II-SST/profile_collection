import numpy as np
import scipy.optimize as opt
from ..CommonFunctions.functions import run_report

run_report(__file__)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
basic general equations applying to gratings and grating instruments
assumes all angular arguments are passed as degrees
assumes length units are in mm 
@author: dvorak
"""


def getAlphaDeg(eV, beta_deg, k_invmm, m):
    # calculate alpha in deg
    # eV: energy
    # beta_deg: diffraction angle
    # k_invmm: central line density
    # m: diffraction order
    hc = 0.0012398  # in units of eV mm
    lambda_mm = hc / eV
    beta = np.radians(beta_deg)
    alpha = np.arcsin((m * k_invmm * lambda_mm - np.sin(beta)))
    return np.degrees(alpha)


def getBetaDeg(eV, alpha_deg, k_invmm, m):
    # calculate beta in deg
    # eV: energy
    # alpha_deg: incident angle
    # k_invmm: central line density
    # m: diffraction order
    hc = 0.0012398  # in units of eV mm
    lambda_mm = hc / eV
    alpha = np.radians(alpha_deg)
    beta = np.arcsin((m * k_invmm * lambda_mm - np.sin(alpha)))
    return np.degrees(beta)


def getEv(alpha_deg, beta_deg, k_invmm, m):
    # calculate energy in eV
    # alpha_deg: incident angle
    # beta_deg: diffraction angle
    # k_invmm: central line density
    # m: diffraction order
    hc = 0.0012398  # in units of eV mm
    alpha = np.radians(alpha_deg)
    beta = np.radians(beta_deg)
    lambda_mm = (1 / (m * k_invmm)) * (np.sin(alpha) + np.sin(beta))
    eV = hc / lambda_mm
    return eV


def getMag(alpha_deg, beta_deg, ra, rb):
    # calculate the magnification of the image
    # alpha_deg: incident angle in deg
    # beta_deg: diffracted angle in deg
    # ra: entrance arm length (ra and rb must have same units)
    # rb: exit arm length (ra and rb must have same units)
    alpha = np.radians(alpha_deg)
    beta = np.radians(beta_deg)
    return (rb * np.cos(alpha)) / (ra * np.cos(beta))


def getAngDisp(alpha_deg, beta_deg, k_invmm, m):
    # calculate the energy dispersion in terms of eV/rad
    # alpha_deg: incident angle in deg
    # beta_deg: diffracted angle in deg
    # k_invmm: central line density in mm-1
    # m: diffraction order
    hc = 0.0012398  # in units of eV mm
    alpha = np.radians(alpha_deg)
    beta = np.radians(beta_deg)
    # angular dispersion dE/d(beta)
    angDisp = -hc * k_invmm * m * np.cos(beta) * (np.sin(alpha) + np.sin(beta)) ** -2
    return angDisp


def getLinDisp(alpha_deg, beta_deg, k_invmm, m, rb_mm):
    # calculate the linear energy dispersion at the exit slit
    #   in units of eV/mm
    # alpha_deg: incident angle in deg
    # beta_deg: diffracted angle in deg
    # k_invmm: central line density in mm-1
    # m: diffraction order
    # rb_mm: exit arm length in mm

    angDisp = getAngDisp(alpha_deg, beta_deg, k_invmm, m)
    linDisp = (1 / rb_mm) * angDisp
    return linDisp


def blazeAngDeg(eV, alpha_deg, k_invmm, m):
    # calculate the required blaze angle in deg
    # parameter list is self descriptive
    # blaze angle is negative in negative order!
    beta_deg = getBetaDeg(eV, alpha_deg, k_invmm, m)
    return 0.5 * (alpha_deg + beta_deg)


def blazeAngDeg2(eV, cff, k_invmm, m):
    # calculate the required blaze angle in deg
    # parameter list is self descriptive
    # blaze angle is negative in negative order!
    alpha_deg = ruben2005eqn8m(eV, cff, k_invmm, m)
    beta_deg = getBetaDeg(eV, alpha_deg, k_invmm, m)
    return 0.5 * (alpha_deg + beta_deg)


def alphaOnBlazeA(eV, k_invmm, m, blaze_deg):
    # calc on blaze alpha in deg for a given blaze angle analytically
    # parameter list is self descriptive
    # blaze angle is negative in negative order!
    hc = 0.0012398  # in units of eV mm
    lambda_mm = hc / eV
    alpha = np.radians(blaze_deg) + np.arccos(
        (m * k_invmm * lambda_mm) / (2 * np.sin(np.radians(blaze_deg)))
    )
    return np.degrees(alpha)


def alphaOnBlaze(eV, k_invmm, m, blaze_deg):
    # calculate the on blaze alpha in deg for a given blaze angle
    # parameter list is self descriptive
    # blaze angle is negative in negative order!
    args = (eV, k_invmm, m, blaze_deg)
    llim, ulim = onBlazeBracket(*args)
    try:
        result = opt.bisect(onBlazeFn, llim, ulim, args)
    except:
        result = float("nan")
    return result


def onBlazeFn(alpha_deg, *args):
    # trancendental function to solve for alpha given blaze angle
    # arg parameters are self descriptive
    # *args = (eV, k_invmm, m, blaze_deg)
    # blaze angle is negative for negative orders
    eV = args[0]
    k_invmm = args[1]
    m = args[2]
    blaze_deg = args[3]
    #
    bl = np.radians(blaze_deg)
    alpha = np.radians(alpha_deg)
    hc = 0.0012398  # in units of eV mm
    lambda_mm = hc / eV
    try:
        result = np.degrees(
            bl - 0.5 * (alpha + np.arcsin(m * k_invmm * lambda_mm - np.sin(alpha)))
        )
    except:
        result = float("nan")
    return result


def onBlazeBracket(eV, k_invmm, m, blaze_deg):
    # find the range in deg of valid values for the onBlaze numerical solver
    # this is required for bracketing the numerical problem solver
    # input parameters are self explanatory
    alphaLow = 0.0
    alphaHigh = 90.0
    tolerance = 0.0000001
    arg = (eV, k_invmm, m, blaze_deg)

    # initial case test 0 and 90 degrees
    testLow = onBlazeFn(alphaLow, *arg)
    if np.isnan(testLow):
        raise RuntimeError("No valid solution")
    testHigh = onBlazeFn(alphaHigh, *arg)
    if not np.isnan(testHigh):
        return (0.0, 90.0)

    # current state
    #    alphaLow = 0
    #    alphaHigh = nan
    alphaLowOld = 0
    while True:
        alphaMid = (alphaHigh + alphaLow) / 2
        # print (alphaLow, alphaMid, alphaHigh)
        testMid = onBlazeFn(alphaMid, *arg)
        if np.isnan(testMid):
            # alphaLow does not change
            alphaHigh = alphaMid
        else:
            # alphaHigh does not change
            alphaLow = alphaMid
            if abs(alphaLow - alphaLowOld) < tolerance:
                break
            else:
                alphaLowOld = alphaLow
    return (0, alphaLow)


def ruben2005eqn8m(eV, c, k, m):
    #   eqn 8, Ruben 2005, to calculate alpha from c
    #   generalized to include higher orders
    #   c is unitless
    #   k is central line density in mm-1
    #   m is the diffraction order, and integer
    #   returns alpha in degrees
    #   works for grazing incidence, 2000 eV, 1800 mm-1, cff=2, m=+1 thru +5
    #   works for grazing incidence, 2000 eV, 1800 mm-1, cff=0.2, m=-1 thru -5
    aa = 1 / (c ** 2 - 1)
    llambda = (12398 / eV) * 1e-7  # wavelength in mm
    return np.degrees(
        np.arcsin(-m * k * llambda * aa + np.sqrt(1 + (c * m * k * llambda * aa) ** 2))
    )


# needs error checking
def ruben2005eqn9(eV, k, ra, rb, a1):
    #   eqn 9, Ruben 2005, to calculate c to zero defocus term for given
    #   geometry and plane VLS parameters for m = +1 (inside order)
    #   k is central line density in mm-1
    #   ra and rb are in mm
    #   a1 is VLS focusing term in mm-2
    rr = rb / ra
    A0 = k * (12398 / eV) * 1e-7
    A2 = -(1 / 2) * (12398 / eV) * 1e-7 * rb * a1
    t1 = 2 * A2
    t2 = 4 * (A2 / A0) ** 2
    t3 = (4 + 2 * A2 - A0 ** 2) * rr
    t4 = -4 * (A2 / A0) * np.sqrt((1 + rr) ** 2 + 2 * A2 * (1 + rr) - A0 ** 2 * rr)
    t5 = -4 + A0 ** 2 - 4 * A2 + 4 * (A2 / A0) ** 2
    return np.sqrt((t1 + t2 + t3 + t4) / t5)


##############################################################################


# for beamline soft xray grating instruments


def softXrayMono1(eV, k, m, c, rb_mm, bounce, inOff_deg, outOff_deg, verbose):
    """
    # calculate premirror and grating angles for NSLS-II soft xray monos
    # eV: energy
    # k: central line density in mm-1
    # m: diffraction order
    # c: cff 0 < cff < infinity
    # bounce = 'up' or 'down'
    # inOff_deg - input beam angle relative to horizontal, NSLSII sense
    # outOff_deg - output beam angle relative to horizontal, NSLSII sense
    """
    # correct for several energies for Centurion
    # correctly reverses sign of angles if geometry is flipped upside-down

    # consider bounce direction
    if bounce == "up":
        a = -1
    elif bounce == "down":
        a = +1
    else:
        a = float("nan")

    # calculate angles, no offsets
    alpha_deg = ruben2005eqn8m(eV, c, k, m)
    beta_deg = getBetaDeg(eV, alpha_deg, k, m)
    # include offsets
    thetaPMinc_deg = abs(
        +0.5 * (outOff_deg - inOff_deg + a * (180.0 - alpha_deg + beta_deg))
    )
    thetaPM_deg = +0.5 * (outOff_deg + inOff_deg + a * (180.0 - alpha_deg + beta_deg))
    thetaGR_deg = a * (90.0 + beta_deg) + outOff_deg
    disp = getLinDisp(alpha_deg, beta_deg, k, m, rb_mm)
    if verbose:
        # alpha, beta both relative to normal and surface
        print("eV=", eV, "c=", c)
        print("alpha=", alpha_deg, 90.0 - alpha_deg)
        print("beta=", beta_deg, (90 + beta_deg))
        print("incident angle on pm=", thetaPMinc_deg)
        print("dispersion (eV/mm) =", disp)
        # grating and premirror rotation angles
        print("rotation angles relative to horizontal")
        print("     premirror", thetaPM_deg)
        print("     grating", thetaGR_deg)
    return (thetaPM_deg, thetaGR_deg, alpha_deg, beta_deg, thetaPMinc_deg, disp)


def softXrayMono2(k_invmm, m, grAng_deg, pmAng_deg, bounce, inOff_deg, outOff_deg):
    """
    # calculate the energy for a given premirr and grating angle for a PGM
    # the angles are relative to the horizontal, using NSLS-II standard
    # k_invmm: central line density in mm-1
    # m: diffraction order
    # grAng_deg: grating angle, relative to horizontal
    # pmAng_deg: premirror angle, relative to horizontal
    # bounce = 'up' or 'down'
    # inOff_deg - input beam angle relative to horizontal, NSLSII sense
    # outOff_deg - output beam angle relative to horizontal, NSLSII sense
    """
    ### correct for several energies for Centurion
    ### correctly reverses sign of angles if geometry is flipped upside-down
    # not error checked yet

    # consider bounce direction
    if bounce == "up":
        a = -1
    elif bounce == "down":
        a = +1
    else:
        a = float("nan")

    beta_deg = -90 + a * (grAng_deg - outOff_deg)
    alpha_deg = +180 + beta_deg + a * (outOff_deg + inOff_deg - 2 * pmAng_deg)
    beta = np.radians(beta_deg)
    alpha = np.radians(alpha_deg)
    lambda_mm = (np.sin(alpha) + np.sin(beta)) / (m * k_invmm)
    hc = 0.0012398  # in units of eV mm
    eV = hc / lambda_mm
    if alpha_deg > 90:
        eV = np.nan
    return eV


# conditional code
def getAlphaDegH(eV, k_invmm, m):
    # calculate the horizon angle for alpha for grazing incidence
    # for outside diffraction orders, as alpha goes more to grazing, eventually
    # beta will become 90 degrees - I call this the horizon angle for alpha
    # eV: energy
    # k_invmm: central line density
    # m: diffraction order
    hc = 0.0012398  # in units of eV mm
    lambda_mm = hc / eV
    alpha = np.arcsin((m * k_invmm * lambda_mm + 1))
    return np.degrees(alpha)


# Eliot adding this for getting the mirror and grating angles for the monochromator based on energy, c, m, and k
def get_mirror_grating_angles(eV, c, m, k):
    grating_angle = (
        -(
            180
            - ruben2005eqn8m(eV, c, k, m)
            + getBetaDeg(eV, ruben2005eqn8m(eV, c, k, 1), k, m)
        )
        / 2
    )
    mirror_angle = -90 - getBetaDeg(eV, ruben2005eqn8m(eV, c, k, m), k, m)
    return [mirror_angle, grating_angle]
