from maya import cmds
import reference
from ..cache import alembic
from ....version.create_folder import Version
from ....metadata import handler


class ExportVersion(Version):

    def __init__(self):

        """
        Child of the version.create.Version

        Export an animation version many different uses.

        - geometry caches
        - transform caches
        - mixed geo/transform caches
        - maya offline MA files

        It is necessary to set the start and end time.  Pre-roll/post-roll will not be exported if set to none.
        """

        super(ExportVersion, self).__init__()

        self.start_frame = 1001.0
        self.end_frame = 1100.0

        #
        self.pre_roll_start_frame = None
        self.post_roll_end_frame = None

        self.alembic_class = None

        self.output_file_path = ""

    def alembic_cache_setup(self):

        """
        Prepare an alembic cache to output.

        The alembic cache
        :return:
        """

        # Write alembic cache
        self.alembic_class = alembic.AlembicCache()

        # Set the time line
        if self.pre_roll_start_frame is not None:
            self.alembic_class.pre_roll_frame = self.start_frame

        self.alembic_class.start_frame = self.start_frame
        self.alembic_class.end_frame = self.end_frame

        self.alembic_class.file_path = self.output_file_path

    def alembic_cache_write(self):

        """
        Write an alembic cache to disc.
        :return:
        """

        self.alembic_class()
        self.alembic_class.export()

    def meta_data(self):

        """

        :return:
        """

    def offline_ma_setup(self, referenced_asset=None):

        """
        Export an offline MA file of reference edits.
        :param referenced_asset:
        :return:
        """

        if referenced_asset is None:
            raise RuntimeError("You must set a referenced asset")
