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
tex_id_manager.py
-----------------
This module contains the TextureIDManager class for managing texture ID patterns.

Author: Suhail
License: MIT
"""

# Default python packages


import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class TextureIDManager:
    def __init__(self, config_file: str = 'textureID.json', config_file_path: str = None):
        if config_file_path:
            self.config_file = os.path.join(config_file_path, config_file)
        else:
            self.config_file = os.path.join(os.getcwd(), config_file)
        
        self.textureType = self._load_texture_types()
        self.asset_name = ''
        self._get_texture_types()
        
    def _load_texture_types(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file {self.config_file} not found.")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from configuration file {self.config_file}.")
            return {}

    def _get_texture_types(self):
        import hou
        message = 'Set Texture ID names. No Spaces Allowed!'
        input_labels = ["Asset Name:"] + [f"{data['label']}:" for data in self.textureType.values()]
        initial_contents = [''] + [f"{data['pattern']}" for data in self.textureType.values()]

        input_labels = tuple(input_labels)
        initial_contents = tuple(initial_contents)

        title = 'Set Texture ID names'
        buttons = ('OK', 'Cancel')
        default_choice = 0
        close_choice = 1
        
        user_input_button, user_input_values = hou.ui.readMultiInput(
            message=message,
            input_labels=input_labels,
            initial_contents=initial_contents,
            title=title,
            buttons=buttons,
            default_choice=default_choice,
            close_choice=close_choice
        )

        self.user_input_button = user_input_button
        self.user_input_values = user_input_values

        if user_input_button == default_choice:
            self.asset_name = user_input_values[0]  # Asset Name is the first input
            updated = False
            for idx, key in enumerate(self.textureType.keys()):
                new_value = user_input_values[idx + 1]  # +1 to skip 'Asset Name'
                if self.textureType[key]['pattern'] != new_value:
                    self.textureType[key]['pattern'] = new_value
                    updated = True
            if updated:
                self._save_texture_types()

    def _save_texture_types(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.textureType, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving configuration to {self.config_file}: {e}")
