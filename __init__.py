bl_info = {
    "name": "Emoticons Utils",
    "author": "Christian F. (known as Chryfi)",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D window toolshelf > emoticons utils tab",
    "description": "This addon adds some utility functions that can become handy when working with the Minecraft Emoticons mod rigs.",
    "warning": "",
    "category": "Object"
}

import bpy

from .mixamo_converter import *
from .morph_tracker_applier import *
from .props import *
from .utils import *

classes = (
EMOTICONS_UTILS_Props,
EMOTICONS_UTILS_PT_mixamo_panel,
EMOTICONS_UTILS_OT_convert_mixamo,
EMOTICONS_UTILS_PT_morph_tracker_panel,
EMOTICONS_UTILS_OT_apply_morph_trackers
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        if issubclass(cls, EMOTICONS_UTILS_RegisterModule):
            cls.register()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        if issubclass(cls, EMOTICONS_UTILS_RegisterModule):
            cls.unregister()


if __name__ == "__main__":
    register()
