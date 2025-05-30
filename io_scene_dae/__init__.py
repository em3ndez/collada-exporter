# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty

from bpy_extras.io_utils import ExportHelper
bl_info = {
    "name": "Better Collada Exporter",
    "author": "Juan Linietsky, artell, Panthavma",
    "version": (1, 10, 11),
    "blender": (3, 0, 1),
    "api": 38691,
    "location": "File > Import-Export",
    "description": ("Export DAE Scenes. This plugin actually works better! "
                    "Otherwise contact the Godot Engine community."),
    "warning": "",
    "wiki_url": ("https://godotengine.org"),
    "tracker_url": "https://github.com/godotengine/collada-exporter",
    "support": "OFFICIAL",
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "export_dae" in locals():
        importlib.reload(export_dae)  # noqa


class CE_OT_export_dae(bpy.types.Operator, ExportHelper):
    """Selection to DAE"""
    bl_idname = "export_scene.dae"
    bl_label = "Export DAE"
    bl_options = {"PRESET"}

    filename_ext = ".dae"
    filter_glob : StringProperty(default="*.dae", options={"HIDDEN"})

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling
    object_types : EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        items=(("EMPTY", "Empty", ""),
               ("CAMERA", "Camera", ""),
               ("LAMP", "Lamp", ""),
               ("ARMATURE", "Armature", ""),
               ("MESH", "Mesh", ""),
               ("CURVE", "Curve", ""),
               ),
        default={"EMPTY", "CAMERA", "LAMP", "ARMATURE", "MESH", "CURVE"},
        )

    use_export_selected : BoolProperty(
        name="Selected Objects",
        description="Export only selected objects (and visible in active "
                    "layers if that applies).",
        default=False,
        )
    use_mesh_modifiers : BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to mesh objects (on a copy!).",
        default=False,
        )
    use_exclude_armature_modifier : BoolProperty(
        name="Exclude Armature Modifier",
        description="Exclude the armature modifier when applying modifiers "
                      "(otherwise animation will be applied on top of the last pose)",
        default=True,
        )
    use_tangent_arrays : BoolProperty(
        name="Tangent Arrays",
        description="Export Tangent and Binormal arrays "
                    "(for normalmapping).",
        default=False,
        )
    use_triangles : BoolProperty(
        name="Triangulate",
        description="Export Triangles instead of Polygons.",
        default=False,
        )

    use_copy_images : BoolProperty(
        name="Copy Images",
        description="Copy Images (create images/ subfolder)",
        default=False,
        )
    use_active_layers : BoolProperty(
        name="Active Layers",
        description="Export only objects on the active layers.",
        default=True,
        )
    use_exclude_ctrl_bones : BoolProperty(
        name="Exclude Control Bones",
        description=("Exclude skeleton bones with names beginning with 'ctrl' "
                     "or bones which are not marked as Deform bones."),
        default=True,
        )
    use_anim : BoolProperty(
        name="Export Animation",
        description="Export keyframe animation",
        default=False,
        )
    use_anim_action_all : BoolProperty(
        name="All Actions",
        description=("Export all actions for the first armature found "
                     "in separate DAE files"),
        default=False,
        )
    use_anim_skip_noexp : BoolProperty(
        name="Skip (-noexp) Actions",
        description="Skip exporting of actions whose name end in (-noexp)."
                    " Useful to skip control animations.",
        default=True,
        )
    use_anim_optimize : BoolProperty(
        name="Optimize Keyframes",
        description="Remove double keyframes",
        default=True,
        )

    use_shape_key_export : BoolProperty(
        name="Shape Keys",
        description="Export shape keys for selected objects.",
        default=False,
        )
		
    anim_optimize_precision : FloatProperty(
        name="Precision",
        description=("Tolerence for comparing double keyframes "
                     "(higher for greater accuracy)"),
        min=1, max=16,
        soft_min=1, soft_max=16,
        default=6.0,
        )

    use_metadata : BoolProperty(
        name="Use Metadata",
        default=True,
        options={"HIDDEN"},
        )

    @property
    def check_extension(self):
        return True

    def execute(self, context):
        if not self.filepath:
            raise Exception("filepath not set")

        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            "xna_validate",
                                            ))

        from . import export_dae
        return export_dae.save(self, context, **keywords)


def menu_func(self, context):
    self.layout.operator(CE_OT_export_dae.bl_idname, text="Better Collada (.dae)")

	
#classes = (CE_OT_export_dae)

def register():	 
	from bpy.utils import register_class

	register_class(CE_OT_export_dae)
	
	#bpy.types.INFO_MT_file_export.append(menu_func)
	bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():	 
	from bpy.utils import unregister_class
	
	unregister_class(CE_OT_export_dae)
	
	#bpy.types.INFO_MT_file_export.append(menu_func)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
