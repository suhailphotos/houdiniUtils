#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Suhail"
__credits__ = ["Suhail"]
__Lisence__ = "MIT"
__maintainer__ = "Suhail"
__email__ = "suhahilece@gmail.com"
__status__ = "Development"
__version__ = "0.1.4"

"""
renameTexture.py
----------------
This module contains the RenameTexture class for renaming texture files based on specified patterns.

Author: Suhail
License: MIT
"""

# Default python packages

import os
import re
import json
import logging
import platform

# Configure logging
logging.basicConfig(level=logging.INFO)

class RenameTexture:
    def __init__(self, sourceFolder: str = None, old_file_name: bool = True, asset_name: str = None, **kwargs):
        self.old_file_name = old_file_name
        self.asset_name = asset_name
        if not sourceFolder:
            self._get_source_folder()
        else:
            self.sourceFolder = sourceFolder
        self.textureTypes = kwargs.get('textureTypes', {})

    def _get_source_folder(self):
        import hou
        start_directory = hou.getenv('HIP')
        title = 'Select root folder'
        file_type = hou.fileType.Directory
        sourceFolder = hou.ui.selectFile(start_directory=start_directory, title=title, file_type=file_type)
        self.sourceFolder = hou.text.expandString(sourceFolder) if sourceFolder else None

    def renameFolders(self):
        if not self.sourceFolder:
            logging.info('No source folder selected. Operation cancelled.')
            return

        try:
            is_single_folder = all(
                os.path.isfile(os.path.join(self.sourceFolder, item)) and not self._is_hidden_or_system_file(os.path.join(self.sourceFolder, item))
                for item in os.listdir(self.sourceFolder)
            )
            if is_single_folder:
                folder_name = os.path.basename(self.sourceFolder)
                logging.info(f"Renaming files in single folder: {self.sourceFolder}, folder name: {folder_name}")
                self._rename_files_in_folder(self.sourceFolder, folder_name)
            else:
                for root, dirs, files in os.walk(self.sourceFolder):
                    # Filter out hidden and system files and directories
                    dirs[:] = [d for d in dirs if not self._is_hidden_or_system_file(os.path.join(root, d))]
                    files[:] = [f for f in files if not self._is_hidden_or_system_file(os.path.join(root, f))]
                    
                    if root == self.sourceFolder:
                        for subdir in dirs:
                            subdir_path = os.path.join(root, subdir)
                            self._rename_folder_and_files(subdir_path)
        except Exception as e:
            logging.error(f"Error during renaming folders: {e}")

    def _is_hidden_or_system_file(self, file_path):
        if platform.system() == 'Windows':
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            FILE_ATTRIBUTE_SYSTEM = 0x04
            attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
            if attrs == -1:
                return False
            return bool(attrs & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM))
        else:
            return os.path.basename(file_path).startswith('.')

    def _rename_folder_and_files(self, folder_path):
        parent_folder = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        new_folder_name = re.sub(r'[.\s\-\(\)\+]', '_', folder_name)
        new_folder_name = re.sub(r'__+', '_', new_folder_name)
        logging.info(f"Processing folder: {folder_path}, new folder name: {new_folder_name}")
        if not new_folder_name:
            logging.error(f"New folder name is empty for folder: {folder_path}")
            return

        new_folder_path = os.path.join(parent_folder, new_folder_name)
        
        try:
            if folder_path != new_folder_path:
                os.rename(folder_path, new_folder_path)
                logging.info(f"Renamed folder {folder_path} to {new_folder_path}")
                folder_path = new_folder_path
        except PermissionError:
            logging.error(f"Permission denied while renaming folder {folder_path} to {new_folder_path}")
            return
        except Exception as e:
            logging.error(f"Error renaming folder {folder_path} to {new_folder_path}: {e}")
            return
        
        self._rename_files_in_folder(folder_path, new_folder_name)

    def _rename_files_in_folder(self, folder_path, folder_name):
        rename_plan = {}  # Dictionary to plan renaming
        rename_log = []   # List to store old and new file names for JSON log

        try:
            # First pass: collect rename plan and count occurrences
            for file in os.listdir(folder_path):
                if self._is_hidden_or_system_file(os.path.join(folder_path, file)):
                    continue  # Skip hidden and system files
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    file_name, file_ext = os.path.splitext(file)
                    for key, data in self.textureTypes.items():
                        patterns = [pattern.strip() for pattern in data['pattern'].split(',')]
                        regex_patterns = [pattern.replace('*', '.*') for pattern in patterns]
                        regex_pattern = '|'.join(regex_patterns)
                        if re.search(regex_pattern, file_name, re.IGNORECASE):
                            new_file_base = f'{self.asset_name}_{folder_name}_{key}' if self.asset_name else f'{folder_name}_{key}'
                            if new_file_base not in rename_plan:
                                rename_plan[new_file_base] = []
                            rename_plan[new_file_base].append((file_name, file_ext))
                            break

            # Second pass: rename files according to the plan
            for new_file_base, files in rename_plan.items():
                count = len(files)
                for index, (file_name, file_ext) in enumerate(files):
                    old_file_path = os.path.join(folder_path, file_name + file_ext)
                    if count > 1:
                        new_file_name = f'{new_file_base}{index + 1}{file_ext}'
                    else:
                        new_file_name = f'{new_file_base}{file_ext}'
                    new_file_path = os.path.join(folder_path, new_file_name)
                    
                    if self.old_file_name:
                        rename_log.append({"old_name": file_name + file_ext, "new_name": new_file_name})

                    try:
                        os.rename(old_file_path, new_file_path)
                        logging.info(f"Renamed {file_name + file_ext} to {new_file_name}")
                    except PermissionError:
                        logging.error(f"Permission denied while renaming file {old_file_path} to {new_file_path}")
                    except Exception as e:
                        logging.error(f"Error renaming file {old_file_path} to {new_file_path}: {e}")

            if self.old_file_name and rename_log:
                log_file_path = os.path.join(folder_path, f'{folder_name}_rename_log.json')
                try:
                    with open(log_file_path, 'w') as log_file:
                        json.dump(rename_log, log_file, indent=4)
                    logging.info(f"Rename log saved to {log_file_path}")
                except PermissionError:
                    logging.error(f"Permission denied while saving rename log to {log_file_path}")
                except Exception as e:
                    logging.error(f"Error saving rename log to {log_file_path}: {e}")

        except PermissionError:
            logging.error(f"Permission denied while accessing folder {folder_path}")
        except Exception as e:
            logging.error(f"Error during renaming files in folder {folder_path}: {e}")
