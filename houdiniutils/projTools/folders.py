import os, re
import csv

class PathTool:
    def __init__(self, full_path=None, root_path=None, folder=None, file=None):
        if full_path:
            self.full_path = self._fix_path(full_path)
            if os.path.isdir(self.full_path):
                self.root_path = os.path.dirname(self.full_path)
                self.folder = os.path.basename(self.full_path)
                self.file = None
            elif os.path.isfile(self.full_path):
                self.file = os.path.basename(self.full_path)
                self.root_path = os.path.dirname(self.full_path)
                self.folder = os.path.basename(self.root_path)
        elif root_path and folder:
                self.root_path = self._fix_path(root_path)
                self.folder = folder
                if file:
                    self.file = file
                    self.full_path = '/'.join([self.root_path, self.folder, self.file])
                else:
                    self.full_path = '/'.join([self.root_path, self.folder])
                    self.file = None

    def _fix_path(self, old_path, new_sep='/'):
        _path = old_path.replace('\\', new_sep)
        _path = _path.replace('\\\\', new_sep)
        _path = _path.replace('//', new_sep)
        if _path.endswith(new_sep):
            _path = _path[:-1]
        new_path = _path
        return new_path



class Folder:

    def __init__(self, source_proj_folder_path=None, source_proj_folder=None, metadata=None):
        self.source_proj_folder_path = source_proj_folder_path
        self.source_proj_folder = source_proj_folder
        self.metadata = metadata

    def set_proj_folder(self, source_proj_folder):
        self.source_proj_folder = source_proj_folder

    def set_proj_path(self, source_proj_folder_path):
        self.source_proj_folder_path = source_proj_folder_path

    def update_metadata(self, metadata):
        self.metadata = metadata
        try:
            import xattr
            if self.source_proj_folder_path and self.source_proj_folder: 
                full_proj_folder = '/'.join([self.source_proj_folder_path, self.source_proj_folder])
                for k, v in metadata.items():
                    try:
                        key_bytes = k.encode('utf-8')
                        value_bytes = str(v).encode('utf-8')
                        xattr.setxattr(full_proj_folder, key_bytes, value_bytes)
                    except Exception as e:
                        print(f'Error setting custom metadata: {e}')
            else:
                print(f'Source folder and\/or path is not set')
        except ImportError:
            print(f'xattr module is not available')

    def _get_folder_list(self, source_csv_path):
        c1_index = 0
        c2_index = 1
        c1_data = []
        c2_data = []
        with open(source_csv_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader, None)
            for row in csv_reader:
                if len(row)>c1_index and len(row)>c2_index:
                    v1 = row[c1_index].strip()
                    v2 = row[c2_index].strip()
                    if v1!='':
                        c1_data.append(v1)
                    if v2!='':
                        c2_data.append(v2)
        return (c1_data, c2_data)

    def create_proj_folder(self, proj_name, source_csv_path):
        full_proj_folder = '/'.join([self.source_proj_folder_path, self.source_proj_folder])
        folder_list = self._get_folder_list(source_csv_path)
        if not os.path.exists(full_proj_folder):
            os.mkdir(full_proj_folder)
            full_proj_folder_deep = '/'.join([full_proj_folder, proj_name]) 
            os.mkdir(full_proj_folder_deep)
            for folder in folder_list[0]:
                os.mkdir('/'.join([full_proj_folder, folder]))
            for folder in folder_list[1]:
                os.mkdir('/'.join([full_proj_folder_deep, folder]))

    def read_metadata(self):
        if self.source_proj_folder_path and self.source_proj_folder:
            full_proj_folder = '/'.join([self.source_proj_folder_path, self.source_proj_folder])
            try:
                import xattr
                try:
                    metadata_keys = ['PROJNUM', 'PROJECT_NAME', 'PROJECT_CODE', 'PROJECT_PATH', 'PROJECT_FPS', 'PROJECT_START_DATE']
                    self.metadata = {k:xattr.getxattr(full_proj_folder, k).decode('utf-8') for k in metadata_keys}
                    return self.metadata
                except FileNotFoundError:
                    print(f'folder not found')
                except Exception as e:
                    print(f'Error reading extended attributes: {e}')
            except ImportError:
                print(f'xattr module is not available')


if __name__ == '__main__':
    # desktop_folder = Folder('/Users/suhail/Desktop/python_test_folder', '01_test_proj')
    # desktop_folder.create_proj_folder('test_proj', '/Users/suhail/Documents/PyHub/csvFiles/prof_folders.csv')
    # metadata = {
    #     'PROJNUM': 1,
    #     'PROJECT_NAME': '01_test_proj',
    #     'PROJECT_CODE': '01',
    #     'PROJECT_PATH': '/users/documets/etc/',
    #     'PROJECT_FPS': '25',
    #     'PROJECT_START_DATE': '2024-02-02'
    # }
    # desktop_folder.update_metadata(metadata)
    # print(desktop_folder.read_metadata())
    myPath = '\\Users\\suhail\\Desktop\\python_test_folder\\01_test_proj'
    desktop_dir = PathTool(myPath)
    print(desktop_dir.root_path)
