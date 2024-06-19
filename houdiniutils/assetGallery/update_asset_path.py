import hou

def update_asset_path(old_str: str, replace_str: str, asset_gallery: hou.AssetGalleryDataSource, search_filter: str = None):
    if search_filter:
        item_ids = [item_id for item_id in asset_gallery.itemIds() if search_filter in asset_gallery.label(item_id)]
    else:
        item_ids = list(asset_gallery.itemIds())

    for item_id in item_ids:
        current_path = asset_gallery.filePath(item_id)
        new_path = current_path.replace(old_str, replace_str)
        asset_gallery.setFilePath(item_id, new_path)

asset_path = '/Users/suhail/Documents/houdini/assetGalleryDB/usd_assetGallery.db'
asset_gallery = hou.AssetGalleryDataSource(asset_path)
old_str = 'kitbash'
replace_str = 'kbh'
update_asset_path(old_str, replace_str, asset_gallery, 'KB3D')

