# This was an example code to copy the transfrom from detail attrib at SOP level
# To copy it to parent prim in Solaris using pxr library


from pxr import Usd, UsdGeom, Sdf

 node = hou.pwd()
 stage = node.editableStage()

 parent_prim_path = '/box'
 child_prim_path = '/box/mesh_0'

 parent_prim = stage.GetPrimAtPath(parent_prim_path)
 child_prim = stage.GetPrimAtPath(child_prim_path)

 if child_prim:
     myxform_attrib = child_prim.GetAttribute('primvars:myxform')
     if myxform_attrib:
         xform_value = myxform_attrib.Get()
         parent_xform_attrib = parent_prim.GetAttribute('xformOp:transform:xform')
         if not parent_xform_attrib:
             parent_xform_attrib = parent_prim.CreateAttribute('xformOp:transform:xform')
           
         parent_xform_attrib.Set(xform_value)
   
