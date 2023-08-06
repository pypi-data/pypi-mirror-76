"""
#####################################################################

Copyright (C) 1999-2017, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

For details on the method see:
    Cappellari M., 2002, MNRAS, 333, 400
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your
research, I would appreciate an acknowledgement to use of
`the MGE fitting method and software by Cappellari (2002)'.

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

#####################################################################

NAME:
    SECTORS_PHOTOMETRY_TWIST

AUTHOR:
    Michele Cappellari, Astrophysics Sub-department, University of Oxford, UK

PURPOSE:
    Perform photometry of a galaxy image along sectors equally spaced in
    angle. This routine assumes four-fold symmetry, so measurements in
    the four quadrants are averaged together. This routine is useful to
    generate the input photometry required by the MGE fitting routine
    MGE_FIT_SECTORS.

EXPLANATION:
    Further information on SECTORS_PHOTOMETRY is available in
    Cappellari M., 2002, MNRAS, 333, 400
    https://ui.adsabs.harvard.edu/abs/2002MNRAS.333..400C

CALLING SEQUENCE:
    s = sectors_photometry(img, eps, theta, xpeak, ypeak, badpixels=None,
                           n_sectors=19, mask=None, minlevel=0, plot=False)

INPUTS:
    IMG = The galaxy image as a 2D array.
    EPS = The galaxy "average" ellipticity Eps = 1 - b/a = 1 - q'.
        Photometry will be measured along elliptical annuli with
        constant axial ellipticity EPS. The four quantities
        (EPS, ANG, XC, YC) can be measured with the routine FIND_GALAXY.
    ANG = Position angle measured counterclockwise from
        the image Y axis, to the galaxy major axis.
    XC = X coordinate of the galaxy center in pixels.
    YC = Y coordinate of the galaxy center in pixels.

OUTPUTS (attributes of the sectors_photometry class):
    RADIUS = Vector containing the radius of the surface brightness
        measurements, taken from the galaxy center. This is given
        in units of PIXELS (!).
    ANGLE = Vector containing the polar angle of the surface brightness
        measurements, taken from the galaxy major axis.
    COUNTS = Vector containing the actual surface brightness measurements
        in COUNTS (!) at the polar coordinates specified by the vectors
        Radius and Angle. These three vectors have the same
        number of elements.

OPTIONAL INPUT KEYWORDS:
    BADPIXELS - Boolean image mask with the same dimension as IMG.
        True values are masked and ignored in the photometry.
    N_SECTORS - Number of the sectors, equally spaced in exxectric anomaly,
        from the galaxy major axis to the minor axis (one quadrant).
        (default: 36 to cover the whole image with 5 degrees width).
    MASK - Boolean image mask with the same dimension as IMG.
        False values are masked and ignored in the photometry.
        This keyword is just an alternative
        way of specifying the BADPIXELS.
    MINLEVEL - Scalar giving the minimum COUNTS level to include
        in the photometry. The measurement along one profile
        will stop when the counts first go below this level.

EXAMPLE:
    See mge_fit_example.py

MODIFICATION HISTORY:
    V1.0.0: First implementation for the NGC2681 photometric modeling.
        Michele Cappellari, ESO Garching, 27 september 1999
    V2.0.0: Major revisions, to use it with MGE_FIT_SECTORS.
        Leiden, January 2000, MC
    V2.1.0: Further updates, Padova, August 2000, MC
    V2.1.1: Added compilation options, MC, Leiden 20 May 2002
    V2.1.2: Allow for N_SECTORS=1 to get a single profile centered at
        a given PA. Use biweight mean instead of sigma-clipped mean.
        MC, Leiden, 30 April 2004
    V2.1.3: Reduced amount of verbose output. MC, Leiden, 24 October 2004
    V2.1.4: Replaced LOGRANGE keyword in example with the new MAGRANGE.
        MC, Leiden, 1 May 2005
    V2.1.5: Forces image to be positive when computing weighted radius
        to prevent possible negative radii at large radii. Thanks to
        Michael Williams for reporting the problem and the fix.
        MC, Oxford, 16 February 2009
    V3.0.0: Translated from IDL into Python. MC, Aspen Airport, 8 February 2014
    V3.0.1: Support both Python 2.7 and Python 3. MC, Oxford, 25 May 2014
    V3.1.0: Improved image visualization of sampled photometric grid.
        Sample angles uniformly in eccentric anomaly rather than polar angle.
        Removed Scipy dependency. MC, Oxford, 23 September 2014
    V3.1.1: Show badpixels as empty in checkerboard plot.
        Define input badpixels as a boolean mask. MC, Oxford, 30 May 2015
    V3.1.2: Stop profile if cnt <= 0. MC, Paris, 7 April 2016
    V3.1.3: Use interpolation='nearest' to avoid crash on MacOS.
        MC, Oxford, 14 June 2016
    V3.1.4: Fix NaN in _biweight_mean() when most values are zero.
        This can  happen with synthetic images from N-body simulations.
        Check for NaN in input image. MC, Oxford, 13 February 2017
    V3.1.5: Properly drop last radial value from checkerboard plot.
        MC, Oxford, 9 May 2017
    V4.0.0: Converted sectors_photometry into sectors_photometry_twist.
        MC, Oxford, 27 July 2017
    V4.0.1: Fixed DeprecationWarning in Numpy 1.9. MC, Oxford, 11 August 2020

"""

import numpy as np
import matplotlib.pyplot as plt


