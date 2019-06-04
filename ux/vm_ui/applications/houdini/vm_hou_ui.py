from ....vm_ui import vm_base
from functools import partial
from .....application.houdini.import_hou import animation
import utilities
import hou


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_hou = vm_base.VersionMakerWin(parent=utilities.get_houdini_window(), application="houdini")
    vm_hou.job_path = hou.getenv("JOB")
    vm_hou.setStyleSheet(hou.qt.styleSheet())
    vm_hou.setProperty("houdiniStyle", True)
    vm_hou.file_dialog.setStyleSheet(hou.qt.styleSheet())

    vm_hou()
    vm_hou.show()

    vm_hou.import_func = partial(import_func)
    vm_hou.export_func = partial(import_func)

    vm_hou.get_cache_objects_func = partial(get_cacheable_objects)
    vm_hou.print_func = partial(print_func)
    vm_hou.get_selection_func = partial(get_selection)

    return vm_hou


def get_cacheable_objects(asset_name=""):

    """

    :param string asset_name:
    :return:
    """


def get_selection():
    """
    Return the selection as a list of strings
    :return:
    """

    return hou.selectedNodes()


def import_func(version_dict, asset, version_number):

    """
    Import command for the version maker script

    :param dict version_dict:
    :param string asset:
    :param int version_number:
    :return:
    """

    for node in hou.selectedNodes():

        anim_import = animation.AnimationFilmImport()
        # anim_import.version = version_dict["folder_versions"][asset]
        anim_import.show_folder_location = version_dict["show_folder_location"]
        anim_import.show_folder = version_dict["show_folder_name"]
        anim_import.partition = version_dict["partition"]
        anim_import.division = version_dict["division"]
        anim_import.sequence = version_dict["sequence"]
        anim_import.shot = version_dict["shot"]
        anim_import.task = version_dict["task"]
        anim_import.asset = asset
        anim_import()
        anim_import.version_number = version_number

        anim_import.update_alembic_path(node, "input_animation", use_path_expression=True)


def export_func(version_dict, asset):

    """

    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of asset to export
    :return:
    """

    version_dict["folder_versions"][asset].verbose = False


def print_func(string=""):

    """

    :param string string:
    :return:
    """
