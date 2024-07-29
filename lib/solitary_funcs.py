""" Functions for calculating the solitary wave non-hydrostatic test case 

The references for this work are:

xBeach Non-hydrostaic manual url: https://oss.deltares.nl/documents/4142077/4199062/non-hydrostatic_report_draft.pdf

Fenton (1972) DOI: 10.1017/S002211207200014X
"""

# Standard imports
import numpy as np

# Library imports
from lib.trigonometric_funcs import sech
from lib.global_constants import DEBUG

def calc_wave_speed(g, epsilon, d0):
    r"""
    Calc the wave speed for a solitary wave. Equation taken from the xBeach non-hydrostatic manual
    
    Eqn:
        c = (1 + \frac{1}{2} \varepsilon - \frac{3}{20} \varepsilon^{2} + frac{3}{56} \varepsilon^{3}) * \sqrt{g d_{0}}
    
    xBeach Non-hydrostatic manual url: https://oss.deltares.nl/documents/4142077/4199062/non-hydrostatic_report_draft.pdf

    """

    c = (1 + 1/2 * epsilon - 3/20 * epsilon**2 + 3/56 * epsilon**3) * np.sqrt(g * d0)

    return c

def calc_alpha(epsilon):
    r"""
    Purpose: Calc the alpha term in equation 2.10 of non-hyrdostatic model. Derived in Fenton (1972)

    Eqn:
        \alpha = \sqrt{\frac{3}{4} \epsilon} (1 - \frac{5}{8} \epsilon + \frac{71}{128} \epsilon^{2})

    where:
        \epsilon: Ratio of max wave height (\eta_{0}) to initial water depth (d0, h)

    Fenton (1972) DOI: 10.1017/S002211207200014X

    xBeach Non-hydrostatic manual url: https://oss.deltares.nl/documents/4142077/4199062/non-hydrostatic_report_draft.pdf

    """
    
    alpha = np.sqrt(3/4 * epsilon) * (1 - 5/8 * epsilon + 71/128 * epsilon**2)

    return alpha

def calc_s_term(alpha, x, x0, c, t, d0):
    r"""
    Calc the s term in the Fenton (1972) paper

    Eqn:
        s = sech(\alpha x_{*})

    where:
        \alpha: Is an input parameter
        x_{*}: dimensionless x location - x_{*} = x/d0
    
    The equation was modified to account for reference systems that are fixed by xBeach Non-Hydrostatic manual
    The new equation takes the form
    Eqn:
        s = sech(\alpha * (x - x_{0} - c t) * 1/d0)
    
    NOTE: The 1/d0 isn't included in the Non-Hydrostatic manual but I don't think that matters since the water depth is 1
    where:
        x    : the x-location
        x_{0}: the arbitrary intial location
        c    : The wave speed
        t    : time
        d0   : Water depth
    """

    return sech(alpha * ( x - x0 - c * t) * 1/d0)

def calc_th_term(alpha, x, x0, c, t, d0):
    r"""
    Calc the "th" term (as referred to as from the xBeach manual) refrerred to as the "t" term in Fenton (1972)

    From Fenton the original equation is
    Eqn:
        th = tanh(\alpha x_{*})
    
    NOTE: The 1/d0 isn't included in the Non-Hydrostatic manual but I don't think that matters since the water depth is 1
    where:
        \alpha: Is an input parameter
        x_{*} : dimensionless x-location - x_{*} = x/d0

    The equation was modified for reference coordinate systems that are fixed by the xBeach Non-Hydrostatic manual
    The new equaiton takes the form
    Eqn:
        th = tanh(\alpha * (x - x_{0} - c t) * 1/d0)
    """

    return np.tanh(alpha * ( x - x0 - c * t) * 1/d0)

def calc_surface_elevation(epsilon, x0, x, t, g, d0):
    r"""
    Purpose: Calc the normalized surface elevation for a solitary wave
    
    \eta(x,t) = d_0 \left( \varepsilon s^2 - 
                \frac{3}{4}\varepsilon^2 s^2 th^2 
                + \varepsilon^3 \left( \frac{5}{8} s^2 th^2 
                - \frac{101}{80} s^4 th^2 \right) \right)

    where:
        epsilon: ratio of wave height to water depth
        x0: Initial location of the wave
        x: wave height at certain location
        t: time
        g: gravity
        d0: Initial water depth
    """

    # Calc the wave speed
    c = calc_wave_speed(g, epsilon, d0)

    # Calc alpha
    alpha = calc_alpha(epsilon)

    # Calc the s term
    s = calc_s_term(alpha, x, x0, c, t, d0)
    # calc the th term

    th = calc_th_term(alpha, x, x0, c, t, d0)

    # Calc each term in the equation seperately to make reading easier
    
    # NOTE: This is Fenton's first term
    # This makes the water level at d0
    first_term = 1 + epsilon * s**2 

    # NOTE: This is xBeach non-hydro manual solution
    # This makes the water level at zero
    # first_term  = epsilon * s**2

    second_term = -3/4 * epsilon**2 * s**2 * th**2
    third_term  = epsilon**3 * (5/8 * s**2 * th**2 -101/80 * s**4 * th**2)

    # Sum the terms with the correct sign and multiply by the d0 scaling
    eta = (first_term + second_term + third_term) * d0

    if DEBUG:
        print("Printing surface elevation info")
        print("s", s)
        print("th", th)
        print(eta)

    return eta

