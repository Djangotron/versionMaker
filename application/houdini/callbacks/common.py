from .... import op_sys
import os


def parm_names_to_paths(parms=[]):

    """
    Converts parm evals to an output path as a string.
    :param hou.parm parms:
    :return:
    """

    directory = ""
    temp_directory = ""
    for int_parm, parm in enumerate(parms):
        name = parm.evalAsString()
        if int_parm == 0:
            temp_directory += "{}".format(name)
        else:
            temp_directory += "/{}".format(name)

        # return the previous one if this one does not exist
        dir_exists = os.path.exists(temp_directory)
        if not dir_exists:
            break

        directory = temp_directory

    return directory


def open_explorer(parent_parms=[], hou_kwargs=None):

    """
    Opens a explorer window based on evaluated parent parameters as strings.

    whatever the parents are it should

    :param parent_parms:
    :param kwargs hou_kwargs: Takes the keyword args from a houdini button.  We will use the 'parm'
    :return:
    """

    _parents_as_parms = list()
    for parent in parent_parms:

        _tp = type(parent)
        if _tp == str or _tp == unicode:
            parm = hou_kwargs["node"].parm(parent)

        _parents_as_parms.append(parm)


    # Convert the string results of the parent attributes into a directory path
    directory = parm_names_to_paths(parms=_parents_as_parms)

    # print directory
    op_sys.open_explorer(directory=directory)


