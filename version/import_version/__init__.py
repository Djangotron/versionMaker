from .. import folder
from ...metadata import meta_data_file
from ...constants.film import hierarchy


class ImportVersion(hierarchy.Hierarchy):

    def __init__(self):

        """
        Output a version of anything.

        This instantiates the necessary folder creation class, 'Version' and 'WriteFile' from meta_data_file.

        It is your responsibility to
        :return:
        """

        super(ImportVersion, self).__init__()

        self.version = folder.Version()
        self.meta_data = meta_data_file.ReadFile()
