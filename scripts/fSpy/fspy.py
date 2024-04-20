import hou
import math, os, json, re

def frac(num, denom):
    if denom == 0:
        raise ValueError("Denominator cannot be zero.")
    com_div = math.gcd(num, denom)
    sim_num = num // com_div
    sim_den = denom // com_div
    return (sim_num, sim_den)

class fSpy:
    
    def __init__(self):
        self.json_data = {}
        self.cam_data = {}
        self.json_path = ''
        self.image_path = ''
        self.sensor_size = (36, 24)
        self.cam_type = 0
        self.obj_cam = None
        self.stage_cam = None
    
    def get_json(self, title='Select file', file_type=hou.fileType.Any):
        file_path = hou.ui.selectFile(title=title, file_type=file_type)
        if file_path:
            self.json_path = hou.text.expandString(file_path)
            return self.json_path
        else:
            return False

    def get_image(self, title='Select image file', file_type=hou.fileType.Image):
        file_path = hou.ui.selectFile(title=title, file_type=file_type)
        self.image_path = hou.text.expandString(file_path)
    
    def get_cam_inputs(self):
        default_sensor_size = ('36', '24')
        repeat = True
        while repeat:
            repeat = False
            inputs = hou.ui.readMultiInput(message='Camera Info', input_labels=('Sensor Width', 'Sensor Height'), 
                                        buttons=('obj', 'stage', 'both'), initial_contents=default_sensor_size)
            
            if inputs[1][0]=='' or inputs[1][1]=='':
                repeat = True
                continue
            self.sensor_size = (int(inputs[1][0]), int(inputs[1][1]))
            self.cam_type = inputs[0]
        
    def get_fspy_data(self):
        with open(self.json_path, 'r') as file:
            self.json_data = json.load(file)
        match = re.search(r'\/([^\/]+)\.[^\/]+$', self.json_path)
        cam_name = f'{match.group(1)}_fspy'
        rel_focal = self.json_data['relativeFocalLength']
        focal_len = self.sensor_size[0]*rel_focal/2
        res_x = self.json_data['imageWidth']
        res_y = self.json_data['imageHeight']
        res = (res_x, res_y)
        aspect_ratio = frac(res_x, res_y)
        if res_x<res_y:
            aperture = self.sensor_size[1]
        else:
            aperture = self.sensor_size[0]
        h_fov_cal = 2*math.atan(aperture/(2*focal_len))
        cam_xform = hou.Matrix4(self.json_data['cameraTransform']['rows']).transposed()
        pivot = hou.Vector3(0.0, 0.0, 0.0)
        trans = cam_xform.extractTranslates('srt', pivot, pivot)
        rot = cam_xform.extractRotates('srt', 'xyz', pivot, pivot)
        self.cam_data = {
            'camera_name': cam_name,
            'focal_length': focal_len, 
            'aperture':  aperture, 
            'translation': trans, 
            'rotation': rot, 
            'res': res, 
            'aspect_ratio': aspect_ratio
        }

    def create_fspy_cam(self):
        if self.cam_type == 0:
            self.obj_cam = fSpy_Cam(self.image_path, self.cam_data, hou.node('obj'), locked=True)
            return self.obj_cam
        elif self.cam_type == 1:
            self.stage_cam = fSpy_Cam(self.image_path, self.cam_data, hou.node('stage'), locked=True)
            return self.stage_cam
        elif self.cam_type == 2:
            self.obj_cam = fSpy_Cam(self.image_path, self.cam_data, hou.node('obj'), locked=True) 
            self.stage_cam = fSpy_Cam(self.image_path, self.cam_data, hou.node('stage'), locked=True)
            return (self.obj_cam, self.stage_cam)

class fSpy_Cam:
    camera_data = {
        'camera_name': 'cam',
        'focal_length': 50.0,
        'aperture':  41.4214,
        'translation': (0.0, 0.0, 0.0),
        'rotation': (0.0, 0.0, 0.0),
        'res': (1280, 720),
        'aspect_ratio': (16, 9)
    }
    def __init__(self, image_path='', cam_data=camera_data, context=hou.node('/obj/'), locked=False):
        self.cam_data = cam_data
        self.context = context
        self.image_path = image_path
        if self.context.type().name()=='obj':
            cam = self.context.createNode('cam', self.cam_data['camera_name'])
            cam.parmTuple('t').set(self.cam_data['translation'])
            cam.parmTuple('r').set(self.cam_data['rotation'])
            cam.parmTuple('res').set(self.cam_data['res'])
            cam.parm('focal').set(self.cam_data['focal_length'])
            cam.parm('aperture').set(self.cam_data['aperture'])
            if not self.image_path=='':
                bg_image_collapse = hou.text.collapseCommonVars(self.image_path, vars=['$HIP', '$JOB'])
                cam.parm('vm_background').set(bg_image_collapse)
            if locked:
                for cam_parms in cam.parms():
                    if cam_parms.parmTemplate().type()==hou.parmTemplateType.Folder or cam_parms.parmTemplate().type()==hou.parmTemplateType.FolderSet:
                        continue
                    if cam_parms.name()=='vm_bgenable' or cam_parms.name()=='vm_background':
                        continue
                    cam_parms.lock(True)
        elif self.context.type().name()=='stage':
            cam = self.context.createNode('camera', self.cam_data['camera_name'])
            cam.parmTuple('t').set(self.cam_data['translation'])
            cam.parmTuple('r').set(self.cam_data['rotation'])
            cam.parmTuple('aspectratio').set(self.cam_data['aspect_ratio'])
            cam.parm('focalLength').set(self.cam_data['focal_length'])
            cam.parm('horizontalAperture').set(self.cam_data['aperture'])
            bg_image_cntrl = hou.text.encode('houdini:backgroundimage_control')
            bg_image_parm = hou.text.encode('houdini:backgroundimage')
            fg_image_cntrl = hou.text.encode('houdini:foregroundimage_control')
            fg_image_parm = hou.text.encode('houdini:foregroundimage')
            if not self.image_path=="":
                bg_image_collapse = hou.text.collapseCommonVars(self.image_path, vars=['$HIP', '$JOB'])
                cam.parm(bg_image_parm).set(bg_image_collapse)
            # Parm unlock list
            parm_unlock_list = []
            parm_unlock_list.append(bg_image_cntrl)
            parm_unlock_list.append(bg_image_parm)
            parm_unlock_list.append(fg_image_cntrl)
            parm_unlock_list.append(fg_image_parm)
            parm_unlock_list.append('focusDistance_control')
            parm_unlock_list.append('focusDistance')
            parm_unlock_list.append('fStop_control')
            parm_unlock_list.append('fStop')
            parm_unlock_list.append('exposure_control')
            parm_unlock_list.append('exposure')
            parm_unlock_list.append('primpath')
            if locked:
                for cam_parms in cam.parms():
                    if cam_parms.parmTemplate().type()==hou.parmTemplateType.Folder or cam_parms.parmTemplate().type()==hou.parmTemplateType.FolderSet:
                        continue
                    if cam_parms.name() in parm_unlock_list:
                        continue
                    cam_parms.lock(True)



