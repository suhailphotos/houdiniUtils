# houdiniUtils

This package provides a collection of utilities for Houdini, including tools for managing texture IDs and renaming textures based on specified patterns.

* [houdiniUtils](#houdiniUtils)
* [Package Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [License](#license)
* [FAQ](#faq)

## Package Description
* [houdiniUtils](#houdiniUtils)

This package includes tools to manage texture IDs and rename texture files based on specified patterns.

### Usage
* [houdiniUtils](#houdiniUtils)

#### In a Script
You can use the package in a script as follows:

```python
from houdiniutils.textureTools import tex_id_manager, renameTexture

# Initialize TextureIDManager
texid = tex_id_manager.TextureIDManager(config_file_path='path/to/textureID.json')

# Initialize RenameTexture with textureTypes and asset name
renObj = renameTexture.RenameTexture(textureTypes=texid.textureType, asset_name=texid.asset_name)
renObj.renameFolders()
```

### Installation
* [houdiniUtils](#houdiniUtils)

Install the package with:
```bash
pip install houdiniUtils
```

This will automatically copy the scripts to `~/suhailphotos/houdiniUtils`.

To complete the setup:
1. Copy the `houUtils.shelf` file to the `HOUDINI_USER_PREF_DIR/toolbar` directory.
2. Add the following line to your Houdini environment file (`houdini.env`):
   ```bash
   HOUDINI_PATH = ~/suhailphotos/houdiniUtils;&
   ```

To install from source and develop:
```
git clone https://github.com/suhailphotos/houdiniUtils.git
cd houdiniUtils
pip install wheel --upgrade
pip install -r requirements.txt --upgrade
python setup.py sdist bdist_wheel
python setup.py develop
```

### System Requirements
* [houdiniUtils](#houdiniUtils)

Must have Houdini installed. This package is compatible with Linux, macOS, and Windows.

## Testing
* [houdiniUtils](#houdiniUtils)

Run tests on install by doing:
```bash
pip install houdiniUtils --force --install-option test
```

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
```bash
python setup.py test
```

To test a specific submodule, cd into that submodule and run:
```bash
pytest
```

## Development/Contributing
* [houdiniUtils](#houdiniUtils)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## History
* [houdiniUtils](#houdiniUtils)
   * 0.1.0 - Initial commit

## Credits
* [houdiniUtils](#houdiniUtils)

Thanks to the Houdini community for the inspiration and resources.

## License
* [houdiniUtils](#houdiniUtils)

MIT License

## FAQ
* [houdiniUtils](#houdiniUtils)

Q: What is this package for?

A: This package provides utilities for managing textures and other assets in Houdini.
