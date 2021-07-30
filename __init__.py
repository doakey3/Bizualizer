import bpy
import os
import shutil

from .operators import *

bl_info = {
    "name": "Bizualizer-français",
    "description": "Créer un simple visualiseur pour l'audio",
    "author": "doakey3, boubajoker",
    "version": (1, 2, 4),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/doakey3/Bizualizer",
    "tracker_url": "https://github.com/doakey3/Bizualizer/issues",
    "category": "Animation",
    "location": "Properties > Scene"}


class RENDER_PT_ui(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_label = "Bizualizer"
    bl_context = "scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        row = layout.row()
        row.prop(scene, "bz_audiofile", icon="SOUND")
        row = layout.row()
        row.prop(scene, "bz_audio_channel")
        row = layout.row()
        row.operator("sequencerextra.bz_audio_to_sequencer",
                     icon="SEQ_SEQUENCER")
        row.operator("sequencerextra.bz_audio_remove", icon="CANCEL")
        row = layout.row()
        row.prop(scene, "bz_bar_count")
        row.prop(scene, "bz_bar_width")
        row = layout.row()
        row.prop(scene, "bz_amplitude")
        row.prop(scene, "bz_spacing")
        row = layout.row()
        row.prop(scene, "bz_color")
        row = layout.row()
        split = row.split()
        col_a = split.column(align=True)
        col_a.prop(scene, "bz_use_radial")
        col_b = split.column(align=True)
        col_b.prop(scene, "bz_radius")
        if scene.bz_use_radial:
            col_b.enabled = True
        else:
            col_b.enabled = False
        row = layout.row()
        row.operator("object.bz_generate", icon="FILE_REFRESH")
        row = layout.row()
        row.operator("object.bz_align_camera", icon="CAMERA_DATA")

        box = layout.box()
        row = box.row()
        row.prop(scene, 'bbz_config')
        row = box.row()
        row.operator('object.batch_bizualize', icon="ALIGN_LEFT")
        row.operator('object.make_bz_previews')

def initprop():
    bpy.types.Scene.bz_audiofile = bpy.props.StringProperty(
        name="Chemin audio",
        description="definire le chemin du fichier audio",
        subtype="FILE_PATH",
        )

    bpy.types.Scene.bz_audio_channel = bpy.props.IntProperty(
        name="chaîne audio",
        description="Chaîne où l'audio va être ajouté",
        default=1,
        min=1
        )

    bpy.types.Scene.bz_bar_count = bpy.props.IntProperty(
        name="nombre de bars",
        description="le nombre de bars a mettre",
        default=64,
        min=1
        )

    bpy.types.Scene.bz_bar_width = bpy.props.FloatProperty(
        name="Taille des barre",
        description="la taille des barres",
        default=0.8,
        min=0
        )

    bpy.types.Scene.bz_amplitude = bpy.props.FloatProperty(
        name="Amplitude",
        description="Amplitude des barres visualiseuses",
        default=24.0,
        min=0
        )

    bpy.types.Scene.bz_color = bpy.props.FloatVectorProperty(
        name="Barrre de  Couleur",
        subtype='COLOR_GAMMA',
        description="Couleurs appliquées aux bares après que le visualizeur est géneré",
        size=3,
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,)

    bpy.types.Scene.bz_use_radial = bpy.props.BoolProperty(
        name="Utiliser un visualiseur Radieux",
        description="Utuliser un visualizeur circulaire",
        default=False
        )

    bpy.types.Scene.bz_radius = bpy.props.FloatProperty(
        name="Émision",
        description="émission visualizer",
        default=20,
        min=0
        )

    bpy.types.Scene.bz_spacing = bpy.props.FloatProperty(
        name="Espacement",
        description="Escapacement entre les bars",
        default=2.25,
        min=0
        )

    bpy.types.Scene.bbz_config = bpy.props.StringProperty(
        name="fichier de configuration",
        description="chemin de configuration du fichier",
        subtype="FILE_PATH",
        )

classes = [
    RENDER_PT_ui,
    RENDER_OT_align_camera,
    RENDER_OT_audio_to_vse,
    RENDER_OT_batch_bizualize,
    RENDER_OT_generate_visualizer,
    RENDER_OT_make_previews,
    RENDER_OT_remove_bz_audio
]

def register():
    initprop()

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
