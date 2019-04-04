import os, sys
from ..cache import alembic
from ....version.folder import Version
from ....version.import_version import animation_film
from .. import envrionment


class ImportVersion(animation_film.ImportAnimationVersion):

    def __init__(self):

        """
        Child of the version.export_version.Version

        Export an animation version many different uses.

        It is necessary to set the start and end time.  Pre-roll/post-roll will not be exported if set to none.
        """

        super(ImportVersion, self).__init__()

        # set the output meta data to maya
        self.meta_data.application = "houdini"

        # Write alembic cache
        self.alembic_archive = alembic.AlembicArchive()
        self.alembic_name = ""

        self.houdini_output_directory = ""
        self.houdini_output_file_path = ""
        self.houdini_output_file_name = ""

        self.houdini_output_file_paths = list()
        self.houdini_output_file_names = list()

    def find_alembic_file(self):

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

        # Convert to a houdini based expression based on a environment variable
        self.path = ""
        self.path_expression = ""

        self.no_version_warning = "\nDid not find any versions in '{seq}__{shot}__{task}__{asset}'\n"

        self.verbose = False

    def __call__(self):

        """
        This will create the verion and it's meta data.
        :return: bool - Returns true if a version has been found.
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
            sys.stdout.write(self.no_version_warning.format(
                seq=self.sequence,
                shot=self.shot,
                task=self.task,
                asset=self.asset
            ))
            return False

        # Set the current version to the latest if has not been set
        if self.version_number == -1:
            self.version_number = self.version.latest_folder_version

        self.meta_data.meta_data_folder_path = self.version.folder_version_path
        self.meta_data.get_file()
        self.meta_data.load_file()

        if "alembic_paths" not in self.meta_data.ancillary_data:
            sys.stdout.write(self.no_version_warning.format(
                seq=self.sequence,
                shot=self.shot,
                task=self.task,
                asset=self.asset
            ))
            return False

        self.path = self.meta_data.ancillary_data["alembic_paths"][0]
        
        if self.verbose:
            self.version.print_version()
            self.meta_data.print_version()

        return True

    def path_to_path_expression(self, envrionment_key="JOB"):

        """
        Convert the alembic path to a relative path.

        :param string envrionment_key:  The environment variable key, usually JOB or HIP
        :return: string - path_expression attribute
        """

        self.path_expression = envrionment.path_to_path_expression(path=self.path, envrionment_key=envrionment_key)

        return self.path_expression

    def import_alembic_archive(self, use_path_expression=False):

        """
        Imports an alembic cache
        :return:
        """

        # Set the path
        if use_path_expression:
            self.alembic_archive.cache_path = self.path_expression
        else:
            self.alembic_archive.cache_path = self.path

        if self.alembic_name == "":
            if self.meta_data.ancillary_data == dict():
                raise NameError("Must specify an alembic name; Optionally query ancillary data.")

            self.alembic_name = self.meta_data.long_name

        self.alembic_archive.name = self.alembic_name
        self.alembic_archive.create_from_abc_archive()

    def update_alembic_path(self, hou_node, attribute, use_path_expression=False):

        """
        Given a houdini node, this will update the cache path base on the 'AnimationFilmImport.path' attribute

        :param hou.SopNode | hou.GeoNode hou_node:  Sop or Geo node that has a path attribute.
        :param string attribute:  File attribute to update.  This is
        :param bool use_path_expression:  Uses the 'path_expression' attribute instead of 'path'
        :return:
        """

        # node exists
        if hou_node is None:
            raise RuntimeError(
                "hou_node does not exist"
            )

        node_attr = hou_node.parm(attribute)

        # attribute exists
        if node_attr is None:
            raise RuntimeError(
                "hou_node does not have attribute: '{0}'".format(attribute)
            )

        if use_path_expression:
            node_attr.set(self.path_expression)
        else:
            node_attr.set(self.path)
