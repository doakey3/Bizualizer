def find_fcurve(id_data, path, index=0):
    anim_data = id_data.animation_data
    for fcurve in anim_data.action.fcurves:
        if fcurve.data_path == path and fcurve.array_index == index:
            return fcurve