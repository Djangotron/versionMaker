import os, shutil, sorting

__author__ = 'chrish'


class Folder:

    def __init__(self):

        """
        Create the folder structure for a tech rig asset
        :return:
        """

        # Directories
        self.disk = "vdisk"

        # show
        self.show = ""
        self.show_environment_key = "SHOW"
        # show_directory - path to the job location

        # Scene
        self.scene = ""
        self.scene_environment_key = "SCENE"

        # Shot
        self.shot = ""
        self.shot_environment_key = "SHOT"

        # Task
        self.task = ""
        self.task_environment_key = "TASK"

        # User
        self.user = ""
        self.user_environment_key = "USER"

        # work location4
        self.user_workspace_path = ""

        # asset_directory - path to the asset, located under the job
        self.asset_directory = "work/assets/assetb/"
        self.asset = ""

        # top data directory
        self.tech_rig_data = "techRigData"

        # sub data directory
        self.attribute_settings = "attributeSettings"
        self.blend_shape_weights = "blendShapeWeights"
        self.cloth_attributes = "clothAttributes"
        self.cloth_constraints = "clothConstraints"
        self.cloth_weights = "clothWeights"
        self.parenting = "parenting"
        self.pose_driver_folder = "poseDrivers"
        self.pose_reader_folder = "poseReaders"
        self.skin_weights_folder = "skinWeights"
        self.skeleton_folder = "skeleton"

        # all the paths
        self.show_path = ""
        self.asset_path = ""

        #
        self.tech_rig_data_path = ""

        #
        self.folders = [
            self.attribute_settings,
            self.blend_shape_weights,
            self.cloth_attributes,
            self.cloth_constraints,
            self.cloth_weights,
            self.parenting,
            self.pose_driver_folder,
            self.pose_reader_folder,
            self.skin_weights_folder,
            # self.skeleton_folder
        ]

        self.verbose = False

    def __call__(self):

        """
        Sets the default vaiables
        :return:
        """

        # Get all the necessary info
        self._get_show()
        self._get_scene()
        self._get_shot()
        self._get_task()
        self._get_user()

        self._set_workspace_path()
        # self._set_asset_path()
        self._set_tech_rig_data_path()
        self.create_data_folder()
        self.create_sub_directories()

    def _get_show(self):

        """
        Gets the job from environment variables
        :return:
        """

        if self.show == "":

            if self.show_environment_key not in os.environ:
                raise Exception(
                    "\nEnvironment variable:\n '{0}.job_environment_key' not in os.environ".format(self.__module__)
                )

            self.show = os.environ[self.show_environment_key]

    def _get_scene(self):

        """
        Sets the scene attribute from environment
        :return:
        """

        if self.scene == "":
            self.scene = os.environ[self.scene_environment_key]

    def _get_shot(self):

        """
        Sets the shot attribute from environment
        :return:
        """

        if self.shot == "":
            self.shot = os.environ[self.shot_environment_key]

    def _get_task(self):

        """
        Sets the task attribute from environment
        :return:
        """

        if self.task == "":
            self.task = os.environ[self.task_environment_key]

    def _get_user(self):

        """
        Sets the user attribute from environment
        :return:
        """

        if self.user == "":
            self.user = os.environ[self.user_environment_key]

    def _get_asset(self):

        """

        :return:
        """

        if self.asset == "":
            self.asset = os.environ[self.show_environment_key].split("/")[7]

    def _set_workspace_path(self):

        """

        :return:
        """

        self.user_workspace_path = "/{disk}/{show}/{scene}/{shot}/{task}/work_{user}/workspace".format(
            disk=self.disk,
            show=self.show,
            scene=self.scene,
            shot=self.shot,
            task=self.task,
            user=self.user
        )

        user_workspace_exists = os.path.exists(self.user_workspace_path)

        if not user_workspace_exists:

            raise Exception("Directory: {0} Does not exist.".format(self.user_workspace_path))

        if not os.path.exists(self.user_workspace_path):

            os.mkdir(self.user_workspace_path)

    def _set_asset_path(self):

        """

        :return:
        """

        if self.show_path == "":

            raise Exception("Job path has not been set, could not set {0}.asset_path".format(self.__module__))

        self.asset_path = "{disk}/{jobsDirectory}/{job}/{assetsDirectory}{asset}".format(
            disk=self.disk,
            jobsDirectory=self.show_directory,
            job=self.show,
            assetsDirectory=self.asset_directory,
            asset=self.asset
        )

    def _set_tech_rig_data_path(self):

        """

        :return:
        """

        self.tech_rig_data_path = "{0}/{1}".format(self.user_workspace_path, self.tech_rig_data)

    def create_data_folder(self):

        """
        Creates the tech rig data folders
        :return:
        """

        tech_rig_data_path_exists = os.path.exists(self.tech_rig_data_path)

        if not tech_rig_data_path_exists:

            os.makedirs(self.tech_rig_data_path, 0777)
            if self.verbose:
                print "Created Path:", self.tech_rig_data_path

        elif self.verbose:
            print "Path Exists:", self.tech_rig_data_path

        else:
            pass

    def create_sub_directories(self):

        """
        Creates all the folders that you will save data versions to.
        :return:
        """

        if self.tech_rig_data_path == "":

            raise Exception("{0}.tech_rig_data_path path has not been set".format(self.__class__))

        for folder in self.folders:

            path = "{0}/{1}/{2}".format(self.user_workspace_path, self.tech_rig_data, folder)

            if not os.path.exists(path):

                os.makedirs(path, 0777)
                if self.verbose:
                    print "Created Path:", path

            else:
                if self.verbose:
                    print "Path Exists:", path

    def remove_data_folder(self):

        """

        :return:
        """

        if self.tech_rig_data_path == "":

            raise Exception("{0}.tech_rig_data_path path has not been set".format(self.__class__))

        shutil.rmtree(self.tech_rig_data_path)

    def setup(self):

        """
        Requires the call or all the default varaible to be setup prior to running
        :return:
        """

        self.create_data_folder()
        self.create_sub_directories()