#----------------------------------------------------------------------------

def _linspace_open(a, b, num=50):

    dx = (b - a)/num
    x = a + (0.5 + np.arange(num))*dx

    return x

#----------------------------------------------------------------------------

def _biweight_mean(y, itmax=10):
    """
    Biweight estimate of the location (mean).
    Implements the approach described in
    "Understanding Robust and Exploratory Data Analysis"
    Hoaglin, Mosteller, Tukey ed., 1983

    """
    y = np.ravel(y)
    c = 6.
    fracmin = 0.03*np.sqrt(0.5/(y.size - 1))
    y0 = np.median(y)
    mad = np.median(np.abs(y - y0))
    if mad == 0:   # can happen when most pixels are zero
        return np.mean(y)

    for it in range(itmax):
        u2 = ((y - y0)/(c*mad))**2
        u2 = u2.clip(0, 1)
        w = (1 - u2)**2
        y0 += np.sum(w*(y - y0))/np.sum(w)
        mad_old = mad
        mad = np.median(np.abs(y - y0))
        frac = np.abs(mad_old - mad)/mad
        if frac < fracmin:
            break

    return y0

#----------------------------------------------------------------------------

def _coordinates(pos_ang, xc, yc, s):

    ang = np.radians(pos_ang)                   # ang=0 is minor axis
    x, y = np.ogrid[-xc:s[0] - xc, -yc:s[1] - yc]
    rad = np.sqrt(x**2 + y**2)                  # Radius
    phi = np.arctan2(y, x) + ang
    phi = (phi + np.pi/2) % np.pi - np.pi/2     # Polar angle [-pi/2, pi/2]

    return rad, phi

#----------------------------------------------------------------------------

class sectors_photometry_twist:

    def __init__(self, img, ang, xc, yc, badpixels=None,
                  n_sectors=36, mask=None, minlevel=0, plot=False):
        """
        This routine performs photometry along sectors linearly spaced
        in polar angle in half quadrant of a galaxy.
        In output it returns the three vectors RADIUS, ANGLE, CNT,
        containing the photometric measurements in polar coordinates.

        """
        assert np.all(np.isfinite(img)), "Input image contains NaN"
        xc, yc = int(round(xc)), int(round(yc))
        s = img.shape
        minlevel = max(minlevel, 0)

        rad, phi = _coordinates(ang, xc, yc, s)
        rad[xc, yc] = 0.38  # Average radius within the central pixel

        if plot:
            self.grid = np.zeros_like(img, dtype=bool)

        # Sample radii with 24 isophotes per decade: factor 1.1 spacing.
        # Sample polar angle with n_sectors from 0 to pi

        lrad = (24.2*np.log10(rad)).astype(int)
        phi = (n_sectors*(phi/np.pi + 0.5)).astype(int)   # 0 -- (n_sectors-1)

        if mask is not None:
            assert mask.dtype == bool, "MASK must be a boolean array"
            assert mask.shape == img.shape, "MASK and IMG must have the same shape"
            assert badpixels is None, "BADPIXELS and MASK cannot be used together"
            badpixels = ~mask

        if badpixels is not None:
            assert badpixels.dtype == bool, "BADPIXELS must be a boolean array"
            assert badpixels.shape == img.shape, "BADPIXELS and IMG must have the same shape"
            phi[badpixels] = -1  # Negative flag value

        self.radius = self.counts = self.angle = []
        angGrid = _linspace_open(-90, 90, n_sectors)       # Polar angle

        for k, angj in enumerate(angGrid):
            radj, cntj = self._profile(
                    img, xc, yc, rad, lrad, phi, k, plot, minlevel)
            self.radius = np.append(self.radius, radj)
            self.counts = np.append(self.counts, cntj)
            self.angle = np.append(self.angle, np.full_like(radj, angj))

        if plot:
            plt.imshow(np.log(img.clip(img[xc, yc]/1e4)), cmap='hot',
                       origin='lower', interpolation='nearest')
            if badpixels is not None:
                self.grid[badpixels] = False
            plt.imshow(self.grid, cmap='binary', alpha=0.3,
                       origin='lower', interpolation='nearest')
            plt.xlabel("pixels")
            plt.ylabel("pixels")

#----------------------------------------------------------------------------

    def _profile(self, data, xc, yc, rad, lrad, phi, k, plot, minlevel):

        if phi[xc, yc] != -1:
            phi[xc, yc] = k  # Always include central pixel unless bad
        sector = np.flatnonzero(phi == k)
        irad = lrad.flat[sector]
        levels = np.unique(irad)  # get unique levels within sector
        cnt = np.empty(levels.size)
        radius = np.empty(levels.size)

        for j, lev in enumerate(levels):
            sub = sector[irad == lev]
            if sub.size > 9:   # Evaluate a biweight mean
                cnt[j] = _biweight_mean(data.flat[sub])
            else:
                cnt[j] = np.mean(data.flat[sub])  # Usual mean

            if (cnt[j] <= minlevel):   # drop last value
                cnt = cnt[:j]
                radius = radius[:j]
                break

            # Luminosity-weighted average radius in pixels
            flx = data.flat[sub].clip(0)
            radius[j] = np.sum(rad.flat[sub]*flx)/np.sum(flx)

            if plot:
                self.grid.flat[sub] = (lev + k % 2) % 2

        j = np.argsort(radius)
        cnt = cnt[j]
        radius = radius[j]

        return radius, cnt

#----------------------------------------------------------------------------
