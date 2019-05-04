import sys, os
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...lib_vm import images
from functools import partial
from ...version import folder, utilities


ITEM_HEIGHT = 50
ORANGE = [255, 153, 51, 100]
BLUE = [0, 174, 239, 100]


class ItemSetup(QtWidgets.QWidget):

    def __init__(self, parent_list_widget, parent):

        """
        Class to setup a shot tree & shot list widget.
        :param parent_list_widget:
        """

        super(ItemSetup, self).__init__()

        self.parent_list_widget = parent_list_widget
        self.parent = parent

        self.index = self.parent_list_widget

        # The frame is the widget that can hold the layout
        self.item_frame = QtWidgets.QFrame()
        self.item_frame.setLineWidth(0)
        self.item_frame.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.item_frame_size_policy = QtWidgets.QSizePolicy()
        # self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
        self.item_frame_size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
        self.item_frame.setSizePolicy(self.item_frame_size_policy)

        # the layout can hold the widgets
        self.item_layout = QtWidgets.QFormLayout(self.item_frame)
        self.item_layout.setSpacing(0)
        self.item_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)

        self.top_row = QtWidgets.QHBoxLayout()
        self.item_layout.addRow(self.top_row)

        # set up the controls
        # shot
        self.shot_label = QtWidgets.QLabel("Shot:")
        self.shot_label_size = QtCore.QSize(50, 25)
        self.shot_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.shot_label.setFixedSize(self.shot_label_size)

        self.shot_combo_box = QtWidgets.QComboBox()
        self.shot_combo_box_size = QtCore.QSize(150, 25)
        self.shot_combo_box.setFixedSize(self.shot_combo_box_size)

        self.shot_label.setBuddy(self.shot_combo_box)
        self.top_row.addWidget(self.shot_label)
        self.top_row.addWidget(self.shot_combo_box)

        # task
        self.task_label = QtWidgets.QLabel("Task:")
        self.task_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.task_label_size = QtCore.QSize(50, 25)
        self.task_label.setFixedSize(self.shot_label_size)

        self.task_combo_box = QtWidgets.QComboBox()
        self.task_combo_box_size = QtCore.QSize(200, 25)
        self.task_combo_box.setFixedSize(self.task_combo_box_size)

        self.task_label.setBuddy(self.task_combo_box)
        self.top_row.addWidget(self.task_label)
        self.top_row.addWidget(self.task_combo_box)

        self.spacer_1 = QtWidgets.QSpacerItem(
            5,
            25,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        )
        self.top_row.addSpacerItem(self.spacer_1)

        # Create Asset
        self.create_asset_button = QtWidgets.QPushButton("Create Asset")
        self.create_asset_button.setDefault(True)
        self.create_asset_button_size = QtCore.QSize(125, 25)
        self.create_asset_button.setFixedSize(self.create_asset_button_size)
        self.top_row.addWidget(self.create_asset_button, QtCore.Qt.AlignRight)

        self.top_row.addSpacerItem(self.spacer_1)

        # Create Asset
        self.import_button = QtWidgets.QPushButton("Import Checked")
        self.import_button.setDefault(True)
        self.import_button_size = QtCore.QSize(125, 25)
        self.import_button.setFixedSize(self.import_button_size)
        self.top_row.addWidget(self.import_button, QtCore.Qt.AlignRight)

        # Set the expanding spacer
        self.expanding_spacer = QtWidgets.QSpacerItem(
            10,
            25,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.top_row.addSpacerItem(self.expanding_spacer)

        # Remove
        self.remove_button = QtWidgets.QPushButton("Remove")
        self.remove_button.setDefault(True)
        self.remove_button_size = QtCore.QSize(75, 25)
        self.remove_button.setFixedSize(self.remove_button_size)
        self.top_row.addWidget(self.remove_button, QtCore.Qt.AlignRight)

        # Connect
        self.parent.sequence_combo_box.currentIndexChanged.connect(self.shot_combo_box_query)
        self.shot_combo_box.currentIndexChanged.connect(self.task_combo_box_query)
        self.parent.task_default_combo_box.currentIndexChanged.connect(self.task_combo_box_query)
        self.remove_button.clicked.connect(lambda: self.remove_self())

        # List Widget Item to add to the parent_list_widget
        self.shot = ShotListWidget(None)

        n_items = self.parent_list_widget.count()
        self.index = n_items - 1
        self.parent_list_widget.insertItem(self.index, self.shot)

        # Set up the shot tree widget
        self.shot_tree = ShotTree(self.parent)
        self.shot_tree.index = self.index
        self.shot_tree.item_frame = self.item_frame
        self.shot_tree.shot_combo_box = self.shot_combo_box
        self.shot_tree.task_combo_box = self.task_combo_box
        self.item_layout.addRow(self.shot_tree)
        self.parent_list_widget.setItemWidget(self.shot, self.item_frame)

        self.task_combo_box.currentIndexChanged.connect(self.shot_tree.version_query)

        # Set the size from the child widgets
        self.shot.setSizeHint(self.item_frame.sizeHint())

        self.size_policy = QtWidgets.QSizePolicy()
        self.size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(self.size_policy)

        self.shot_combo_box_query()

        col = QtGui.QColor(*ORANGE)
        if self.index % 2 == 0:
            col = QtGui.QColor(*BLUE)
        self.shot.setBackground(QtGui.QBrush(col))

    def import_checked_asset(self):

        """

        :return:
        """

        # Create an import command here from a versionmaker.version


    def remove_self(self):

        """
        Sets the parent to delete this widget.
        :return:
        """

        self.parent.sequence_combo_box.currentIndexChanged.disconnect(self.shot_combo_box_query)
        self.shot_combo_box.currentIndexChanged.disconnect(self.task_combo_box_query)
        self.parent.task_default_combo_box.currentIndexChanged.disconnect(self.task_combo_box_query)

        # Remove self from the parents list of available shot widgets
        self.parent.shot_widgets.pop(self.parent.shot_widgets.index(self))

        self.parent.data_list.takeItem(self.parent.data_list.row(self.shot))

        # reset the colours
        for i in range(self.parent_list_widget.count()):

            col = QtGui.QColor(*ORANGE)
            if i % 2 == 0:
                col = QtGui.QColor(*BLUE)
            self.parent_list_widget.item(i).setBackground(QtGui.QBrush(col))

    def shot_combo_box_query(self):

        """
        Sets the shot combo box on the
        :return:
        """

        if not os.path.exists(self.parent.show_text.text()):
            return

        self.parent.clear_combo_box(self.shot_combo_box)

        production_folder = self.parent.production_combo_box.itemText(self.parent.production_combo_box.currentIndex())
        partition_folder = self.parent.partition_combo_box.itemText(self.parent.partition_combo_box.currentIndex())
        division_folder = self.parent.division_combo_box.itemText(self.parent.division_combo_box.currentIndex())
        sequence_folder = self.parent.sequence_combo_box.itemText(self.parent.sequence_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}/{4}".format(
            self.parent.show_text.text(), production_folder, partition_folder, division_folder, sequence_folder
        )
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
                self.shot_combo_box.addItem(folder)

    def task_combo_box_query(self):

        """
        Sets the shot combo box on the
        :return:
        """

        if not os.path.exists(self.parent.show_text.text()):
            return

        self.parent.clear_combo_box(self.task_combo_box)

        production_folder = self.parent.production_combo_box.itemText(self.parent.production_combo_box.currentIndex())
        partition_folder = self.parent.partition_combo_box.itemText(self.parent.partition_combo_box.currentIndex())
        division_folder = self.parent.division_combo_box.itemText(self.parent.division_combo_box.currentIndex())
        sequence_folder = self.parent.sequence_combo_box.itemText(self.parent.sequence_combo_box.currentIndex())
        shot_folder = self.shot_combo_box.itemText(self.shot_combo_box.currentIndex())

        text = self.parent.task_default_combo_box.itemText(self.parent.task_default_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}/{4}/{5}".format(
            self.parent.show_text.text(),
            production_folder,
            partition_folder,
            division_folder,
            sequence_folder,
            shot_folder
        )
        if not os.path.exists(path):
            return

        folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                folders.append(item)

        index = -1
        if folders == list():
            return
        else:
            for int_folder, folder in enumerate(folders):
                if folder.find(text) != -1:
                    index = int_folder
                self.task_combo_box.addItem(folder)

        self.task_combo_box.setCurrentIndex(index)


