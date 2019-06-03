import os


show_path_env_key = "SHOWPATH"
show_env_key = "SHOW"
production_env_key = "PRODUCTION"
partition_env_key = "PARTITION"
division_env_key = "DVN"
sequence_env_key = "SEQ"
shot_env_key = "SHOT"
task_env_key = "TASK"


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
        self.asset_name = ""
        self.task_name = ""

        self.show_path = "{show_path}/{show}"
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

    def set_from_path(self, path=""):

        """

        :param string path:
        :return:
        """



    def return_asset_name(self):

        """

        :return:
        """



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

        if partition_env_key not in os.environ:
            raise KeyError("Envronment PRODUCTION Variable not set")

        self.sequence_name = os.environ["PRODUCTION"].replace(os.environ["PRODUCTION"]+"/sequences", "")[1:]

        return self.sequence_name

    def return_partition_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if partition_env_key not in os.environ:
            raise KeyError("Envronment {} Variable not set".format(partition_env_key))

        self.sequence_name = os.environ[partition_env_key].replace(os.environ[partition_env_key]+"/sequences", "")[1:]

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

    def return_task_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if "SHOT" not in os.environ:
            raise KeyError("Envronment SHOT Variable not set")

        self.task_name = os.environ["TASK"].replace(os.environ["SHOT"], "")[1:]

        return self.task_name

    def return_sequence_name(self):

        """
        Sets the shot name attribute and returns it.
        :return:
        """

        if "SEQ" not in os.environ:
            raise KeyError("Envronment SEQ Variable not set")

        self.sequence_name = os.environ["SEQ"].replace(os.environ["PARTITION"]+"/sequences", "")[1:]

        return self.sequence_name




def get_show(path=""):

    """

    :param string path:  File path of the scene.
    :return: dict - {"show_folder": show_folder, "show_folder_path": show_folder_path}
    """

    show_preferences = SolFolderStructure().query_project_preferences()
    show_folder = show_preferences["show_folder"]
    show_folder_path = show_preferences["show_folder_path"]
    show_folder_location = show_preferences["show_folder_location"]

    # If we find the path in the file directory we return a dict with the paths
    if path.find(show_folder) != -1:

        return_dict = {
            "show_folder": show_folder,
            "show_folder_path": show_folder_path,
            "show_folder_location": show_folder_location
        }

        return return_dict


def get_division(path):

    """
    Returns if you are in assets or shots.
    :param string path:  File path of the scene.
    :return:
    """

    folder_structure = SolFolderStructure()
    show_preferences = folder_structure.query_project_preferences()

    show_folder = show_preferences["show_folder"]
    show_folder_path = show_preferences["show_folder_path"]
    show_folder_location = show_preferences["show_folder_location"]

    # if its not found
    if path.find(show_folder_path) == -1:
        return

    partition_dict = get_partition(path=path)
    partition_folder = partition_dict["partition_folder"]
    partition_path = partition_dict["partition_path"]

    temp_path = path.replace("{0}/".format(partition_path), "")
    division_folder = temp_path.split("/")[0]

    # {show_path} / {show} / {production} / {division_type} / {division}
    division_path = folder_structure.show_divisions_path.format(
        show_path=show_folder_location,
        show=show_folder,
        production=folder_structure.production_folder,
        partition=partition_folder,
        division=division_folder
    )

    return_dict = {"division_folder": division_folder, "division_path": division_path}

    return return_dict


def get_partition(path):

    """
    Returns if you are in assets or shots.
    :param string path:  File path of the scene.
    :return:
    """

    folder_structure = SolFolderStructure()
    show_preferences = folder_structure.query_project_preferences()

    show_folder = show_preferences["show_folder"]
    show_folder_path = show_preferences["show_folder_path"]
    show_folder_location = show_preferences["show_folder_location"]

    if path.find(show_folder_path) != -1:

        production_path = "{0}/{1}/".format(show_folder_path, folder_structure.production_folder)
        temp_path = path.replace(production_path, "")

        partition = temp_path.split("/")[0]
        # {show_path} / {show} / {production} / {partition}
        partition_path = folder_structure.show_partition_path.format(
            show_path=show_folder_location,
            show=show_folder,
            production=folder_structure.production_folder,
            partition=partition
        )

        return_dict = {"partition_folder": partition, "partition_path": partition_path}

        return return_dict


