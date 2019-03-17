from maya import cmds
import reference


class ExportVersion(object):

    """
    Export an animation version of either geometry or transform caches.  It is necessary to set the start and end time.

    Pre-roll/post-roll will not be exported if set to none.
    """

    def __init__(self):

        """

        """

        self.start_time = 1001.0
        self.end_time = 1100.0

        #
        self.pre_roll_start_time = None
        self.post_roll_end_time = None

    def offline_ma(self, referenced_asset=None):

        """
        Export an offline MA file of reference edits.
        :param referenced_asset:
        :return:
        """

        if referenced_asset == None:
            raise RuntimeError("You must set a referenced asset")

