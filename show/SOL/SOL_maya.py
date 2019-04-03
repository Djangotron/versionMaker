from maya import cmds
from ...application.maya.export_maya import animation
from ...application.maya.import_maya import animation


def export_layout_for_sequence():

    """
    Export all of the cameras in the layout scene.
    :return:
    """

    camera_groups = cmds.listRelatives("__cameras__", children=True)
    cameras = list()
    frame_nums = list()
    for int_cam, cam_grp in enumerate(camera_groups):

        if int_cam != 1:
            continue

        children = cmds.listRelatives(cam_grp, children=True, fullPath=True)
        cam = ""
        for child in children:
            shapes = cmds.listRelatives(child, shapes=True, ad=True, fullPath=True)
            if shapes is not None:
                if cmds.objectType(shapes) == "camera":
                    cam = child

        cameras.append(cam)
        sequence, shot_number = cam.split("|")[-1].split("__")
        frame_number = int(cmds.getAttr("{0}.notes".format(cam_grp)).split(" ")[1])
        frame_nums.append(shot_number)

        #
        cachable_objects = [cam, "itUk:geometry_GRP", "ni:geometry_GRP"]
        for int_cache_obj, cache_obj in enumerate(cachable_objects):

            if int_cache_obj == 0:
                name = "cam"
            else:
                name = cache_obj.split(":")[0]

            afp = animation.AnimationFilmPublish()
            afp.export_alembic = True

            afp.show_folder_location = "D:/Google Drive/Projects"
            afp.show_folder = "sol"
            afp.partition = "3D"
            afp.division = "sequences"
            afp.sequence = sequence
            afp.shot = shot_number
            afp.task = "layout"
            afp.asset = name
            afp.message = "testing publish"
            afp.start_frame = frame_number
            afp.end_frame = frame_number
            afp.cache_sets = cache_obj

            #
            afp.cache_objects = [cache_obj]
            afp()
            afp.alembic_cache_write()


def import_layout_for_shot(sequence="SF", shot="0030", asset=""):

    """

    Example of how to import alembic caches for animation.

    :param string sequence:
    :param string shot:
    :param string asset:
    :return:
    """

    afp = animation.AnimationFilmImport()
    afp.show_folder_location = "D:/Google Drive/Projects"
    afp.show_folder = "sol"
    afp.partition = "3D"
    afp.division = "sequences"
    afp.sequence = sequence
    afp.shot = shot
    afp.task = "layout"
    afp.asset = asset
    afp()

    afp.import_alembic_cache()
