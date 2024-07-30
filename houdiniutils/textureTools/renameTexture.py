import os
import re
import hou

class RenameTexture:
    def __init__(self, sourceFolder: str = None, old_file_name: bool = True, **kwargs):
        self.old_file_name = old_file_name
        if not sourceFolder:
            self._get_source_folder()
        else:
            self.sourceFolder = sourceFolder
        self.textureTypes = kwargs.get('textureTypes', {})

    def _get_source_folder(self):
        start_directory = hou.getenv('HIP')
        title = 'Select root folder'
        file_type = hou.fileType.Directory
        sourceFolder = hou.ui.selectFile(start_directory=start_directory, title=title, file_type=file_type)
        self.sourceFolder = hou.text.expandString(sourceFolder)


