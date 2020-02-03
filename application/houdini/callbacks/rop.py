import os, json
import glob
import hou
import common
from ....constants.film import hierarchy


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


def set_output_picture(parents=[], hou_kwargs=None, out_attrib_name="ar_picture", image_format="EXR"):

    """

    :param list [str, str..] parents:  The parent directory to list the contents of
    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.
    :param string out_attrib_name:  output attribute to set.
    :param string image_format:  the format of the image, default 'exr'.  This could depend on an image format settings
        of the rop
    :return:
    """

    name = hou_kwargs["parm"].name()
    parm = hou_kwargs["parm"]
    parents_attrib = "_{}Parents".format(name)
    string_attrib = "_{}".format(name)
    node = hou_kwargs["node"]

    _parents_as_parms = list()
    _parents_as_parm_values = list()
    _parents_as_str = list()
    for parent in parents:
        parm = hou_kwargs["node"].parm(parent)
        val = parm.evalAsString()
        name = parm.name()
        _parents_as_parms.append(parm)
        _parents_as_parm_values.append(val)
        _parents_as_str.append(name)

    task_name = _parents_as_parm_values[3].split("__")[-1]

    # create the path to search for versions
    _h = hierarchy.Hierarchy()
    directory = _h.seq_shot_task_asset_path.format(
        division_path=_parents_as_parm_values[0],
        sequence=_parents_as_parm_values[1],
        shot=_parents_as_parm_values[2],
        task=_parents_as_parm_values[3],
        task_name=task_name,
        asset=_parents_as_parm_values[4],
    )

    out_images = "{out_dir}__v{version}__$F4.{frmt}".format(
        out_dir=directory,
        version=_parents_as_parm_values[-1],
        frmt=image_format
    )
    job_path = hou.hscriptExpression("$JOB")
    out_images = out_images.replace(job_path, "$JOB")

    out_parm = hou_kwargs["node"].parm(out_attrib_name)
    if out_parm is not None:
        out_parm.set(out_images)


def version_menu_list_folders(hou_kwargs=None):

    """
    Specific setup for versioning parameters
    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.
    :return:
    """

    if hou_kwargs is None:
        return ["--", "--"]

    # entries = menu_list_folders(hou_kwargs=hou_kwargs)

    # ['node', 'parm', 'script_multiparm_index', 'script_multiparm_nesting']

    name = hou_kwargs["parm"].name()
    parents_attrib = "_{}Parents".format(name)
    string_attrib = "_{}".format(name)
    node = hou_kwargs["node"]

    parents_as_string = node.parm(parents_attrib).evalAsString()
    parents = json.loads(parents_as_string)

    _parents_as_parms = list()
    _parents_as_parm_values = list()
    _parents_as_str = list()
    for parent in parents:
        parm = hou_kwargs["node"].parm(parent)
        val = parm.evalAsString()
        name = parm.name()
        _parents_as_parms.append(parm)
        _parents_as_parm_values.append(val)
        _parents_as_str.append(name)

    # Convert the string results of the parent attributes into a directory path
    directory = common.parm_names_to_paths(parms=_parents_as_parms)
    entries = ["--", "--"]

    # create the path to search for versions
    _h = hierarchy.Hierarchy()
    directory = _h.seq_shot_task_asset_path.format(
        division_path=_parents_as_parm_values[0],
        sequence=_parents_as_parm_values[1],
        shot=_parents_as_parm_values[2],
        task=_parents_as_parm_values[3],
        task_name=_parents_as_parm_values[3].split("__")[-1],
        asset=_parents_as_parm_values[4],
    )

    # Search string
    search_str = directory + "__v*"
    found_str = glob.glob(search_str)
    if found_str is None:
        return entries

    rev_found_str = reversed(found_str)
    for token in rev_found_str:

        token_value = token.split("__v")[1]
        entries.append(token)
        entries.append(token_value)

    return entries