def calc_L_scaling(epsilon, delta_scaling = 1/20):
    r"""
    Calc the wave length scaling parameter (L_{sol}). Equation taken from xBeach non-hydrostatic manual

    Eqn:
        L_{sol} = \sqrt{\frac{4}{3 \varepsilon} * acosh(\frac{\varepsilon}{\delta})}

    where:
        epsilon: Ratio of intial wave height to intial depth
        delta_scaling: Scaling of epsilon terms used to calc delta - taken to ;be 1/20 in the manual
    
    xBeach Non-hydrostaic manual url: https://oss.deltares.nl/documents/4142077/4199062/non-hydrostatic_report_draft.pdf

    """

    delta = delta_scaling * epsilon # Ratio set in the paper

    L_sol = np.sqrt(4/(3 * epsilon)) * np.arccosh(np.sqrt(epsilon/delta))

    return L_sol

def calc_Smit_L_scaling(eta_0, d0, delta = 1/20):
    r"""
    Calc the wave length scaling parameter L_{sol} form **Smit (2008)**
    
    inputs:
        - eta_0 : Amplitude of the solitary wave
        - d0    : Still Water depth
        - delta : Scaling factor

    Eqn:
        L = 2 \sqrt{ \frac{ 3 \eta_{0} }{4 d_{0}^{3} }} arccosh( \sqrt( 1 / \delta ) )
    
    where:
        - \eta_{0} : Amplitude of the solitary wave
        - d_{0}    : Still water depth
        - \delta   : Scaling parameter

    [Smit (2008)](https://repository.tudelft.nl/islandora/object/uuid:416ae56c-8fa6-42b1-b532-acc457b28604?collection=education)
    
    """

    inner_fraction = 3 * eta_0 / ( 4 * d0**3 )
    return 2 * np.sqrt(inner_fraction) * np.arccosh(np.sqrt( 1/ delta ) )

def calc_u_vel(epsilon, x0, x, y, t, g, d0):
    r"""
    Calc the u velocity using the third order accurate soln. from Fenton (1972)
    
    Fenton (1972) DOI: 10.1017/S002211207200014X

    Eqn:
        u = { 
                1 + 1/2 \epsilon - 3/20 \epsilon^{2} 
                + 3/56 \epsilon^{3} - \epsilon * s^{2}
                + \epsilon^{2} [ -1/4 s^{2} + s^{4} + y^{2} (3/2 s^{2} - 9/4 s^{4})]
                + \epsilon^{3} [19/40 s^{2} + 1/5 s^{4} - 6/5 s^{6} 
                + y^{2} (-3/2 s^{2} - 15/4 s^{4} + 15/2 s^{6})
                + y^{4} (-3/8 s^{2} + 45/16 s^{4} - 45/16 s^{6})]
            } \sqrt(g h)
        
        with:
        s = sech ( \alpha x)

    where
        - x: x-location
        - y: y-location
        - epsilon: Selection expansion factor
        - g: gravity
        - h: inital water depth

    NOTE: The co-ordinate orign is at a point on the rigid bottom with x in the direction of flow
    NOTE: s and th are shifted from Fentons solution to account for a stationary co-ordinate system
    """
    
    # Calc the wave speed
    c = calc_wave_speed(g, epsilon, d0)

    # Calc alpha
    alpha = calc_alpha(epsilon)

    # Calc the s term
    s  = calc_s_term(alpha, x, x0, c, t, d0)

    # calc the th term
    th = calc_th_term(alpha, x, x0, c, t, d0)
    
    # Calc the terms of the velocity calculation
    first_part  = 1 + 0.5 * epsilon - 3/20 * epsilon**2 +  3/56 * epsilon**3 - epsilon * s**2
    second_part = epsilon**2 * ( -1/4 * s**2 + s**4 + y**2 * (3/2 * s**2 - 9/4 * s**4))
    third_part  = epsilon**3 * (19/40 * s**2 + 1/5 * s**4 -6/5 * s**6
                                + y**2 * (-3/2 * s**2 - 15/4 * s**4 + 15/2 * s**6)
                                + y**4 * (-3/8 * s**2 + 45/16 * s**4 - 45/16 * s**6))
    
    return (first_part + second_part + third_part) * np.sqrt(g * d0)

