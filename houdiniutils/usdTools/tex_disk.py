print("start")
import os
import hou
import re
disk_textures = []
materials = []

### RBL TEXT Converter_v001
###SET DEFAULT VALUES, NO SPACES ALLOWED####
default_matlib_name = "Converted_Material_Library"
default_basecol_name = "basecolor"
default_metallic_name = "metallic"
default_roughness_name = "roughness"
default_normal_name = "normal"
default_displacement_name = "height"
default_emission_name = "emissive"
default_opacity_name = "alpha"
default_transmission_name = "refraction"
default_displacement_amount = "0"
default_ao_name = "ao" 

#select folder
scan_dir = hou.ui.selectFile(file_type=hou.fileType.Directory) 
print(scan_dir)

#remap input texture names
user_input_button, user_input_values = hou.ui.readMultiInput(
        "Set texture ID names. No Spaces Allowed!", ("Add collect node suffix:", "Base Color:", "Metallic:", "Roughness:", "Normal:", "Displacement:", "Emission:", "Opacity:", "Refraction:", "Displacement Amount:", "Ambient Occlution:"),
    initial_contents=("", default_basecol_name, default_metallic_name, default_roughness_name, default_normal_name, default_displacement_name, default_emission_name, default_opacity_name, default_transmission_name, default_displacement_amount, default_ao_name),
    title="Remap Input",
    buttons=("OK", "Cancel"),
    default_choice=0, close_choice=1,
)

user_suffix = user_input_values[0]
user_basecol_name = user_input_values[1]
user_metallic_name = user_input_values[2]
user_roughness_name = user_input_values[3]
user_normal_name = user_input_values[4]
user_displacement_name = user_input_values[5]
user_emission_name = user_input_values[6]
user_opacity_name = user_input_values[7]
user_transmission_name = user_input_values[8]
user_displacement_amount = user_input_values[9]
user_ao_name = user_input_values[10]

if (user_displacement_amount.isnumeric()==False):
    hou.ui.displayMessage("Displacement Amount must be numeric", severity=hou.severityType.Warning)
    quit()

#scan folder
for root, dirs, files in os.walk(scan_dir, topdown=False):
   for file in files:
        if file.endswith(user_basecol_name+".jpg") or file.endswith(user_basecol_name+".png") or file.endswith(user_basecol_name+".jpeg"):
            text_file = (root+"/"+file)
            
            #ignore mipmaps
            if (".rat" in file) or (".tx" in file):
                print("mipmap found, ignoring "+file)
            else:
                disk_textures.append(text_file)

if (len(disk_textures)==0):
    hou.ui.displayMessage("No basecolor of that name was found on a .jpg, .jpeg, or .png. Note this tool does not support UDIMS", severity=hou.severityType.Warning)
    quit()

            
            




print("INITIALIZING MATERIAL BUILDER")

#check if arnold exists
hpath = hou.houdiniPath()
ar_exists = 0
for x in hpath:
    if ("htoa" in x):
        ar_exists = 1
        print("HtoA Found")

        
#setup arnold colorspace function
def ar_colorspace_setup(input_var, cf_var, cs_var, input_num, output_num):
    color_family = input_var.path()+"/color_family"
    color_space = input_var.path()+"/color_space"
    single_channel = input_var.path()+"/single_channel"
    
    input_var.parm(color_family).set(cf_var)
    input_var.parm(color_space).set(cs_var)
    
    ar_surface.setNamedInput(input_num, ar_image, output_num)
    
    if len(output_num)==1:
        input_var.parm(single_channel).set(1)

        
#setup Karma colorspace function
def km_colorspace_setup(input_var, cs_var, input_num, output_num):
    signature = input_var.path()+"/signature"
    input_var.parm(signature).set(cs_var)
    
    km_surface.setNamedInput(input_num, km_image, output_num)
 
#turn update mode to manual
hou.ui.setUpdateMode(hou.updateMode.Manual)

#create material library
new_root = "/stage"
mtl_lib = hou.node(new_root).createNode("materiallibrary", default_matlib_name)
mtl_lib.parm("matpathprefix").set("/ASSET/mtl/")    
mtl_lib_path = mtl_lib.path()




#define textures with name changes
name_change = []

