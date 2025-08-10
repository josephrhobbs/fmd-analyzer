# Analysis Constants

# Twitch kinetics cutoff for first twitch
TK_CUTOFF = 800 # ms

# Twitch kinetics moving median filter kernel size
TK_KERNEL_SIZE = 15 # ms

# Twitch kinetics threshold for rise and decay
TK_FRAC = 0.1

# Twitch kinetics decay time buffer
TK_BUFFER = 10 # ms

# Maximum number of tissues per folder (T1, T2, ..., Tn)
MAX_TISSUE_COUNT = 10

# File and directory names
MAXFORCES        = "maxforces"
MAXFORCES_CSV    = "maxforces.csv"
OUTPUT_CSV       = "output.csv"
PLOTS            = "plots"
SPECIAL_DIRS     = [MAXFORCES, PLOTS]

# Force file extension
FORCE_EXT        = ".fmd"

# Vertical line colors
LINE_COLORS = [
    "red",
    "orange",
    "steelblue",
    "darkgreen",
]

# Output file header
OUTPUT_HEADER = [
    "Filename",
    "Baseline (mN)",
    "Maximum (mN)",
    "Active (mN)",
    "Passive (mN)",
    "Rise Time (ms)",
    "Decay Time (ms)",
    "Total Time (ms)",
]

# Baseline measurement indicator (found in filename)
BASELINE_INDICATOR = "L000"