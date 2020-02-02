import os
import subprocess


def windows_explorer_open(directory=""):

    """

    :param directory:
    :return:
    """

    directory = windows_path_conversion(path=directory)
    # os.system('explorer "{0}"'.format(directory))

    subprocess.Popen('explorer "{0}"'.format(directory))


def windows_path_conversion(path):

    """
    Takes a unix stype path and makes sure it is of windows type.  Basically replacing '/' with '\\' for windows paths.
    :param string path:  Path to a folder in a unix style path.
    :return:
    """

    return path.replace(r"/", r"\\").decode("string_escape")