import os


show_path_env_key = "SHOWPATH"
show_env_key = "SHOW"
partition_env_key = "PARTITION"
division_env_key = "DVN"
sequence_env_key = "SEQ"
shot_env_key = "SHOT"


class Hierarchy(object):

    def __init__(self):

        """
        Creates a folder structure for a animation / vfx show.

        """

        # Folder names
        self.show_folder_location = ""
        self.show_folder = ""
        self.show_folder_path = ""

        self.partition_name = ""
        self.division_name = ""
        self.sequence_name = ""
        self.shot_name = ""
        self.task_name = ""

        self.show_partition_path = "{show_path}/{show}/{production}/{partition}"
        self.show_divisions_path = "{show_path}/{show}/{production}/{partition}/{division}"
        self.show_sequences_path = "{show_path}/{show}/{production}/{partition}/{division}/{sequence}"
        self.show_shots_path = "{show_path}/{show}/{production}/{partition}/{division}/{sequence}/{sequence}__{shot}"
        self.task_path = "{shot_path}/{sequence}__{shot}__{task}"
        self.task_publish_path = "{shot_path}/{sequence}__{shot}__{task}/{sequence}__{shot}__publish"

        self.task_publish_asset_path = "{task_publish_path}/{sequence}__{shot}__{task}__{asset}"
        self.task_publish_asset = "{sequence}__{shot}__{task}__{asset}"

        self.environments = []

        # Shots variables
        self.sequences_folder = "sequences"
        self.production_folder = "production"
        self.assets_folder = "assets"

        self.divisions = [self.assets_folder, self.sequences_folder]

        # Partition, different elements such as audio, 2D or 3D
        self.partition_folders = ""
        self.two_d_folder = "2D"
        self.three_d_folder = "3D"
        self.hdri_folder = "HDRI"
        self.partitions = {
            "2D": ["comps", "HDRI", "renders"],
            "3D": ["assets", "sequences"],
            "Audio": ["music", "soundFx"]
        }

        self.tasks = ["animation", "layout", "creatureFx", "fx", "lighting"]

        # applications & publish
        self.software_maya = "maya"
        self.software_houdini = "houdini"
        self.software_publish = "publish"
        self.three_d_software = (self.software_publish, self.software_maya, self.software_houdini)

    def relative_task_asset_path(self):

        """
        Returns the asset in a shot
        :return:
        """

        return self.task_publish_asset_path.replace(self.show_folder_location, "")[1:]

    def return_production_name(self):

        """
        Returns the production folder name.
        :return:
        """

        if "PARTITION" not in os.environ:
            raise KeyError("Envronment PARTITION Variable not set")

        self.sequence_name = os.environ["PARTITION"].replace(os.environ["PARTITION"]+"/sequences", "")[1:]

        return self.sequence_name

    def return_partition_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if "PARTITION" not in os.environ:
            raise KeyError("Envronment PARTITION Variable not set")

        self.sequence_name = os.environ["PARTITION"].replace(os.environ["PARTITION"]+"/sequences", "")[1:]

        return self.sequence_name

    def return_shot_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if "SHOT" not in os.environ:
            raise KeyError("Envronment SHOT Variable not set")

        self.shot_name = os.environ["SHOT"].replace(os.environ["SEQ"], "")[1:]

        return self.shot_name

    def return_sequence_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if "SEQ" not in os.environ:
            raise KeyError("Envronment SEQ Variable not set")

        self.sequence_name = os.environ["SEQ"].replace(os.environ["PARTITION"]+"/sequences", "")[1:]

        return self.sequence_name
