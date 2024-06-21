# Standard imports
import numpy as np

def sech(x):
    """
    Purpose: Calc sech, numpy doesn't have the in-built function 
    """

    return 1/np.cosh(x)