#loop through each texture 
for x in disk_textures:
            
    
    root=mtl_lib.path()
    
    
    file_name = x.split("/")
    mat_name = file_name[-1]
    parse_name = mat_name.split("_")
    name = mat_name.replace(("_"+parse_name[-1]), "")
    usd_name = name.replace("-", "_")
    
    if (name!=usd_name):
        name_change.append(name)
        
    
    disp_amount = user_displacement_amount
    remap_found = 0
    
    current_mat_textures = []
    
    for root2, dirs2, files2 in os.walk(scan_dir, topdown=False):
        for file2 in files2:
            if (name in file2):
                file_directory = root2
                #ignore mipmaps
                if (".rat" in file2) or (".tx" in file2):
                    print("mipmap found, ignoring "+file2)
                else:
                    current_mat_textures.append(file_directory+"/"+file2)
                
    
    print("Creating "+name)
###### ARNOLD SETUP #########
    if (ar_exists==1):

        #create arnold material builder
        ar = hou.node(root).createNode("arnold_materialbuilder", "arnold_"+usd_name)
        ar_ao: bool = False # <---- Code inserted by Suhail
    
        ar_path = ar.path()+"/"
        ar_output = hou.node(ar.path()+"/OUT_material")
        
        #create standard surface
        ar_surface = hou.node(ar_path).createNode("standard_surface")
        ar_surface.parm(ar_path+"standard_surface1/specular_roughness").set(.5)
        ar_output.setInput(0, ar_surface, 0)
        ar_image_basecol: hou.Node = None # <---- Code inserted by Suhail

        
        for text in current_mat_textures:
            #create image node
            ar_image = hou.node(ar_path).createNode("image")
            
    
            #set file path
            ar_fileparm = ar_image.path()+"/filename"
            ar_image.parm(ar_fileparm).set(text)
            ar_ao = bool(re.search(r'_ao\.[^.]*$', text)) # <---- Code inserted by Suhail
            if ar_ao: # <---- Code inserted by Suhail
                ar_image_ao = ar_image # <---- Code inserted by Suhail        
            
            #define initial inputs
            if (("_")+user_basecol_name) in text:
                ar_image_basecol = ar_image # <---- Code inserted by Suhail
                ar_colorspace_setup(ar_image, "Utility", "sRGB - Texture", "base_color", "rgba")
                
            if (("_")+user_metallic_name) in text:
                ar_colorspace_setup(ar_image, "ACES", "ACEScg", "metalness", "r")                  
    
            if (("_")+user_roughness_name) in text:
                ar_colorspace_setup(ar_image, "ACES", "ACEScg", "specular_roughness", "r")
                
            if (("_")+user_emission_name) in text:
                ar_colorspace_setup(ar_image, "Utility", "sRGB - Texture", "emission_color", "r")
                ar_surface.parm(ar_path+"standard_surface1/emission").set(1)
                
            if (("_")+user_opacity_name) in text:
                ar_colorspace_setup(ar_image, "Utility", "Raw", "opacity", "r")
                
            if (("_")+user_transmission_name) in text:
                ar_colorspace_setup(ar_image, "Utility", "Raw", "transmission", "r")
            
            #specialize for normal and for height    
            if (("_")+user_normal_name) in text:
                ar_colorspace_setup(ar_image, "Utility", "Raw", "normal", "rgba") 
                
                #create normal node
                ar_normal = hou.node(ar_path).createNode("normal_map")
                
                #connect inputs and position
                ar_normal.setNamedInput("input", ar_image, "rgba")
                ar_surface.setNamedInput("normal", ar_normal, "vector")
                
            #specialize for height displacement
            if (("_")+user_displacement_name) in text:
                ar_colorspace_setup(ar_image, "ACES", "ACEScg", "diffuse_roughness", "rgba")
                
                ar_surface.setInput(2, None)
                ar_height = hou.node(ar_path).createNode("arnold::multiply", "displacement_amount")
                
                ar_height.parm("input2r").set(disp_amount)
                ar_height.parm("input2g").set(disp_amount)
                ar_height.parm("input2b").set(disp_amount)
                
                #if remapped
                if (remap_found==1):
                    ar_height_offset = hou.node(ar_path).createNode("arnold::range", "displacement_remap")
                    ar_height_offset.parm("output_min").set(low_offset)
                    ar_height_offset.parm("output_max").set(high_offset)
                    
                    ar_height_offset.setNamedInput("input", ar_image, "rgba")
                    ar_height.setNamedInput("input1", ar_height_offset, "rgb")
                    ar_output.setNamedInput("displacement", ar_height, "rgb")
                    
                else:
                    ar_height.setNamedInput("input1", ar_image, "rgba")
                    ar_output.setNamedInput("displacement", ar_height, "rgb")

            if ar_ao: # <---- if block code inserted by Suhail
                ar_mul_node = hou.node(ar_path).createNode("arnold::multiply", "multiply_ao")
                ar_mul_node.setInput(0, ar_image_ao,0)
                ar_mul_node.setInput(1, ar_image_basecol,0)
                ar_surface.setInput(1, ar_mul_node,0)

                                                                                            
            #name image nodes
            nodename = text.split("/")
            if (".jpg" in nodename[-1]):
                node_name = nodename[-1].replace(".jpg", "_ar")
                ar_image.setName(node_name.replace("-", "_"), unique_name=True)
                print("Created Arnold "+node_name)
            
            if (".png" in nodename[-1]):
                node_name = nodename[-1].replace(".png", "_ar")
                ar_image.setName(node_name.replace("-", "_"), unique_name=True)
                print("Created Arnold "+node_name)

            
        #nicely layout arnold nodes
        ar.layoutChildren(horizontal_spacing = 2.0, vertical_spacing = 2.0)
        ar.setMaterialFlag(False)
       
