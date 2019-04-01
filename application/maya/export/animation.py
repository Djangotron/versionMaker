import os
from ..cache import alembic
from ....version.folder import Version
from ....version.export import animation_film


class ExportVersion(animation_film.ExportAnimationVersion):

    def __init__(self):

        """
        Child of the version.export.Version

        Export an animation version many different uses.

        - geometry caches
        - transform caches
        - mixed geo/transform caches
        - maya offline MA files

        It is necessary to set the start and end time.  Pre-roll/post-roll will not be exported if set to none.
        """

        super(ExportVersion, self).__init__()

        # set the output meta data to maya
        self.meta_data.application = "maya"

        self.alembic_class = None

        self.output_file_path = ""

    def alembic_cache_setup(self):

        """
        Prepare an alembic cache to output.

        The alembic cache
        :return:
        """

        self.meta_data.file_types = ["alembic"]

        # Write alembic cache
        self.alembic_class = alembic.AlembicCache()

        # Set the time line
        if self.pre_roll_start_frame is not None:
            self.alembic_class.pre_roll_frame = self.start_frame

        self.alembic_class.start_frame = self.start_frame
        self.alembic_class.end_frame = self.end_frame

        self.alembic_class.file_path = "{0}.abc".format(self.output_file_path)

    def alembic_cache_write(self):

        """
        Write an alembic cache to disc.
        :return:
        """

        self.alembic_class()
        self.alembic_class.export()

    def offline_ma_setup(self, referenced_asset=None):

        """
        Export an offline MA file of reference edits.
        :param referenced_asset:
        :return:
        """

        if referenced_asset is None:
            raise RuntimeError("You must set a referenced asset")

    def save_master_scene(self):

        """
        Saves a version of the current scene at publish time.
        :return:
        """


class AnimationFilmPublish(ExportVersion):

    def __init__(self):

        """
        A final class to wrap all of the export tasks to.
        """

        super(AnimationFilmPublish, self).__init__()

        self.partition = ""
        self.division = ""
        self.sequence = ""
        self.shot = ""
        self.task = ""
        self.asset = ""

        self.message = ""

        # this is the name of the file to output
        self.asset_file_name = ""

    def __call__(self):

        """
        runs the create version from the
        :return:
        """

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
        self.version.get_latest_version()

        # for key, val in sorted(self.__dict__.items()):
        #     print "\t", key, ":", val

        for key, val in sorted(self.version.__dict__.items()):
            print "\t", key, ":", val

        # set the meta data attributes
        self.meta_data.message = self.message
        self.meta_data.folder_location = self.task_publish_asset_path
        self.meta_data.relative_folder_location = self.relative_task_asset_path()
        self.meta_data.long_name = self.task_publish_asset

        # Set the output data
        self.set_animation_export_variable()

        new_version = self.version.create_version()

        self.meta_data.version_file_path = new_version
        self.meta_data.meta_data_file_name = self.task_publish_asset

        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.create_file()
