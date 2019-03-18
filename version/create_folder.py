import os
import utilities
import read_write


class Version(object):

    def __init__(self):

        """
        Sets, gets, and queries latest version of folders with a specific suffix.

        You must set the type
        :return:
        """

        # Path to the type of data you are working with
        self.path_to_versions = ""

        # type (Name) of data folder you are dealing with
        self.type_folder = ""

        self.version_prefix = "__v"
        self.version = -1

        # Version of data
        self.folder_version_number = ""
        self.folder_version = ""
        self.folder_version_path = ""

        # All the versions
        self.folder_versions = list()
        self.latest_folder_version = 0

        self.number_padding = 4

        self.verbose = False

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

        if self.folder_version_number == "":

            if self.version == -1:

                raise AttributeError(
                    "'folder_version_number' has not been set. #"
                    "\n# Please set 'version' and run '_set_folder_version_string'."
                )

            else:
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

    def create_version(self):

        """
        Creates a new version folder for
        :return:
        """

        self.set_version(new_version=True)

        if not os.path.exists(self.folder_version_path):
            os.mkdir(self.folder_version_path)
            read_write.set_file_read_only(self.folder_version_path)

        return self.folder_version_path

    def get_latest_version(self):

        """
        Return the latest version of the data.

        You must set the 'path_to_version' attributes and
        :return:
        """

        self.get_folder_versions()

        return self.folder_versions[-1]

    def get_folder_versions(self):

        """
        List all the folders version in a directory from attribute 'path_to_versions'.
        Sort them and remove any files.

        :return:
        """

        folder_contents = os.listdir(self.path_to_versions)
        self.folder_versions = utilities.natural_sort(text_list=folder_contents)

        # test to make sure this is not a file
        for folder in self.folder_versions[::]:
            has_period = folder.find(".") != -1
            if has_period:
                self.folder_versions.remove(folder)

    def set_version(self, version_number=None, new_version=None):

        """
        Set to the version we want to use

        :param int | None version_number:
        :param bool new_version:
        :return:
        """

        add_version = 0
        if new_version:
            add_version = 1

        self.get_folder_versions()
        len_versions = len(self.folder_versions)

        if version_number:
            self.version = version_number
        else:
            if len_versions == 0:
                self.version = 0
            else:
                self.version = len_versions-1

        # If there are none, create version 1
        if len_versions is 0:
            self._set_folder_version_path()

        else:
            latest = int(self.folder_versions[-1].rpartition(self.version_prefix)[2])
            self.version = latest + add_version
            self._set_folder_version_path()

    def _version_from_folder(self, folder=""):

        """
        take the folder name and extract the version number suffix.

        :param string folder:  The folder name we want to query the version of.
        :return:
        """

        return int(folder.rpartition(self.version_prefix)[2])
