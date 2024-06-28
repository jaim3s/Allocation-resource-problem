import os

current_directory = os.getcwd()
content_folder_path = current_directory + "\\content"
parameters_folder_path = current_directory + "\\parameters"

# Mobility models
MOBILITY_MODELS = [
    "brownian_motion",
]