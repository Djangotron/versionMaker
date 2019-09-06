import os
from functools import partial
from ....vm_ui import vm_base
from .....application.maya.import_maya import animation as import_animation
from .....application.maya.export_maya import animation as export_animation
from .....version import folder
import utilities
from maya import cmds, OpenMaya


CACHE_SET = "cache_SET"


def vm_run(*args):

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window(), application="maya")

    if "SHOW" in os.environ:
        vm_maya.job_path = os.environ["SHOW"]

    vm_maya.import_func = import_func
    vm_maya.export_func = export_func

    vm_maya.get_cache_objects_func = get_cacheable_objects
    vm_maya.get_selection_func = get_selection
    vm_maya.list_publishable_scene_objects_func = list_publishable_scene_objects
    vm_maya.print_func = print_func

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


def list_publishable_scene_objects():

    """
    Lists the objects in scene that can be published.

    For Maya, These must be:
    - have a namespace
    - have a cache set in the namespace

    :return:
    """

    cmds.namespace(setNamespace=':')
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)

    return_dict = dict()
    for namespace in namespaces:

        cache_set_name = "{0}:{1}".format(namespace, CACHE_SET)
        cache_sets = cmds.ls("{0}:{1}".format(namespace, CACHE_SET))
        len_cache_sets = len(cache_sets)

        if len_cache_sets > 0:
            return_dict[namespace] = {"cache_set": cache_set_name}

    return return_dict


def return_asset_name_from_dir():

    """
    Takes the asset, queries if it is referenced.  If it is, it will look to see which asset folder it comes from.
    :return:
    """


def get_selection():

    """
    Return the selection as a list of strings
    :return:
    """

    return cmds.ls(sl=True)


def import_func(version_dict, asset, version_number):

    """
    Import command for the version maker script

    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of the asset
    :param int version_number:  Version to import
    :return:
    """

    version_dict["folder_versions"][asset].verbose = False

    anim_import = import_animation.AnimationFilmImport()
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

    Use for create progress bar
    https://www.mail-archive.com/python_inside_maya@googlegroups.com/msg18725.html
    https://groups.google.com/forum/#!msg/python_inside_maya/V_v3lMnrVME/ooZ8YDFKBAAJ

    https://fredrikaverpil.github.io/2013/10/11/catching-string-from-stdout-with-python/


    :param dict version_dict:  Dictionary denoting location on disk to use.
    :param string asset:  Name of asset to export
    :return:
    """

    version_dict["folder_versions"][asset].verbose = False

    afp = export_animation.AnimationFilmPublish()
    afp.export_alembic = True
    afp.export_master_scene = True

    afp.show_folder_location = version_dict["show_folder_location"]
    afp.show_folder = version_dict["show_folder_name"]
    afp.partition = version_dict["partition"]
    afp.division = version_dict["division"]
    afp.sequence = version_dict["sequence"]
    afp.shot = version_dict["shot"]
    afp.task = version_dict["task"]
    afp.asset = asset
    afp.version = version_dict["folder_versions"][asset]

    afp.message = version_dict["message"]
    afp.start_frame = version_dict["start_frame"]
    afp.end_frame = version_dict["end_frame"]
    afp.cache_sets = ""

    afp.cache_objects = version_dict["cache_objects"]

    afp()
    afp.set_meta_data()
    afp.alembic_cache_write()


class Progress(object):

    def __init__(self):

        """
        Class to increment progress bars in the export queue
        """

        self.qt_widget = None

        self.time_changed_id = None
        self.time_unit_changed_id = None
        self.call_back_id = None

    def __call__(self):

        """ Set the time changed callback """

        self.call_back_id = OpenMaya.MEventMessage.addEventCallback("timeChanged", self.time_change_update)

    def remove_call_back_id(self):

        OpenMaya.MEventMessage.removeCallback(self.call_back_id)

    def time_change_update(self, *args):

        """
        Used to update the UI based on the change of frame.
        :return:
        """

        print
        print args[0]
        print "testing progress with ABC"
        print cmds.currentTime(query=True)


def print_func(string=""):

    """

    :param string string:
    :return:
    """

    OpenMaya.MGlobal.displayInfo(string)
