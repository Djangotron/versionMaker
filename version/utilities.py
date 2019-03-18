import re, os


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


def windows_path_conversion(path):

    """
    Takes a unix stype path and makes sure it is of windows type.  Basically replacing '/' with '\\' for windows paths.
    :param string path:  Path to a folder in a unix style path.
    :return:
    """

    return path.replace(r"/", r"\\").decode("string_escape")