######### END ARNOLD SETUP ####################

######### START KARMA SETUP ####################
    #create Karma material builder
    km = hou.node(root).createNode("subnet", "karma_"+usd_name)

    km_path = km.path()+"/"
    km_output = hou.node(km.path()+"/suboutput1")
    #hou.node(km.path()+"/subinput1").destroy()
    
######### START KARMA MTL BUILDER EXTRACT #############

    km.setDebugFlag(False)
    km.setDetailLowFlag(False)
    km.setDetailMediumFlag(False)
    km.setDetailHighFlag(True)
    km.bypass(False)
    km.setCompressFlag(True)
    km.hide(False)
    km.setSelected(True)
    
    hou_parm_template_group = hou.ParmTemplateGroup()
    # Code for parameter template
    hou_parm_template = hou.FolderParmTemplate("folder1", "Karma Material Builder", folder_type=hou.folderType.Collapsible, default_value=0, ends_tab_group=False)
    hou_parm_template.setTags({"group_type": "collapsible", "sidefx::shader_isparm": "0"})
    # Code for parameter template
    hou_parm_template2 = hou.IntParmTemplate("inherit_ctrl", "Inherit from Class", 1, default_value=([2]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2"]), menu_labels=(["Never","Always","Material Flag"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.StringParmTemplate("shader_referencetype", "Class Arc", 1, default_value=(["n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r"]), default_expression=(["n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r"]), default_expression_language=([hou.scriptLanguage.Python]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["none","reference","inherit","specialize","represent"]), menu_labels=(["None","Reference","Inherit","Specialize","Represent"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template2.setTags({"sidefx::shader_isparm": "0", "spare_category": "Shader"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.StringParmTemplate("shader_baseprimpath", "Class Prim Path", 1, default_value=(["/__class_mtl__/`$OS`"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template2.setTags({"script_action": "import loputils\nloputils.selectPrimsInParm(kwargs, False)", "script_action_help": "Select a primitive in the Scene Viewer or Scene Graph Tree pane.\nCtrl-click to select using the primitive picker dialog.", "script_action_icon": "BUTTONS_reselect", "sidefx::shader_isparm": "0", "sidefx::usdpathtype": "prim", "spare_category": "Shader"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.SeparatorParmTemplate("separator1")
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.StringParmTemplate("tabmenumask", "Tab Menu Mask", 1, default_value=(["karma USD ^mtlxUsd* ^mtlxramp* ^hmtlxramp* ^hmtlxcubicramp* MaterialX parameter constant collect null genericshader subnet subnetconnector suboutput subinput"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template2.setTags({"spare_category": "Tab Menu"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.StringParmTemplate("shader_rendercontextname", "Render Context Name", 1, default_value=(["kma"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
    hou_parm_template2.setTags({"sidefx::shader_isparm": "0", "spare_category": "Shader"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    # Code for parameter template
    hou_parm_template2 = hou.ToggleParmTemplate("shader_forcechildren", "Force Translation of Children", default_value=True)
    hou_parm_template2.setTags({"sidefx::shader_isparm": "0", "spare_category": "Shader"})
    hou_parm_template.addParmTemplate(hou_parm_template2)
    hou_parm_template_group.append(hou_parm_template)
    km.setParmTemplateGroup(hou_parm_template_group)
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/folder1 parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("folder1")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set(0)
    hou_parm.setAutoscope(False)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/inherit_ctrl parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("inherit_ctrl")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set(2)
    hou_parm.setAutoscope(False)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/shader_referencetype parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("shader_referencetype")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set("inherit")
    hou_parm.setAutoscope(False)
    
    # Code for first keyframe.
    # Code for keyframe.
    hou_keyframe = hou.StringKeyframe()
    hou_keyframe.setTime(0)
    hou_keyframe.setExpression("n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r", hou.exprLanguage.Python)
    hou_parm.setKeyframe(hou_keyframe)
    
    # Code for last keyframe.
    # Code for keyframe.
    hou_keyframe = hou.StringKeyframe()
    hou_keyframe.setTime(0)
    hou_keyframe.setExpression("n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r", hou.exprLanguage.Python)
    hou_parm.setKeyframe(hou_keyframe)
    
    # Code for keyframe.
    hou_keyframe = hou.StringKeyframe()
    hou_keyframe.setTime(0)
    hou_keyframe.setExpression("n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r", hou.exprLanguage.Python)
    hou_parm.setKeyframe(hou_keyframe)
    
    # Code for keyframe.
    hou_keyframe = hou.StringKeyframe()
    hou_keyframe.setTime(0)
    hou_keyframe.setExpression("n = hou.pwd()\nn_hasFlag = n.isMaterialFlagSet()\ni = n.evalParm('inherit_ctrl')\nr = 'none'\nif i == 1 or (n_hasFlag and i == 2):\n    r = 'inherit'\nreturn r", hou.exprLanguage.Python)
    hou_parm.setKeyframe(hou_keyframe)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/shader_baseprimpath parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("shader_baseprimpath")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set("/__class_mtl__/`$OS`")
    hou_parm.setAutoscope(False)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/tabmenumask parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("tabmenumask")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set("karma USD ^mtlxUsd* ^mtlxramp* ^hmtlxramp* ^hmtlxcubicramp* MaterialX parameter constant collect null genericshader subnet subnetconnector suboutput subinput")
    hou_parm.setAutoscope(False)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/shader_rendercontextname parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("shader_rendercontextname")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set("kma")
    hou_parm.setAutoscope(False)
    
    
    # Code for /obj/KB3D_MTM/matnet/karmamaterial/shader_forcechildren parm 
    if locals().get("km") is None:
        km = hou.node("/obj/KB3D_MTM/matnet/karmamaterial")
    hou_parm = km.parm("shader_forcechildren")
    hou_parm.lock(False)
    hou_parm.deleteAllKeyframes()
    hou_parm.set(1)
    hou_parm.setAutoscope(False)
    
    
    km.setExpressionLanguage(hou.exprLanguage.Hscript)
    
    if hasattr(km, "syncNodeVersionIfNeeded"):
        km.syncNodeVersionIfNeeded("20.0.653")
####### END KARMA BUILDER EXTRACT#########            
    
    #create standard surface
    km_surface = hou.node(km_path).createNode("mtlxstandard_surface")
    km_ao: bool = False  # <---- Code inserted by Suhail
    km_image_basecol: hou.Node = None # <---- Code inserted by Suhail
    km_image_ao: hou.Node = None  # <---- Code inserted by Suhail

    
    km_output.setInput(0, km_surface, 0)
    has_disp = 0
    
    for text in current_mat_textures:
        #create image node
        km_image = hou.node(km_path).createNode("mtlximage")
        

        #set file path
        km_fileparm = km_image.path()+"/file"
        km_image.parm(km_fileparm).set(text)
        km_ao = bool(re.search(r'_ao\.[^.]*$', text)) # <---- Code inserted by Suhail
        if km_ao: # <---- Code inserted by Suhail 
            km_image_ao = km_image # <---- Code inserted by Suhail

        
        #define initial inputs
        if (("_")+user_basecol_name) in text:
            km_image_basecol = km_image
            km_colorspace_setup(km_image, "color3", "base_color", "out")
            
        if (("_")+user_metallic_name) in text:
            km_colorspace_setup(km_image, "default", "metalness", "out")                  

        if (("_")+user_roughness_name) in text:
            km_colorspace_setup(km_image, "default", "specular_roughness", "out")
            
        if (("_")+user_emission_name) in text:
            km_colorspace_setup(km_image, "color3", "emission_color", "out")
            km_surface.parm(km_path+"mtlxstandard_surface1/emission").set(1)
            
        if (("_")+user_opacity_name) in text:
            km_colorspace_setup(km_image, "default", "opacity", "out")
            
        if (("_")+user_transmission_name) in text:
            km_colorspace_setup(km_image, "default", "transmission", "out")
        
        #specialize for normal and for height    
        if (("_")+user_normal_name) in text:
            km_colorspace_setup(km_image, "vector3", "normal", "out") 
            
            #create normal node
            km_normal = hou.node(km_path).createNode("mtlxnormalmap")
            
            #connect inputs and position
            km_normal.setNamedInput("in", km_image, "out")
            km_surface.setNamedInput("normal", km_normal, "out")
            
        #specialize for height displacement
        if (("_")+user_displacement_name) in text:
            km_colorspace_setup(km_image, "default", "diffuse_roughness", "out")
            has_disp = 1
            
            #create displacement node and set scale
            km_surface.setInput(2, None)
            km_height = hou.node(km_path).createNode("mtlxdisplacement")
            km_height.parm("scale").set(disp_amount)
            
            if (remap_found==1):
                #create offset node set range
                km_height_offset = hou.node(km_path).createNode("mtlxremap")
                km_height_offset.parm("outlow").set(low_offset)
                km_height_offset.parm("outhigh").set(high_offset)
                
                #connect nodes
                km_height_offset.setNamedInput("in", km_image, "out")
                km_height.setNamedInput("displacement", km_height_offset, "out")
                km_output.setInput(1, km_height, 0)
                
            else:
                km_height.setNamedInput("displacement", km_image, "out")
                km_output.setInput(1, km_height, 0)
                
        if km_ao: # <---- if block code inserted by Suhail
            km_mul_node = hou.node(km_path).createNode("mtlxmultiply", "multiply_ao")
            km_mul_node.parm('signature').set('color3')
            km_mul_node.setInput(0, km_image_ao,0)
            km_mul_node.setInput(1, km_image_basecol,0)
            km_surface.setInput(1, km_mul_node,0)


        
        #name image nodes
        nodename = text.split("/")
        if (".jpg" in nodename[-1]):
            node_name = nodename[-1].replace(".jpg", "_km")
            km_image.setName(node_name.replace("-", "_"), unique_name=True)
            print("Created Karma "+node_name)
        
        if (".png" in nodename[-1]):
            node_name = nodename[-1].replace(".png", "_km")
            km_image.setName(node_name.replace("-", "_"), unique_name=True)
            print("Created Karma "+node_name)


    
    #create karma properties
    km_properties = hou.node(km_path).createNode("kma_material_properties")
    km_output.setInput(2, km_properties, 0)
    km_output.parm("name1").set("surface")        
    km_output.parm("name2").set("displacement")
    
    #nicely layout karma nodes
    km.layoutChildren(horizontal_spacing = 2.0, vertical_spacing = 2.0) 
    
######END KARMA SETUP#######

    
    #create collect node
    if (user_suffix!=""):
        col = hou.node(root).createNode("collect", (usd_name+"_"+user_suffix))
    else:
        col = hou.node(root).createNode("collect", usd_name)
    if (ar_exists==1):
        col.setInput(0, ar, 0)
        col.setInput(1, km, 0)
        col.setInput(2, km, 1)
        if (has_disp==1):
            col.setInput(2, km, 1)
            col.setInput(3, km, 2)
    else:
        col.setInput(0, km, 0)
        col.setInput(1, km, 1)
        if (has_disp==1):
            col.setInput(1, km, 1)
            col.setInput(2, km, 2)
    
#switch update mode to automatic
hou.ui.setUpdateMode(hou.updateMode.AutoUpdate)

 #flag errors if nodes did not contain matx nodes
if (len(name_change)>0):
    error_mat_str = "\n".join(str(element) for element in name_change)
    hou.ui.displayMessage("The materials below had a '-' in the file name. \nThis has been changed changed to an '_' for USD naming standards. \nBe aware auto naming may break with the following materials:\n\n"+error_mat_str, severity=hou.severityType.Warning)

#layout materials
mtl_lib.layoutChildren()
mtl_lib.setCurrent(True, clear_all_selected=True)

