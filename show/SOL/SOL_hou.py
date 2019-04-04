from ...application.houdini.export_hou import animation as export_animation
from ...application.houdini.import_hou import animation as import_animation
from ...application.houdini.task.render import create as render_create
from ...application.houdini.cache import alembic
import _alembic_hom_extensions as hou_abc


def import_layout_for_shot(sequence="SF", shot="0030", asset="cam"):

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

    # Call it, set the shot variables
    found_asset = afp()
    if not found_asset:
        return
    # afp.find_alembic_file()

    afp.path_to_path_expression()
    afp.import_alembic_archive(use_path_expression=True)

    cameras = afp.alembic_archive.return_cameras()

    # setup the output render node
    render_node = render_create.RenderNode()

    render_node.output_directory = "ip"
    render_node.create_arnold(name=afp.alembic_name)
    render_node.camera_path = cameras[0].path()
    render_node.set_camera()

    # Create a merge node if it does not already exist
    render_merge = render_create.create_render_merge(name="SF__layout__merge")
    render_merge.setInput(0, render_node.rop_node)


def import_layout_for_sequence(sequence="SF", asset="cam"):

    """

    :param sequence:
    :param asset:
    :return:
    """

    iaa = import_animation.AnimationFilmImport()
    iaa.show_folder_location = "D:/Google Drive/Projects"
    iaa.show_folder = "sol"
    iaa.partition = "3D"
    iaa.division = "sequences"
    shot_folders = iaa.return_shot_numbers(partition="3D", division="sequences", sequence=sequence)
    shot_numbers = [i.split("__")[1] for i in shot_folders]

    print shot_numbers
    for shot in shot_numbers:
        import_layout_for_shot(sequence="SF", shot=shot, asset=asset)
