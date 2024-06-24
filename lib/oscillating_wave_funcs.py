"""
File contains functions that are required to generate the analytical solution to the osicillating basin problem and do some post analysis 
comparison with the xBeach solution

Author: WaveHello
Last Updated: 06/24/2024
"""

# Standard imports
import numpy as np


# Library imports

# Linear dispersion function
def calc_non_h_dispersion_relation(k, g, H):
    r"""
    Purpose: Calc the dispersion relation for a wave using non-hydrostatic linearized
    Eqn: $$ k * \sqrt{\frac{gH}{1 + 0.25(kH)^{2}} $$
    where,

    k: wave number [rad/m]
    g: gravity
    H: Water depth at an x, y location
    """

    numerator = g * H
    denominator = 1 + 0.25 * (k * H)**2

    return k * np.sqrt(numerator/denominator)

def calc_linear_dispersion_relation(k, g, H):
    r"""
    Calc the linear dispersion relation

    Eqn:
        \omega = \sqrt{ g k tanh(k H)}
    where:
    \omega: Linear wave dispersion
    g     : gravity
    k     : norm wave number
    H     : initial water depth
    """

    return np.sqrt(g * k * np.tanh(k * H))

def calc_wave_number(k_x, k_y):
    r"""
    Purpose: Calc the magnitude of the individual directional wave numbers
    In multidimensional systems, the wave number is the magnitude of the wave vector

    NOTE: Eqn. taken from Wave-current interaction (wci) XBeach manual section
    """
    return np.sqrt(k_x**2 + k_y**2)

def calc_surface_elevation(zeta_0, k_x, k_y, x, y, t, omega):
    r"""
    Purpose: Calc the surface elevation linear dispersion, formula taken from xBeach non-hydrostatic manual
    
    Eqn: $$ \zeta(x, y, t) = \zeta_{0} cos(k_{x} x) cos(k_{y} y) cos(\omega t) $$

    \zeta:     Surface elevation
    \zeta_{0}: Initial surface displacement??
    k_{x}:     wave number in the x-direction
    k_{y}:     wave number in the y-direction
    x:         x-location
    y:         y-location
    t:         time
    omega:     linear dispersion
    """

    return zeta_0 * np.cos(k_x * x) * np.cos(k_y * y) * np.cos(omega * t)

# average velocity functions

# x-velocity
def calc_U_velocity(eta_0, g, k_x, k_y, H, x, y, t, omega):
    r"""
    Purpose: Calc the average U velocity using the relation provided in xBeach non-hydrostatic in the linear dispersion example

    Eqn: $$U(x, y, t) = \frac{\eta_{0} g k_{x}}{k H \omega} sin(k_{x} x) cos(k_{y} y) sin(\omega t)$$
     
    \eta_{0}: Initial water elevation
    g:        gravity
    k_{x}:    x-direction wave number
    k_{y}:    y-direction wave number
    H:        water depth
    x:        x-location
    y:        y-location
    t:        time
    \omega:   dispersion
    k:        wave number (magnitude of the individual componets)
    """
    k = calc_wave_number(k_x, k_y)

    frac = eta_0 * g * k_x/(k * H * omega)
    trig_part = np.sin(k_x * x) * np.cos(k_y * y) * np.sin(omega * t)

    return frac * trig_part

# y-velocity
def calc_V_velocity(eta_0, g, k_x, k_y, H, x, y, t, omega):
    r"""
    Purpose: Calc the average V velocity using the relation provided in xBeach non-hydrostatic in the linear dispersion example

    Eqn: $$V(x, y, t) = \frac{\eta_{0} g k_{y}}{k H \omega} cos(k_{x} x) sin(k_{y} y) sin(\omega t)$$

    \eta_{0}: Initial water elevation
    g:        gravity
    k_{x}:    x-direction wave number
    k_{y}:    y-direction wave number
    H:        water depth
    x:        x-location
    y:        y-location
    t:        time
    \omega:   dispersion
    k:        wave number (magnitude of the individual componets)
    """

    # Calc the magnitude of the wave number vector
    k = calc_wave_number(k_x, k_y)

    frac = eta_0 * g * k_y/(k * H * omega)

    trig_part = np.cos(k_x * x) * np.sin(k_y * y) * np.sin(omega * t)

    return frac * trig_part
    




