# Plot Force Data

from matplotlib import pyplot as plt

from constants import *

def plot_forces(data, path, source_filename, vlines=None):
    """
    Plot force data and TK (if pertinent) and save to output file
    """
    if vlines is None:
        vlines = []

    # Output filename
    output_filename = f"{source_filename.rstrip(FORCE_EXT)}.png"

    # Format plot
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"]   = 12

    # Create new figure
    fig, ax = plt.subplots()

    # Plot data
    ax.plot(data, color="black")

    # Plot TK
    for i, (x, name) in enumerate(vlines):
        if x is not None:
            ax.axvline(
                x=x,
                color=LINE_COLORS[i % len(LINE_COLORS)],
                linestyle="--",
                label=name,
            )

    # Create title and axis labels
    fig.suptitle(source_filename)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Force (mN)")

    # Create legend
    if [x for x, _ in vlines if x is not None]:
        fig.legend(loc="lower right")

    # Save plot
    fig.tight_layout()
    fig.savefig(path / output_filename)

    # Close figure
    plt.close(fig)