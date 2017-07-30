import bpy
import ntpath

class AudioToVSE(bpy.types.Operator):
    bl_idname = "sequencerextra.bz_audio_to_sequencer"
    bl_label = "Add Audio to VSE"
    bl_description = "Adds the audio file to the VSE"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == "":
            return False
        else:
            return True

    def execute(self, context):

        bpy.ops.sequencerextra.bz_audio_remove()
        
        scene = context.scene
        audiofile = bpy.path.abspath(scene.bz_audiofile)
        name = ntpath.basename(audiofile)
        chan = scene.bz_audio_channel
        start = 1
        if not scene.sequence_editor:
            scene.sequence_editor_create()

        sound_strip = scene.sequence_editor.sequences.new_sound(
            "bz_" + name, audiofile, chan, start)

        

        frame_start = 300000
        frame_end = -300000
        for strip in scene.sequence_editor.sequences:
            try:
                if strip.frame_final_start < frame_start:
                    frame_start = strip.frame_final_start
                if strip.frame_final_end > frame_end:
                    frame_end = strip.frame_final_end - 1
            except AttributeError:
                pass

        if frame_start != 300000:
            scene.frame_start = frame_start
        if frame_end != -300000:
            scene.frame_end = frame_end

        return {"FINISHED"}
