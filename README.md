
# houdiniUtils

This package provides a collection of utilities for Houdini, including tools for managing texture IDs and renaming textures based on specified patterns.

## Installation

Install the package with:
```bash
pip install houdiniutils
```

## Setup

1. **Download the Houdini Shelf Tool**:
   Download the `houUtils.shelf` file from [this link](https://github.com/suhailphotos/houdiniUtils/blob/36c5893a1dcd1949c12b66942708bc425d1d993b/houdiniutils/textureTools/houdiniUtils.shelf).

2. **Copy the Houdini Shelf Tool**:
   Copy the downloaded `houdiniUtils.shelf` file to the `HOUDINI_USER_PREF_DIR/toolbar` directory. The `HOUDINI_USER_PREF_DIR` is typically located in your home directory under `houdiniX.Y` (e.g., `~/houdini20.5`).

```powershell
cp <your_downloads_folder>/houUtils.shelf $HOUDINI_USER_PREF_DIR/toolbar/
```

3. **Create the `houdiniUtils.json` File**:

   Run the following Python command to determine the site-packages path and create the `houdiniUtils.json` file:

```powershell
python -c "import site, json; path = [p.replace('\\', '/') for p in site.getsitepackages() if 'site-packages' in p][0]; config = {'env': [{'PYTHONPATH': [path]}]}; with open('houdiniUtils.json', 'w') as f: json.dump(config, f, indent=4)"
```

   This command does the following:
   - Imports necessary modules.
   - Finds and formats the site-packages path.
   - Creates a JSON configuration with the `PYTHONPATH` set to the site-packages path.
   - Writes the configuration to a `houdiniUtils.json` file.

4. **Copy the `houdiniUtils.json` File**:

   Copy the generated `houdiniUtils.json` file to the `packages` folder in your Houdini user preferences directory:

```powershell
cp houdiniUtils.json $HOUDINI_USER_PREF_DIR/packages/
```

By following these steps, you will have set up the `houdiniUtils` package and configured the necessary environment variables for Houdini.
