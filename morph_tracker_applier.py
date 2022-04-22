import bpy

class EMOTICONS_UTILS_PT_morph_tracker_panel(bpy.types.Panel):
    bl_label = "Apply morph trackers"
    bl_idname = "EMOTICONS_UTILS_PT_morph_tracker_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emoticons Utils"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        properties = scene.emoticonsutils
        
        layout.prop_search(properties, "tracker_emoticons_armature", scene, "objects", text="Emoticons")
        layout.prop_search(properties, "trackers_root_collection", bpy.data, "collections", text="Collection")

        layout.prop(properties, "tracker_collection_keywords")
        layout.prop(properties, "sort_morph_trackers")
        layout.label(text="Copy the armature and apply the trackers")
        layout.operator("emoticons_utils.apply_morph_trackers")
        
class EMOTICONS_UTILS_OT_apply_morph_trackers(bpy.types.Operator):
    bl_label = "Apply morph trackers"
    bl_idname = "emoticons_utils.apply_morph_trackers"
    keywords = ["low", "right", "left", "arm", ".end", "leg", "anchor", "body", "head"]
    
    def execute(self, context):
        scene = context.scene
        properties = scene.emoticonsutils

        if properties.trackers_root_collection is None:
            self.report({'ERROR'}, 'Trackers root collection is not selected')

            return {"CANCELLED"}
        
        if properties.tracker_collection_keywords.split(",") == "":
            self.report({'ERROR'}, 'Tracker collection keywords can not be empty')

            return {"CANCELLED"}

        if properties.tracker_emoticons_armature is None:
            self.report({'ERROR'}, 'Emoticons armature is not selected')

            return {"CANCELLED"}

        #parse collection keywords -> convert multiple spaces to one space and remove comma separator
        collectionBaseName = " ".join((" ".join(properties.tracker_collection_keywords.split(","))).split())

        if properties.sort_morph_trackers:
            for object in properties.trackers_root_collection.objects:

                #ignore object if the name is not a valid emoticons morph tracker name or if the object has a parent
                if not object.parent is None or self.parseName(object.name) == None:
                    continue

                #remove all _
                customName = object.name.replace("_", " ")

                #remove all the emoticon limb names
                for emoticonsKey in self.keywords:
                    customName = customName.replace(emoticonsKey, " ")

                #remove all .
                customName = customName.replace(".", " ")

                #split the customname using dynamic amount of spaces
                customKeywords = customName.split()

                #join the keywords using only one space
                customKeywords = " ".join(customKeywords)

                collectionName = collectionBaseName + " " + customKeywords

                trackerCollectionIndex = properties.trackers_root_collection.children.find(collectionName)
                trackerCollection = None

                if trackerCollectionIndex == -1:
                    trackerCollection = bpy.data.collections.new(collectionName)

                    properties.trackers_root_collection.children.link(trackerCollection)
                else:
                    trackerCollection = properties.trackers_root_collection.children[trackerCollectionIndex]

                for coll in object.users_collection:
                    coll.objects.unlink(object)
                
                trackerCollection.objects.link(object)


        #go through the tracker collections
        for coll in properties.trackers_root_collection.children:

            #check if every keyword is in the current collection name
            if not all(keyword in coll.name for keyword in (" ".join(properties.tracker_collection_keywords.split(","))).split()):
                continue

            srcArmature = properties.tracker_emoticons_armature
            srcChildren = srcArmature.children #the parent model objects
            armature = srcArmature.copy()
        
            self.linkObject(armature, srcArmature)
            
            #copy the models of the armature
            for child in srcChildren:
                childCopy = child.copy()
                
                self.linkObject(childCopy, srcArmature)
                
                if bpy.context.view_layer.objects.active is not None:
                    bpy.context.view_layer.objects.active.select_set(False)
                
                #first select child then armature to parent them using operators
                bpy.context.view_layer.objects.active = childCopy
                childCopy.select_set(True)
                bpy.ops.object.parent_clear(type='CLEAR')
                
                bpy.context.view_layer.objects.active = armature
                armature.select_set(True)
                
                bpy.ops.object.parent_set(type='ARMATURE')
                
                childCopy.select_set(False)
                armature.select_set(False)
            
            armature.name = coll.name
            
            #go through the trackers in the collection
            for object in coll.objects:
                boneName = self.parseName(object.name)
                
                boneindex = armature.pose.bones.find(boneName)
                
                #get the bone in the emoticons armature from the parsed name
                if boneindex != -1:
                    bone = armature.pose.bones[boneindex]
                    
                    constraint = bone.constraints.new('COPY_TRANSFORMS')
                    constraint.target = object
                    constraint.subtarget = object.data.bones[0].name

        return {'FINISHED'}

    def linkObject(self, obj, src):
        for collection in src.users_collection:
            collection.objects.link(obj)

    def parseName(self, name):
        if "low" in name:
            if "right" in name:
                if "arm" in name:
                    if ".end" in name:
                        return "low_right_arm.end"
                    else:
                        return "low_right_arm"
                elif "leg" in name:
                    return "low_leg_right"
            elif "left" in name:
                if "arm" in name:
                    if ".end" in name:
                        return "low_left_arm.end"
                    else:
                        return "low_left_arm"
                elif "leg" in name:
                    return "low_left_leg"
            elif "body" in name:
                return "low_body"
        else:
            if "anchor" in name:
                return "anchor"
            elif "body" in name:
                return "body"
            elif "head" in name:
                return "head"
            elif "right" in name:
                if "arm" in name:
                    return "right_arm"
                elif "leg" in name:
                    return "right_leg"
            elif "left" in name:
                if "arm" in name:
                    return "left_arm"
                elif "leg" in name:
                    return "left_leg"