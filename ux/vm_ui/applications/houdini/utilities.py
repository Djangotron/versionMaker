import hou
from PySide2 import QtCore, QtUiTools, QtWidgets
# from shiboken2 import wrapInstance


def get_houdini_window():

    # main_window = wrapInstance(long(hou.ui.mainQtWindow()), QtWidgets.QWidget)

    return hou.ui.mainQtWindow()
