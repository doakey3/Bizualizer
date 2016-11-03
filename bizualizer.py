bl_info = {
    "name": "Bizualizer",
    "description": "Create a simple vizualizer for audio",
    "author": "doakey3",
    "version": (1, 0, 3),
    "blender": (2, 7, 8),
    "wiki_url": "https://github.com/doakey3/Bizualizer",
    "tracker_url": "https://github.com/doakey3/Bizualizer/issues",
    "category": "Animation",
    "location": "Properties > Scene"}

import bpy
import math
import ntpath
import time
import sys

class BizualizerUI(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_label = "Bizualizer"
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        row = layout.row()
        row.prop(scene,'bz_audiofile',icon="SOUND")
        row = layout.row()
        row.prop(scene,'bz_audio_channel')
        row = layout.row()
        row.operator("sequencerextra.bz_audio_to_sequencer",
            icon="SEQ_SEQUENCER")
        row.operator("sequencerextra.bz_audio_remove",icon="CANCEL")
        row = layout.row()
        row.prop(scene,'bz_bar_count')
        row.prop(scene,'bz_bar_width')
        row = layout.row()
        row.prop(scene,'bz_amplitude')
        row.prop(scene,'bz_spacing')
        row = layout.row()
        split = row.split()
        col_a = split.column(align=True)
        col_a.prop(scene,'bz_use_radial')
        col_b = split.column(align=True)
        col_b.prop(scene,'bz_radius')
        if scene.bz_use_radial:
            col_b.enabled = True
        else:
            col_b.enabled = False
        row = layout.row()
        row.operator("object.bz_generate",icon="RADIO")

class AudioToVSE(bpy.types.Operator):
    bl_idname = "sequencerextra.bz_audio_to_sequencer"
    bl_label = "Add Audio to VSE"
    bl_description = "Adds the audio file to the VSE"
    
    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == '':
            return False                 
        else:
            return True
            
    def execute(self, context):
        scene = context.scene
        audiofile = bpy.path.abspath(scene.bz_audiofile)
        name = ntpath.basename(audiofile)
        chan = scene.bz_audio_channel
        start = 1
        if not scene.sequence_editor:
            scene.sequence_editor_create()
            
        sound_strip = scene.sequence_editor.sequences.new_sound(
            'bz_' + name,audiofile,chan,start)
        return {'FINISHED'}

class RemoveBZAudio(bpy.types.Operator):
    bl_idname = "sequencerextra.bz_audio_remove"
    bl_label = "Remove Audio"
    bl_description = "Adds the audio file to the VSE"
    
    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == '':
            return False                 
        else:
            return True
    
    def execute(self, context):
        scene = context.scene
        audiofile = bpy.path.abspath(scene.bz_audiofile)
        name = ntpath.basename(audiofile)
        all_strips = list(sorted(
            bpy.context.scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        bpy.ops.sequencer.select_all(action='DESELECT')
        count = 0
        for strip in all_strips:
            if strip.name.startswith('bz_' + name):
                strip.select = True
                bpy.ops.sequencer.delete()
                
        return {'FINISHED'}
                

class GenerateVizualizer(bpy.types.Operator):
    bl_idname = "object.bz_generate"
    bl_label = "(re)Generate Vizualizer"
    bl_description = "Generates visualizer bars and animation"
    
    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.bz_audiofile == '':
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
        
        bpy.ops.object.select_all(action='DESELECT')
        
        #Remove any visualizer bars in the scene
        count = 0
        while count < len(scene.objects):
            if scene.objects[count].name.startswith('bz_bar'):
                scene.objects[count].select = True
                bpy.ops.object.delete()
            else:
                count += 1
        
        wm = context.window_manager
        wm.progress_begin(0, 100.0)
        
        context.area.type = 'GRAPH_EDITOR'
        for i in range(0, bar_count):
            #Add a plane with it's origin = center
            name = 'bz_bar' + (("%0" + digits + "d") % i)
            mesh = bpy.data.meshes.new(name)
            bar = bpy.data.objects.new(name,mesh)
            scene.objects.link(bar)
            bar.select = True
            scene.objects.active = bar
            verts = [(-1,2,0), (1,2,0), (1,0,0), (-1,0,0)]
            faces = [(3,2,1,0)]
            mesh.from_pydata(verts,[],faces)
            mesh.update()
            
            loc = [0.0, 0.0, 0.0]
            
            #If radial, rotate the bar around an angle
            if scene.bz_use_radial:
                angle = -2 * i * math.pi/bar_count
                bar.rotation_euler[2] = angle
                loc[0] = -math.sin(angle) * radius
                loc[1] = math.cos(angle) * radius
            
            else:
                loc[0] = (i * spacing) - ((bar_count * spacing)/2)
            
            #Set the bar's current location
            bar.location = (loc[0], loc[1], loc[2])
            
            #Scale the plane on x and y axis
            bar.scale.x = bar_width
            bar.scale.y = amplitude
            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)
            
            #Insert a scaling keyframe and lock the x and z axis
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            bar.animation_data.action.fcurves[0].lock = True
            bar.animation_data.action.fcurves[2].lock = True
            
            l = h
            h = l*(a**noteStep)
            
            bpy.ops.graph.sound_bake(
                filepath=audiofile, low=(l),high=(h))
            active = bpy.context.active_object
            active.animation_data.action.fcurves[1].lock = True
            bar.select = False
            progress = 100 * (i/bar_count)
            wm.progress_update(progress)
            update_progress("Generating Vizualizer", progress/100.0)
        
        wm.progress_end()
        update_progress("Generating Vizualizer", 1)
        context.area.type = 'PROPERTIES'
        scene.objects.active = None
        return {'FINISHED'}
        
def update_progress(job_title, progress):
    length = 20 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
        "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()

def initprop():
    bpy.types.Scene.bz_audiofile = bpy.props.StringProperty(
        name = "Audio File",
        description = "Define path of the audio file",
        subtype = 'FILE_PATH',
        )
    
    bpy.types.Scene.bz_audio_channel = bpy.props.IntProperty(
        name = "Audio Channel",
        description="Channel where audio will be added",
        default=1,
        min=1)
    
    bpy.types.Scene.bz_bar_count = bpy.props.IntProperty(
        name = "Bar Count",
        description="The number of bars to make",
        default=64,
        min=1)
    
    bpy.types.Scene.bz_bar_width = bpy.props.FloatProperty(
        name = "Bar Width",
        description="The width of the bars",
        default=0.8,
        min=0)
    
    bpy.types.Scene.bz_amplitude = bpy.props.FloatProperty(
        name = "Amplitude",
        description="Amplitude of visualizer bars",
        default=24.0,
        min=0)
    
    bpy.types.Scene.bz_use_radial = bpy.props.BoolProperty(
        name = "Use Radial",
        description="Use a circular vizualizer",
        default=False)
        
    bpy.types.Scene.bz_radius = bpy.props.FloatProperty(
        name = "Radius",
        description="Radius of the radial vizualizer",
        default=20,
        min=0)
    
    bpy.types.Scene.bz_spacing = bpy.props.FloatProperty(
        name = "Spacing",
        description="Spacing between bars",
        default=2.25,
        min=0)

def register():
    bpy.utils.register_class(BizualizerUI)
    bpy.utils.register_class(AudioToVSE)
    bpy.utils.register_class(GenerateVizualizer)
    bpy.utils.register_class(RemoveBZAudio)
    
    initprop()
    
def unregister():
    bpy.utils.unregister_class(BizualizerUI)
    bpy.utils.unregister_class(AudioToVSE)
    bpy.utils.unregister_class(RemoveBZAudio)
    bpy.utils.unregister_class(GenerateVizualizer)
    
    del bpy.types.Scene.bz_audiofile
    del bpy.types.Scene.bz_bar_count
    del bpy.types.Scene.bz_bar_width
    del bpy.types.Scene.bz_amplitude
    del bpy.types.Scene.bz_spacing
    del bpy.types.Scene.bz_use_radial
    del bpy.types.Scene.bz_radius
