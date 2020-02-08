import sys
import hou
from PySide2 import QtWidgets, QtGui, QtCore
from .....show.SOL import SOL_hou


class RenderSequenceUi(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(RenderSequenceUi, self).__init__(parent)

        self.setWindowTitle('Render Sequence')

        self.exec_btn = QtWidgets.QPushButton('Create')
        self.camera = QtWidgets.QLineEdit("")
        self.sequence = QtWidgets.QLineEdit("EL")
        self.task = QtWidgets.QLineEdit("layout")

        self.setWidth = 600
        self.setMinimumWidth = 600
        self.setFixedSize(400, 110)


    def construct_ui(self):

        """ Build the ui """

        # match look & feel to H16
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)

        # main widget
        main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(main_widget)

        # layout initialize
        g_layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QFormLayout()
        main_widget.setLayout(g_layout)

        self.exec_btn.clicked.connect(self.build)

        layout.addRow("Camera ABC Archive:", self.camera)
        layout.addRow("Sequence:", self.sequence)
        layout.addRow("Task:", self.task)

        # global layout setting
        g_layout.addLayout(layout)
        g_layout.addWidget(self.exec_btn)

    def closeEvent(self, event):

        self.setParent(None)
        super(RenderSequenceUi, self).closeEvent(event)

    def build(self):

        """
        Creates the rock in path
        :return:
        """

        cam_node = hou.node(self.camera.text())
        rig_build = SOL_hou.render_sequence(
            camera_archive=cam_node,
            sequence=self.sequence.text(),
            task=self.task.text()
        )

        self.close()

        return self


def show_window():
    """
    http://www.sidefx.com/docs/houdini/hom/hou/qt.html#mainWindow

    :return:
    """

    w = RenderSequenceUi()
    w.construct_ui()

    #  Needs to be parented to main window so it doesnt disappear on garbage collection
    w.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    w.width = 1200
    w.show()

    return w
