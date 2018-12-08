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

        if not scene.sequence_editor:
            return {"FINISHED"}

        audiofile = bpy.path.abspath(scene.bz_audiofile)
        name = ntpath.basename(audiofile)
        all_strips = list(sorted(
            bpy.context.scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        bpy.ops.sequencer.select_all(action="DESELECT")
        count = 0
        for strip in all_strips:
            if strip.name.startswith("bz_" + name):
                strip.select = True
                bpy.ops.sequencer.delete()

        return {"FINISHED"}
