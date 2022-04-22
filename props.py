import bpy
from bpy.props import (BoolProperty, IntProperty, PointerProperty, StringProperty)

from .utils import *

class EMOTICONS_UTILS_Props(bpy.types.PropertyGroup, EMOTICONS_UTILS_RegisterModule):
    frame_start: IntProperty(name = "Frame Start", description = "Start frame", default = 0)
    frame_end: IntProperty(name = "Frame End", description = "End frame", default = 100)
    frame_step: IntProperty(name = "Frame Step", description = "Frame step", default = 1)
    use_hands: BoolProperty(name = "Use Hands", description = "Copy the hands animation data to the emoticons arm.end bones", default = False)
    limit_rotation_axis: BoolProperty(name = "Limit Rotation Axis", description = "Humans dont move the same way as Minecraft characters should, this option deletes the Y and Z rotation channels for the lower legs and lower arms", default=False)
    use_euler_filter: BoolProperty(name = "Use Discontinuity (Euler) Filter", description = "The conversion from quaternions to euler angles can cause jumps in the euler animation, using the discontinuity filter fixes this", default=True)
    use_human_parent_space: BoolProperty(name = "Use Neck, Shoulder and Spine", description = "Take into account the transformations of the shoulders, the additional spines and the neck bones", default=True)
    emoticons_armature: PointerProperty(name = "The emoticons armature for the Mixamo animation", type = bpy.types.Object)
    tracker_emoticons_armature: PointerProperty(name = "The emoticons armature for the morph trackers", type = bpy.types.Object)
    trackers_root_collection: PointerProperty(name = "Define the root collecion that contains all of the morph trackers. The morph trackers need to contain the keywords 'low', 'arm', 'leg', 'left', 'right', 'body', 'anchor', '.end' and 'head'", type = bpy.types.Collection)
    mixamo_armature: PointerProperty(name = "The Mixamo armature", type = bpy.types.Object)
    tracker_collection_keywords: StringProperty(name = "Collection keywords", description = "Define the keywords that the collections should contain. Separate multiple keywords with a \",\". The collections should contain all of the morph trackers from one individual emoticons morph", default = "morph, trackers")
    sort_morph_trackers: BoolProperty(name = "Sort the morph trackers", description = "Sort the morph trackers into bundled collections based on their names and keywords that are not part of the emoticons limb names. The collection names will include the keywords defined in the \"Collection keywords\" field", default=True)
    
    def register():
        bpy.types.Scene.emoticonsutils = bpy.props.PointerProperty(type=EMOTICONS_UTILS_Props)

    #def unregister():
    #    del bpy.types.Scene.emoticonsutils