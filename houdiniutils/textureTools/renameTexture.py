import os
import re
import json
import hou

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
        start_directory = hou.getenv('HIP')
        title = 'Select root folder'
        file_type = hou.fileType.Directory
        sourceFolder = hou.ui.selectFile(start_directory=start_directory, title=title, file_type=file_type)
        self.sourceFolder = hou.text.expandString(sourceFolder) if sourceFolder else None

    def renameFolders(self):
        if not self.sourceFolder:
            print('No source folder selected. Operation cancelled.')
            return

        is_single_folder = all(os.path.isfile(os.path.join(self.sourceFolder, item)) for item in os.listdir(self.sourceFolder))
        if is_single_folder:
            self._rename_files_in_folder(self.sourceFolder)
        else:
            for root, dirs, files in os.walk(self.sourceFolder):
                if root == self.sourceFolder:
                    for subdir in dirs:
                        subdir_path = os.path.join(root, subdir)
                        self._rename_folder_and_files(subdir_path)
            # Rename the top-level folders
            self._rename_folder_and_files(self.sourceFolder)

    def _rename_folder_and_files(self, folder_path):
        parent_folder = os.path.dirname(folder_path)
        folder_name = os.path.basename(folder_path)
        new_folder_name = re.sub(r'[.\s-]', '_', folder_name)
        new_folder_path = os.path.join(parent_folder, new_folder_name)
        
        if folder_path != new_folder_path:
            os.rename(folder_path, new_folder_path)
            print(f"Renamed folder {folder_path} to {new_folder_path}")
            folder_path = new_folder_path
        
        self._rename_files_in_folder(folder_path, new_folder_name)

    def _rename_files_in_folder(self, folder_path, folder_name):
        rename_plan = {}  # Dictionary to plan renaming
        rename_log = []   # List to store old and new file names for JSON log

        # First pass: collect rename plan and count occurrences
        for file in os.listdir(folder_path):
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

                os.rename(old_file_path, new_file_path)
                print(f"Renamed {file_name + file_ext} to {new_file_name}")

        if self.old_file_name and rename_log:
            log_file_path = os.path.join(folder_path, f'{folder_name}_rename_log.json')
            with open(log_file_path, 'w') as log_file:
                json.dump(rename_log, log_file, indent=4)
            print(f"Rename log saved to {log_file_path}")

