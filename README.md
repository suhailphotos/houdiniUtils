
# houdiniUtils

This package provides a collection of utilities for Houdini, including tools for managing texture IDs and renaming textures based on specified patterns.

## Installation

### 1. Ensure Python is Installed

Before installing the `houdiniUtils` package, make sure Python is installed on your system. You can check this by running the following command in your terminal (macOS) or PowerShell (Windows):

```bash
python --version
```

or

```bash
python3 --version
```

If Python is not installed, you can download and install it from the official [Python website](https://www.python.org/downloads/).

### 2. Install the Package

You can install the `houdiniUtils` package either globally or within a virtual environment. However, we recommend using a virtual environment to avoid any potential conflicts, especially since Houdini 20.5.XXX uses Python 3.11.7.

#### 2.1 Using a Virtual Environment

To create and activate a virtual environment, follow the instructions provided in the [Python documentation on venv](https://docs.python.org/3/library/venv.html).

After activating your virtual environment, you can install the package by running:

```bash
pip install houdiniutils
```

### 3. Run the Post-Installation Script

Once the package is installed, you need to generate and copy `houdiniUtils.shelf` to the toolbar directory and `houdiniUtils.json` to the packages directory within your Houdini user preferences directory. This can be done by running the following post-installation command:

```bash
houdiniutils_post_install
```

This command will automatically detect your Houdini user preferences directory, create the necessary files, and place them in the appropriate locations.

By following these steps, you will have successfully set up the `houdiniUtils` package and configured the necessary environment variables for Houdini.
