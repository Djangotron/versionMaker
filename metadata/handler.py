import json


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
        """

        self.global_data = [
            "date",
            "message",
            "file_location",
            "relative_file_path",
            "application",
            "file_type",
            "version_number",
            "publish_type",
            "long_name"
        ]

        self.further_data = [
            "start_frame",
            "end_frame",
            "pre_roll_start_frame"
        ]

        self.output_data = dict()

        self.verbose = False

    def validate_globals(self):

        """
        Validates that the globals have been set
        :return:
        """

        for _global in self.global_data:
            if _global not in self.output_data:
                raise AttributeError("MetaData Global: '{0}' has not been set.".format(_global))
