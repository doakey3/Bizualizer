import bpy
from .find_fcurve import find_fcurve

def collect_bar_heights_list(song_path, bar_count, scene):
    """Analyze the song and get the y_scale animation data"""
    
    scene.bz_audiofile = song_path
    scene.bz_bar_count = bar_count
    scene.bz_amplitude = 10
    
    bpy.ops.object.bz_generate()
    
    bz_bars = []
    bar_heights_list = []
    
    count = 0
    while count < len(scene.objects):
        if scene.objects[count].name.startswith("bz_bar"):
            bz_bars.append(scene.objects[count].name)
        count += 1
    
    for b in range(len(bz_bars)):
        bar_heights_list.append([])
        fcurve = find_fcurve(bpy.data.objects[bz_bars[b]], 'scale', 1)
        for i in range(scene.frame_start, scene.frame_end):
            bar_heights_list[-1].append(fcurve.evaluate(i))
    return bar_heights_list
