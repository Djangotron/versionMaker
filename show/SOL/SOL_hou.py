from application.maya.export_maya import animation
from application.maya.import_maya import animation as import_animation


def import_layout_for_shot(sequence="SF", shot="0030", asset="itUk"):

    """

    Example of how to import alembic caches for animation.

    :param string sequence:
    :param string shot:
    :param string asset:
    :return:
    """

    afp = import_animation.AnimationFilmImport()
    afp.show_folder_location = "D:/Google Drive/Projects"
    afp.show_folder = "sol"
    afp.partition = "3D"
    afp.division = "sequences"
    afp.sequence = sequence
    afp.shot = shot
    afp.task = "layout"
    afp.asset = asset
    afp()
