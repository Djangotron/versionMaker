import os
import utilities


def return_type_folder(folder_version):

    """
    Returns the task_folder from the
    :param string folder_version:
    :return:
    """

    ver = Version()

    return folder_version.partition(ver.version_prefix)[0]


class Version(object):

    def __init__(self):

        """
        Sets, gets, and queries latest version of folders with a specific suffix.

        We count versions from 1 not 0

        You must set the type
        :return:
        """

        # Path to the type of data you are working with
        self.path_to_versions = ""

        # type (Name) of data folder you are dealing with
        self.type_folder = ""

        self.version_prefix = "__v"
        self.version = -1

        self.new_version = True

        # Version of data
        self.folder_version_number = ""
        self.folder_version = ""
        self.folder_version_path = ""

        # All the versions
        self.folder_versions = list()
        self.folder_version_paths = list()
        self.folder_version_numbers = list()

        self.latest_folder_version = 0

        self.number_padding = 3

        self.verbose = False

    def _get_folder_version_number(self, folder=""):

        """
        Returns the folder number from the string
        :return:
        """

        return int(folder.rpartition(self.version_prefix)[2])

    def _set_folder_version_string(self):

        """
        Sets the "folder_version" attribute string.  This is only the version number.
        :return:
        """

        self.folder_version_number = "{prefix}{intVersion:0{numPad}d}".format(
            prefix=self.version_prefix,
            intVersion=self.version,
            numPad=self.number_padding
        )

    def _set_folder_version_path(self):

        """
        Sets the entire folder name.
        :return:
        """

        # Checking naming / numbering
        if self.path_to_versions == "":
            raise AttributeError("'path_to_versions' has not been set.  Please specify type of data to version.")

        # Checking naming / numbering
        if self.type_folder == "":
            raise AttributeError("'type_folder' has not been set.  Please specify type of data to version.")

        # Set the file version suffix
        self._set_folder_version_string()

        self.folder_version = "{typeFolder}{version}".format(
            typeFolder=self.type_folder,
            version=self.folder_version_number
        )

        self.folder_version_path = "{path}/{typeFolder}{version}".format(
            path=self.path_to_versions,
            typeFolder=self.type_folder,
            version=self.folder_version_number
        )

        if self.folder_version not in self.folder_versions:
            self.folder_versions.append(self.folder_version)

    def create_version(self, search_string=None):

        """
        Creates a new version folder for
        :return:
        """

        self.set_version(search_string=search_string, new_version=self.new_version)

        if not os.path.exists(self.folder_version_path):
            os.mkdir(self.folder_version_path)
            utilities.set_file_read_only(self.folder_version_path)

        self.get_latest_version(search_string=search_string)

        return self.folder_version_path

    def get_latest_version(self, search_string=None):

        """
        Return the latest version of the data.

        You must set the 'path_to_version' attribute.

        :param string | None search_string:
        :return: string - name of the latest version
        """

        self.set_version(search_string=search_string, new_version=False)

    def get_folder_versions(self, search_string=None):

        """
        List all the folders version in a directory from attribute 'path_to_versions'.
        Sort them and remove any files.

        :param string | None search_string:  This is the what we are looking for in the folder name.  It is case sensitive.
        :return:
        """

        if search_string is None:
            raise RuntimeError("Cannot query folder versions; Need a search string.")

        folder_contents = os.listdir(self.path_to_versions)
        folder_contents = utilities.natural_sort(text_list=folder_contents)

        # test to make sure this is not a file
        for _folder in folder_contents:
            has_period = _folder.find(".") != -1
            if has_period:
                continue

            # At the name should be a per character match in the string name
            folder_name_split = _folder.split("__")
            if search_string not in folder_name_split:
                continue

            if search_string:
                if _folder.find(search_string) != -1:

                    if _folder not in self.folder_versions:
                        self.folder_versions.append(_folder)

        # create the path to the versions as well
        for _folder in self.folder_versions:
            folder_version_path = "{0}/{1}".format(self.path_to_versions, _folder)
            if folder_version_path not in self.folder_version_paths:
                self.folder_version_paths.append(folder_version_path)

            # Append the folder number as well
            version_number = self._get_folder_version_number(folder=_folder)
            if version_number not in self.folder_version_numbers:
                self.folder_version_numbers.append(version_number)

    def print_version(self):

        """
        Prints all attributes out nicely.
        :return:
        """

        for key, val in sorted(self.__dict__.items()):
            if type(val) == list:
                print "\t", key, ":\n\t\t", "\n\t\t".join(val)
            else:
                print "\t", key, ":", val

    def set_version(self, search_string=None, version_number=None, new_version=None):

        """
        Set to the version we want to use

        :param string | None search_string:
        :param int | None version_number:
        :param bool new_version:
        :return:
        """

        add_version = 0
        if new_version:
            add_version = 1

        self.get_folder_versions(search_string=search_string)
        len_versions = len(self.folder_versions)

        if version_number:
            self.version = version_number
        else:
            if len_versions == 0:
                self.version = 1
            else:
                self.version = len_versions-1

        # If there are none, create version 1
        if len_versions is 0:
            if new_version:
                self._set_folder_version_path()

        else:
            latest = int(self.folder_versions[-1].rpartition(self.version_prefix)[2])
            self.version = latest + add_version
            self._set_folder_version_path()

        self.latest_folder_version = self.version

    def _version_from_folder(self, folder=""):

        """
        take the folder name and extract the version number suffix.

        :param string folder:  The folder name we want to query the version of.
        :return:
        """

        return int(folder.rpartition(self.version_prefix)[2])
