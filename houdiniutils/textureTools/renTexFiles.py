import os
import re
import json
import hou

class RenameTexture:
    def __init__(self, sourceFolder: str = None, config_file: str = 'textureID.json', config_file_path: str = None):
        if config_file_path:
            self.config_file = os.path.join(config_file_path, config_file)
        else:
            self.config_file = config_file
        self.textureType = self._load_texture_types()
        if not sourceFolder:
            self._get_source_folder()
        else:
            self.sourceFolder = sourceFolder
        self._get_texture_types()
        
    def _load_texture_types(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)
        
    def _get_source_folder(self):
        start_directory = hou.getenv('HIP')
        title = 'Select root folder'
        file_type = hou.fileType.Directory
        sourceFolder = hou.ui.selectFile(start_directory=start_directory, title=title, file_type=file_type)
        self.sourceFolder = hou.text.expandString(sourceFolder)

    def _get_texture_types(self):
        message = 'Set Texture ID names. No Spaces Allowed!'
        input_labels = ["Asset Name:"] + [f"{data['label']}:" for data in self.textureType.values()]
        initial_contents = [''] + [f"{data['value']}" for data in self.textureType.values()]

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
            updated = False
            for idx, key in enumerate(self.textureType.keys()):
                new_value = user_input_values[idx + 1]  # +1 to skip 'Asset Name'
                if self.textureType[key]['value'] != new_value:
                    self.textureType[key]['value'] = new_value
                    updated = True

            if updated:
                self._save_texture_types()
    def _save_texture_types(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.textureType, f, indent=4)


