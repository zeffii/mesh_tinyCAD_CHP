import math

import bpy
import bmesh
import mathutils

from mathutils import Vector, Matrix

from mathutils.geometry import intersect_line_line as LineIntersect
from mathutils.geometry import intersect_point_line as PtLineIntersect

OWN_PRECISION = 1.0e-5

def point_on_edge(p, edge):
    '''
    > p:        vector
    > edge:     tuple of 2 vectors
    < returns:  True / False if a point happens to lie on an edge
    '''
    pt, _percent = PtLineIntersect(p, *edge)
    on_line = (pt-p).length < OWN_PRECISION
    return on_line and (0.0 <= _percent <= 1.0)


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

    p0 = isect[0]
    p1 = point_on_edge(p0, edge_1)
    p2 = point_on_edge(p0, edge_2)
    if (p1 and p2):
        print('point lies on both edges'
        return
    elif (p1 or p2):
        print('point lies on 1 edge'
        return
    
    # reaches this point if the intersection doesnt lie on either edge
    def get_vertex(edge):
        IDX_BOOL = bool((edge.verts[0]-p0).length < (edge.verts[1]-p0).length)
        return edge.verts[IDX_BOOL]

    v1 = bm.verts.new(p0)
    e1 = bm.edges.new(v1, get_vertex(edge_1))
    e2 = bm.edges.new(v1, get_vertex(edge_2))
    edge_1.select = False
    edge_2.select = False
    e1.select = True
    e2.select = True
    

        
    

class TCChamferPlus(bpy.types.Operator):
    bl_idname = "tinycad.chamfer_plus"
    bl_label = "CHP | Chamfer Plus"
    bl_description = "Extends towards intersection, then Fillet"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return all([bool(ob), ob.type == 'MESH', ob.mode == 'EDIT'])

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
