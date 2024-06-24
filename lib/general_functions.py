"""
File Contains functions that are general purpose
"""

# Standard imports
import numpy as np

# Library imports

def find_closest_value_index(arr, value):
    # Purpose find the index of the closest number in arr to value
    
    diff_arr = np.abs(arr - value)
    index = diff_arr.argmin()

    return index