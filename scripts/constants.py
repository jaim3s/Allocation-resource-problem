import os

current_directory = os.getcwd()
content_folder_path = current_directory + "\\content"
parameters_folder_path = current_directory + "\\parameters"

# Step size
STEP_SIZE = 1

# Mobility actions
MOBILITY_ACTIONS = [-1, 0, 1]

# Mobility models
MOBILITY_MODELS = [
    "brownian_motion",
]