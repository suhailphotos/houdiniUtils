import hou
import math

class Primitive:
    def __init__(self, prim:hou.Prim):
        if not isinstance(prim, hou.Prim):
            raise TypeError('Obj is not a geometry type')
        self.prim = prim
        self.angle = None
        self.group_id = None
        self.orientation = None
        self.duplicate = None

    def __getattr__(self, attr):
        return getattr(self.prim, attr)

class Attribs:
    def __init__(self, node: hou.Node):
        if not isinstance(node, hou.Node):
            raise TypeError('obj is not a houdini node')
        self.node = node
        self.geo = node.geometry()
        self.curves = [Primitive(prim) for prim in self.geo.prims()]
        self.orientation = self._get_orientation()

    def _get_orientation(self):
        bbox = self.geo.boundingBox()
        diag_vec = bbox.maxvec() - bbox.minvec()
        y_axis = hou.Vector3((0, 1, 0))
        x_axis = hou.Vector3((1, 0, 0))
        z_axis = hou.Vector3((0, 0, 1))
        if diag_vec.dot(y_axis)==0.0:
            return (2,0)
        elif diag_vec.dot(x_axis)==0.0:
            return (2,1)
        elif diag_vec.dot(z_axis)==0.0:
            return (1,0)
        else:
            return None
    
    def group_prims(self, epsilon):
        curves = self.curves
        orient = self.orientation
        for curve in curves:
            center = curve.boundingBox().center()
            curve.angle = math.atan2(center[orient[0]], center[orient[1]])
        curves.sort(key=lambda x:x.angle)
        self.curves = curves
        angle_to_group_id = {}
        current_group_id = 1
        for curve in curves:
            assigned_group = False
            for angle_group, group_id in angle_to_group_id.items():
                if abs(curve.angle - angle_group)<=epsilon:
                    curve.group_id = group_id
                    assigned_group = True
                    break
            if not assigned_group:
                angle_to_group_id[curve.angle]=current_group_id
                curve.group_id = current_group_id
                current_group_id+=1
        group_id = self.geo.addAttrib(hou.attribType.Prim, 'group_id',0,create_local_variable=False)
        for curve in curves:
            curve.setAttribValue(group_id, curve.group_id)
    
    
epsilon = hou.pwd().evalParm('epsilon')
attrs = Attribs(hou.pwd())
attrs.group_prims(epsilon)
