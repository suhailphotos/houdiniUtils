from pxr import Usd, UsdGeom, Sdf, Gf

node = hou.pwd()
stage = node.editableStage()

prim = stage.GetPrimAtPath('/env/fg/KB3D_NEC_BldgLG_A')
xformPrim = prim.GetAttribute('xformOp:transform')
translateOp = UsdGeom.XformOp(xformPrim)
translation_matrix = Gf.Matrix4d().SetTranslate(Gf.Vec3d(-80.0, 50.0, 30.0))
translateOp.Set(translation_matrix)
