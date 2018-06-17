import bpy
import os
import ntpath
import csv

import shutil
import sys
import subprocess

from .tools.update_progress import update_progress
from .tools.get_settings import get_settings

from .tools.check_config import check_config
from .tools.collect_bar_heights_list import collect_bar_heights_list
from .tools.hexcode_to_color import hexcode_to_color

from .frame_makers.make_bottom_frame import make_bottom_frame
from .frame_makers.make_top_frame import make_top_frame
from .frame_makers.make_top_bottom_frame import make_top_bottom_frame
from .frame_makers.make_left_frame import make_left_frame
from .frame_makers.make_right_frame import make_right_frame
from .frame_makers.make_left_right_frame import make_left_right_frame
from .frame_makers.make_horizontal_center_frame import make_horizontal_center_frame
from .frame_makers.make_vertical_center_frame import make_vertical_center_frame

import sys
sys.path.append(os.path.dirname(__file__))
import piexif

def make_heights_list(bar_heights, index):
    heights = []
    for i in range(len(bar_heights)):
        heights.append(bar_heights[i][index])
    return heights

def insert_jpg_name(image_path):
    from PIL import Image
    exif_dict = piexif.load(image_path)
    exif_dict["0th"][269] = ntpath.basename(image_path)
    exif_bytes = piexif.dump(exif_dict)

    img = Image.open(image_path)
    img.save(image_path, exif=exif_bytes)

def insert_mp4_artwork(mp4_path, artwork_path):
    from mutagen.mp4 import MP4, MP4Cover
    mp4 = MP4(mp4_path)

    f = open(artwork_path, 'rb')
    artwork = f.read()
    f.close()

    mp4['covr'] = [MP4Cover(artwork, imageformat=MP4Cover.FORMAT_JPEG)]
    mp4.save()


def make_mp4(song_path, bg_img_path, bar_color, bar_count, space_fraction,
             height_fraction, bar_heights_list, frame_rate,
             total_time, bar_style, fade):
    """Create frames, then make an MP4"""
    from PIL import Image
    frames_path = os.path.splitext(song_path)[0] + '_frames'
    if os.path.isdir(frames_path):
        shutil.rmtree(frames_path)
    os.mkdir(frames_path)

    # BG img must be divisible by 2
    img = Image.open(bg_img_path)
    if not img.size[0] / 2 == int(img.size[0] / 2):
        img = img.resize([img.size[0] + 1, img.size[1]])
        img.save(bg_img_path)
    if not img.size[1] / 2 == int(img.size[1] /2):
        img = img.resize([img.size[0], img.size[1] + 1])
        img.save(bg_img_path)

    for i in range(len(bar_heights_list[0])):
        heights = make_heights_list(bar_heights_list, i)
        outfile = os.path.join(frames_path, "%09d" % i + ".png")
        if bar_style == 'bottom':
            make_bottom_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'top':
            make_top_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'top-bottom':
            make_top_bottom_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'left':
            make_left_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'right':
            make_right_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'left-right':
            make_left_right_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'horizontal-center':
            make_horizontal_center_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)
        elif bar_style == 'vertical-center':
            make_vertical_center_frame(
                song_path, bg_img_path, bar_color, bar_count,
                space_fraction, height_fraction, heights, outfile)

        progress = (i / len(bar_heights_list[0]))
        update_progress("Generating Frames", progress)
    update_progress("Generating Frames", 1)
    frames = '"' + os.path.join(frames_path, '%09d.png') + '"'
    mp3 = '"' + song_path + '"'
    mp4 = '"' + os.path.splitext(song_path)[0] + '.mp4' + '"'

    fadeout_start = int((frame_rate * total_time) - frame_rate)


    filter_line = ''.join([
        'fade=in:0:', str(frame_rate),
        ',fade=out:', str(fadeout_start), ':', str(frame_rate)
        ])

    command = [
        'ffmpeg', '-r', str(frame_rate), '-i', frames, '-i', mp3,
        '-codec:v', 'libx264', '-codec:a', 'copy',
        '-pix_fmt', 'yuv420p', '-y']

    if fade == True:
        command.append('-vf')
        command.append(filter_line)

    command.append(mp4)

    command = ' '.join(command)

    subprocess.call(command, shell=True)

    shutil.rmtree(frames_path)

    img = Image.open(bg_img_path)
    img = img.convert('RGB')
    jpg_path = os.path.splitext(bg_img_path)[0] + '.jpg'

    img.save(jpg_path)

    insert_jpg_name(jpg_path)

    mp4 = os.path.splitext(song_path)[0] + '.mp4'

    insert_mp4_artwork(os.path.splitext(song_path)[0] + '.mp4', jpg_path)

def space_fill(count, symbol):
    """makes a string that is count long of symbol"""
    x = ""
    for i in range(0, count):
        x = x + symbol
    return x


class BatchBizualize(bpy.types.Operator):
    bl_label = 'Batch Bizualize'
    bl_idname = 'object.batch_bizualize'
    bl_description = 'Generate MP4 Files with Bizualizers based on the config file.\nSee Github page for how to enable this'

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            from PIL import Image
            from mutagen.mp4 import MP4, MP4Cover
            from mutagen.mp3 import MP3
        except ImportError:
            return False
        if os.path.isfile(scene.bbz_config) and scene.bbz_config.endswith('.csv'):
            return True
        else:
            return False

    def execute(self, context):
        from mutagen.mp3 import MP3
        scene = context.scene
        message = check_config(scene.bbz_config)

        if not message == '':
            self.report(set({'ERROR'}), message)
            return {"FINISHED"}

        settings = get_settings(bpy.path.abspath(scene.bbz_config))
        config_folder = os.path.dirname(bpy.path.abspath(scene.bbz_config))

        for i in range(len(settings)):

            song_path = os.path.join(config_folder, settings[i]['Song'])
            vid_path = os.path.splitext(song_path)[0] + '.mp4'
            if os.path.isfile(vid_path):
                os.remove(vid_path)

            frame_rate = scene.render.fps / scene.render.fps_base
            total_time = MP3(song_path).info.length

            scene.frame_end = int(frame_rate * total_time)

            print('')
            print(settings[i]['Song'])
            print(space_fill(len(settings[i]['Song']), '='))

            bg_img_path = os.path.join(config_folder, settings[i]['Background'])
            bar_color = settings[i]['Bar Color']
            bar_count = settings[i]['Bar Count']
            space_fraction = settings[i]['Space Fraction']
            height_fraction = settings[i]['Height Fraction']
            bar_style = settings[i]['Bar Style']
            fade = settings[i]['Fade']

            bar_color = settings[i]['Bar Color']

            bar_heights_list = collect_bar_heights_list(song_path, bar_count, scene)

            make_mp4(
                song_path, bg_img_path, bar_color, bar_count, space_fraction,
                height_fraction, bar_heights_list, frame_rate,
                total_time, bar_style, fade)
            print('')

        return {"FINISHED"}
