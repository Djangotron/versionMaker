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

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window(), application="houdini")

    if "SHOW" in os.environ:
        vm_maya.job_path = os.environ["SHOW"]

    vm_maya()
    vm_maya.show()

    vm_maya.import_func = partial(import_func)

    return vm_maya


def import_func(version_dict, asset, version_number):

    """
    Import command for the version maker script

    :param dict version_dict:
    :param string asset:
    :param int version_number:
    :return:
    """

    anim_import = animation.AnimationFilmImport()
    anim_import.version = version_dict["folder_versions"][asset]
    anim_import.asset = asset
    anim_import()
    anim_import.version_number = version_number

    anim_import.import_alembic_cache()
