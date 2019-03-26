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


class MetaDataCreate(object):

    def __init__(self):

        """
        Sets useful information for the metadata output.  Contains a list of global attributes that will always be set.

        Allows for other possible attributes to be set here as well.
        use the 'ancillary_data' dictionary to set data based on task / type
        """

        self.global_data = [
            "date_time",
            "message",
            "file_location",
            "relative_file_path",
            "application",
            "file_types",
            "version_number",
            "publish_type",
            "long_name"
        ]

        self.further_data = [
            "start_frame",
            "end_frame",
            "pre_roll_start_frame"
        ]

        # global data
        self.message = ""
        self.file_location = ""
        self.application = ""
        self.applications = ["maya", "houdini"]
        self.file_types = list()
        self._publish_types = ["publish", "user"]
        self.version_number = -1
        self.publish_type = ""
        self.long_name = ""

        self.output_data = dict()
        self.ancillary_data = dict()

        self.verbose = False

    def set_globals(self):

        """
        Set all of the globals for a meta data file.
        :return:
        """

        # set the publish time
        self.output_data["date_time"] = str(datetime.datetime.now())

        # message
        if self.message == "":
            raise AttributeError("Please set {0}".format(self.message))
        self.output_data["message"] = self.message

        # file_location
        if self.file_location == "":
            raise AttributeError("Please set {0}".format(self.file_location))
        self.output_data["file_location"] = self.file_location

        # application
        if self.application == "":
            raise AttributeError("Please set {0}".format(self.application))
        self.output_data["application"] = self.application

        # file type
        if self.file_types == "":
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

    def validate_globals(self):

        """
        Validates that the globals have been set
        :return:
        """

        for _global in self.global_data:
            if _global not in self.output_data:
                raise Warning("MetaData Global: '{0}' has not been set.".format(_global))
