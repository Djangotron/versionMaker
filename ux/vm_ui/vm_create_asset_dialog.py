import sys, os
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools


class CreateAsset(QtWidgets.QInputDialog):

    def __init__(self):

        """
        Get an asset name from a user input.
        """

