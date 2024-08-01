#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Suhail"
__credits__ = ["Suhail"]
__Lisence__ = "MIT"
__maintainer__ = "Suhail"
__email__ = "suhahilece@gmail.com"
__status__ = "Development"
__version__ = "0.1.0"

"""
main.py
-------
Main entry point for the texture renaming utility.

Author: Suhail
License: MIT
"""

# Default python packages

import os
from houdiniutils.textureTools import tex_id_manager, renameTexture

def main():
    # Set the config file path
    config_file_path = os.path.dirname(__file__)

    # Initialize TextureIDManager
    texid = tex_id_manager.TextureIDManager(config_file_path=config_file_path)

    # Initialize RenameTexture with textureTypes and asset name
    renObj = renameTexture.RenameTexture(textureTypes=texid.textureType, asset_name=texid.asset_name)
    renObj.renameFolders()

if __name__ == "__main__":
    main()
