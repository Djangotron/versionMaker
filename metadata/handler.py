import json
import datetime


# setup default structure for meta data
"""
date / time
message
file location
relative file location
application
version number
user or master

further data
"""

global_data = [
    "date_time",
    "message",
    "folder_location",
    "relative_folder_location",
    "application",
    "file_types",
    "version_number",
    "publish_type",
    "long_name"
]
applications = ["maya", "houdini"]
publish_types = ["publish", "user"]


class MetaData(object):

    def __init__(self):

        """
        Sets useful information for the metadata output.  Contains a list of global attributes that will always be set.

        Allows for other possible attributes to be set here as well.
        use the 'ancillary_data' dictionary to set data based on task / type
        """

        # global data
        self.message = ""
        self.folder_location = ""
        self.relative_folder_location = ""
        self.application = ""
        self.file_types = list()
        self.version_number = -1
        self.publish_type = ""
        self.long_name = ""
        self.time_stamp = ""

        self.input_data = dict()
        self.output_data = dict()

        self.ancillary_data = dict()

        self.verbose = False

    def get_globals(self):

        """
        Sets all of the global attributes from a meta data file
        :return:
        """

        self.time_stamp = self.input_data["date_time"]
        self.message = self.input_data["message"]
        self.folder_location = self.input_data["folder_location"]
        self.relative_folder_location = self.input_data["relative_folder_location"]
        self.application = self.input_data["application"]
        self.file_types = self.input_data["file_types"]
        self.version_number = self.input_data["version_number"]
        self.publish_type = self.input_data["publish_type"]
        self.long_name = self.input_data["long_name"]
        self.ancillary_data = self.input_data["ancillary_data"]

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

    def set_globals(self):

        """
        Set all of the globals for a meta data file.
        :return:
        """

        # set the publish time
        self.time_stamp = str(datetime.datetime.now())
        self.output_data["date_time"] = self.time_stamp

        # message
        if self.message == "":
            Warning("Please set a Message")
        self.output_data["message"] = self.message

        # file_location
        if self.folder_location == "":
            raise AttributeError("Please set {0}".format(self.folder_location))
        self.output_data["folder_location"] = self.folder_location

        # file_location
        if self.relative_folder_location == "":
            raise AttributeError("Please set {0}".format(self.relative_folder_location))
        self.output_data["relative_folder_location"] = self.relative_folder_location

        # application
        if self.application == "":
            raise AttributeError("Please set {0}".format(self.application))
        self.output_data["application"] = self.application

        # file type
        if self.file_types == list():
            raise AttributeError("Please set {0}".format(self.file_types))
        self.output_data["file_types"] = self.file_types

        # Version number
        if self.version_number == "":
            raise AttributeError("Please set {0}".format(self.version_number))
        self.output_data["version_number"] = self.version_number

        # Publish
        if self.publish_type == "":
            raise AttributeError("Please set {0}".format(self.publish_type))
        self.output_data["publish_type"] = self.publish_type

        # Name
        if self.long_name == "":
            raise AttributeError("Please set {0}".format(self.long_name))
        self.output_data["long_name"] = self.long_name

        self.output_data["ancillary_data"] = self.ancillary_data

    def validate_globals_output(self):

        """
        Validates that the globals have been set
        :return:
        """

        for _global in global_data:
            if _global not in self.output_data:
                raise Warning("MetaData Global: '{0}' has not been set.".format(_global))
