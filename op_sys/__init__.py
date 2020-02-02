import platform


def open_explorer(directory=""):

    """
    Opens a directory based on the current os.

    :param directory:
    :return:
    """

    platform_system = platform.system()
    if platform_system == "Windows":
        import windows
        windows.windows_explorer_open(directory)
    else:
        raise NotImplementedError("Can't open an explorer on this operating system.")
