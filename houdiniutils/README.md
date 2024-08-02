# houdiniUtils

This package provides a collection of utilities for Houdini, including tools for managing texture IDs and renaming textures based on specified patterns.

## Installation

Install the package with:
```bash
pip install houdiniUtils
```

## Setup

1. **Download the Houdini Shelf Tool**:
   Download the `houUtils.shelf` file from [this link](path/to/houUtils.shelf).

2. **Copy the Houdini Shelf Tool**:
   Copy the downloaded `houUtils.shelf` file to the `HOUDINI_USER_PREF_DIR/toolbar` directory. The `HOUDINI_USER_PREF_DIR` is typically located in your home directory under `houdiniX.Y` (e.g., `~/houdini19.5`).

   ```bash
   cp path/to/downloaded/houUtils.shelf $HOUDINI_USER_PREF_DIR/toolbar/
   ```

3. **Update the Houdini Environment File**:
   Add the following line to your Houdini environment file (`houdini.env`). This file is usually located in the same directory as `HOUDINI_USER_PREF_DIR`.

   Replace `<site-packages-path>` with the actual path where the `site-packages` directory is located on your system.

   ```bash
   HOUDINI_PATH = <site-packages-path>/houdiniutils;&
   ```

   To find the `site-packages` path, you can use the following Python command:
   ```bash
   python -c "import site; print(site.getsitepackages())"
   ```

   This will output the path(s) to the `site-packages` directory. Use the appropriate path from the output.

## Usage

### In a Script

You can use the package in a script as follows:

```python
from houdiniutils.textureTools import tex_id_manager, renameTexture

# Initialize TextureIDManager
texid = tex_id_manager.TextureIDManager(config_file_path='path/to/config/folder')

# Initialize RenameTexture with textureTypes and asset name
renObj = renameTexture.RenameTexture(textureTypes=texid.textureType, asset_name=texid.asset_name)
renObj.renameFolders()
```

## License

MIT License
