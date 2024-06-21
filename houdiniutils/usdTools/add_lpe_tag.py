import hou
from pxr import Usd, Sdf

node = hou.pwd()
stage = node.editableStage()

# fg lights
fg_lght_prim_path1 = '/lights/fg_lght1'

# md lights
md_lght_prim_path1 = '/lights/md_lght1'

# bg lights
bg_lght_prim_path1 = '/lights/bg_lght1'
bg_lght_prim_path2 = '/lights/bg_lght2'

# fg lights prims
fg_lght_prim1 = stage.GetPrimAtPath(fg_lght_prim_path1)

# md lights prims
md_lght_prim1 = stage.GetPrimAtPath(md_lght_prim_path1)

# bg lights prims
bg_lght_prim1 = stage.GetPrimAtPath(bg_lght_prim_path1)
bg_lght_prim2 = stage.GetPrimAtPath(bg_lght_prim_path2) 



# create property if it doesn't exist

fg_lght_prim_lpe_tag = fg_lght_prim1.GetAttribute('karma:light:lpetag')
if not fg_lght_prim_lpe_tag:
    fg_lght_prim_lpe_tag = fg_lght_prim1.CreateAttribute('karma:light:lpetag', Sdf.ValueTypeNames.String)
fg_lght_prim_lpe_tag.Set('fg_lgts')

md_lght_prim_lpe_tag = md_lght_prim1.GetAttribute('karma:light:lpetag')
if not md_lght_prim_lpe_tag:
    md_lght_prim_lpe_tag = md_lght_prim1.CreateAttribute('karma:light:lpetag', Sdf.ValueTypeNames.String)
md_lght_prim_lpe_tag.Set('md_lgts')

bg_lght_prim_lpe_tag1 = bg_lght_prim1.GetAttribute('karma:light:lpetag')
if not mg_lght_prim_lpe_tag1:
    bg_lght_prim_lpe_tag1 = bg_lght_prim1.CreateAttribute('karma:light:lpetag', Sdf.ValueTypeNames.String)
bg_lght_prim_lpe_tag1.Set('bg_lgts')

bg_lght_prim_lpe_tag = bg_lght_prim2.GetAttribute('karma:light:lpetag')
if not bg_lght_prim_lpe_tag2:
    bg_lght_prim_lpe_tag2 = bg_lght_prim2.CreateAttribute('karma:light:lpetag', Sdf.ValueTypeNames.String)
bg_lght_prim_lpe_tag2.Set('bg_lgts')

