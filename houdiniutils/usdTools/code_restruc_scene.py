from pxr import Sdf, Pcp

errors = None
node = hou.pwd()
parent = node.node("..")
prim_pattern = parent.evalParm("primpattern")
op = parent.evalParm("op")
err_msg_key = '__err'
warn_msg_key = '__warn'
missing_prims = []
target_paths = []
remove_empty_variants =parent.evalParm("removeemptyvariants")
WARN_PREFIX = "__WARNING:"
WARN_BEHIND_ARC = """Primitive is embedded in a composition arc: {}\n
It would be necessary to flatten the stage to access it."""
ERR_MISSING_PRIM = "Unable to find primitive: {}"

NAME_TOKEN = "@name"
PRIM_IDX_TOKEN = "@index"
WILD_TOKEN = "*"

sel = hou.LopSelectionRule()
sel.setPathPattern(prim_pattern)
src_paths = sel.expandedPaths(node.inputs()[0])
specs = {'def':Sdf.SpecifierDef,
         'over':Sdf.SpecifierOver,
         'class':Sdf.SpecifierClass}
input_stage = node.node("../INPUT").stage()
layer = node.editableLayer()


def _getSpecsToRemove(path_list, stage, layer):
    """
    Alternative, hopefully cleaner way to get possible variant paths from a simple prim path.
    """
    
    all_paths = []
    
    for _path in path_list:
        usd_prim = stage.GetPrimAtPath(_path)
        if usd_prim.IsValid():
            prim_index = usd_prim.GetPrimIndex()
            if layer.GetPrimAtPath(prim_index.rootNode.path):
                all_paths.append(prim_index.rootNode.path)
            if prim_index.rootNode.children:
                for i, child_node in enumerate(prim_index.rootNode.children):
                    if layer.GetPrimAtPath(child_node.path) \
                            and child_node.arcType == Pcp.ArcTypeVariant:
                        all_paths.append(child_node.path)
    
    return list(set(all_paths))


def _getAllNameChildren(path_list, spec, match_name=None):
    """
    Recurse through a primSpec, and return all
    namechildren paths. Also traverse child variantSpecs for primSpecs.
    
    When traversing variantSpecs, we may want to match a name because
    we are matching a primitive pattern, where teh match_name is the name
    of a prim which may be a child spec of a variant.
    """
    if spec:
        if spec.nameChildren:
            for nc in spec.nameChildren.values():
                if match_name:
                    if nc.path.name == match_name:
                        path_list.append(nc.path)
                        # Once we've matched the name, we no longer neeed this check
                        match_name=None
                # We shouldn't just add specs that don't match the name... I'm not sure what this gives us...
                #elif:
                #    path_list.append(nc.path)
                _getAllNameChildren(path_list, nc, match_name)
        if spec.variantSets:
            for varset_spec in spec.variantSets.values():
                for varsel in varset_spec.variants:
                    _getAllNameChildren(path_list, varsel.primSpec)
    return path_list

