import bpy
from bpy_extras import anim_utils
import math

from .tools.update_progress import update_progress


def make_color(name, rgb):
    if name in bpy.data.materials:
        material = bpy.data.materials[name]
    else:
        material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    nodes = material.node_tree.nodes
    for node in nodes:
        nodes.remove(node)

    node_lightpath = nodes.new(type='ShaderNodeLightPath')
    node_lightpath.location = [-200, 100]

    node_emission = nodes.new(type='ShaderNodeEmission')
    node_emission.inputs[0].default_value = (rgb[0], rgb[1], rgb[2], 1)
    node_emission.location = [0, -50]

    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_mix.location = [200, 0]

    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = [400,0]

    links = material.node_tree.links
    links.new(node_lightpath.outputs[0], node_mix.inputs[0])
    links.new(node_emission.outputs[0], node_mix.inputs[2])
    links.new(node_mix.outputs[0], node_output.inputs[0])

    return material


def get_context_area(context, context_dict, area_type='GRAPH_EDITOR',
                     context_screen=False):
    '''
    context : the current context
    context_dict : a context dictionary. Will update area, screen, scene,
                   area, region
    area_type: the type of area to search for
    context_screen: Boolean. If true only search in the context screen.
    '''
    if not context_screen:  # default
        screens = bpy.data.screens
    else:
        screens = [context.screen]
    for screen in screens:
        for area_index, area in screen.areas.items():
            if area.type == area_type:
                for region in area.regions:
                    if region.type == 'WINDOW':
                        context_dict["area"] = area
                        context_dict["screen"] = screen
                        context_dict["scene"] = context.scene
                        context_dict["window"] = context.window
                        context_dict["region"] = region
                        return area
    return None


class RENDER_OT_generate_visualizer(bpy.types.Operator):
    bl_idname = "object.bz_generate"
    bl_label = "(re)Generate Visualizer"
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
                scene.objects[count].select_set(True)
                bpy.ops.object.delete()
            else:
                count += 1

        wm = context.window_manager
        wm.progress_begin(0, 100.0)

        for i in range(0, bar_count):
            name = "bz_bar" + (("%0" + digits + "d") % i)
            mesh = bpy.data.meshes.new(name)
            bar = bpy.data.objects.new(name, mesh)
            scene.collection.objects.link(bar)
            bar.select_set(True)
            bpy.context.view_layer.objects.active = bar
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

                if bar_count % 2 == 0:
                    loc[0] += spacing / 2

            bar.location = (loc[0], loc[1], loc[2])

            bar.scale.x = bar_width
            bar.scale.y = amplitude

            c = {attr_name: getattr(bpy.context, attr_name) for attr_name in dir(bpy.context) if attr_name != 'grease_pencil'}

            get_context_area(bpy.context, c)

            bpy.ops.object.transform_apply(
                location=False, rotation=False, scale=True)

            bpy.ops.anim.keyframe_insert_menu(type="Scaling")
            anim_data = bar.animation_data
            action = anim_data.action
            slot = anim_data.action_slot

            channelbag = anim_utils.action_get_channelbag_for_slot(action, slot)
            for fcu in channelbag.fcurves:
                if fcu.data_path == "scale" and fcu.array_index in (0, 2):
                    fcu.lock = True

            l = h
            h = l*(a**noteStep)

            area = bpy.context.area.type
            bpy.context.area.type = 'GRAPH_EDITOR'

            bpy.ops.graph.sound_to_samples(filepath=audiofile, low=(l), high=(h))

            bpy.context.area.type = area

            active = bpy.context.active_object
            anim_data = active.animation_data
            action = anim_data.action
            slot = anim_data.action_slot

            channelbag = anim_utils.action_get_channelbag_for_slot(action, slot)

            for fcu in channelbag.fcurves:
                if fcu.data_path == "scale" and fcu.array_index == 1:
                    fcu.lock = True

            red = scene.bz_color[0]
            green = scene.bz_color[1]
            blue = scene.bz_color[2]
            material = make_color('bz_color', [red, green, blue])
            active.active_material = material

            bar.select_set(False)
            progress = 100 * (i/bar_count)
            wm.progress_update(progress)
            update_progress("Generating Visualizer", progress/100.0)

        wm.progress_end()
        update_progress("Generating Visualizer", 1)
        bpy.context.view_layer.objects.active = None
        return {"FINISHED"}
