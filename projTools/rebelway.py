import hou
import os, json


project_list = '/Users/suhail/Documents/houdini/python/config/proj_list.json'
try:
    with open(project_list, 'r') as f:
        data = json.load(f)
except ValueError:
    data={}

def fix_path(old_path, new_sep='/'):
    _path = old_path.replace('\\', new_sep)
    _path = _path.replace('\\\\', new_sep)
    _path = _path.replace('//', new_sep)
    if _path.endswith(new_sep):
        _path = _path[:-1]
    new_path = _path
    return new_path

def error(message, severity=hou.severityType.Error):
    print(f'{severity.name()}: {message}')
    hou.ui.displayMessage(message, severity=severity)



def add_proj():
    _proj_name = None
    path = None
    proj_name = None
    proj_code = None
    proj_fps = None


    repeat = True
    while repeat:
        repeat = False
        _path = hou.ui.selectFile(title='Select Project Directory', file_type=hou.fileType.Directory)
        path = os.path.dirname(_path)
        if path=='':
            return
        for k, v in data.items():
            if fix_path(path) == fix_path(v['PATH']):
                error(f'Project path is already used by project {k}\nPlease select a different path')
                repeat = True
                break
        if repeat:
            continue
        _proj_name = os.path.split(path)[-1]

    
    repeat = True
    while repeat:
        repeat = False
        inputs = hou.ui.readMultiInput(message='Enter Project Data', input_labels=('Project Name', 'Project Code', 'FPS'), 
                                    buttons=('OK', 'Cancel'), severity=hou.severityType.Message, initial_contents=(_proj_name, "", "25"))
        if inputs[0] == 1:
            return
        proj_name = inputs[1][0]
        proj_code = inputs[1][1]
        proj_fps = inputs[1][2]
        
        if proj_name == '' or proj_code == '' or proj_fps == '':
            error('Please fill in all fields')
            repeat = True
            continue

        try:
            proj_fps = int(proj_fps)
        except ValueError:
            error('FPS not set to a number.\nPlease enter an integer')
            repeat = True
            continue

        for k, v in data.items():
            if proj_name==k:
                error(f'Project name is already in use\nPlease select a different name')
                repeat = True
                break
            if proj_code==v['CODE']:
                error(f'Project code is already in use\nPlease select a different code')
                repeat = True
                break

        if repeat:
            continue

    if proj_name and proj_code and proj_fps:
        proj_data = {
            'CODE': proj_code,
            'PATH': path,
            'FPS': proj_fps
        }
        data[proj_name] = proj_data

    if data:
        with open(project_list, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)

            