try:
    with Sdf.ChangeBlock():
    
        edit = Sdf.BatchNamespaceEdit()
        
        # Reparent Primitives
        if op == 0:
            create_parent_prim = parent.evalParm("createparentprim")
            create_only_missing_prims = parent.evalParm("parentonlymissing")
            parent_prim_path = parent.evalParm("primnewparent")
            _spec = specs[parent.evalParm("parentspecifier")] if create_parent_prim else Sdf.SpecifierOver
            _type = parent.evalParm("parentprimtype").replace("UsdGeom","")
            parent_prim = Sdf.Path(parent_prim_path)
    
            while not parent_prim.IsAbsoluteRootPath():
                if not create_parent_prim and layer.GetPrimAtPath(parent_prim):
                    parent_prim = parent_prim.GetParentPath()
                else:
                    parent_primspec = Sdf.CreatePrimInLayer(layer, parent_prim)
                    parent_primspec.specifier = _spec
                    if create_parent_prim:
                        parent_primspec.typeName = _type
                    parent_prim = parent_prim.GetParentPath()
            parent_prim = Sdf.Path(parent_prim_path)
            
            dst_paths = []
            for path in src_paths:
                # Verify the path is a primspec; it could be under a variantspec
                if not path.HasPrefix(parent_prim):
                    new_path = parent_prim.AppendChild(path.name)
                    if new_path in dst_paths:
                        new_path = Sdf.Path(hou.text.incrementNumberedString(new_path.pathString))
                    dst_paths.append(new_path)
                    # For some reason, BatchEditNamespace doesn't udpate relationships like copyspec does...
                    # For now, we'll just copyspec, then remove the old spec; maybe there is a missing option
                    # in there somewhere...
                    #edit.Add(path, new_path)
                    Sdf.CopySpec(layer, path, layer,new_path)
                    edit.Add(path, Sdf.Path.emptyPath)
                    #edit.Add(Sdf.NamespaceEdit.Reparent(path, new_path, Sdf.NamespaceEdit.same))
                
            if layer.CanApply(edit):
                layer.Apply(edit)
            
        # Rename Primitives
        elif op == 1:
            dst_paths = []
            for idx,path in enumerate(src_paths):
                old_name = parent.evalParm("primoldname")
                new_name = parent.evalParm("primnewname")
                old_name = "*{}*".format(old_name) if NAME_TOKEN in old_name else old_name
                new_name = "*{}*".format(new_name) if NAME_TOKEN in new_name else new_name
    
                # Replace special name token with current name of prim
                new_name = new_name.replace(NAME_TOKEN, path.name)
                old_name = old_name.replace(NAME_TOKEN,  path.name)

  
                if new_name != old_name and hou.text.patternMatch(old_name, path.name):
                    # Replace special index token with the prim number
                    new_name = new_name.replace(PRIM_IDX_TOKEN, str(idx))
                    old_name = old_name.replace(PRIM_IDX_TOKEN, str(idx))

                    _name = hou.text.patternRename(path.name, old_name, new_name)
                    new_path = path.GetParentPath().AppendChild(_name)

                    if new_path in dst_paths or layer.GetPrimAtPath(new_path):
                        while new_path in dst_paths or layer.GetPrimAtPath(new_path):
                            new_path = Sdf.Path(hou.text.incrementNumberedString(new_path.pathString))#+str(idx-1)))
                            if new_path not in dst_paths or not layer.GetPrimAtPath(new_path):
                                break
                    dst_paths.append(new_path)
                    
                    # For some reason, BatchEditNamespace doesn't udpate relationship targets like copyspec does...
                    # For now, we'll just copyspec, then remove the old spec; maybe there is a mission option
                    # in there somewhere...
                    #edit.Add(path, new_path)
                    Sdf.CopySpec(layer,path,layer,new_path)
                    edit.Add(path, Sdf.Path.emptyPath)
                
            if layer.CanApply(edit):
                layer.Apply(edit)
            
                
        # Remove Primitives
        elif op == 2:
            removal_paths = _getSpecsToRemove(src_paths, input_stage, layer)
            prefixes = list(set([x.GetParentPath() for x in removal_paths]))

            for path in removal_paths:
                edit.Add(path, Sdf.Path.emptyPath)
    
            if layer.CanApply(edit):
                layer.Apply(edit)
                
            # Remove empty variants/variantsets on the parent prim(s)
            if remove_empty_variants:
                ancestor_paths = list(set([x.GetParentPath() for x in removal_paths]))
                for ancestor_path in ancestor_paths:
                    ancestor_spec = layer.GetObjectAtPath(ancestor_path)
                    
                    if isinstance(ancestor_spec, Sdf.VariantSpec):
                        # Remove the variant spec that has no remaining child specs
                        if not ancestor_spec.primSpec.nameChildren:
                            ancestor_spec.owner.RemoveVariant(ancestor_spec)

        # Rename Variant Set
        elif op == 3:

            old_name = parent.evalParm("variantsetoldname")
            new_name = parent.evalParm("variantsetnewname")
            
            if old_name and old_name != new_name:
                for path in src_paths:
                    primspec = layer.GetPrimAtPath(path)
                    if primspec:
                        if old_name in primspec.variantSetNameList.GetAddedOrExplicitItems():
                            if NAME_TOKEN in new_name:
                                new_name = new_name.replace(NAME_TOKEN, old_name)
                            old_vset = primspec.variantSets[old_name]
                            variants = old_vset.variants
                            selected = primspec.variantSelections[old_name] 
                            
                            for variant, variantspec in variants.items():
                                new_variantspec = Sdf.CreateVariantInLayer(layer, path, new_name, variant)
                                Sdf.CopySpec(layer, variantspec.path, layer, new_variantspec.path)
    
                            primspec.variantSetNameList.Erase(old_name)
                            primspec.variantSelections[new_name] = selected
                        else:
                            raise hou.Error("{}Variant Set '{}' not found on {}.".format(WARN_PREFIX, old_name, path))
                        
        # Remove Variant Sets
        elif op == 4:
            
            parm_value = parent.evalParm("variantset")
            remove_all_variants = parm_value == WILD_TOKEN

            #vspec_deletions = {}
            #variant_name = parent.evalParm("variantname")
            for path in src_paths:
                primspec = layer.GetPrimAtPath(path)
                if primspec:
                    if remove_all_variants:
                        for vset_name in primspec.variantSetNameList.GetAddedOrExplicitItems():
                            primspec.variantSetNameList.Erase(vset_name)
                    else:
                        for vset_name in primspec.variantSetNameList.GetAddedOrExplicitItems():
                            for vset_pattern in parm_value.split(" "):
                                if hou.text.patternMatch(vset_pattern, vset_name):
                                    primspec.variantSetNameList.Erase(vset_name)

                        #raise hou.Error("{}Variant Set '{}' not found on {}.".format(WARN_PREFIX, vset_name, path))                   

        # Remove Variants (TODO)
        elif op == 5:
            vset_name = parent.evalParm("variantremovevariantset")
            parm_value = parent.evalParm("variantremovename")
            remove_all_variants = parm_value == WILD_TOKEN

            for path in src_paths:
                primspec = layer.GetPrimAtPath(path)
                if primspec:
                    if remove_all_variants:
                        for vset_name in primspec.variantSetNameList.GetAddedOrExplicitItems():
                            primspec.variantSetNameList.Erase(vset_name)
                    else:
                        for vset_name in primspec.variantSetNameList.GetAddedOrExplicitItems():
                            for vset_pattern in parm_value.split(" "):
                                if hou.text.patternMatch(vset_pattern, vset_name):
                                    primspec.variantSetNameList.Erase(vset_name)
                        
        # Remove Other Arcs
        elif op == 6:
            for path in src_paths:
                primspec = layer.GetPrimAtPath(path)
                if parent.evalParm("removereferences"):
                    for i in primspec.referenceList.GetAddedOrExplicitItems():
                        primspec.referenceList.Erase(i)
                if parent.evalParm("removepayloads"):
                    for i in primspec.payloadList.GetAddedOrExplicitItems():
                        primspec.payloadList.Erase(i)
                if parent.evalParm("removeinherits"):
                    for i in primspec.inheritPathList.GetAddedOrExplicitItems():
                        primspec.inheritPathList.Erase(i)                
                if parent.evalParm("removespecializes"):
                    for i in primspec.specializesList.GetAddedOrExplicitItems():
                        primspec.specializesList.Erase(i)

        node.setCachedUserData(err_msg_key, None)
        node.setCachedUserData(warn_msg_key, None)
            
except Exception as e:
    NO_SPEC_START = "'Cannot copy unknown spec at <"
    NO_SPEC_END = "> from layer "
    msg_key = ""
    
    if str(e).startswith(WARN_PREFIX):
        msg = str(e).replace(WARN_PREFIX,"")
        msg_key = warn_msg_key
    else:
        # To provide cleaner warnings/errors, without the Python LOP's extra cruft...
        msg = str(e).split(" : ")[-1]
        if msg.startswith(NO_SPEC_START):
            # Check if the error'd prim is missing, or if it's behind a reference or other arc
            _err_path = msg.split(NO_SPEC_START)[-1].split(NO_SPEC_END)[0]
            if input_stage.GetPrimAtPath(_err_path):
                msg = WARN_BEHIND_ARC.format(_err_path)
            else:
                msg = ERR_MISSING_PRIM.format(_err_path)
        else:
            msg = msg[1:-1]
    
    node.setCachedUserData(msg_key, msg)

