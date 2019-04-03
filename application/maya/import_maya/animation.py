import os
from maya import cmds
from ..cache import alembic
from ....version.folder import Version
from ....version.import_version import animation_film


class ImportVersion(animation_film.ImportAnimationVersion):

    def __init__(self):

        """
        Child of the version.export_version.Version

        Export an animation version many different uses.

        - geometry caches
        - transform caches
        - mixed geo/transform caches
        - maya offline MA files

        It is necessary to set the start and end time.  Pre-roll/post-roll will not be exported if set to none.
        """

        super(ImportVersion, self).__init__()

        # set the output meta data to maya
        self.meta_data.application = "maya"

        # Write alembic cache
        self.alembic_class = alembic.AlembicCache()
        self.cache_objects = list()
        self.cache_sets = list()

        self.maya_output_directory = ""
        self.maya_output_file_path = ""
        self.maya_output_file_name = ""

        self.maya_output_file_paths = list()
        self.maya_output_file_names = list()

    def alembic_cache_setup(self):

        """
        Prepare an alembic cache to input.

        The alembic cache
        :return:
        """

    def find_alembic_file(self):

        """
        Create the alembic name and path attributes
        :return:
        """

        # make sure you
        if self.maya_output_file_name == "":
            raise NameError("output_file_name not set for alembic")

        # make sure the file extension is set
        if self.maya_output_file_name.find(".abc") == -1:
            self.maya_output_file_name = "{0}.abc".format(self.maya_output_file_name)

        # Append to the names list
        if self.maya_output_file_name not in self.maya_output_file_names:
            self.maya_output_file_names.append(self.maya_output_file_name)

        # make sure you have a directory to put the file in
        if self.maya_output_directory == "":
            raise RuntimeError("'output_file_name' not set for alembic")

        if self.maya_output_file_path == "":
            self.maya_output_file_path = "{0}/{1}".format(
                self.maya_output_directory,
                self.maya_output_file_name
            )

        # Append to the names list
        if self.maya_output_file_path not in self.maya_output_file_paths:
            self.maya_output_file_paths.append(self.maya_output_file_path)

        return self.maya_output_file_name, self.maya_output_file_path


class AnimationFilmImport(ImportVersion):

    def __init__(self):

        """
        A final class to wrap all of the export tasks to.
        """

        super(AnimationFilmImport, self).__init__()

        self.partition = ""
        self.division = ""
        self.sequence = ""
        self.shot = ""
        self.task = ""
        self.asset = ""

        self.message = ""
        self.version_number = -1

        # this is the name of the file to output
        self.asset_file_name = ""

        self.asset_version = ""

        self.verbose = False

        self.import_alembic_under_asset_transform = True

        self.export_alembic = False
        self.export_master_scene = False
        self.export_offline_file = False

    def __call__(self):

        """
        This will create the verion and it's meta data.
        :return:
        """

        self.version.verbose = self.verbose

        # Set the shot and the asset
        self.set_shot(
            partition=self.partition,
            division=self.division,
            sequence=self.sequence,
            shot=self.shot,
            task=self.task
        )
        self.set_asset(asset_name=self.asset, force_create=True)

        # we can get the version after the asset has been set
        self.version.get_latest_version(search_string=self.asset)

        if self.version.folder_version_path == "":
            cmds.warning("Did not find any versions")
            return

        # Set the current version to the latest if has not been set
        if self.version_number == -1:
            self.version_number = self.version.latest_folder_version

        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.get_file()
        self.meta_data.load_file()
        self.meta_data.print_version()

        if "alembic" in self.meta_data.file_types:
            self.alembic_class.file_path = self.meta_data.ancillary_data["alembic_paths"][0]
            # If we will create a node from the name of the asset
            if self.import_alembic_under_asset_transform:
                self.alembic_class.import_parent = self.asset

            self.alembic_class.set_import_command()

        if self.verbose:
            self.version.print_version()

    def import_alembic_cache(self):

        """
        Imports an alembic cache
        :return:
        """

        if self.import_alembic_under_asset_transform:
            if not cmds.objExists(self.asset):
                cmds.createNode("transform", name=self.asset)

        self.alembic_class.import_cache()
