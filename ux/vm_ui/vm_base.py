import sys, os, json
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...lib_vm import images
from functools import partial
from ...constants.film import hierarchy
from ...version import utilities
import vm_shot_tree
import vm_export_wizard


is_windows = sys.platform == "win32"
icon_path = images.__file__.replace(images.__file__.split("\\")[-1], "")

# Environment keys
show_env_key = "SHOW"
partition_env_key = "PARTITION"
division_env_key = "DVN"
sequence_env_key = "SEQ"
shot_env_key = "SHOT"
task_env_key = "TASK"
all_keys = [show_env_key, partition_env_key, division_env_key, sequence_env_key, shot_env_key, task_env_key]


class VersionMakerWin(QtWidgets.QWidget):

    def __init__(self, parent, application):

        """
        Class to import and export version from a window
        """

        for entry in QtWidgets.QApplication.allWidgets():
            if type(entry).__name__ == 'VersionMakerWin':
                entry.close()

        super(VersionMakerWin, self).__init__(parent)

        for env_key in all_keys:
            if env_key not in os.environ:
                os.environ[env_key] = ""

        self.setWindowTitle("Version Maker")
        self.main_layout = QtWidgets.QVBoxLayout()

        # Application specific data
        self.application = application

        # Setup the functions for importing and exporting
        self.import_func = None
        self.export_func = None

        self.progress_bar_class = Progress()

        self.get_cache_objects_func = None
        self.get_selection_func = None
        self.list_publishable_scene_objects_func = None
        self.print_func = None

        self.sequence_folders = list()
        self.shot_folders = list()

        # Append import or export commands to this queue
        self.import_queue = list()
        self.export_func_queue = list()
        self.export_queue = list()

        # copy the hierarchy paths
        self.hierarchy = hierarchy.Hierarchy()
        self.file_dialog = FileDialog()

        # LOGO
        self.icon_path = icon_path
        vm_logo = self.icon_path + "version_maker_banner_v01_tenPercent.png"
        if is_windows:
            vm_logo = vm_logo.replace(os.sep, "/")

        self.logo_label = QtWidgets.QLabel(self)
        self.logo_label.setPixmap(QtGui.QPixmap(vm_logo))

        # Create the job
        self.job_path = ""
        self.job_layout = QtWidgets.QVBoxLayout()
        self.job_layout.setStretch(0, 0)
        self.job_layout.setSpacing(0)
        self.job_layout.setContentsMargins(0, 0, 0, 0)
        self.job_layout.addWidget(self.logo_label)

        # DIRECTORY TO FIND THE SHOW
        self.show_label = QtWidgets.QLabel("Show:")
        self.show_line_layout = QtWidgets.QHBoxLayout()
        self.show_text = QtWidgets.QLineEdit()
        self.show_text_button = QtWidgets.QPushButton()

        # Set the button to manually find a folder structure
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
        # self.add_job_box()

        # GRID LAYOUT FOR PRODUCTION / PARTITION / DIVISION / SEQUENCE
        self.sequence_grid = QtWidgets.QGridLayout()
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

        #
        combo_box_row = 1
        self.sequence_grid.addWidget(self.production_combo_box, combo_box_row, 0, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.partition_combo_box, combo_box_row, 1, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.division_combo_box, combo_box_row, 2, label_row_span, label_column_span, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.sequence_combo_box, combo_box_row, 3, label_row_span, label_column_span, QtCore.Qt.AlignTop)

        self.show_text.textChanged.connect(self.production_combo_box_query)
        self.production_combo_box.currentIndexChanged.connect(self.partition_combo_box_query)
        self.partition_combo_box.currentIndexChanged.connect(self.division_combo_box_query)
        self.division_combo_box.currentIndexChanged.connect(self.sequence_combo_box_query)

        # Set a default task
        self.task_default_label = QtWidgets.QLabel("Current Task")
        self.task_default_combo_box = QtWidgets.QComboBox()
        self.sequence_grid.addWidget(self.task_default_label, 2, 0, 1, 1, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.task_default_combo_box, 3, 0, 1, 1, QtCore.Qt.AlignTop)

        #
        self.remove_all_shots_button = QtWidgets.QPushButton("Remove all shots in list")
        self.create_all_shots_button = QtWidgets.QPushButton("Create all shots in sequence")
        self.sequence_grid.addWidget(self.remove_all_shots_button, 2, 2, 1, 1, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.create_all_shots_button, 3, 2, 1, 1, QtCore.Qt.AlignTop)
        self.remove_all_shots_button.clicked.connect(self.remove_all_shots)
        self.create_all_shots_button.clicked.connect(self.append_all_shots)

        # Set a default task
        self.in_out_label = QtWidgets.QLabel("Import / Export")
        self.in_out_combo_box = QtWidgets.QComboBox()
        self.in_out_combo_box.addItem("Import")
        self.in_out_combo_box.addItem("Export")
        self.sequence_grid.addWidget(self.in_out_label, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.sequence_grid.addWidget(self.in_out_combo_box, 3, 1, 1, 1, QtCore.Qt.AlignTop)
        self.in_out_combo_box.currentIndexChanged.connect(self.import_export_changed)

        self.shots_list_label = QtWidgets.QLabel("Shots List:")
        self.sequence_grid.addWidget(self.shots_list_label, 4, 0, 1, 1, QtCore.Qt.AlignTop)

        self.main_layout.addLayout(self.sequence_grid)

        # Setup the current task
        self.defaults_layout = QtWidgets.QHBoxLayout()

        for task in self.hierarchy.tasks:
            self.task_default_combo_box.addItem(task)

        # The Ancillary data box
        self.data_list = QtWidgets.QListWidget()
        # self.data_list.setMinimumHeight(300)
        self.append_shot_button = QtWidgets.QPushButton("Append Shot")
        self.append_shot_button.setMinimumHeight(30)

        # Final row for global IO tools
        self.final_row = QtWidgets.QHBoxLayout()

        # Stacked widget for
        self.io_button_stack = QtWidgets.QStackedWidget()
        self.io_button_stack.setFixedSize(QtCore.QSize(400, 25))

        # Import Selected
        self.import_all_selected_button = QtWidgets.QPushButton("Import Selected")
        self.import_all_selected_button.setDefault(True)
        self.import_all_selected_button.clicked.connect(self.import_selected)

        # Export Selected
        self.export_all_selected_button = QtWidgets.QPushButton("Export All Selected")
        self.export_all_selected_button.setDefault(True)
        self.export_all_selected_button.clicked.connect(self.export_selected)

        # Show Wizard
        self.show_wizard_button = QtWidgets.QPushButton("Show Export Wizard")
        self.show_wizard_button.clicked.connect(self.show_export_wizard)

        self.io_button_stack.addWidget(self.import_all_selected_button)
        self.io_button_stack.addWidget(self.export_all_selected_button)

        self.final_row.addWidget(self.io_button_stack)
        self.final_row.addWidget(self.show_wizard_button)
        # self.final_row.addWidget(self.export_all_selected_button)

        self.main_layout.addWidget(self.data_list)
        self.main_layout.addLayout(self.final_row)

        # len_main_layout = self.main_layout.count()
        # self.main_layout.setStretch(len_main_layout-1, 0)

        self.setLayout(self.main_layout)

        # List of shots and associated widgets in the list
        self.shot_widgets = list()

        # EXPORT WIZARD
        self.export_wizard = vm_export_wizard.GetterOuttaHere(self)

        # window
        self.resize(1000, 600)
        self.setParent(parent, QtCore.Qt.Window)

        # vm_shot_tree.ItemSetup(self.data_list, self)
        self.setup_append_shot_button()

    def __call__(self):

        """
        Set the initial combo box settings.
        :return:
        """

        self.show_text.setText(self.job_path)

        partition_name = hierarchy.Hierarchy().return_partition_name()
        set_combo_box(self.partition_combo_box, partition_name)

        sequence_name = hierarchy.Hierarchy().return_sequence_name()
        set_combo_box(self.sequence_combo_box, sequence_name)

        task_name = hierarchy.Hierarchy().return_task_name()
        set_combo_box(self.task_default_combo_box, task_name.split("__")[-1])

        self.progress_bar_class.create()
        self.export_wizard.progress_bar_class = self.progress_bar_class

        self.append_shot()

    def add_job_box(self):

        """
        The Job box is where we set the location of the show
        :return:
        """

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

    def append_shot(self):

        """
        Add a shot to the data_list
        :return:
        """

        shot = vm_shot_tree.ItemSetup(self.data_list, self)
        self.shot_widgets.append(shot)
        self.import_export_changed()

    def append_all_shots(self):

        """
        Add a shot to the data_list
        :return:
        """

        self.query_shots()

        current_shots = list()
        for shot_widget in self.shot_widgets:
            shot_name = shot_widget.shot_combo_box.currentText()
            current_shots.append(shot_name)

        for int_shot, shot in enumerate(self.shot_folders):

            if shot in current_shots:
                continue

            shot_item = vm_shot_tree.ItemSetup(self.data_list, self)
            shot_item.shot_combo_box.setCurrentIndex(int_shot)
            self.shot_widgets.append(shot_item)
            self.import_export_changed()

    def closeEvent(self, event):

        """
        Wrapper for the close event

        We must clean up the progress bar
        :return:
        """

        if self.progress_bar_class is not None:
            # cannot use has attr https://hynek.me/articles/hasattr/
            try:
                self.progress_bar_class.close()
            finally:
                None

    def clear_combo_box(self, combo_box):

        """

        :param QtWidget.QComboBox combo_box:
        :return:
        """

        num_options = combo_box.count()
        for int_option in range(num_options):
            val = (num_options - 1) - int_option
            combo_box.removeItem(val)

    def division_combo_box_query(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        self.clear_combo_box(self.division_combo_box)

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

    def export_selected(self):

        """
        Exports the selected assets
        :return:
        """

        for shot_widget in self.shot_widgets:
            shot_widget.export_selected()

        self.export_wizard.query_export_queue()
        self.export_wizard.exec_()

    def file_dialog_call(self):

        """
        wrapper for the file dialog command
        :return:
        """

        self.file_dialog.create()

        if os.path.exists(self.file_dialog.folder_name):
            self.show_text.setText(self.file_dialog.folder_name)

        # self.production_combo_box_query()

    def format_label(self, label_widget, label_name=""):

        """

        :param QWidget.QtWidgets label_widget:
        :param string label_name:
        :return:
        """

        label_widget.setText(label_name)

    def import_selected(self):

        """
        Import the selected assets.
        :return:
        """

    def import_export_changed(self):

        """
        Modify the current visible tools for imports and exports
        :return:
        """

        len_shot_widgets = len(self.shot_widgets)
        if len_shot_widgets == 0:
            return

        # Check if we are importing or exporting
        _in = True
        if self.in_out_combo_box.currentIndex() == 1:
            _in = False

        if _in:
            self.io_button_stack.setCurrentWidget(self.import_all_selected_button)
        else:
            self.io_button_stack.setCurrentWidget(self.export_all_selected_button)

        # Get the shot widgets
        for shot_widget in self.shot_widgets:

            if _in:
                shot_widget.create_button_stack.setCurrentWidget(shot_widget.create_empty_label)
                shot_widget.io_button_stack.setCurrentWidget(shot_widget.import_button)
                shot_widget.export_options_stack.setCurrentWidget(shot_widget.create_empty_label)
            else:
                shot_widget.create_button_stack.setCurrentWidget(shot_widget.create_asset_button)
                shot_widget.io_button_stack.setCurrentWidget(shot_widget.export_button)
                shot_widget.export_options_stack.setCurrentWidget(shot_widget.export_options_button)

            # Get the shot tree of the widget
            shot_tree = shot_widget.shot_tree.item_frame.children()[-1]
            for asset_version_control_dict in shot_tree.asset_version_controls:
                asset_name, asset_version_control = asset_version_control_dict.items()[0]

                # if we are importing or exporting
                if _in:
                    asset_version_control.item_layout.setCurrentWidget(
                        asset_version_control.import_asset_version_control
                    )

                else:
                    asset_version_control.item_layout.setCurrentWidget(
                        asset_version_control.export_asset_version_control
                    )

    def production_combo_box_query(self):

        """
        Queries the show folder for the production folder
        :return:
        """

        self.clear_combo_box(self.production_combo_box)

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

        self.clear_combo_box(self.partition_combo_box)

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())

        path = "{0}/{1}".format(self.show_text.text(), production_folder)
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
                self.partition_combo_box.addItem(folder)

        default_index = 0
        if "3D" in folders:
            default_index = folders.index("3D")

        self.partition_combo_box.setCurrentIndex(default_index)

    def query_shots(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())
        partition_folder = self.partition_combo_box.itemText(self.partition_combo_box.currentIndex())
        division_folder = self.division_combo_box.itemText(self.division_combo_box.currentIndex())
        sequence_folder = self.sequence_combo_box.itemText(self.sequence_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}/{4}".format(
            self.show_text.text(), production_folder, partition_folder, division_folder, sequence_folder
        )
        if not os.path.exists(path):
            return

        self.shot_folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                self.shot_folders.append(item)

    def remove_all_shots(self):

        """
        Removes each shot from the list by running each shots 'remove_self' command
        :return:
        """

        remove_shot_list = self.shot_widgets[::]
        for int_shot_widget, shot_widget in enumerate(remove_shot_list):
            shot_widget.remove_self()

    def return_partial_shot_export(self):

        """
        Reads the export queue partial functions and returns it's sequence, shot and asset for
        transferring to the export queue.

        :return:
        """

        self.export_queue = list()
        for export_func in self.export_func_queue:

            asset_export_dict = dict()
            asset_export_dict["sequence"] = export_func.args[0]["sequence"]
            asset_export_dict["shot"] = export_func.args[0]["shot"]
            asset_export_dict["task"] = export_func.args[0]["task"]
            asset_export_dict["asset"] = export_func.args[1]
            self.export_queue.append(asset_export_dict)

    def sequence_combo_box_query(self):

        """

        :return:
        """

        if not os.path.exists(self.show_text.text()):
            return

        self.clear_combo_box(self.sequence_combo_box)

        production_folder = self.production_combo_box.itemText(self.production_combo_box.currentIndex())
        partition_folder = self.partition_combo_box.itemText(self.partition_combo_box.currentIndex())
        division_folder = self.division_combo_box.itemText(self.division_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}".format(self.show_text.text(), production_folder, partition_folder, division_folder)
        if not os.path.exists(path):
            return

        self.sequence_folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                self.sequence_folders.append(item)

        if self.sequence_folders == list():
            return
        else:
            for folder in self.sequence_folders:
                self.sequence_combo_box.addItem(folder)

    def setup_append_shot_button(self):

        """
        Creates the append button.
        :return:
        """

        self.append_shot_button_item = QtWidgets.QListWidgetItem()

        index = self.data_list.count()-1
        self.data_list.insertItem(index, self.append_shot_button_item)
        self.data_list.setItemWidget(self.append_shot_button_item, self.append_shot_button)

        self.append_shot_button.clicked.connect(lambda: self.append_shot())

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

    def show_export_wizard(self):

        """
        Wrapper for show export wizard
        :return:
        """

        self.export_wizard.exec_()


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


def set_combo_box(combo_box, value):

    """
    Simple set value command for combo box that will pass on error.

    :param QtWidgets.QComboBox combo_box:
    :param string value: Name of the
    :return:
    """

    index = combo_box.findText(value)
    if index != -1:
        combo_box.setCurrentIndex(index)


class Progress(object):

    def __init__(self):

        """
        Class to increment progress bars in the export queue

        You must reimplement this on a per-DCC basis to link the cache output to the Ui's progress bar.

        This has been designed with maya in mind but should be capable of working for anything else that
        uses Qt.
        """

        self.qt_widget = None

        self.time_changed_id = None
        self.time_unit_changed_id = None
        self.call_back_id = None

        self.current_frame = 1001.0
        self.min_frame = 1001
        self.max_frame = 1002

    def create(self):

        """

        :return:
        """

    def close(self):

        """
        Remove the call back
        :return:
        """

    def set_widget(self):

        """ Set the time changed callback """

    def update(self, *args):

        """
        Used to update the UI based on the change of frame.
        :return:
        """