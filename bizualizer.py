import bpy
import math
import ntpath
import sys


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


class RemoveBZAudio(bpy.types.Operator):
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


class GenerateVizualizer(bpy.types.Operator):
    bl_idname = "object.bz_generate"
    bl_label = "(re)Generate Vizualizer"
    bl_description = "Generates visualizer bars and animation"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == "":
            return False
        else:
            return True

    def execute(self, context):
        scene = context.scene
        scene.frame_current = 1
        bar_count = scene.bz_bar_count
        bar_width = scene.bz_bar_width
        amplitude = scene.bz_amplitude
        spacing = scene.bz_spacing
        radius = scene.bz_radius
        audiofile = bpy.path.abspath(scene.bz_audiofile)
        digits = str(len(str(bar_count)))

        noteStep = 120.0/bar_count
        a = 2**(1.0/12.0)
        l = 0.0
        h = 16.0

        bpy.ops.object.select_all(action="DESELECT")

        count = 0
        while count < len(scene.objects):
            if scene.objects[count].name.startswith("bz_bar"):
                scene.objects[count].select = True
                bpy.ops.object.delete()
            else:
                count += 1

        wm = context.window_manager
        wm.progress_begin(0, 100.0)

        context.area.type = "GRAPH_EDITOR"
        for i in range(0, bar_count):
            name = "bz_bar" + (("%0" + digits + "d") % i)
            mesh = bpy.data.meshes.new(name)
            bar = bpy.data.objects.new(name, mesh)
            scene.objects.link(bar)
            bar.select = True
            scene.objects.active = bar
            verts = [(-1, 2, 0), (1, 2, 0), (1, 0, 0), (-1, 0, 0)]
            faces = [(3, 2, 1, 0)]
            mesh.from_pydata(verts, [], faces)
            mesh.update()

            loc = [0.0, 0.0, 0.0]

            if scene.bz_use_radial:
                angle = -2 * i * math.pi / bar_count
                bar.rotation_euler[2] = angle
                loc[0] = -math.sin(angle) * radius
                loc[1] = math.cos(angle) * radius

            else:
                loc[0] = (i * spacing) - ((bar_count * spacing) / 2)

            bar.location = (loc[0], loc[1], loc[2])

            bar.scale.x = bar_width
            bar.scale.y = amplitude
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            bpy.ops.anim.keyframe_insert_menu(type="Scaling")
            bar.animation_data.action.fcurves[0].lock = True
            bar.animation_data.action.fcurves[2].lock = True

            l = h
            h = l*(a**noteStep)

            bpy.ops.graph.sound_bake(
                filepath=audiofile, low=(l), high=(h))
            active = bpy.context.active_object
            active.animation_data.action.fcurves[1].lock = True
            bar.select = False
            progress = 100 * (i/bar_count)
            wm.progress_update(progress)
            update_progress("Generating Vizualizer", progress/100.0)

        wm.progress_end()
        update_progress("Generating Vizualizer", 1)
        context.area.type = "PROPERTIES"
        scene.objects.active = None
        return {"FINISHED"}


def update_progress(job_title, progress):
    length = 20
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
                                     "#" * block + "-" * (length-block),
                                     "%.2f" % (progress * 100))
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()
