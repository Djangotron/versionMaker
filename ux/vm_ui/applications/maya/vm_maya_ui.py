import os
from functools import partial
from ....vm_ui import vm_base
from .....application.maya.import_maya import animation
from .....version import folder
import utilities
from maya import cmds


CACHE_SET = "cache_SET"


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window(), application="maya")

    if "SHOW" in os.environ:
        vm_maya.job_path = os.environ["SHOW"]

    vm_maya.import_func = partial(import_func)
    vm_maya.export_func = partial(export_func)

    vm_maya.get_cache_objects_func = partial(get_cacheable_objects)

    vm_maya()
    vm_maya.show()

    return vm_maya


def get_cacheable_objects(asset_name=""):

    """

    :param string asset_name:
    :return:
    """

    names_spaces = utilities.list_namespaces()
    if asset_name not in names_spaces:
        raise NameError("Asset Name: '{0}' not in current namespaces".format(asset_name))

    cache_sets = cmds.ls("{0}:{1}".format(asset_name, CACHE_SET))
    len_cache_sets = len(cache_sets)

    if len_cache_sets == 0:
        raise NameError("No cache set: '{0}:{1}' found for asset: {0}".format(asset_name, CACHE_SET))
    elif len_cache_sets > 1:
        raise NameError("Multiple Cache sets found: '{0}:{1}' found for asset: {0}".format(asset_name, CACHE_SET))

    cache_objects = cmds.sets(cache_sets[0], query=True)
    if cache_objects is None:
        cache_objects = list()

    return cache_objects


def import_func(version_dict, asset, version_number):

    """
    Import command for the version maker script

    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of the asset
    :param int version_number:  Version to import
    :return:
    """

    version_dict["folder_versions"][asset].verbose = False

    anim_import = animation.AnimationFilmImport()
    anim_import.version = version_dict["folder_versions"][asset]
    anim_import.asset = asset
    anim_import.partition = version_dict["partition"]
    anim_import.division = version_dict["division"]
    anim_import.sequence = version_dict["sequence"]
    anim_import.shot = version_dict["shot"]
    anim_import.task = version_dict["task"]
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

    version_dict["folder_versions"][asset].verbose = False