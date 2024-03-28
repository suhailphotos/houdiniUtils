import sys, os, re
import datetime as dt
import json, csv
from configparser import ConfigParser
import hou
import pprint

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

    def update_metadata(self, metadata=None):
        if metadata:
            self.metadata = metadata
        if self.metadata:
            try:
                import xattr
                if self.source_proj_folder_path and self.source_proj_folder: 
                    full_proj_folder = '/'.join([self.source_proj_folder_path, self.source_proj_folder])
                    for k, v in self.metadata.items():
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
        else:
            print('Please provide metadata')

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

class MyJson:
    
    def __init__(self, data_list=None, file_path=None):
        self.data_list = data_list
        self.file_path = file_path
    
    def update_data_list(self, data_list):
        self.data_list = data_list

    
    def save_to_json(self):
        if self.data_list:
            try:
                with open(self.file_path, 'w') as json_file:
                    json.dump(self.data_list, json_file, indent=4)
            except Exception:
                self.data_list={}
    def load_from_json(self):
        try:
            with open(self.file_path, 'r') as json_file:
                self.data_list = json.load(json_file)
                return self.data_list
        except ValueError:
            self.data_list={}

class ProjConfig:

    def __init__(self, config_file_path, key):
        self.config_file_path = config_file_path
        self.key = key
        config = ConfigParser()
        config.read(self.config_file_path)
        self.json_path = config[key]['JSON_PATH']
        self.proj_path = config[key]['PROJECTS_PATH']


class Proj:
    def __init__(self, projnum=None, project_path=None, project_code=None, project_name=None, start_date=None, project_fps='25'):
        self.projnum = projnum
        self.project_path = project_path
        self.project_name = project_name
        self.project_code = project_code
        self.project_fps = project_fps
        self.start_date = start_date
        if not self.start_date:
            self.start_date = str(dt.date.today())

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            if self.project_path == other.project_path:
                return self.project_name == other.project_name and self.project_code == other.project_code
            else:
                return NotImplemented

    def __hash__(self):
        return hash(''.join([self.project_name, self.project_code]))

    def __repr__(self):
        return (f'<object with project_code: {self.project_code}, project_name: {self.project_name}, start_date: {self.start_date}')

    def isPresent(self, other):
        if isinstance(self, other.__class__):
            if self.project_path == other.project_path:
                return (self.project_name == other.project_name, self.project_code == other.project_code)
        else:
            return NotImplemented