class ShotTree(QtWidgets.QTreeWidget):

    def __init__(self, parent):

        """

        A wrapper for common Qt QTree tasks.
        :param QtTreeWidget parent:
        """

        super(ShotTree, self).__init__(parent)

        self.item_frame = None
        self.shot_combo_box = None
        self.task_combo_box = None

        # VersionMakerWin
        self.parent = parent
        self.setColumnCount(2)

        self.shot_box = QtWidgets.QComboBox()

        self.shot_item = QtWidgets.QTreeWidgetItem()
        self.setItemWidget(self.shot_item, 1, self.shot_box)
        self.column_names = ["Asset", "Version"]
        self.setHeaderLabels(self.column_names)
        # self.setHeaderHidden(1)

        self.size_policy = QtWidgets.QSizePolicy()
        self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
        self.size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Maximum)
        self.setSizePolicy(self.size_policy)

        self.index = -1

    def version_query(self):

        """
        Sets the shot combo box on the
        :return:
        """

        self.clear()

        if not os.path.exists(self.parent.show_text.text()):
            return

        production_folder = self.parent.production_combo_box.itemText(self.parent.production_combo_box.currentIndex())
        partition_folder = self.parent.partition_combo_box.itemText(self.parent.partition_combo_box.currentIndex())
        division_folder = self.parent.division_combo_box.itemText(self.parent.division_combo_box.currentIndex())
        sequence_folder = self.parent.sequence_combo_box.itemText(self.parent.sequence_combo_box.currentIndex())

        shot_folder = self.shot_combo_box.itemText(self.shot_combo_box.currentIndex())
        task_folder = self.task_combo_box.itemText(self.task_combo_box.currentIndex())

        path = "{0}/{1}/{2}/{3}/{4}/{5}/{6}/{5}__publish/".format(
            self.parent.show_text.text(),
            production_folder,
            partition_folder,
            division_folder,
            sequence_folder,
            shot_folder,
            task_folder,
        )
        if not os.path.exists(path):
            return

        folders = dict()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                # get the type name
                type_folder = folder.return_type_folder(item)

                # Insert the name
                if type_folder not in folders:
                    folders[type_folder] = list()

                folders[type_folder].append(item)

        # return if there are no folders
        if folders == list():
            return

        # add top level items to the
        for type_folder, folder_version_names in folders.items():

            # set the name
            asset_name = type_folder.split("__")[3]

            # create the item
            item = ShotTaskAssetItem()
            item.folder_path = path
            item.asset = asset_name
            item.type_folder = type_folder
            item()

            # Set the tree widget
            item.setText(0, asset_name)
            self.addTopLevelItem(item)

            item.setCheckState(0, QtCore.Qt.Unchecked)

            # set the version box widget to the frame
            version_box = AssetVersionControl(self.parent, self, item)
            version_box.set_widget()

            # set the size of the item to the size of the frame
            item.setSizeHint(1, version_box.frame.sizeHint())

            # list in reverse order so the latest versions are listed first
            for ver in reversed(item.version_class.folder_versions):

                index = item.version_class.folder_versions.index(ver)
                ver_num = item.version_class.folder_version_numbers[index]
                version_box.avc_verison_box.addItem(str(ver_num))


