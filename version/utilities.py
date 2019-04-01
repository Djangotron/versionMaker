import re, os
from stat import S_IREAD, S_IRGRP, S_IROTH


def make_dir_recursive(dir_path):

    """
    Normally for windows you need to have \\ escape characters for creation.  I think with makedirs it works with / instead.
    :param string dir_path:  Path to the directory to be created.  You can give it as many uncreated folders as you want.
    :return:
    """

    if os.path.isdir(dir_path):
        return

    head, tail = os.path.split(dir_path) # head/tail
    if not os.path.isdir(head):
        make_dir_recursive(head)

    os.makedirs(dir_path)


def natural_sort(text_list=list()):
    """
    Sorts text_list as a natural sort without the need for number padding.

    http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort

    :param list text_list:  texts to sort
    :return:
    """

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(text_list, key=alphanum_key)


def set_file_read_only(file_path):

    """
    Sets the file to have read only status.

    "https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"

    :param string file_path: absolute file path to your file
    :return:
    """

    os.chmod(file_path, S_IREAD | S_IRGRP | S_IROTH)


def path_conversion(path):

    """
    Takes a unix stype path and makes sure it is of windows type.  Basically replacing '/' with '\\' for windows paths.
    :param string path:  Path to a folder in a unix style path.
    :return:
    """

    return path.replace("\\", r"/").decode("string_escape")


def windows_path_conversion(path):

    """
    Takes a unix stype path and makes sure it is of windows type.  Basically replacing '/' with '\\' for windows paths.
    :param string path:  Path to a folder in a unix style path.
    :return:
    """

    return path.replace(r"/", r"\\").decode("string_escape")