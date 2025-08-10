#!/usr/bin/env python3
# Force Data File Discovery

from os import mkdir, path, system, walk
from pathlib import Path
import time

import tkinter as tk
from tkinter import filedialog, messagebox

from analyze import analyze_force
from constants import *
from csv_writer import OutputFile
from plot_forces import plot_forces

def analyze_directory(dirname, create_plots=False):
    """
    Analyze all force data files in a given directory

    Parameters:
    - `dirname`: directory name or file path

    Returns: nothing, modifies directories to create:
    - `output.csv`: file containing analysis output for each FMD file in this directory
    - `maxforces`: directory containing
        - `maxforces.csv`: file containing analysis output for highest performing stretch length per tissue
        - Time-series data in FMD format corresponding to each measurement listed in `maxforces.csv`
    - `plots`: (optional) directory containing plots of time series represented by `.fmd` data
    """   
    # Walk directory
    dirname = Path(dirname)
    dirpath, subdirs, files = next(walk(dirname))
    dirpath = Path(dirpath)

    # Sort subdirectories
    subdirs.sort()

    # Analyze all valid subdirectories (skip maxforces)
    _ = [
        analyze_directory(dirname / s, create_plots=create_plots)
        for s in subdirs
        if s not in SPECIAL_DIRS
    ]

    # If no FMD files in this directory, stop
    if not any([f.endswith(".fmd") for f in files]):
        return

    # Sort filenames alphabetically
    files.sort()

    # Create special subdirectories and empty them, if they exist
    for special_dir in SPECIAL_DIRS:
        if path.exists(dirpath / special_dir):
            system(f"rm -r {dirpath / special_dir}")
        mkdir(dirpath / special_dir)

    # Initialize output file and maxforces output file
    output = OutputFile(
        dirpath / OUTPUT_CSV,
        OUTPUT_HEADER,
    )
    maxforces_output = OutputFile(
        dirpath / MAXFORCES / MAXFORCES_CSV,
        OUTPUT_HEADER,
    )

    # Save max value for each tissue and corresponding filename
    # Also save min value for each tissue
    max_forces = {}
    min_forces = {}
    for i in range(1, MAX_TISSUE_COUNT+1):
        max_forces[f"T{i}"] = (0.0, None)
        min_forces[f"T{i}"] =  0.0
    
    # CSV rows
    data = []

    for filename in files:
        # Skip non-FMD files
        if not filename.endswith(FORCE_EXT):
            continue

        # Start performance counter
        start = time.perf_counter()

        # Are twitch kinetics required?
        tk_required = "FB" not in filename

        # Force analysis & twitch kinetics
        results = analyze_force(
            dirpath / filename,
            twitch_kinetics=tk_required,
        )

        # Save plot, if TK required and plot requested
        if create_plots and tk_required:
            plot_forces(
                results["raw_data"],
                dirpath / PLOTS,
                filename,
                vlines=[
                    (results["rise_start"], "Start Rise"),
                    (results["rise_end"], "End Rise"),
                    (results["decay_start"], "Start Decay"),
                    (results["decay_end"], "End Decay"),
                ],
            )

        # Check baseline value by tissue
        for i in range(1, MAX_TISSUE_COUNT+1):
            tissue_number = f"T{i}"
            if tissue_number in filename:
                if BASELINE_INDICATOR in filename:
                    min_forces[tissue_number] = results["min_force"]
                elif results["active_force"] > max_forces[tissue_number][0]:
                    max_forces[tissue_number] = results["active_force"], filename
        
        # Append analyzed data
        output.add([
            filename,
            results["min_force"],
            results["max_force"],
            results["active_force"],
            results["passive_force"], # currently this is `None`
            results["rise_time"],
            results["decay_time"],
            results["total_time"],
        ])

        # End performance counter
        analysis_time = time.perf_counter() - start
        unit          = "us" if analysis_time < 1e-3 else "ms"
        multiplier    =  1e6 if analysis_time < 1e-3 else 1e3
        print(f"Analyzed {filename} in {round(multiplier * analysis_time, 3)} {unit}")

    # Filenames corresponding to files with maximum active force per tissue
    max_force_filenames = [n for v, n in max_forces.values() if n is not None]
    max_force_filenames.sort()

    # Calculate passive force and create maxforces CSV
    for j, (fname, minf, maxf, actf, _pasf, rist, dect, tott) in enumerate(output):
        # Evaluate the passive force for this tissue
        pasf = None
        for i in range(1, MAX_TISSUE_COUNT+1):
            tissue_number = f"T{i}"
            if tissue_number in fname:
                pasf = round(minf - min_forces[tissue_number], 3)
                break
            
        # Save passive force
        output[j, "Passive (mN)"] = pasf

        if fname in max_force_filenames:
            maxforces_output.add([fname, minf, maxf, actf, pasf, rist, dect, tott])

    # Write output CSV
    output.save()

    # Write `maxforces` CSV
    maxforces_output.save()

    # Populate `maxforces` directory with `.fmd` files
    for _value, filename in max_forces.values():
        if filename is not None:
            system(f"cp {dirpath / filename} {dirpath / MAXFORCES}")

if __name__ == "__main__":
    # Start Tkinter
    root = tk.Tk()
    root.withdraw()

    # Get directory
    dirname = filedialog.askdirectory(title="Select Input Directory")

    # Check if user wants plots
    # 
    # Plots are time-intensive so they should only be
    #   generated if requested
    create_plots = messagebox.askyesno(
        "Force Curves",
        "Generate force curves?  This will take longer.",
    )

    # Analyze given directory
    analyze_directory(
        dirname,
        create_plots=create_plots,
    )

    # Inform user
    messagebox.showinfo(
        "FMD Analyzer Complete",
        "Analysis is complete! :)",
    )

    # End Tkinter
    root.destroy()
