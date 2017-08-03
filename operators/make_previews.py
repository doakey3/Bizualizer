import bpy
import os
import shutil
import ntpath

from .tools.update_progress import update_progress
from .tools.get_settings import get_settings

from .tools.check_config import check_config

from .frame_makers.make_bottom_frame import make_bottom_frame
from .frame_makers.make_top_frame import make_top_frame
from .frame_makers.make_top_bottom_frame import make_top_bottom_frame
from .frame_makers.make_left_frame import make_left_frame
from .frame_makers.make_right_frame import make_right_frame
from .frame_makers.make_left_right_frame import make_left_right_frame
from .frame_makers.make_horizontal_center_frame import make_horizontal_center_frame
from .frame_makers.make_vertical_center_frame import make_vertical_center_frame

def make_bar_heights_list(bar_count):
    bar_heights_list = []
    for i in range(bar_count):
        bar_heights_list.append(i / (bar_count - 1))
    return bar_heights_list

class MakePreviews(bpy.types.Operator):
    bl_label = 'Make Previews'
    bl_idname = 'object.make_bz_previews'
    bl_description = 'Make Preview Images'
    
    
    def execute(self, context):
        scene = context.scene
        message = check_config(scene.bbz_config)
        
        if not message == '':
            self.report(set({'ERROR'}), message)
            return {"FINISHED"}
        
        settings = get_settings(bpy.path.abspath(scene.bbz_config))
        config_folder = os.path.dirname(bpy.path.abspath(scene.bbz_config))
        preview_folder = os.path.join(config_folder, 'BZ_Previews')
        if os.path.isdir(preview_folder):
            shutil.rmtree(os.path.join(preview_folder))
        os.makedirs(preview_folder)
        
        for i in range(len(settings)):
            song_path = os.path.join(config_folder, settings[i]['Song'])
            song_name = ntpath.basename(os.path.splitext(song_path)[0])
            preview_img = os.path.join(preview_folder, song_name + '.png')
            
            bg_img_path = os.path.join(config_folder, settings[i]['Background'])
            
            bar_color = settings[i]['Bar Color']
            bar_count = settings[i]['Bar Count']
            space_fraction = settings[i]['Space Fraction']
            height_fraction = settings[i]['Height Fraction']
            bar_style = settings[i]['Bar Style']
            
            bar_color = settings[i]['Bar Color']
            
            bar_heights = make_bar_heights_list(bar_count)
            
            if bar_style == 'bottom':
                make_bottom_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'top':
                make_top_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'top-bottom':
                make_top_bottom_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'left':
                make_left_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'right':
                make_right_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'left-right':
                make_left_right_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'horizontal-center':
                make_horizontal_center_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            elif bar_style == 'vertical-center':
                make_vertical_center_frame(song_path, bg_img_path, bar_color, 
                    bar_count, space_fraction, height_fraction, bar_heights,
                    preview_img)
            
            update_progress("Making Previews", i / len(settings))
        update_progress("Making Previews", 1)
        
        return {"FINISHED"}
