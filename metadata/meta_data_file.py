import json
import os
import datetime
import handler
from ..constants import meta_data


class WriteFile(handler.MetaDataCreate):

    def __init__(self):

        """
        Create a meta data file.
        """

        super(WriteFile, self).__init__()

        self.version_file_path = ""

        self.meta_data_file_name = ""
        self.meta_data_file_path = ""
        self.meta_data_folder_path = ""

        self.current_time = str()

    def create_file(self):

        """
        Create the output meta data file for reading.
        :return:
        """

        # check it exists
        path_exists = os.path.exists(self.meta_data_folder_path)
        if not path_exists:
            raise RuntimeError("File path: '{0}' does not exist.".format(self.meta_data_folder_path))

        self.current_time = str(datetime.datetime.now())
        self.output_data["date_time"] = self.current_time

        # check the globals have been set
        self.validate_globals()

        self._format_file_name()

        with open(self.meta_data_file_path, 'w') as outfile:
            json.dump(self.output_data, outfile)

    def _format_file_name(self):

        """
        Formats the name of the meta data file.
        :return:
        """

        if self.version_file_path == "":
            raise NameError(
                "'version_file_path' not set in meta data. Unable to create meta data file."
            )

        if self.meta_data_file_name == "":
            raise NameError(
                "'meta_data_file_name' not set. Unable to create meta data file."
            )

        self.meta_data_file_path = "{0}/{1}.{2}".format(
            self.version_file_path,
            self.meta_data_file_name,
            meta_data.META_DATA_SUFFIX
        )
