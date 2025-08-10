# Force Data Analysis

from sys import argv
from os import walk, mkdir, system, path
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

from read_fmd import read_fmd
from constants import *

def analyze_force(filename, twitch_kinetics=True):
    """
    Analyze a force data file (in FMD format)

    Parameters:
    - `filename`: Filename or file path
    - `twitch_kinetics` (bool): Should we consider twitch kinetics?

    Returns: a dictionary containing
        - Max force (millinewtons)
        - Min force (millinewtons)
        - Active force (millinewtons)
        - Rise time (milliseconds)
        - Decay time (milliseconds)
        - Total time (milliseconds)
        - Raw data
    """
    # Read in force data
    data = read_fmd(filename)

    # Compute baseline, maximum, and active forces
    min_force = np.min(data)
    max_force = np.max(data)
    active_force = max_force - min_force

    # Twitch kinetics results
    rise_start = None
    rise_end = None
    decay_start = None
    decay_end = None
    rise_time = None
    decay_time = None
    total_time = None

    if twitch_kinetics:
        # Truncate data again and filter
        data = signal.medfilt(data[:TK_CUTOFF], kernel_size=TK_KERNEL_SIZE)

        # Recompute bounds
        tk_min_force = np.min(data)
        tk_max_force = np.max(data)

        # Thresholds
        lower       = tk_min_force + TK_FRAC*(tk_max_force - tk_min_force)
        upper       = tk_min_force + (1-TK_FRAC)*(tk_max_force - tk_min_force)

        # Get rise time
        rise_start  = np.argmax(data > lower)
        rise_end    = np.argmax(data > upper)
        rise_time   = rise_end - rise_start

        # Get decay time
        i           = rise_end + TK_BUFFER
        decay_data  = data[i:]
        if np.size(decay_data):
            decay_start = i + np.argmax(decay_data < upper)
            decay_end   = i + np.argmax(decay_data < lower)
            decay_time  = decay_end - decay_start

        # Get total time
        if decay_time is not None:
            total_time  = decay_end - rise_start

    return {
        "min_force": min_force,
        "max_force": max_force,
        "active_force": active_force,
        "passive_force": None,         # calculated later
        "rise_time": rise_time,
        "decay_time": decay_time,
        "total_time": total_time,
        "raw_data": data,
        "rise_start": rise_start,
        "rise_end": rise_end,
        "decay_start": decay_start,
        "decay_end": decay_end
    }
