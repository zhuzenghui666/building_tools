bl_info = {
    "name": "Cynthia",
    "author": "Ian Ichung'wa Karanja (ranjian0)",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Toolshelf > Cynthia",
    "description": "Building Generation Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

import bpy
from bpy.props import *
from .core import register_core, unregister_core

# =======================================================
#
#           PANEL UI
#
# =======================================================

class PROP_items(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        sp = layout.split(percentage=.9)
        sp.prop(item, "name", text="", emboss=False, translate=False, icon='SNAP_PEEL_OBJECT')
        sp.operator("cynthia.remove_property", text="", emboss=False, icon="X")

    def invoke(self, context, event):
        pass


class CynthiaPanel(bpy.types.Panel):
    """Docstring of CynthiaPanel"""
    bl_idname = "VIEW3D_PT_cynthia"
    bl_label = "Cynthia Building Tools"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Cynthia Tools'

    def draw(self, context):
        layout = self.layout
        active = context.object

        # Draw the operators
        col = layout.column(align=True)

        row = col.row(align=True)
        row.operator("cynthia.add_floorplan")
        row.operator("cynthia.add_floors")

        row = col.row(align=True)
        row.operator("cynthia.add_window")
        row.operator("cynthia.add_door")

        row = col.row(align=True)
        row.operator("cynthia.add_balcony")
        row.operator("cynthia.add_railing")

        col.operator("cynthia.add_stairs")
        # col.operator("cynthia.add_staircase")

        col.operator("cynthia.add_roof")

        # Draw Properties
        col = layout.column(align=True)
        col.box().label("Properties")

        if active:
            box = col.box()
            obj = context.object

            # Draw UIlist for all property groups
            rows = 2
            row = box.row()
            row.template_list("PROP_items", "", obj, "property_list", obj, "property_index", rows=rows)


            # draw  properties for active group
            active_index = obj.property_index
            if not len(obj.property_list):
                return
            active_prop = obj.property_list[active_index]

            if active_prop.type     == 'FLOORPLAN':
                fp_props = obj.building.floorplan
                fp_props.draw(context, box)
            elif active_prop.type   == 'FLOOR':
                floor_props = obj.building.floors
                floor_props.draw(context, box)
            elif active_prop.type   == 'WINDOW':
                win_prop = obj.building.windows[active_prop.id]
                win_prop.draw(context, box)
            elif active_prop.type   == 'DOOR':
                door_prop = obj.building.doors[active_prop.id]
                door_prop.draw(context, box)


# =======================================================
#
#           REGISTER
#
# =======================================================

def register():
    register_core()


def unregister():
    unregister_core()

if __name__ == "__main__":
    import os
    os.system("clear")
    # useful for continuous updates
    try:
        unregister()
    except Exception as e:
        import traceback; traceback.print_exc()
        print("UNREGISTERED MODULE .. FAIL", e)
    register()


    # # optional run tests
    # from .tests import CynthiaTest
    # CynthiaTest.run_tests()

    # Dev --init workspace
    # --clear
    # bpy.ops.object.select_all(action="SELECT")
    # bpy.ops.object.delete(use_global=False)
    # for mat in bpy.data.materials:
    #     bpy.data.materials.remove(mat)
    # # -- add
    # bpy.ops.cynthia.add_floorplan()
    # bpy.ops.cynthia.add_floors()
    # bpy.context.object.building.floors.floor_count = 3
    # bpy.context.object.building.floors.floor_height = 3
