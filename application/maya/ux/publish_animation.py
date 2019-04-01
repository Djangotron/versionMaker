from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
import utilities
from ..export import animation


class AnimationPublishWindow(QtCore.QObject):

    def __init__(self, parent=utilities.getMayaWindow()):
        """

        :param parent:
        """

        super(AnimationPublishWindow, self).__init__(parent)

        # https://www.programcreek.com/python/example/81317/PyQt5.QtWidgets.QMainWindow