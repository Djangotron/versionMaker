import os, json
import hou
import common


menu_child_folders = "menu_child_folders"
NONE_ENTRIES = ["--", "--"]


def list_directory_for_entries(directory):

    """

    :param string directory:
    :return:
    """

    child_folders = os.listdir(directory)

    entries = ["--", "--"]
    for folder in child_folders:

        # if only_folders:
        if os.path.isdir(folder):
            continue

        if folder.find(".") != -1:
            continue

        formatted_name = str(folder.split("__")[-1])
        entries.append(folder)
        entries.append(formatted_name)

    return entries


def menu_list_folders_callback(parents=list(), hou_kwargs=None, child_parameters=list()):

    """
    Because menu list scripts can be called many points with we make a separate callback to query disc

    :param list [str, str..] parents:  The parent directory to list the contents of
    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.  We will use the 'parm'
    :param [hou.Parm, ..] child_parameters:  Parameters that will need their lists updated after
        this param has been updated.
    :return:
    """

    if "node" not in hou_kwargs:
        raise KeyError("hou_kwargs does not contain node, cannot query parameters.")

    # this is a hack.  It seems that there are extra calls to this call back but without the args set.  I have seen docs
    # that say this is not a bug and I think it is related to the eventloop in qt
    if parents == list():
        return None

    node = hou_kwargs["node"]
    name = hou_kwargs["parm"].name()
    parents_attrib = "_{}Parents".format(name)
    string_attrib = "_{}".format(name)

    parents_as_string = node.parm(parents_attrib).evalAsString()
    parents = json.loads(parents_as_string)

    _parents_as_parms = list()
    for parent in parents:
        parm = hou_kwargs["node"].parm(parent)
        _parents_as_parms.append(parm)

    # Convert the string results of the parent attributes into a directory path
    directory = common.parm_names_to_paths(parms=_parents_as_parms)

    # Check
    dir_exists = os.path.exists(directory)
    if not dir_exists:
        raise Exception(
            "Directory does not exist:\n\t'{0}'".format(directory)
        )

    entries = list_directory_for_entries(directory)

    # set to json
    holder = json.dumps(entries)
    string_parm = hou_kwargs["node"].parm(string_attrib)

    if string_parm is not None:
        hou_kwargs["node"].parm(string_attrib).set(holder)


def menu_list_folders(hou_kwargs=None):

    """
    For child parms you should order them in the way you want them updated.

    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.

    https://forums.odforce.net/topic/22387-updating-menu-items-with-python/

    https://www.sidefx.com/forum/topic/12725/

    :return:
    """

    # ['node', 'parm', 'script_multiparm_index', 'script_multiparm_nesting']

    name = hou_kwargs["parm"].name()
    parm = hou_kwargs["parm"]
    parents_attrib = "_{}Parents".format(name)
    string_attrib = "_{}".format(name)
    node = hou_kwargs["node"]

    parents_as_string = node.parm(parents_attrib).evalAsString()
    parents = json.loads(parents_as_string)

    _parents_as_parms = list()
    for parent in parents:
        parm = hou_kwargs["node"].parm(parent)
        _parents_as_parms.append(parm)

    # Convert the string results of the parent attributes into a directory path
    directory = common.parm_names_to_paths(parms=_parents_as_parms)

    # Check
    dir_exists = os.path.exists(directory)
    if not dir_exists:
        return ["--", "--"]
        # raise Exception("Directory does not exist:\n\t'{0}'".format(directory))

    entries = list_directory_for_entries(directory)

    # set to json
    holder = json.dumps(entries)
    string_parm = hou_kwargs["node"].parm(string_attrib)

    if string_parm is not None:
        hou_kwargs["node"].parm(string_attrib).set(holder)

    return entries


def version_menu_list_folders(hou_kwargs=None):

    """
    Specific setup for versioning parameters
    :param hou_kwargs:
    :return:
    """

    # entries = menu_list_folders(hou_kwargs=hou_kwargs)

    # ['node', 'parm', 'script_multiparm_index', 'script_multiparm_nesting']

    name = hou_kwargs["parm"].name()
    parents_attrib = "_{}Parents".format(name)
    string_attrib = "_{}".format(name)
    node = hou_kwargs["node"]

    entries = ["--", "--"]
    # entries = list_dir_for_entries(directory)

    return entries
