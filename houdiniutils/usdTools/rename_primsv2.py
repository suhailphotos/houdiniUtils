## This Script is to bulk rename primitives


from pxr import Sdf

node = hou.pwd()
layer = node.editableLayer()


def rename_prims(layer, parent_pattern):
    parent_path = Sdf.Path(parent_pattern)
    parent_prim = layer.GetPrimAtPath(parent_path)
    edit = Sdf.BatchNamespaceEdit()
    
    if not parent_prim:
        return []  

    for child in parent_prim.nameChildren:
        orig_prim_path = child.path
        orig_prim_name = orig_prim_path.name
        new_prim_name = orig_prim_name.replace('KB3D', 'SUHAIL3D')
        ren = Sdf.NamespaceEdit.Rename(orig_prim_path, new_prim_name)
        edit.Add(ren)
        
    layer.Apply(edit)
        
        
parent_pattern = '/env/fg'
rename_prims(layer, parent_pattern)