class ShotListWidget(QtWidgets.QListWidgetItem):

    def __init__(self, parent):

        """
        A wrapper for the list widget item.

        We need this to insert the shot into the shots list.
        """

        super(ShotListWidget, self).__init__(parent)


class ShotTaskAssetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self):

        """
        A wrapper for common QTreeWidgetItem tasks and settings.

        This houses each individual assets publish versions and file paths.
        """

        super(ShotTaskAssetItem, self).__init__()

        self.folder_path = str()

        self.version_class = folder.Version()
        self.asset = ""
        self.type_folder = ""  # Type folder is folder name sans version number

        # self.addChild(QtWidgets.QTreeWidgetItem())

    def __call__(self):

        """
        Call to set version class
        :return:
        """

        self.version_class.path_to_versions = self.folder_path
        self.version_class.type_folder = self.type_folder
        self.version_class.get_latest_version(search_string=self.asset)

        print "versions:", self.version_class.folder_versions


class AssetVersionControl(QtWidgets.QWidget):

    def __init__(self, parent, parent_tree=None, item=None):

        """
        This is a widget to select the version and run commands on the widget
        """

        super(AssetVersionControl, self).__init__(parent)

        # Set the parents
        self.parent_tree = parent_tree
        self.item = item

        self.frame = QtWidgets.QFrame()
        self.frame.setLineWidth(0)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)

        # the layout can hold the widgets
        self.item_layout = QtWidgets.QFormLayout(self.frame)
        self.item_layout.setSpacing(0)
        self.item_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)

        self.top_row = QtWidgets.QHBoxLayout()
        # self.top_row.addSpacing(0.1)
        self.item_layout.addRow(self.top_row)

        # set up the controls
        # shot
        self.avc_verison_label = QtWidgets.QLabel("Version:")
        self.avc_verison_label_size = QtCore.QSize(75, 15)
        self.avc_verison_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.avc_verison_label.setFixedSize(self.avc_verison_label_size)

        self.avc_verison_box = QtWidgets.QComboBox()
        self.avc_verison_box_size = QtCore.QSize(100, 25)
        self.avc_verison_box.setFixedSize(self.avc_verison_box_size)

        self.avc_basic_spacer = QtWidgets.QSpacerItem(
            30,
            25,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        )

        self.avc_status_label = QtWidgets.QLabel("Status:")
        self.avc_status_label.setFixedSize(self.avc_verison_box_size)

        # Layout for the
        self.avc_status_value_frame = QtWidgets.QFrame()
        self.avc_status_value_layout = QtWidgets.QFormLayout(self.avc_status_value_frame)
        self.avc_status_value_layout.setSpacing(0)

        self.avc_status_value_label = QtWidgets.QLabel("Published")
        self.avc_status_value_label.setFixedSize(self.avc_verison_box_size)

        # Create Asset
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.setDefault(True)
        self.import_button_size = QtCore.QSize(125, 25)
        self.import_button.setFixedSize(self.import_button_size)

        # STRETCH SPACER
        self.avc_status_spacer = QtWidgets.QSpacerItem(
            10,
            25,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        # Add the widgets
        self.top_row.addWidget(self.avc_verison_label)
        self.top_row.addWidget(self.avc_verison_box)
        self.top_row.addSpacerItem(self.avc_basic_spacer)
        self.top_row.addWidget(self.avc_status_label)
        self.top_row.addWidget(self.avc_status_value_label)
        self.top_row.addSpacerItem(self.avc_basic_spacer)
        self.top_row.addWidget(self.import_button, QtCore.Qt.AlignRight)
        self.top_row.addSpacerItem(self.avc_status_spacer)

        # self.top_row.addLayout(self.avc_status_value_layout)
        # self.avc_status_value_layout.addWidget(self.avc_status_value_label)

        self.avc_verison_label.setBuddy(self.avc_verison_box)

    def set_widget(self):

        """

        :return:
        """

        self.parent_tree.setItemWidget(self.item, 1, self.frame)


class AncillaryDataWidget(QtWidgets.QWidget):

    def __init__(self):

        """
        This widget Displays the versions meta data
        """

        super(AncillaryDataWidget, self).__init__()

