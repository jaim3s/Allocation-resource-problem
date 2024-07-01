import os

current_directory = os.getcwd()
content_folder_path = current_directory + "\\content"
parameters_folder_path = current_directory + "\\parameters"

# Separation character
SEPARATION_CHAR = "="

# False and true value
TRUE_VALUES = [
    "true", 
    "1", 
    "yes", 
    "y", 
    "on"
]

FALSE_VALUES = [
    "false", 
    "0", 
    "no", 
    "n", 
    "off"
]

# Step size
STEP_SIZE = 1

# Mobility actions
MOBILITY_ACTIONS = [-1, 0, 1]

# Mobility models
MOBILITY_MODELS = [
    "brownian_motion",
]