def get_sequence(path):

    """
    Get the 'SHOW' environment variable.
    :return:
    """

    folder_structure = SolFolderStructure()
    show_preferences = folder_structure.query_project_preferences()

    show_folder = show_preferences["show_folder"]
    show_folder_path = show_preferences["show_folder_path"]
    show_folder_location = show_preferences["show_folder_location"]

    # if its not found
    if path.find(show_folder_path) == -1:
        return

    partition_dict = get_partition(path=path)
    partition_folder = partition_dict["partition_folder"]
    partition_path = partition_dict["partition_path"]

    division_dict = get_division(path=path)
    division_folder = division_dict["division_folder"]
    division_path = division_dict["division_path"]

    temp_path = path.replace("{0}/".format(division_path), "")
    sequence = temp_path.split("/")[0]

    # {show_path} / {show} / {production} / {division_type} / {division} / {sequence}
    sequence_path = folder_structure.show_sequences_path.format(
        show_path=show_folder_location,
        show=show_folder,
        production=folder_structure.production_folder,
        partition=partition_folder,
        division=division_folder,
        sequence=sequence
    )

    return_dict = {"sequence_folder": sequence, "sequence_path": sequence_path}

    return return_dict


def get_shot(path):

    """
    Get the 'SHOW' environment variable.
    :return:
    """

    folder_structure = SolFolderStructure()
    show_preferences = folder_structure.query_project_preferences()

    show_folder = show_preferences["show_folder"]
    show_folder_path = show_preferences["show_folder_path"]
    show_folder_location = show_preferences["show_folder_location"]

    # if its not found
    if path.find(show_folder_path) == -1:
        return

    partition_dict = get_partition(path=path)
    partition_folder = partition_dict["partition_folder"]

    division_dict = get_division(path=path)
    division_folder = division_dict["division_folder"]

    sequence_dict = get_sequence(path=path)
    sequence_folder = sequence_dict["sequence_folder"]
    sequence_path = sequence_dict["sequence_path"]

    temp_path = path.replace("{0}/".format(sequence_path), "")
    shot_folder = temp_path.split("/")[0]

    # {show_path} / {show} / {production} / {division_type} / {division} / {sequence}
    shot_path = folder_structure.show_shots_path_env.format(
        show_path=show_folder_location,
        show=show_folder,
        production=folder_structure.production_folder,
        partition=partition_folder,
        division=division_folder,
        sequence=sequence_folder,
        shot=shot_folder
    )

    return_dict = {"shot_folder": shot_folder, "shot_path": shot_path}

    return return_dict


def get_task(path):

    """
    Get the 'SHOW' environment variable.
    :return:
    """

    folder_structure = SolFolderStructure()
    show_preferences = folder_structure.query_project_preferences()
    show_folder_path = show_preferences["show_folder_path"]

    # if its not found
    if path.find(show_folder_path) == -1:
        return

    shot_dict = get_shot(path)
    shot_path = shot_dict["shot_path"]

    temp_path = path.replace("{0}/".format(shot_path), "")
    task_folder = temp_path.split("/")[0]

    # {shot_path} / {task_folder}
    task_path = folder_structure.task_path.format(
        shot_path=shot_path,
        task=task_folder
    )

    return_dict = {"task_folder": task_folder, "task_path": task_path}

    return return_dict


def set_show(path):

    """

    :param string path:
    :return:
    """

    show_folder = SolFolderStructure().query_project_preferences()["show_folder_path"]

    if path.find(show_folder) != -1:
        return show_folder
    else:
        return ""