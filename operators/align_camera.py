import bpy

class AlignCamera(bpy.types.Operator):
    bl_idname = "object.bz_align_camera"
    bl_label = "Align Camera"
    bl_description = "Aligns camera to bizualizer bars"

    @classmethod
    def poll(self, context):
        scene = context.scene
        if scene.camera:
            return True
        return False

    def execute(self, context):
        scene = context.scene

        camera = scene.camera
        bpy.data.cameras[camera.data.name].type = 'ORTHO'
        
        bar_count = scene.bz_bar_count
        spacing = scene.bz_spacing
        bar_width = scene.bz_bar_width
        
        res_x = scene.render.resolution_x
        res_y = scene.render.resolution_y

        extra_cushion = spacing - (bar_width * 2)
        ortho_scale = (bar_count * spacing) + extra_cushion
        bpy.data.cameras[camera.data.name].ortho_scale = ortho_scale

        loc = camera.location
        loc[0] = 0.0
        loc[1] = (ortho_scale / (res_x / res_y)) / 2
        loc[2] = 5.0

        camera.location = loc
        camera.rotation_mode = 'XYZ'
        camera.rotation_euler = [0.0, 0.0, 0.0]
        return {"FINISHED"}
