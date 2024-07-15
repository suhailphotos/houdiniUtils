import hou
import sys

# List of environment variables to check
var_list = ['JOB', 'POSE', 'SHOTS', 'ASSETS']

# Folder lookup dictionary for different platforms
folder_lookup = {
    'DROPBOX': {
        'darwin': '/Users/suhail/Library/CloudStorage/Dropbox',
        'Windows': 'C:/Users/Shadow/Dropbox'
    },
    'USD_LIB': {
        'darwin': '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/usd',
        'Windows': 'C:/Users/Shadow/Dropbox/threeD/lib/usd'
    },
    'COURSES': {
        'darwin': '/Users/suhail/Library/CloudStorage/Dropbox/threeD/courses',
        'Windows': 'C:/Users/Shadow/Dropbox/threeD/courses'
    },
    'PROJECTS': {
        'darwin': '/Users/suhail/Library/CloudStorage/Dropbox/threeD/projects',
        'Windows': 'C:/Users/Shadow/Dropbox/threeD/projects'
    }
}

# Function to update environment variables
def update_environment_variables():
    current_platform = 'darwin' if sys.platform == 'darwin' else 'Windows'
    other_platform = 'Windows' if current_platform == 'darwin' else 'darwin'

    for var in var_list:
        current_value = hou.getenv(var)
        if current_value:
            for key, paths in folder_lookup.items():
                if paths[other_platform] in current_value:
                    new_value = current_value.replace(paths[other_platform], paths[current_platform])
                    hou.putenv(var, new_value)
                    break

