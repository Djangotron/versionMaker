from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
import utilities


class AnimationPublishWindow(QtCore.QObject):

    def __init__(self, parent=utilities.getMayaWindow()):
        """

        :param parent:
        """

        super(AnimationPublishWindow, self).__init__(parent)
