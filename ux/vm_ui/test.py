import sys
import re
from PySide2 import QtGui, QtCore, QtWidgets


# class TestWindow(QtWidgets.QDialog):
#     def __init__(self):
#         super(TestWindow, self).__init__()
#         layout = QtWidgets.QVBoxLayout()
#         self.setLayout(layout)
#         button = QtWidgets.QPushButton('hi i am a dialog')
#         button.clicked.connect(self.close)
#         layout.addWidget(button)
#         self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
#         self.show()


# class MainWindow(QtWidgets.QWidget): # or QMainWindow
#
#     def __init__(self):
#
#         """
#
#         """
#
#         self.can_exit = True
#
#     def closeEvent(self, event):
#         # do stuff
#         if self.can_exit:
#             event.accept() # let the window close
#         else:
#             event.ignore()

class TestWindow(QtWidgets.QWidget):
    def createInsertBoxes(self):
        # Create new Widget with GridLayout
        insert = QtWidgets.QGroupBox("Inputs")
        insertLayout = QtWidgets.QGridLayout()

        # Frames
        nframes = QtWidgets.QLabel('Number of Frames')
        insertLayout.addWidget(nframes, 1, 1)
        self.frames = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.frames, 1, 2)

        # Time UI Mins
        mins = QtWidgets.QLabel('Minutes')
        insertLayout.addWidget(mins, 2, 1, 0)
        self.minutes = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.minutes, 2, 2)

        # Time UI Secs
        secs = QtWidgets.QLabel('Seconds')
        insertLayout.addWidget(secs, 3, 1, 0)
        self.seconds = QtWidgets.QLineEdit()
        insertLayout.addWidget(self.seconds, 3, 2)

        # Set Layout of this section
        insert.setLayout(insertLayout)
        return insert

    def createResultBoxes(self):

        result = QtWidgets.QGroupBox("Results")
        resultLayout = QtWidgets.QGridLayout()

        # ResultUI
        self.res = QtWidgets.QLabel('Result', self)

        resultLayout.addWidget(self.res, 1, 2)
        self.res.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        result.setLayout(resultLayout)
        return result

    def calc(self):
        frames = self.frames.displayText()
        if frames == "":
            frames = 0
        else:
            frames = int(re.search(r'\d+', frames).group())

        mins = self.minutes.displayText()
        if mins == "":
            mins = 0
        else:
            mins = int(re.search(r'\d+', mins).group())

        secs = self.seconds.displayText()
        if secs == "":
            secs = 0
        else:
            secs = int(re.search(r'\d+', secs).group())

        # Res in Seconds
        res = (secs + mins * 60) * frames
        # Res to
        m, s = divmod(res, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        res = str(d) + " Days " + str(h) + " Hours " + str(m) + " Minutes " + str(s) + " Seconds "

        self.res.setText(res)

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        mainLayout = QtWidgets.QGridLayout()

        # AddInsertLayout
        mainLayout.addWidget(self.createInsertBoxes(), 1, 1)

        # AddResultLayout
        mainLayout.addWidget(self.createResultBoxes(), 2, 1)

        # Make Button to Trigger Calculation
        calcB = QtWidgets.QPushButton("Calculate")
        mainLayout.addWidget(calcB, 3, 1, 1, 1)

        # Button Events
        self.connect(calcB, QtCore.SIGNAL('clicked()'), self.calc)

        # Apply Layout
        mainLayout.setRowMinimumHeight(3, 1)
        mainLayout.setSpacing(2)
        self.setLayout(mainLayout)

        # Apply Houdini styling to the main widget.
        self.setProperty("houdiniStyle", True)
        self.show()