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


class Version(object):

    def __init__(self):

        """
        Does a look up for versions
        :return:
        """

        self.version_prefix = "v"
        self.version = 1

        # Path to the type of data you are working with
        self.type_folder = ""
        self.type_folder_path = ""

        # Version of data
        self.folder_version = ""
        self.folder_version_path = ""

        # All the versions
        self.folder_versions = list()
        self.latest_folder_version = 0

        self.number_padding = 4

        self.verbose = False

    def _get_folder_versions(self):

        """
        list all the folders version in a directory
        :return:
        """

        self._set_folder_version_path()
        self._set_type_folder_path()
        self.folder_versions = natural_sort(text_list=os.listdir(self.type_folder_path))

        # test to make sure this is not a file
        for folder in self.folder_versions[::]:

            has_period = folder.find(".") != -1

            if has_period:

                self.folder_versions.remove(folder)

    def _set_folder_version(self):

        """

        :return:
        """

        self.folder_version = "{prefix}{intVersion:0{numPad}d}".format(
            prefix=self.version_prefix,
            intVersion=self.version,
            numPad=self.number_padding
        )

    def _set_folder_version_path(self):

        """

        :return:
        """

        self._set_folder_version()
        self._set_type_folder_path()

        self.folder_version_path = "{typeFolder}/{version}".format(
            typeFolder=self.type_folder_path,
            version=self.folder_version
        )

    def _set_paths(self):

        """

        :return:
        """

        self.__call__()

    def _set_type_folder_path(self):

        """

        :return:
        """

        self.type_folder_path = "{path}/{typeFolder}".format(path=self.tech_rig_data_path, typeFolder=self.type_folder)

    def create_version(self):

        """
        Creates a version folder for
        :return:
        """

        self.set_version()

        if not os.path.exists(self.folder_version_path):

            os.mkdir(self.folder_version_path)

    def get_latest_version(self):

        """

        :return:
        """

        self._get_folder_versions()

    def set_version(self, new_version=None):

        """

        :return:
        """

        add_version = 0
        if new_version != False:
            add_version = 1

        self._set_paths()
        self._get_folder_versions()

        # If there are none, create version 1
        if len(self.folder_versions) is 0:
            self._set_folder_version_path()

        else:
            latest = int(self.folder_versions[-1].replace(self.version_prefix, ""))
            self.version = latest + add_version
            self._set_folder_version_path()

        # print "{0}: version set to path: {1}".format()