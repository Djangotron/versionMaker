from ...application.houdini.export_hou import animation as export_animation
from ...application.houdini.import_hou import animation as import_animation
from ...application.houdini.task.render import create as render_create
from ...application.houdini.cache import alembic
import _alembic_hom_extensions as hou_abc


def import_layout_for_shot(sequence="SF", shot="0030", asset="cam", index=0):

    """

    Example of how to import alembic caches for animation.

    :param string sequence:
    :param string shot:
    :param string asset:
    :return:
    """

    afp = import_animation.AnimationFilmImport()
    afp.show_folder_location = "D:/gDrive/Projects"
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

    start_frame = afp.meta_data.ancillary_data["start_frame"]
    end_frame = afp.meta_data.ancillary_data["end_frame"]

    # Import the camera
    afp.path_to_path_expression()
    afp.import_alembic_archive(use_path_expression=True)
    cameras = afp.alembic_archive.return_cameras()
    for cam in cameras:
        cam.parm("resx").set(2048)
        cam.parm("resy").set(858)

    # setup the output directory
    render_output = export_animation.AnimationFilmPublish()
    render_output.show_folder_location = "D:/gDrive/Projects"
    render_output.show_folder = "sol"
    render_output.partition = "3D"
    render_output.division = "sequences"
    render_output.sequence = sequence
    render_output.shot = shot
    render_output.task = "layout"
    render_output.asset = "render"
    render_output.message = "testing publish"
    render_output.start_frame = start_frame
    render_output.end_frame = end_frame
    render_output.meta_data.file_types = ["png"]
    render_output()

    # setup the output render node
    render_node = render_create.RenderNode()
    render_node.output_directory = render_output.houdini_output_directory
    render_node.output_name = render_output.houdini_output_file_name
    render_node.format_output_path()

    render_node.start_frame = start_frame
    render_node.end_frame = end_frame
    render_node.create_arnold(name=afp.alembic_name)
    render_node.camera_path = cameras[0].path()
    render_node.set_camera()

    # Create a merge node if it does not already exist
    render_merge = render_create.create_render_merge(name="SF__layout__merge")
    render_merge.setNextInput(render_node.rop_node)


def import_layout_for_sequence(sequence="SF", asset="cam"):

    """

    :param sequence:
    :param asset:
    :return:
    """

    iaa = import_animation.AnimationFilmImport()
    iaa.show_folder_location = "D:/gDrive/Projects"
    iaa.show_folder = "sol"
    iaa.partition = "3D"
    iaa.division = "sequences"
    shot_folders = iaa.return_shot_numbers(partition="3D", division="sequences", sequence=sequence)
    shot_numbers = [i.split("__")[1] for i in shot_folders]

    # shot_numbers = ["0030"]
    for shot in shot_numbers:
        import_layout_for_shot(sequence=sequence, shot=shot, asset=asset)
