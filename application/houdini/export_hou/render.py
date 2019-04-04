import os
from ..cache import alembic
from ....version.folder import Version
from ....version.export_version import animation_film


class ExportVersion(animation_film.ExportAnimationVersion):

    def __init__(self):

        """
        Child of the version.export_version.Version

        Export an animation version many different uses.

        - geometry caches
        - transform caches
        - mixed geo/transform caches
        - houdini offline MA files

        It is necessary to set the start and end time.  Pre-roll/post-roll will not be exported if set to none.
        """

        super(ExportVersion, self).__init__()

        # set the output meta data to houdini
        self.meta_data.application = "houdini"

        self.houdini_output_directory = ""
        self.houdini_output_file_path = ""
        self.houdini_output_file_name = ""

        self.houdini_output_file_paths = list()
        self.houdini_output_file_names = list()

    def save_master_scene(self):

        """
        Saves a version of the current scene at publish time.
        :return:
        """

    def set_name(self):

        """
        Create the alembic name and path attributes
        :return:
        """

        # make sure you
        if self.houdini_output_file_name == "":
            raise NameError("output_file_name not set for alembic")

        # make sure the file extension is set
        if self.houdini_output_file_name.find(".abc") == -1:
            self.houdini_output_file_name = "{0}.abc".format(self.houdini_output_file_name)

        # Append to the names list
        if self.houdini_output_file_name not in self.houdini_output_file_names:
            self.houdini_output_file_names.append(self.houdini_output_file_name)

        # make sure you have a directory to put the file in
        if self.houdini_output_directory == "":
            raise RuntimeError("'output_file_name' not set for alembic")

        if self.houdini_output_file_path == "":
            self.houdini_output_file_path = "{0}/{1}".format(
                self.houdini_output_directory,
                self.houdini_output_file_name
            )

        # Append to the names list
        if self.houdini_output_file_path not in self.houdini_output_file_paths:
            self.houdini_output_file_paths.append(self.houdini_output_file_path)

        return self.houdini_output_file_name, self.houdini_output_file_path


class RenderFilmPublish(ExportVersion):

    def __init__(self):

        """
        A final class to wrap all of the export tasks to.
        """

        super(RenderFilmPublish, self).__init__()

        self.partition = ""
        self.division = ""
        self.sequence = ""
        self.shot = ""
        self.task = ""
        self.asset = ""

        self.message = ""

        # this is the name of the file to output
        self.asset_file_name = ""

        self.asset_version = ""

        self.verbose = False

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

        # set the meta data attributes
        self.meta_data.message = self.message
        self.meta_data.folder_location = self.task_publish_asset_path
        self.meta_data.relative_folder_location = self.relative_task_asset_path()
        self.meta_data.long_name = self.task_publish_asset

        # Create the new version
        new_version = self.version.create_version(search_string=self.asset)

        self.meta_data.version_number = self.version.version

        self.houdini_output_directory = self.version.folder_version_path
        self.houdini_output_file_name = self.version.folder_version

        # Set the output data
        self.set_animation_export_variable()

        # copy the data from the new version
        self.meta_data.version_file_path = new_version
        self.meta_data.meta_data_file_name = self.version.folder_version
        self.meta_data.meta_data_folder_path = self.version.folder_version_path

        self.meta_data.create_file()

        if self.verbose:
            self.version.print_version()
