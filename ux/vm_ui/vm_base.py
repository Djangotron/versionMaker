import sys, os
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...lib_vm import images
from ...version import utilities


class VersionMakerWin(QtWidgets.QWidget):

    def __init__(self, parent):

        """
        Class to
        """

        super(VersionMakerWin, self).__init__()

        self.setWindowTitle("Version Maker")

        # print __file__.replace("vm_base.py", "vm.ui")
        # ui_path = __file__.replace("vm_base.py", "vm.ui")
        # ui_path = utilities.path_conversion(path=ui_path)
        # print ui_path
        # ui_file = QtCore.QFile(ui_path)
        # print ui_file
        # ui_file.open(QtCore.QFile.ReadOnly)
        #
        # loader = QtUiTools.QUiLoader()
        # self.window = loader.load(ui_file)
        # ui_file.close()
        # self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

        self.main_layout = QtWidgets.QVBoxLayout()

        # print "test:", images.__file__.replace(images.__file__.split("\\")[-1], "")
        vm_logo = images.__file__.replace(images.__file__.split("\\")[-1], "") + r"\version_maker_maker_logo_v01.png"
        print vm_logo
        self.logo_label = QtWidgets.QLabel(self)
        self.logo_label.setPixmap(QtGui.QPixmap(vm_logo))

        # Create the job
        self.job_layout = QtWidgets.QVBoxLayout()
        self.job_layout.setStretch(0, 0)
        self.job_layout.setSpacing(0)
        self.job_layout.setContentsMargins(0, 0, 0, 0)
        self.add_job_box()
        # self.job_layout.setGeometry(QtCore.QRect(0, 10, 40, 40))

        #
        self.sequence_grid = QtWidgets.QGridLayout()
        self.add_sequence_box()

        #
        self.data_v_box = QtWidgets.QVBoxLayout()
        self.add_data_box()

        self.setLayout(self.main_layout)

        # window
        self.resize(400, 600)
        self.setParent(parent, QtCore.Qt.Window)

    def add_data_box(self):

        """
        Append data tree
        :return:
        """

        # The Ancillary data box
        self.data_tree = QtWidgets.QTreeWidget()
        self.main_layout.addWidget(self.data_tree)

    def add_job_box(self):

        """

        :return:
        """
        self.main_layout.addWidget(self.logo_label)

        self.show_label = QtWidgets.QLabel("Show:")
        self.show_text = QtWidgets.QLineEdit()

        self.job_layout.addWidget(self.show_label)
        self.job_layout.addWidget(self.show_text)

        self.main_layout.addLayout(self.job_layout)

    def add_sequence_box(self):

        """

        :return:
        """
        # self.sequence_grid.setRowStretch(0, 0)
        # self.sequence_grid.setRowStretch(1, 0)
        # self.sequence_grid.setColumnStretch(0, 0)
        # self.sequence_grid.setColumnStretch(1, 0)
        self.sequence_grid.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        # Create the labels
        self.production_label = QtWidgets.QLabel()
        self.partition_label = QtWidgets.QLabel()
        self.division_label = QtWidgets.QLabel()
        self.sequence_label = QtWidgets.QLabel()

        label_row = 0
        label_row_span = 1
        label_column_span = 1
        self.sequence_grid.addWidget(self.production_label, label_row, 0, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.partition_label, label_row, 1, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.division_label, label_row, 2, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.sequence_label, label_row, 3, label_row_span, label_column_span, QtCore.Qt.AlignTop)

        self.format_label(self.production_label, label_name="Production")
        self.format_label(self.partition_label, label_name="Partition")
        self.format_label(self.division_label, label_name="Division")
        self.format_label(self.sequence_label, label_name="Sequence")

        # Set the Actual boxes
        self.production_combo_box = QtWidgets.QComboBox()
        self.partition_combo_box = QtWidgets.QComboBox()
        self.division_combo_box = QtWidgets.QComboBox()
        self.sequence_combo_box = QtWidgets.QComboBox()

        combo_box_row = 1
        self.sequence_grid.addWidget(self.production_combo_box, combo_box_row, 0, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.partition_combo_box, combo_box_row, 1, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.division_combo_box, combo_box_row, 2, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.sequence_combo_box, combo_box_row, 3, label_row_span, label_column_span, QtCore.Qt.AlignTop)

        self.main_layout.addLayout(self.sequence_grid)

    def format_label(self, label_widget, label_name=""):

        """

        :param QWidget.QtWidgets label_widget:
        :param string label_name:
        :return:
        """

        label_widget.setText(label_name)
