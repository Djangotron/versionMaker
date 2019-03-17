import json
import os
import datetime
import handler


class WriteFile(handler.MetaDataCreate):

    def __init__(self):

        """
        Create a meta data file.
        """

        super(WriteFile, self).__init__()

        self.meta_data_file_path = ""

        self.current_time = str()

    def create_file(self):

        """
        Create the output meta data file for reading.
        :return:
        """

        # check it exists
        path_exists = os.path.exists(self.meta_data_file_path)
        if not path_exists:
            raise RuntimeError("File path: '{0}' does not exist.".format(self.meta_data_file_path))

        # check the globals have been set
        self.validate_globals()

        self.current_time = str(datetime.datetime.now())
        self.__global_data["date_time"] = self.current_time

        with open(self.meta_data_file_path, 'w') as outfile:
            json.dump(self.output_data, outfile)
