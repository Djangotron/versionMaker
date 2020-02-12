import hou
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
    render_output.show_folder_location = "D:/Google Drive/Projects"
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
    iaa.show_folder_location = "D:/Google Drive/Projects"
    iaa.show_folder = "sol"
    iaa.partition = "3D"
    iaa.division = "sequences"
    shot_folders = iaa.return_shot_numbers(partition="3D", division="sequences", sequence=sequence)
    shot_numbers = [i.split("__")[1] for i in shot_folders]

    # shot_numbers = ["0030"]
    for shot in shot_numbers:
        import_layout_for_shot(sequence=sequence, shot=shot, asset=asset)


def render_sequence(camera_archive=hou.node, sequence="EL", task="layout"):

    """
    Queries an entire sequence and creates the render nodes and renderers for the sequence
    :param hou.node camera_archive:  the camera
    :param string sequence:  The name of the sequence on disk
    :param string task:  The name of the sequence on disk
    :return:
    """

    # turn off the hierarchy
    bs = camera_archive.parm("buildSubnet")
    bs.set(0)

    aa = alembic.AlembicArchive()
    aa.archive = camera_archive
    aa.update_hierarchy()
    cameras = aa.return_cameras()

    # print cameras

    cam_dict = dict()
    for int_cam, cam in enumerate(cameras):

        cam_name = cam.name()
        name = cam_name
        if name.find("Shape") != -1:
            name = name.replace("Shape", "")

        seq_shot = render_create.RenderNode()
        seq_shot.image_file_type = "exr"
        seq_shot.camera_path = cam.path()

        name_split = name.split("__")
        seq = name_split[0]

        # create arnold node
        seq_shot.create_arnold(name="arnold_{}".format(name))
        render_node = seq_shot.create_vm_render_node(name="RenderNode_{}".format(name))
        seq_shot.rop_node.setInput(0, render_node)

        # must be set in this order
        # --> seq / shot / task / version
        # seq
        render_node.parm("sequence").set(seq)

        # shot
        mi = render_node.parm("shot").menuItems()
        shot_index = mi.index(name)
        render_node.parm("shot").set(shot_index)

        # task
        mi = render_node.parm("task").menuItems()
        task_index = mi.index("{0}__{1}".format(name, task))
        render_node.parm("task").set(task_index)

        # version
        render_node.parm("version").set(1)

        frame = 1001 + int_cam
        render_node.parm("frx").set(frame)
        render_node.parm("fry").set(frame)

        render_node.parm("set").pressButton()
        render_node.parm("usetheforce").set(1)
        render_node.parm("message").set("Initial version")

        # expressions
        seq_shot.rop_node.parm("ar_picture").setExpression('chs("../{}/outPath")'.format(render_node))
        seq_shot.rop_node.parm("f1").setExpression('ch("../{}/frx")'.format(render_node))
        seq_shot.rop_node.parm("f2").setExpression('ch("../{}/fry")'.format(render_node))

        cam_dict[cam] = {
            'arnold': seq_shot.rop_node,
            'renderNode': render_node
        }

    merge = render_create.create_render_merge(name="merge_{}".format(sequence))

    for int_cam, cam in enumerate(cameras):

        merge.setInput(int_cam, cam_dict[cam]["arnold"])

    return merge, cam_dict