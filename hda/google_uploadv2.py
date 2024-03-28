import os, sys
import time
import hou
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class FilePath:
    def __init__(self, node: hou.Node):
        self.node = node
        self.desk_dir = None
        self.file_path = None

    def _get_userid(self) -> str:
        user_id = hou.getenv('USER_ID')
        if not user_id:
            user_id = str(0).zfill(5)
        return user_id

    def set_path(self):
        file_parm = self.node.parm('file')
        default_path = file_parm.evalAsString()
        dest_dir = '/'.join(default_path.split('/')[:-1])
        self.dest_dir = dest_dir
        try:
            file_version = len([file for file in os.listdir(self.dest_dir) if file.endswith('bgeo.sc')])
        except:
            os.mkdir(self.dest_dir)
            file_version = len([file for file in os.listdir(self.dest_dir) if file.endswith('bgeo.sc')])
        user_id = self._get_userid()
        self.file_path = '/'.join([self.dest_dir, f'{hou.getenv("HIPNAME")}_{user_id}_asset_v{str(file_version).zfill(2)}.bgeo.sc']) 
        self.node.parm('file').set(self.file_path)

class GoogleCache:
    def __init__(self, node: hou.Node, folder_id: str, google_auth_config: str):
        self.node = node
        self.folder_id = folder_id
        self.google_auth_config = google_auth_config

    def _wait_for_file(self):
        while not os.path.exists(self.file_path):
            time.sleep(1)

    def upload_to_google(self):
        f1=FilePath(self.node)
        f1.set_path()
        self.node.parm('execute').pressButton()
        self._wait_for_file()
        gauth = GoogleAuth()
        gauth.settings['client_config_file'] = self.google_auth_config 
        gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication
        drive = GoogleDrive(gauth)
        upload_file_list = [self.file_path] 
        for upload_file in upload_file_list: 
            gfile = drive.CreateFile({'parents': [{'id': self.folder_id}]}) # Read file and set it as the content of this instance. 
            gfile.SetContentFile(upload_file) 
            gfile['title'] = os.path.basename(upload_file)
            gfile.Upload() # Upload the file.


