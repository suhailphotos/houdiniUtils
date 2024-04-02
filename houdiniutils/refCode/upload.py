from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

upload_file_list = ['1.jpg', '2.jpg'] 
for upload_file in upload_file_list: 
    gfile = drive.CreateFile({'parents': [{'id': '1yvjPUUxKS1RAhBKCesF8SdY1KlwwHLp-'}]}) # Read file and set it as the content of this instance. 
    gfile.SetContentFile(upload_file) 
    gfile.Upload() # Upload the file.

