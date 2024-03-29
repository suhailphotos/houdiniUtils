'''
## Running the Tool in Houdini

To use the fSpy tool in Houdini, follow these steps:

1. **Create a New Shelf Tool:**
   - Open Houdini and create a new shelf tool.
   - Give it a descriptive name such as 'fspy import.'

2. **Copy Script Contents:**
   - Open the newly created shelf tool.
   - Navigate to the 'Scripts' tab.
   - Copy the contents of the `shelf_hou.py` file into the script editor.

3. **Download fSpy Branch from GitHub:**
   - Download the fSpy branch from [GitHub](https://github.com/suhailphotos/houdiniUtils/tree/fSpy) to your desired location.

4. **Set Python Path:**
   - Add the path to the fSpy branch to Houdini's Python path.
   - This can be accomplished in two ways:
     - **houdini.env:** Add the path to the `houdini.env` file. For example:
       ```
       PYTHONPATH = $PYTHONPATH;YOUR_PATH_TO_FSPY_BRANCH
       ```
     - **Houdini Packages:** Alternatively, use Houdini packages to manage Python paths.

Now, the 'fspy import' tool on your shelf should be ready to use for importing cameras using fSpy in Houdini.

'''


import houdiniUtils
from importlib import reload
reload(houdiniUtils.fSpy)
fspy_cam = houdiniUtils.fSpy.fSpy()
json_path = fspy_cam.get_json()
def create_camera():
    if json_path:
        fspy_cam.get_image()
        fspy_cam.get_cam_inputs()
        fspy_cam.get_fspy_data()
        fspy_cam.create_fspy_cam()
    else:
        return
         
create_camera()