def calc_v_vel(epsilon, x0, x, y, t, g, d0):
    r"""
    Calculate the v velocity using the third order accurate solution. Equation taken from Fenton

    Fenton (1972) DOI: 10.1017/S002211207200014X

    Eqn:
        v = (3 * epsilon)^(1/2) * y * th * {
                -epsilon * s^2 + epsilon^2 * [3/8 s^2 + 2 s^4 + y^2 (1/2 s^2 - 3/2 s^4)]
                + epsilon^3 [49/640 s^2 - 17/20 s^4 - 18/5 s^6 
                + y^2 (-13/16 s^2 - 25/16 s^4 + 15/2 s^6)
                + y^4 (-3/40 s^2 + 9/8 s^4 - 27/16 s^6)]
            } sqrt(g h)

        with:
        s  = sech(alpha * (x - x0 - ct))
        th = tanh(alpha * (x - x0 - ct))

    where
        - x: x-location
        - y: y-location
        - epsilon: Selection expansion factor
        - g: gravity
        - d0: initial water depth
    
    NOTE: The co-ordinate orign is at a point on the rigid bottom with x in the direction of flow
    NOTE: s and th are shifted from Fentons solution to account for a stationary co-ordinate system
    """
    
    # Calc the wave speed
    c = calc_wave_speed(g, epsilon, d0)

    # Calc alpha
    alpha = calc_alpha(epsilon)

    # Calc the s term 
    s  = calc_s_term(alpha, x, x0, c, t, d0)

    # calc the th term
    th = calc_th_term(alpha, x, x0, c, t, d0)

    # Calculate the terms of the velocity calculation
    first_part  = -epsilon * s**2
    second_part = epsilon**2 * (3/8 * s**2 + 2 * s**4 + y**2 * (1/2 * s**2 - 3/2 * s**4))
    third_part  = epsilon**3 * (49/640 * s**2 - 17/20 * s**4 - 18/5 * s**6
                                + y**2 * (-13/16 * s**2 - 25/16 * s**4 + 15/2 * s**6)
                                + y**4 * (-3/40 * s**2 + 9/8 * s**4 - 27/16 * s**6))
    
    return np.sqrt(3 * epsilon) * y * th * (first_part + second_part + third_part) * np.sqrt(g * d0)

def calc_depth_average_u(epsilon, x0, x, t, g, d0):
    r""""
    Calc the depth average horizontal (u_avg) velocity. 
    The equation was found by depth averaging Fenton's (1972) u-velocity equation.
    
    Eqn:

        u_{avg} =  { 
                1 + 1/2 \epsilon - 3/20 \epsilon^{2} 
                + 3/56 \epsilon^{3} - \epsilon s^{2} 
                + \epsilon^{2}[-1/4 s^{2} + s^{4} + \eta^{2}/3 ( 3/2 s^{2} - 9/4 s^{4})] 
                + \epsilon^{3} [
                    19/40 s^{2} + 1/5 s^{4} - 6/5 s^{6} 
                    + \eta^{2}/3 (-3/2  s^{2} - 15/4 s^{4} + 15/2 s^{6})
                    + \eta^{4}/5 (-3/8 s^{2} + 45/16 s^{4} - 45/16 s^{6})
                ]
            }\sqrt(gh)

    with:
        s = sech ( \alpha x)

    where
        - x      : x-location
        - y      : y-location
        - epsilon: Selection expansion factor
        - g      : gravity
        - h      : inital water depth
        - \eta   : Water surface elevation
 
    NOTE: The co-ordinate orign is at a point on the rigid bottom with x in the direction of flow
    NOTE: s and th are shifted from Fentons solution to account for a stationary co-ordinate system
    """
    
    # Calc the wave speed
    c = calc_wave_speed(g, epsilon, d0)

    # Calc alpha
    alpha = calc_alpha(epsilon)

    # Calc the s term
    s  = calc_s_term(alpha, x, x0, c, t, d0)

    # Calc the water surface elevation
    eta = calc_surface_elevation(epsilon, x0, x, t, g, d0)

    first_term  = 1 + 0.5 * epsilon - 3/20 * epsilon**2
    second_term = 3/56 * epsilon**3 - epsilon * s**2
    third_term  = epsilon**2 * (-1/4 * s**2 + s**4 + eta**2/3 * (3/2 * s**2 -9/4 * s**4))
    fourth_term = epsilon**3 * (
        19/40 * s**2 + 1/5 * s**4 -6/5 * s**6
        + eta**2/3 * (-3/2 * s**2 - 15/4 *  s**4 + 15/2  * s**6)
        + eta**4/5 * (-3/8 * s**2 + 45/16 * s**4 - 45/16 * s**6)
    ) 

    return (first_term + second_term + third_term + fourth_term) * np.sqrt(g * d0)