import bpy
import mathutils
import math

class EMOTICONS_UTILS_PT_mixamo_panel(bpy.types.Panel):
    bl_label = "Convert Mixamo to Emoticons"
    bl_idname = "EMOTICONS_UTILS_PT_mixamo_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emoticons Utils"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.emoticonsutils
        
        layout.prop_search(properties, "emoticons_armature", scene, "objects", text="Emoticons")
        layout.prop_search(properties, "mixamo_armature", scene, "objects", text="Mixamo")

        layout.label(text="Frame range:")
        layout.prop(properties, "frame_start")
        layout.prop(properties, "frame_end")
        layout.prop(properties, "frame_step")
        
        layout.prop(properties, "use_hands")
        layout.prop(properties, "use_human_parent_space")
        layout.prop(properties, "limit_rotation_axis")
        layout.prop(properties, "use_euler_filter")

        layout.label(text="Convert and copy the animation")
        layout.operator("emoticons_utils.convert_mixamo")
        
class EMOTICONS_UTILS_OT_convert_mixamo(bpy.types.Operator):
    bl_label = "Convert Mixamo"
    bl_idname = "emoticons_utils.convert_mixamo"
    
    def execute(self, context):
        scene = context.scene
        properties = scene.emoticonsutils

        if properties.emoticons_armature is None or properties.mixamo_armature is None:
            self.report({'ERROR'}, 'Emoticons or Mixamo armature is not selected')

            return {"CANCELLED"}
        
        for frame in range(properties.frame_start, properties.frame_end + 1, properties.frame_step):
            scene.frame_set(frame)
    
            #go through every mixamo bone
            for mixamoBone in properties.mixamo_armature.pose.bones:
                boneName = self.parseMixamoName(mixamoBone.name, properties)
        
                if boneName == None:
                    continue
        
                deltarotation = self.getDeltaRotation(boneName)
        
                rotation = mathutils.Quaternion((mixamoBone.rotation_quaternion[0],
                mixamoBone.rotation_quaternion[1],
                mixamoBone.rotation_quaternion[2],
                mixamoBone.rotation_quaternion[3]))
        
                rotation = rotation @ deltarotation
        
                boneindex = properties.emoticons_armature.pose.bones.find(boneName)
                
                #get the bone in the emoticons armature from the parsed name
                if boneindex != -1:
                    bone = properties.emoticons_armature.pose.bones[boneindex]
                    
                    bone.rotation_quaternion = rotation
                        
                    if "body" in bone.name:
                        if "low" in bone.name:
                            if properties.use_human_parent_space:
                                bone.rotation_quaternion = self.getParentSpace(mixamoBone, 2) @ bone.rotation_quaternion
                        else:
                            bone.location = mixamoBone.location * 0.01 #mixamo armature object is scaled with 0.01
                        
                            bone.location[0] *= -1
                            bone.location[1] *= 1
                            bone.location[2] *= -1
                        
                        self.mirrorQuat(bone.rotation_quaternion, 'Y')
                    elif "arm" in bone.name:
                        if ".end" in bone.name:
                            self.mirrorQuat(bone.rotation_quaternion, 'X')
                        
                        if "low" in bone.name:
                            self.swapComponents(bone.rotation_quaternion, 1, 2)
                        
                            if "left" in bone.name:
                                self.mirrorQuat(bone.rotation_quaternion, 'YZ')
                            if "right" in bone.name:
                                self.mirrorQuat(bone.rotation_quaternion, 'XZ')
                        else:
                            #take into account shoulder space
                            if properties.use_human_parent_space:
                                bone.rotation_quaternion = self.getParentSpace(mixamoBone, 1) @ bone.rotation_quaternion
                        
                            self.mirrorQuat(bone.rotation_quaternion, 'Z')
                    elif "leg" in bone.name:
                        self.mirrorQuat(bone.rotation_quaternion, 'Z')
                    elif "head" in bone.name:
                        #take into account neck space
                        if properties.use_human_parent_space:
                            bone.rotation_quaternion = self.getParentSpace(mixamoBone, 1) @ bone.rotation_quaternion
                    
                    bone.rotation_euler = bone.rotation_quaternion.to_euler()
                    
                    if properties.limit_rotation_axis and ("low" in bone.name and (("arm" in bone.name and not ".end" in bone.name) or "leg" in bone.name)):
                        bone.rotation_euler[1] = 0
                        bone.rotation_euler[2] = 0
                    
                    bone.keyframe_insert(data_path="rotation_euler", frame=frame)
                    bone.keyframe_insert(data_path="location", frame=frame)
                    
        if (properties.frame_end - properties.frame_start + 1) > 1:
            self.selectSoloObj(properties.emoticons_armature)
            
            for bone in properties.emoticons_armature.pose.bones:
                bpy.context.object.data.bones.active = bone.bone
                
            self.eulerFilter(properties)
            
        return {'FINISHED'}
        
    def parseMixamoName(self, name, properties):
        name = name.lower()
    
        if "up" in name:
            if "left" in name:
                if "leg" in name:
                    return "left_leg"
            elif "right" in name:
                if "leg" in name:
                    return "right_leg"
        else:
            if "hips" in name:
                return "body"
            elif "head" in name and not "end" in name:
                return "head"
            elif "spine2" in name:
                return "low_body"
            elif "left" in name:
                if "arm" in name:
                    if "fore" in name:
                        return "low_left_arm"
                    else:
                        return "left_arm"
                elif "leg" in name:
                    return "low_left_leg"
                elif "mixamorig:lefthand" == name and properties.use_hands:
                    return "low_left_arm.end"
            elif "right" in name:
                if "arm" in name:
                    if "fore" in name:
                        return "low_right_arm"
                    else:
                        return "right_arm"
                elif "leg" in name:
                    return "low_leg_right"
                elif "mixamorig:righthand" == name and properties.use_hands:
                    return "low_right_arm.end"
            
    #this method mirrors the quaternion using one axis or a plane
    def mirrorQuat(self, quat, axis):
        axis.upper()
        
        indices = [1,2,3]
        
        indices[ord(axis[0]) - 88] = -1
        
        if len(axis) == 2:
            indices[ord(axis[1]) - 88] = -1
            
        for i in indices:
            if i != -1:
                quat[i] *= -1
        
    def swapComponents(self, quat, i, j):
        tmp = quat[i]
        quat[i] = quat[j]
        quat[j] = tmp
    
            
    def getDeltaRotation(self, name):
        if "arm" in name and not "low" in name:
            if "left" in name:
                return mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(90.0))
            elif "right" in name:
                return mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(-90.0))
        
        return mathutils.Quaternion((0.0, 0.0, 0.0), math.radians(0.0))

    def getParentSpace(self, bone, depth):
        if depth == 1:
            return bone.parent.rotation_quaternion

        return self.getParentSpace(bone.parent, depth - 1) @ bone.parent.rotation_quaternion
            
    def eulerFilter(self, properties):
        if not properties.use_euler_filter:
            return
        
        window = bpy.context.window
        screen = window.screen

        #avoid TOPBAR - for some reason it caused problems
        for area in screen.areas:
            if area.type != 'TOPBAR':
                oldtype = area.type
                area.type = 'GRAPH_EDITOR'
                override = {'window': window, 'screen': screen, 'area': area}

                bpy.ops.graph.euler_filter(override)
                area.type = oldtype

                break
        
    def selectSoloObj(self, obj):
        #make the obj the only selected active object
        if bpy.context.view_layer.objects.active is not None:
            bpy.context.view_layer.objects.active.select_set(False)
            
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)