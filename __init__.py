import math

import bpy
import bmesh
import mathutils

from mathutils import Vector, Matrix

from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect


def operate(context, bm, selected):
    edge_1, edge_2 = selected
    edge_1_co_1 = edge_1.verts[0].co
    edge_1_co_2 = edge_1.verts[1].co
    edge_2_co_1 = edge_2.verts[0].co
    edge_2_co_2 = edge_2.verts[1].co
    isect = LineIntersect(edge_1_co_1, edge_1_co_2, edge_2_co_1, edge_2_co_2)

    if (not isect) or ((isect[0] - isect[1]).length >= 1.0e-5):
        print('these edges do not intersect')
        return
    else:    
        print('definite intersection found')

    
    

class TCChamferPlus(bpy.types.Operator):
    bl_idname = "tinycad.chamfer_plus"
    bl_label = "CHP | Chamfer Plus"
    bl_description = "Extends towards intersection, then Fillet"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return bool(obj) and (obj.type == 'MESH') and (obj.mode == 'EDIT')

    def execute(self, context):
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        selected = [e for e in bm.edges if e.select and (not e.hide)]

        if len(selected) == 2:
            operate(context, bm, selected)

        bmesh.update_edit_mesh(me, True)
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
