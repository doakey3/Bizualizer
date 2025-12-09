import bpy
import ntpath

class RENDER_OT_remove_bz_audio(bpy.types.Operator):
    bl_idname = "sequencerextra.bz_audio_remove"
    bl_label = "Remove Audio"
    bl_description = "Adds the audio file to the VSE"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == "":
            return False
        else:
            return True

    def execute(self, context):
        scene = context.scene
        seq = scene.sequence_editor
        if not seq:
            return {'CANCELLED'}

        to_remove = [strip for strip in seq.strips_all
                     if strip.name.startswith("bz_")]

        for strip in to_remove:
            try:
                seq.strips.remove(strip)
            except RuntimeError:
                pass

        return {'FINISHED'}
