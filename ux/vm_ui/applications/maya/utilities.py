# import PySide2
from PySide2 import QtCore, QtUiTools, QtWidgets
from PySide2.QtGui import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as apiUI
from maya import cmds


def get_maya_window():

    maya_main_window_ptr = apiUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)

    return maya_main_window


# https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2017/ENU/Maya-SDK/files/GUID-3F96AF53-A47E-4351-A86A-396E7BFD6665-htm.html

def list_namespaces():

    """
    Returns a list of namespaces
    :return:
    """

    cmds.namespace(setNamespace=':')
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
