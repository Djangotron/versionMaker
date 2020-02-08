import os, json
import glob
import hou
import common
from ....constants.film import hierarchy
from ....application.houdini.export_hou import animation as export_animation


menu_child_folders = "menu_child_folders"
NONE_ENTRIES = ["--", "--"]


def create_version(parents=list, hou_kwargs=None):

    """
    Creates a version of the specified asset

    Parents order must match the set_output_picture order parents.

    :param list [str, str..] parents:  The parent directory to list the contents of
    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.

    :return:
    """

    name = hou_kwargs["parm"].name()
    parm = hou_kwargs["parm"]
    node = hou_kwargs["node"]

    _parents = common.return_parents(this_node=node, parents=parents)
    _parents_as_parms = _parents["parms"]
    _parents_as_parm_values = _parents["parm_values"]
    _parents_as_str = _parents["names"]

    # We don't know the path location but we know that the last 4 elements in this list
    # are going to be broken out as the show folder, production, partition, division
    show_path_split = _parents_as_parm_values[0].split("/")
    show_location = ""
    for int_path, _path in enumerate(show_path_split[:-4]):
        if int_path == 0:
            show_location += "{}".format(_path)
        else:
            show_location += "/{}".format(_path)

    show_folder_location = _parents_as_parm_values[0].split(show_path_split[-4])[0][0:-1]
    show_folder = show_path_split[-4]
    partition = show_path_split[-2]
    division = show_path_split[-1]

    sequence = _parents_as_parm_values[1]
    shot = _parents_as_parm_values[2].rpartition("__")[2]
    task = _parents_as_parm_values[3].rpartition("__")[2]
    asset = _parents_as_parm_values[4]
    current_version = _parents_as_parm_values[5]
    message = _parents_as_parm_values[6]
    start_frame = _parents_as_parm_values[7]
    end_frame = _parents_as_parm_values[8]

    # setup the output directory
    render_output = export_animation.AnimationFilmPublish()
    render_output.show_folder_location = show_folder_location
    render_output.show_folder = show_folder
    render_output.partition = partition
    render_output.division = division
    render_output.sequence = sequence
    render_output.shot = shot
    render_output.task = task
    render_output.asset = asset
    render_output.message = message
    render_output.start_frame = start_frame
    render_output.end_frame = end_frame
    render_output.meta_data.file_types = ["exr"]
    render_output()

    # Set the version number ui menu to the latest version
    version_parm = _parents_as_parms[5]
    version_parm.set(1)  # 0 = '--', 1 == 'latest version'

    # Set the output attribute
    set_output_picture(
        parents=parents,
        hou_kwargs=hou_kwargs,
        version_number_override=render_output.version.latest_folder_version
    )


def use_the_force(parents=list, hou_kwargs=None):

    """
    Takes the parent attributes, queries if we can create a new version and either creates it or allows it to be
    rendered over it.
    :return:
    """

    node = hou_kwargs["node"]
    parm = hou_kwargs["parm"]

    # get the parms value and see if we can create a new version
    value = parm.eval()
    print value


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

    entries = list_directory_for_entries(directory)

    # set to json
    holder = json.dumps(entries)
    string_parm = hou_kwargs["node"].parm(string_attrib)

    if string_parm is not None:
        hou_kwargs["node"].parm(string_attrib).set(holder)

    return entries


def set_output_picture(parents=[], hou_kwargs=None, version_number_override=-1, out_attrib_name="outPath", image_format="exr"):

    """

    :param list [str, str..] parents:  The parent directory to list the contents of
    :param kwargs hou_kwargs:  Takes the keyword args from a houdini button.
    :param int version_number_override:  If this is not -1 it will use
    :param string out_attrib_name:  output attribute to set.
    :param string image_format:  the format of the image, default 'exr'.  This could depend on an image format settings
        of the rop
    :return:
    """

    node = hou_kwargs["node"]
    out_parm = node.parm(out_attrib_name)

    _parents = common.return_parents(this_node=node, parents=parents)
    _parents_as_parms = _parents["parms"]
    _parents_as_parm_values = _parents["parm_values"]
    _parents_as_str = _parents["names"]

    task_name = _parents_as_parm_values[3].split("__")[-1]

    #
    if _parents_as_parm_values[-1] == "--":
        if out_parm is not None:
            out_parm.set("ERROR - No version created yet!")

        return

    version_number = _parents_as_parm_values[-1]
    if version_number_override != -1:
        version_number = "{0:03d}".format(version_number_override)

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
    out_images = "{out_dir}__v{version}/{task}__{asset}.$F4.{frmt}".format(
        out_dir=directory,
        task=_parents_as_parm_values[3],
        asset=_parents_as_parm_values[4],
        version=version_number,
        frmt=image_format
    )
    job_path = hou.hscriptExpression("$JOB")
    out_images = out_images.replace(job_path, "$JOB")

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
        entries.append(token_value)
        entries.append(token_value)

    return entries
