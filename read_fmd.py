# FMD Data File Utility

import numpy as np

def read_fmd(filename):
    """
    Given a file path, read an FMD file and return the raw data in NumPy array format

    Note: a sample rate of 1 kHz is assumed for all FMD files

    Parameters:
    - `filename`: a filename or file path

    Returns: raw force data (in millinewtons) over time
    """
    # Read in data file
    with open(filename, "r") as f:
        lines = f.read().split()

    # Numeric force data (mN)
    data = []

    # Are we reading real data yet?
    flag = False

    # TODO: Actually save the header?
    for value in lines:
        if flag:
            data.append(float(value))
        else:
            flag = value == "abcd"

    # Truncate data to first third only
    # Note: I don't know why this happens, I'm just copying a MATLAB script LOL
    data = data[:len(data)//3]

    return np.array(data)
