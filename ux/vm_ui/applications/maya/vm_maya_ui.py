import os
from functools import partial
from ....vm_ui import vm_base
from .....application.maya.import_maya import animation
from .....version import folder
import utilities


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window(), application="maya")

    if "SHOW" in os.environ:
        vm_maya.job_path = os.environ["SHOW"]

    vm_maya()
    vm_maya.show()

    vm_maya.import_func = partial(import_func)

    return vm_maya


def import_func(version_dict, asset, version_number):

    """
    Import command for the version maker script

    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of the asset
    :param int version_number:  Version to import
    :return:
    """

    print version_dict["path"]
    print version_dict["folder_versions"]
    print version_dict["folder_versions"][asset]
    print version_number

    anim_import = animation.AnimationFilmImport()
    anim_import.version = version_dict["folder_versions"][asset]
    anim_import.asset = asset
    anim_import.verbose = False
    anim_import()
    anim_import.meta_data.verbose = False
    anim_import.version_number = version_number

    anim_import.import_alembic_cache()


def export_func(version_dict, asset):

    """

    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of asset to export
    :return:
    """