# Emoticons Utils add-on
This Blender add-on adds utility functions to work with Emoticons inside Blender. The add-on is located in the tool shelf here:
![Screenshot_338](https://user-images.githubusercontent.com/71967555/164560401-a2bf7c2c-2f59-4f03-8cf7-abf334028ac5.png)

# Functionalities

**Mixamo to Emoticons converter**

**IMPORTANT!**
Mixamo changed the rig of the X-Bot character, which means you need to upload the old rig provided in this file `mixamo_old_rig.fbx` and use it ![Screenshot_629](https://user-images.githubusercontent.com/71967555/201525241-db40f01b-bc39-4d54-9350-4691255a0385.png)

You can convert Mixamo rigs / animation to Emoticons rigs. You just import the FBX file of mixamo and the emoticons rig and select them in the menu. You also have options to, for example, also conver the hand animation or limit the rotation axis for some limbs. Every button has a tooltip for further explanations.
<hr>

**Apply morph trackers**

This is for morph trackers exported by the Aperture mod. If you track an emoticons morph, you can use this functionality to automatically attach an emoticons rig to the individual limb trackers. This is especially helpful if you want to track a lot of emoticons morphs. The add-on will then copy the specified emoticons armature for the emoticons morphs trackers. The add-on basically does everything for you.

**IMPORTANT: the morph trackers in the emoticons morphs need to contain these keywords in order to be detected: 'low', 'arm', 'leg', 'left', 'right', 'body', 'anchor', '.end', 'head'.**

It is okay if you don't want to track, for example, the anchor or end bones, however if you do track them, they need to contain the specified keywords so the add-on knows where to attach them.
