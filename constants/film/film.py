

class Hierarchy(object):

    def __init__(self):

        """
        Creates a folder structure for a animation / vfx show.
        """

        # Folder names
        self.show_folder_location = ""
        self.show_folder = ""
        self.show_folder_path = ""

        self.production_folder = "production"

        self.assets_folder = "assets"

        self.show_partition_path = "{show_path}/{show}/{production}/{partition}"
        self.show_divisions_path = "{show_path}/{show}/{production}/{partition}/{division}"

        self.environments = []

        # Shots variables
        self.sequences_folder = "sequences"
        self.show_sequences_path = "{show_path}/{show}/{production}/{partition}/{division}/{sequence}"

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

        self.show_shots_path_env = "{show_path}/{show}/{production}/{partition}/{division}/{sequence}/{shot}"