from pxr import Sdf

node = hou.pwd()
parent = node.node('..')

root_prim_path = node.evalParm('rootprimpath')
new_name = node.evalParm('newname')
edit = Sdf.BatchNamespaceEdit()

input_stage = node.input(0).stage()
layer = node.editableLayer()

root_prim = Sdf.Path(root_prim_path)
prim = input_stage.GetPrimAtPath(root_prim)

if prim.IsValid():
    # Define the parent path and the new path
    parent_path = root_prim.GetParentPath()
    new_path = parent_path.AppendChild(new_name)
    
    if not layer.GetPrimAtPath(new_path):
        # Rename the primitive by copying the spec and clearing the old one
        with Sdf.ChangeBlock():
            Sdf.CopySpec(layer, root_prim, layer, new_path)
            edit.Add(root_prim_path, Sdf.Path.emptyPath)
            
    if layer.CanApply(edit):
        layer.Apply(edit)
