from PySide2 import QtCore, QtUiTools
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI


def getMayaWindow():
    apiUI.MQtUtil.mainWindow()
    ptr = apiUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtCore.QObject)