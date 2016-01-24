import bpy
import mathutils
import math

from mathutils import Vector, Matrix


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
        ...
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
