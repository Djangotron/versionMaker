from PySide2 import QtCore
from PySide2.QtGui import *
import utilities


class AnimationPublishWindow(QtCore.QObject):

    def __init__(self, parent=utilities.get_maya_window()):
        """

        :param parent:
        """

        super(AnimationPublishWindow, self).__init__(parent)

        # https://www.programcreek.com/python/example/81317/PyQt5.QtWidgets.QMainWindow