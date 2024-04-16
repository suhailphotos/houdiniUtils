import hou
import os, re

def kitbash_matfile_paths(kitname: str = 'MTM'):
    kb3d_mtm = hou.node(f'/obj/KB3D_{kitname}')
    matnet_node = kb3d_mtm.node('matnet')
    for subnet in matnet_node.children():
        if subnet.type().name() == 'subnet':
            for mtlximage_node in subnet.children():
                if mtlximage_node.type().name()=='mtlximage':
                    file_parm = mtlximage_node.parm('file')
                    if file_parm is not None:
                        file_path = file_parm.eval()
                        if not os.path.exists(file_path):
                            print(f'`{os.path.basename(file_path)}`')

                        
kitbash_matfile_paths('MTM')
