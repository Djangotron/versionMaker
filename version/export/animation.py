import os
import version.export
import constants.film.hierarchy


class ExportAnimationVersion(version.export.ExportVersion, constants.film.hierarchy.Hierarchy):

    def __init__(self):

        """
        Sets common animation data to output in the meta data file.
        """

        super(ExportAnimationVersion, self).__init__()

        if "SHOT" not in os.environ:
            raise KeyError("Envronment Variable 'SHOT' not set")

        self.version.type_folder = "{0}__animation"
        self.meta_data.publish_type = "animation"

        self.frame_rate = 24.0

        self.start_frame = 1001.0
        self.end_frame = 1100.0

        #
        self.pre_roll_start_frame = None
        self.post_roll_end_frame = None

    def set_animation_export_variable(self):

        """
        Sets common animation values to the
        :return:
        """

        if self.pre_roll_start_frame is not None:
            self.meta_data.ancillary_data["pre_roll_start_frame"] = self.pre_roll_start_frame

        if self.post_roll_end_frame is not None:
            self.meta_data.ancillary_data["post_roll_end_frame"] = self.post_roll_end_frame

        self.meta_data.ancillary_data["frame_rate"] = self.frame_rate
        self.meta_data.ancillary_data["start_frame"] = self.start_frame
        self.meta_data.ancillary_data["end_frame"] = self.end_frame

        # Set all of the meta data values to the meta data dictionary
        self.meta_data.set_globals()

    def set_folder_naming(self):

        """
        Reads the environment variables to create an output.
        :return:
        """

    def set_asset(self, asset_name=""):

        """
        Sets the
        :param string asset_name:  Name of the asset to export.  This could be a character /prop / ect.
        :return:
        """
