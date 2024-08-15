import os
import site
import json
import platform
import re

def get_houdini_versions(base_dir, pattern):
    versions = []
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            match = re.match(pattern, item)
            if match:
                versions.append(match.group(1))
    return versions

def get_latest_houdini_version(base_dir, pattern):
    versions = get_houdini_versions(base_dir, pattern)
    if versions:
        return max(versions, key=lambda v: list(map(int, v.split('.'))))
    return None

def get_current_houdini_version(base_dir, pattern):
    current_path = os.path.join(base_dir, 'Current')
    if os.path.islink(current_path):
        actual_path = os.readlink(current_path)
        version = os.path.basename(actual_path)
        match = re.match(pattern, version)
        if match:
            return match.group(1)
    return None

def get_houdini_major_version():
    system = platform.system()
    if system == "Windows":
        base_dir = "C:\\Program Files\\Side Effects Software"
        pattern = r'Houdini (\d+\.\d+)\.\d+'
        check_current = False
    elif system == "Darwin":
        base_dir = "/Applications/Houdini"
        pattern = r'Houdini(\d+\.\d+)\.\d+'
        check_current = True
    else:
        print("Unsupported operating system.")
        return None

    latest_version = get_latest_houdini_version(base_dir, pattern)

    if latest_version:
        return latest_version
    elif check_current:
        current_version = get_current_houdini_version(base_dir, pattern)
        if current_version:
            return current_version

    return None

def post_install():
    print("Running post install setup...")
    houdini_version = get_houdini_major_version()
    if not houdini_version:
        print("No Houdini versions found.")
        return

    user_pref_dir = ''
    if platform.system() == 'Windows':
        onedrive_dir = os.path.expanduser(f'~/OneDrive/Documents/houdini{houdini_version}')
        default_dir = os.path.expanduser(f'~/Documents/houdini{houdini_version}')
        user_pref_dir = onedrive_dir if os.path.exists(onedrive_dir) else default_dir
    elif platform.system() == 'Darwin':
        user_pref_dir = os.path.expanduser(f'~/Library/Preferences/Houdini/{houdini_version}')

    print(f"Determined Houdini user preference directory: {user_pref_dir}")

    toolbar_dir = os.path.join(user_pref_dir, 'toolbar')
    packages_dir = os.path.join(user_pref_dir, 'packages')
    shelf_file_path = os.path.join(toolbar_dir, 'houdiniUtils.shelf')
    json_file_path = os.path.join(packages_dir, 'houdiniUtils.json')

    print(f"Toolbar directory: {toolbar_dir}")
    print(f"Packages directory: {packages_dir}")
    print(f"Shelf file path: {shelf_file_path}")
    print(f"JSON file path: {json_file_path}")

    os.makedirs(toolbar_dir, exist_ok=True)
    os.makedirs(packages_dir, exist_ok=True)

    # Updated shelf content
    shelf_content = '''<?xml version="1.0" encoding="UTF-8"?>
<shelfDocument>
  <toolshelf name="houdiniUtils" label="Houdini Utils">
    <memberTool name="ren_tex_files1"/>
  </toolshelf>
  <tool name="ren_tex_files1" label="Ren Texture" icon="hicon:/SVGIcons.index?SOP_grouprename.svg">
    <script scriptType="python"><![CDATA[__author__ = "Suhail"
__credits__ = ["Suhail"]
__Lisence__ = "MIT"
__maintainer__ = "Suhail"
__email__ = "suhailece@gmail.com"
__status__ = "Development"
__version__ = "0.1.5"

from houdiniutils.textureTools import main
from importlib import reload

reload(main)
main.main()]]></script>
  </tool>
  <tool name="ren_tex_files" label="Ren Texture" icon="hicon:/SVGIcons.index?SOP_grouprename.svg">
    <script scriptType="python"><![CDATA[from houdiniutils.textureTools import main
from importlib import reload

reload(main)
main.main()]]></script>
  </tool>
</shelfDocument>'''

    with open(shelf_file_path, 'w') as f:
        f.write(shelf_content)

    print(f"Written shelf file to {shelf_file_path}")

    site_packages_path = [p.replace("\\", "/") for p in site.getsitepackages() if "site-packages" in p][0]
    config = {"env": [{"PYTHONPATH": [site_packages_path]}]}
    with open(json_file_path, 'w') as f:
        json.dump(config, f, indent=4)

    print(f"Written JSON file to {json_file_path}")

if __name__ == "__main__":
    post_install()
