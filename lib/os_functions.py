# Standard imports
import os

# Libary imports

""""
File contains scripts that operate on the file or operating system
"""

def write_2d_arr_2_file(arr, filename):
    """
    Writes a 2d arr into a file with each row of the 2d arr written as a row in the file
    
    Inputs:
        filename: Name of the file that the data should be written to
        arr     : 2d Array that should be written to the file
    """

    # Open the file in write mode
    with open(filename, 'w') as file:
        # Write each row of the array to the file
        for row in arr:
            file.write(' '.join(map(str, row)) + '\n')

    print(f"2D array values have been written to {filename}")
