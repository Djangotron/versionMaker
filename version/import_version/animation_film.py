import os
from .. import import_version
from ...constants.film import hierarchy


class ImportAnimationVersion(import_version.ExportVersion, hierarchy.Hierarchy):

    def __init__(self):

        """
        Sets common animation data to output in the meta data file.
        """

        super(ImportAnimationVersion, self).__init__()

        # hierarchy.Hierarchy.__init__(self)

        self.frame_rate = 24.0

        self.start_frame = 1001.0
        self.end_frame = 1100.0

        #
        self.pre_roll_start_frame = None
        self.post_roll_end_frame = None

    def set_shot(self, partition, division, sequence, shot, task):

        """
        Sets shot paths we are going to export an animation version for.

        the set paths are:

        show_shots_path
        task_path
        task_publish_path

        meta_data.publish_type

        :return:
        """

        self.partition_name = partition
        self.division_name = division
        self.sequence_name = sequence
        self.shot_name = shot
        self.task_name = task

        self.show_shots_path = self.show_shots_path.format(
            show_path=self.show_folder_location,
            show=self.show_folder,
            production=self.production_folder,
            partition=partition,
            division=division,
            sequence=sequence,
            shot=shot
        )

        if not os.path.exists(self.show_shots_path):
            raise Exception("Shot Path:\n{0}\nDoes not exist\n".format(self.show_shots_path))

        # set the task
        self.task_path = self.task_path.format(
            shot_path=self.show_shots_path,
            sequence=sequence,
            shot=shot,
            task=task
        )
        # set the task publish folder
        self.task_publish_path = self.task_publish_path.format(
            shot_path=self.show_shots_path,
            sequence=sequence,
            shot=shot,
            task=task
        )

        self.meta_data.publish_type = task

    def set_asset(self, asset_name="", force_create=False):

        """
        Sets the asset in the current shot.

        This will set the 'path_to_versions' & 'type_folder' attributes in the the version class

        :param string asset_name:  Name of the asset to export.  This could be a character /prop / ect.
        :param bool force_create:  This will create the path if it does not already exist.
        :return:
        """

        if self.task_publish_path == "{shot_path}/{sequence}__{shot}__{task}/{sequence}__{shot}__publish":
            raise RuntimeError("Please run '{0}.set_shot' to set the task_publish_path".format(self.__module__))

        self.task_publish_asset_path = self.task_publish_asset_path.format(
            task_publish_path=self.task_publish_path,
            sequence=self.sequence_name,
            shot=self.shot_name,
            task=self.task_name,
            asset=asset_name
        )

        self.task_publish_path = self.task_publish_path.format(
            task_publish_path=self.task_publish_path,
            sequence=self.sequence_name,
            shot=self.shot_name,
            task=self.task_name
        )

        self.task_publish_asset = self.task_publish_asset.format(
            sequence=self.sequence_name,
            shot=self.shot_name,
            task=self.task_name,
            asset=asset_name
        )

        if not os.path.exists(self.task_publish_asset_path):
            if force_create is False:
                raise Exception("Asset path:\n{0}\ndoes not exist.\n".format(
                    self.task_publish_asset_path
                ))

        # set the versionable folder
        self.version.path_to_versions = self.task_publish_path
        self.version.type_folder = self.task_publish_asset

        return_dict = {
            "task_publish_asset_path": self.task_publish_asset_path,
            "task_publish_path": self.task_publish_path,
            "task_publish_asset": self.task_publish_asset
        }

        return return_dict
