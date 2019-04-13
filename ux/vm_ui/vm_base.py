import sys, os
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...lib_vm import images
from functools import partial
from ...constants.film import hierarchy
from ...version import utilities
import vm_shot_tree


is_windows = sys.platform == "win32"
icon_path = images.__file__.replace(images.__file__.split("\\")[-1], "")


class VersionMakerWin(QtWidgets.QWidget):

    def __init__(self, parent):

        """
        Class to
        """

        super(VersionMakerWin, self).__init__()

        self.setWindowTitle("Version Maker")
        self.main_layout = QtWidgets.QVBoxLayout()

        # copy the hierarchy paths
        self.hierarchy = hierarchy.Hierarchy()

        # Logo
        vm_logo = icon_path + "version_maker_banner_v01_tenPercent.png"
        if is_windows:
            vm_logo = vm_logo.replace(os.sep, "/")

        self.logo_label = QtWidgets.QLabel(self)
        self.logo_label.setPixmap(QtGui.QPixmap(vm_logo))

        self.file_dialog = FileDialog()

        # Create the job
        self.job_path = ""
        self.job_layout = QtWidgets.QVBoxLayout()
        self.job_layout.setStretch(0, 0)
        self.job_layout.setSpacing(0)
        self.job_layout.setContentsMargins(0, 0, 0, 0)
        self.add_job_box()

        #
        self.sequence_grid = QtWidgets.QGridLayout()
        self.add_sequence_box()

        #
        self.data_v_box = QtWidgets.QVBoxLayout()

        # The Ancillary data box
        self.data_list = QtWidgets.QListWidget()
        self.main_layout.addWidget(self.data_list)

        self.setLayout(self.main_layout)

        # window
        self.resize(800, 600)
        self.setParent(parent, QtCore.Qt.Window)

        vm_shot_tree.ItemSetup(self.data_list, self)

    def __call__(self):

        """

        :return:
        """

        self.show_text.setText(self.job_path)

    def add_job_box(self):

        """
        The Job box is where we set the location of the show
        :return:
        """

        self.job_layout.addWidget(self.logo_label)

        self.show_label = QtWidgets.QLabel("Show:")
        self.show_line_layout = QtWidgets.QHBoxLayout()
        self.show_text = QtWidgets.QLineEdit()
        self.show_text_button = QtWidgets.QPushButton()

        button_logo = icon_path + "mg_icon.png"
        if is_windows:
            button_logo = button_logo.replace(os.sep, "/")
        self.show_text_button.setIcon(QtGui.QIcon(QtGui.QPixmap(button_logo)))

        self.show_text_button.clicked.connect(partial(self.file_dialog_call))

        self.job_layout.addWidget(self.show_label)
        self.job_layout.addLayout(self.show_line_layout)
        self.show_line_layout.addWidget(self.show_text)
        self.show_line_layout.addWidget(self.show_text_button)

        self.main_layout.addLayout(self.job_layout)

    def add_sequence_box(self):

        """

        :return:
        """

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

        self.show_text.textChanged.connect(self.production_combo_box_query)
        self.production_combo_box.currentIndexChanged.connect(self.partition_combo_box_query)
        self.partition_combo_box.currentIndexChanged.connect(self.division_combo_box_query)
        self.division_combo_box.currentIndexChanged.connect(self.sequence_combo_box_query)

        self.main_layout.addLayout(self.sequence_grid)

    def show_text_edit(self):

        """
        when the text is edited this will update the production folder
        :return:
        """

        if not os.path.exists(self.show_text.text()):

            # set the hierarchy env variables
            self.hierarchy.show_folder_path = ""
            self.hierarchy.show_folder_location = ""
            self.hierarchy.show_folder = ""
            return

        show_path, slash, show = self.show_text.text().rpartition("/")

        # set the hierarchy env variables
        self.hierarchy.show_folder_path = self.show_text.text()
        self.hierarchy.show_folder_location = show_path
        self.hierarchy.show_folder = show_path

    def production_combo_box_query(self):

        """
        Queries the show folder for the production folder
        :return:
        """

        clear_combo_box(self.production_combo_box)

        path = self.show_text.text()
        if not os.path.exists(path):
            return

        folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue

            elif item_path.find(".") != -1:
                continue

            else:
                folders.append(item)

        if folders == list():
            return
        else:
            for folder in folders:
                self.production_combo_box.addItem(folder)

        default_index = 0
        if "production" in folders:
            default_index = folders.index("production")

        self.production_combo_box.setCurrentIndex(default_index)

    def partition_combo_box_query(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        clear_combo_box(self.partition_combo_box)

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())

        path = "{0}/{1}".format(self.show_text.text(), production_folder)
        if not os.path.exists(path):
            return

        folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            print os.path.isfile(item_path), item_path
            if os.path.isfile(item_path):
                continue

            else:
                folders.append(item)

        if folders == list():
            return
        else:
            for folder in folders:
                self.partition_combo_box.addItem(folder)

        default_index = 0
        if "3D" in folders:
            default_index = folders.index("3D")

        self.partition_combo_box.setCurrentIndex(default_index)

    def division_combo_box_query(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        clear_combo_box(self.division_combo_box)

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())
        partition_folder = self.partition_combo_box.itemText(self.partition_combo_box.currentIndex())

        path = "{0}/{1}/{2}".format(self.show_text.text(), production_folder, partition_folder)
        if not os.path.exists(path):
            return

        folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                folders.append(item)

        if folders == list():
            return
        else:
            for folder in folders:
                self.division_combo_box.addItem(folder)

        default_index = 0
        if "sequences" in folders:
            default_index = folders.index("sequences")

        self.division_combo_box.setCurrentIndex(default_index)

    def sequence_combo_box_query(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        clear_combo_box(self.sequence_combo_box)

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())
        partition_folder = self.partition_combo_box.itemText(self.partition_combo_box.currentIndex())
        division_folder = self.division_combo_box.itemText(self.division_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}".format(self.show_text.text(), production_folder, partition_folder, division_folder)
        if not os.path.exists(path):
            return

        folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                folders.append(item)

        if folders == list():
            return
        else:
            for folder in folders:
                self.sequence_combo_box.addItem(folder)

    def file_dialog_call(self):

        """

        :return:
        """

        self.file_dialog.create()
        self.show_text.setText(self.file_dialog.folder_name)

        # self.production_combo_box_query()

    def format_label(self, label_widget, label_name=""):

        """

        :param QWidget.QtWidgets label_widget:
        :param string label_name:
        :return:
        """

        label_widget.setText(label_name)


class FileDialog(QtWidgets.QFileDialog):

    def __init__(self):

        """

        """

        super(FileDialog, self).__init__()

        self.setFileMode(QtWidgets.QFileDialog.Directory)
        self.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)

        self.folder_name = ""

    def create(self):

        self.folder_name = self.getExistingDirectory()


def clear_combo_box(combo_box):

    """

    :param QtWidget.QComboBox combo_box:
    :return:
    """

    num_options = combo_box.count()
    for int_option in range(num_options):
        val = (num_options - 1) - int_option
        combo_box.removeItem(val)
