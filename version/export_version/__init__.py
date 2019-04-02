from .. import folder
from ...metadata import meta_data_file
from ...constants.film import hierarchy


class ExportVersion(hierarchy.Hierarchy):

    def __init__(self):

        """
        Output a version of anything.

        This instantiates the necessary folder creation class, 'Version' and 'WriteFile' from meta_data_file.

        It is your responsibility to
        :return:
        """

        super(ExportVersion, self).__init__()

        self.version = folder.Version()
        self.meta_data = meta_data_file.WriteFile()

    def example(self):

        self.version = folder.Version()
        # self.version.path_to_versions = "D:\\temp\\test"
        # self.version.type_folder = "SH__0010__ni__animation"
        self.version.get_folder_versions()

        self.meta_data = meta_data_file.WriteFile()
        # self.meta_data.publish_type = "animation"
        self.meta_data.meta_data_file_path = "{0}\\SH__0010__ni__{1}.json".format(self.version.folder_version_path, self.meta_data.publish_type)
        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.message = "testing a publish"
        self.meta_data.folder_location = "{0}\\{1}.json".format(self.version.folder_version_path, self.version.type_folder)
        self.meta_data.long_name = "SH__0010__ni__animation__v{0:04}".format(self.version.version)
        # self.meta_data.file_types = "alembic"
        # self.meta_data.application = "maya"

    def run(self):

        """
        runs the create folder command and creates the meta data file
        :return:
        """

        self.version.create_version()
        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.create_file()