class ProjManager:
    def __init__(self, config_path=None, key=None, json_path=None, project_path=None):
        self.projects = set()
        if json_path and project_path:
            self.json_path = json_path
            self.project_path = project_path
            self._load_projects()
        elif config_path and key:
            proj_config = ProjConfig(config_path, key)
            self.json_path = proj_config.json_path
            self.project_path = proj_config.proj_path
            self._load_projects()

    def _load_projects(self):
        proj_json = MyJson(file_path=self.json_path)
        data_list = proj_json.load_from_json()
        for data_item in data_list:
            proj_num = data_item['PROJNUM']
            project_path = data_item['PROJECT_PATH']
            project_code = data_item['PROJECT_CODE']
            project_name = data_item['PROJECT_NAME']
            start_date = data_item['PROJECT_START_DATE']
            project_fps = data_item['PROJECT_FPS']
            self.projects.add(Proj(proj_num, project_path, project_code, project_name, start_date, project_fps))

    def _convert_to_underscores(self, input_string):
        modified_string = re.sub(r'[-\s]', '_', input_string)
        return modified_string

    def _parse_foldername(self, folder):
        match = re.search(r'([^_]+)_(.+)', folder)
        if match:
            return (match.group(1), match.group(2))

    def _metadata_kwargs(self, projnum, project_path, project_code, project_name, start_date, project_fps):
        metadata = {
            'PROJNUM': projnum,
            'PROJECT_PATH': project_path,
            'PROJECT_CODE': project_code,
            'PROJECT_NAME': project_name,
            'PROJECT_START_DATE': start_date,
            'PROJECT_FPS': project_fps
            }
        return metadata

    def _set_hou_env(self, projnum, project_path, project_folder, project_code, project_name, start_date, project_fps):
        hou_env_var = {
                'PROJECT': project_name,
                'CODE': project_code,
                'PROJ_FPS': project_fps,
                'PROJECT_PATH': '/'.join([project_path, project_folder]),
                'SCENES_PATH': '/'.join([project_path, project_folder, project_name, 'scenes']),
                'HDA_PATH': '/'.join([project_path, project_folder, project_name, 'hda']),
                'SCRIPTS_PATH': '/'.join([project_path, project_folder, project_name, 'scripts']),
                'JOB': '/'.join([project_path, project_folder, project_name]),
                'HIP': '/'.join([project_path, project_folder, project_name, 'scenes'])
            }
        for key, value in hou_env_var.items():
            if key=='PROJ_FPS':
                hou.putenv(key, str(value))
                hou.setFps(int(value))
                continue
            elif key=='HDA_PATH':
                hou.putenv(key, value)
                # hda_paths = [value, ]
                # scan_path = hou.getenv('HOUDINI_OTLSCAN_PATH')
                # if scan_path:
                #     hda_paths += scan_path.split(';')
                # hda_paths = list(set(hda_paths))
                # hou.putenv('HOUDINI_OTLSCAN_PATH', ';'.join(hda_paths))
                # hou.hda.reloadAllFiles()
                continue
            elif key=='SCRIPTS_PATH':
                hou.putenv(key, value)
                sys_paths = set(sys.path)
                if value not in sys_paths:
                    sys.path.append(value)
                continue
            else:
                hou.putenv(key, value)

    def _user_proj_info(self, project_name, project_code, start_date, project_fps):
        repeat = True
        while repeat:
            repeat = False
            inputs = hou.ui.readMultiInput(message='Enter Project Data', input_labels=('Project Name', 'Project Code', 'Start Date', 'FPS'), 
                                        buttons=('OK', 'Cancel'), severity=hou.severityType.Message, initial_contents=(project_name, project_code, start_date, project_fps))
            if inputs[0] == 1:
                return
            project_name = inputs[1][0]
            project_code = inputs[1][1]
            start_date = inputs[1][2]
            project_fps = inputs[1][3]
            if project_name == '' or project_code == '' or project_fps == '':
                error('Please fill in all fields')
                repeat = True
                continue
            try:
                project_fps = int(project_fps)
            except ValueError:
                error('FPS not set to a number.\nPlease enter an integer')
                repeat = True
                continue
        return (project_name, project_code, start_date, project_fps)

    def _append_proj_json(self, new_proj):
        if new_proj not in self.projects:
            self.projects.add(new_proj)
            projects = list(self.projects)
            projects = sorted(projects, key=lambda proj : proj.projnum)
            project_list = [
                    {
                        'PROJNUM': project.projnum,
                        'PROJECT_NAME': project.project_name,
                        'PROJECT_CODE': project.project_code,
                        'PROJECT_PATH': project.project_path,
                        'PROJECT_FPS': project.project_fps,
                        'PROJECT_START_DATE': project.start_date
                }
                    for project in projects
            ]
            proj_json = MyJson(file_path=self.json_path, data_list=project_list)
            proj_json.save_to_json()
            return True
        else:
            print('Project already in the database')
            return

    def addProj(self):
        repeat = True
        while repeat:
            repeat = False
            hou_path = hou.ui.selectFile(title='Select Project Directory', file_type=hou.fileType.Directory)
            if hou_path == '':
                return
            hou_path = hou.text.expandString(hou_path)
            currentPath = PathTool(hou_path)
            if repeat:
                continue
        proj_tuple = self._parse_foldername(currentPath.folder)
        project_code = proj_tuple[0]
        project_name = proj_tuple[1]
        start_date = str(dt.date.today())
        project_fps = '25'
        project_info = self._user_proj_info(project_name, project_code, start_date, project_fps)
        if project_info:
            project_name = project_info[0]
            project_code = project_info[1]
            start_date = project_info[2]
            project_fps = project_info[3]
            projnum = len(self.projects)+1
            project_path = currentPath.root_path
            new_proj = Proj(projnum, project_path, project_code, project_name, start_date, project_fps)
            json_bol = self._append_proj_json(new_proj)
            if json_bol:
                metadata = self._metadata_kwargs(projnum, project_path, project_code, project_name, start_date, project_fps)
                new_folder = Folder(currentPath.root_path, currentPath.folder, metadata)
                new_folder.update_metadata()
        else:
            return

    def create_proj(self, source_csv_path):
        projnum = len(self.projects)+1
        project_name = 'project name...'
        project_code = str(projnum).zfill(2)
        start_date = str(dt.date.today())
        project_fps = '25'
        project_info = self._user_proj_info(project_name, project_code, start_date, project_fps)
        if project_info:
            project_name = self._convert_to_underscores(project_info[0])
            project_code = project_info[1]
            start_date = project_info[2]
            project_fps = project_info[3]
            project_path = self.project_path
            metadata = self._metadata_kwargs(projnum, project_path, project_code, project_name, start_date, project_fps)
            project_folder = '_'.join([str(projnum).zfill(2), self._convert_to_underscores(project_name)])
            project_folder_obj = Folder(project_path, project_folder, metadata)
            new_proj = Proj(projnum, project_path, project_code, project_name, start_date, project_fps)
            json_bolean = self._append_proj_json(new_proj)
            if json_bolean:
                project_folder_obj.create_proj_folder(project_name, source_csv_path)
                project_folder_obj.update_metadata()
                self._set_hou_env(projnum, project_path, project_folder, project_code, project_name, start_date, project_fps)
        else:
            return
        
if __name__ == '__main__':
    course_projs = ProjManager('/Users/suhail/Documents/PyHub/config/config.ini', 'courses')
    pprint.pprint(course_projs.projects)

