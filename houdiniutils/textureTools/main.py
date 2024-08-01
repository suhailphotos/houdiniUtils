import os
from houdiniutils.textureTools import tex_id_manager, renameTexture

def main():
    # Set the config file path
    config_file_path = os.path.dirname(__file__)
    print(config_file_path)

    # Initialize TextureIDManager
    texid = tex_id_manager.TextureIDManager(config_file_path=config_file_path)

    # Initialize RenameTexture with textureTypes and asset name
    renObj = renameTexture.RenameTexture(textureTypes=texid.textureType, asset_name=texid.asset_name)
    renObj.renameFolders()

if __name__ == "__main__":
    main()
