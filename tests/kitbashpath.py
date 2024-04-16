import hou
import re

def kitbash_filepaths(kitname: str = 'MTM'):
    kb3d_mtm = hou.node(f'/obj/KB3D_{kitname}')
    for subnet in kb3d_mtm.children():
        if subnet.type().name() == 'subnet':
            for file_node in subnet.children():
                if file_node.type().name()=='file':
                    file_parm = file_node.parm('file')
                    if file_parm is not None:
                        file_path = file_parm.rawValue()
                        pattern = re.compile(r"\$KITBASH_ASSETS/geo/([^/]+\.bgeo)")
                        new_file_path = re.sub(pattern, r"$KITBASH_ASSETS/{}/geo/\1".format(kitname), file_path)
                        file_parm.set(new_file_path)

kitbash_filepaths('MTM')





