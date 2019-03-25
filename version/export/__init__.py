import version.folder
import metadata.meta_data_file
import constants


class ExportVersion(object):

    def __init__(self):

        """
        Output a version of an animation a
        :return:
        """

        self.version = version.folder.Version()
        self.version.path_to_versions = "D:\\temp\\test"
        self.version.type_folder = "SH__0010__ni__animation"
        self.version.get_folder_versions()

        self.meta_data = metadata.meta_data_file.WriteFile()
        self.meta_data.publish_type = "animation"
        self.meta_data.meta_data_file_path = "{0}\\SH__0010__ni__{1}.json".format(self.version.folder_version_path, self.meta_data.publish_type)
        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.message = "testing a publish"
        self.meta_data.file_location = "{0}\\{1}.json".format(self.version.folder_version_path, self.versiontype_folder)
        self.meta_data.long_name = "SH__0010__ni__animation__v{0:04}".format(self.version.version)
        self.meta_data.file_types = "alembic"
        self.meta_data.application = "maya"

    def __call__(self):

        """
        Checks the globals are set.
        :return:
        """

        self.meta_data.set_globals()

    def run(self):

        """
        Sets the show variable
        :return:
        """

        self.version.create_version()

        self.meta_data.create_file()
        print self.meta_data.folder_version_path