class Version(Folder):

    def __init__(self):

        """
        Does a look up for versions
        :return:
        """

        self.version_prefix = "v"
        self.version = 1

        # Path to the type of data you are working with
        self.type_folder = ""
        self.type_folder_path = ""

        # Version of data
        self.folder_version = ""
        self.folder_version_path = ""

        # All the versions
        self.folder_versions = list()
        self.latest_folder_version = 0

        self.number_padding = 3

        self.verbose = False

        Folder.__init__(self)

    def _get_folder_versions(self):

        """
        list all the folders version in a directory
        :return:
        """

        self._set_folder_version_path()
        self._set_type_folder_path()
        self.folder_versions = sorting.natural_sort(text_list=os.listdir(self.type_folder_path))

        # test to make sure this is not a file
        for folder in self.folder_versions[::]:

            has_period = folder.find(".") != -1

            if has_period:

                self.folder_versions.remove(folder)

    def _set_folder_version(self):

        """

        :return:
        """

        self.folder_version = "{prefix}{intVersion:0{numPad}d}".format(
            prefix=self.version_prefix,
            intVersion=self.version,
            numPad=self.number_padding
        )

    def _set_folder_version_path(self):

        """

        :return:
        """

        self._set_folder_version()
        self._set_type_folder_path()

        self.folder_version_path = "{typeFolder}/{version}".format(
            typeFolder=self.type_folder_path,
            version=self.folder_version
        )

    def _set_paths(self):

        """

        :return:
        """

        self.__call__()

    def _set_type_folder_path(self):

        """

        :return:
        """

        self.type_folder_path = "{path}/{typeFolder}".format(path=self.tech_rig_data_path, typeFolder=self.type_folder)

    def create_version(self):

        """
        Creates a version folder for
        :return:
        """

        self.set_version()

        if not os.path.exists(self.folder_version_path):

            os.mkdir(self.folder_version_path)

    def get_latest_version(self):

        """

        :return:
        """

        self._get_folder_versions()

    def set_version(self, new_version=None):

        """

        :return:
        """

        add_version = 0
        if new_version != False:
            add_version = 1

        self._set_paths()
        self._get_folder_versions()

        # If there are none, create version 1
        if self.folder_versions == []:
            self._set_folder_version_path()

        else:
            latest = int(self.folder_versions[-1].replace(self.version_prefix, ""))
            self.version = latest + add_version
            self._set_folder_version_path()

        # print "{0}: version set to path: {1}".format()


class Data(Version):

    def __init__(self):

        """
        Creates the data path for a type of data, specified in dataPath.Folder().folders.

        *NOTE*
        You HAVE TO set the data type and then run the call on the Data class.
        (This is because it sets the folder type for you!)
        :return:
        """

        self.data_type = ""

        self.data_file_name = ""
        self.data_file_path = ""

        self.data_file_type = "json"

        Version.__init__(self)

    def __call__(self):

        """
        Sets the folder type from the data type
        :return:
        """

        Folder.__call__(self)

    def _check_data_type(self):

        """
        Check if the data_type is set to one of the proper folder types
        :return:
        """

        if self.data_type not in self.folders:

            raise Exception("{0}.data_type: '{1}' is not in folders".format(self.__module__, self.data_type))

    def _set_data_file_name(self):

        """
        Set the name of the savable file
        :return:
        """

        self._check_data_type()

        if self.data_type == "skeleton":
            self.data_file_type = "ma"

        self.data_file_name = "{dataType}_{folderVersion}.{fileType}".format(
            dataType=self.data_type,
            folderVersion=self.folder_version,
            fileType=self.data_file_type
        )

    def save(self, new_version=None):

        """
        Returns a new version to save

        :param new_version:
        :return:
        """

        self._check_data_type()

        # set the type so we can name things appropriately
        self.type_folder = self.data_type
        # Find the latest version so we can create the path and name the file
        self.set_version(new_version=new_version)
        # set the file name
        self._set_data_file_name()
        # Create a new folder
        self.create_version()

        self.data_file_path = "{path}/{file_name}".format(
            path=self.folder_version_path,
            file_name=self.data_file_name
        )

        return self.data_file_path

    def load(self):

        """

        :return:
        """

        self._check_data_type()

        # set the type so we can name things appropriately
        self.type_folder = self.data_type

        # Find the latest version so we can create the path and name the file
        self.set_version(new_version=False)

        # set the file name
        self._set_data_file_name()

        self.data_file_path = "{path}/{file_name}".format(
            path=self.folder_version_path,
            file_name=self.data_file_name)

        return self.data_file_path

    def print_types(self):

        """
        Quick way to print out all the folder types.
        :return:
        """

        print "\nCurrent folder types implemented are:"

        for folder in self.folders:

            print folder
