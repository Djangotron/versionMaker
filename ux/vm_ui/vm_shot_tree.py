import sys, os
from functools import partial
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...constants.film import hierarchy
from ...lib_vm import images
from functools import partial
from ...version import folder, utilities
from ...application.maya.export_maya import animation as export_animation
import vm_create_asset_dialog
import vm_set_export_variables


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

        # Import functions are created
        self.import_functions = dict()

        self.shot_folders = list()

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
        test = "\n".join(hierarchy.Hierarchy().tasks)
        task_tip = "Set the task for the:\n\n{}".format(test)
        self.task_label.setToolTip(task_tip)

        self.task_combo_box = QtWidgets.QComboBox()
        self.task_combo_box_size = QtCore.QSize(175, 25)
        self.task_combo_box.setFixedSize(self.task_combo_box_size)
        self.task_combo_box.setToolTip(task_tip)

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

        # Deselect
        self.deselect_button = QtWidgets.QPushButton("Deselect")
        self.deselect_button.setDefault(True)
        self.deselect_button.setFixedSize(QtCore.QSize(75, 25))
        self.top_row.addWidget(self.deselect_button, QtCore.Qt.AlignRight)
        self.top_row.addSpacerItem(self.spacer_1)

        # Deselect
        self.select_all_button = QtWidgets.QPushButton("Select All")
        self.select_all_button.setDefault(True)
        self.select_all_button.setFixedSize(QtCore.QSize(75, 25))
        self.top_row.addWidget(self.select_all_button, QtCore.Qt.AlignRight)
        self.top_row.addSpacerItem(self.spacer_1)

        # Create Asset
        self.create_button_stack = QtWidgets.QStackedWidget()
        self.top_row.addWidget(self.create_button_stack)
        self.create_asset_button = QtWidgets.QPushButton("Create Asset")
        self.create_asset_button.setDefault(True)
        self.create_asset_button.setFixedSize(QtCore.QSize(75, 25))
        self.top_row.addSpacerItem(self.spacer_1)

        self.create_empty_label = QtWidgets.QLabel("")
        self.create_button_stack.addWidget(self.create_empty_label)
        self.create_button_stack.addWidget(self.create_asset_button)

        # Stacked widget for
        self.io_button_stack = QtWidgets.QStackedWidget()
        # self.top_row.addWidget(self.io_button_stack, QtCore.Qt.AlignRight)

        # Import Selected
        self.import_button = QtWidgets.QPushButton("Import Selected")
        self.import_button.setDefault(True)
        self.import_button_size = QtCore.QSize(100, 25)
        self.import_button.setFixedSize(self.import_button_size)
        self.io_button_stack.addWidget(self.import_button)
        self.import_button.clicked.connect(self.import_selected)

        # Export Selected
        self.export_button = QtWidgets.QPushButton("Export Selected")
        self.export_button.setDefault(True)
        self.export_button.setFixedSize(QtCore.QSize(100, 25))
        self.io_button_stack.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_selected)

        # Set the expanding spacer
        self.expanding_spacer = QtWidgets.QSpacerItem(
            10,
            25,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.top_row.addSpacerItem(self.expanding_spacer)

        # shot export options
        self._export_options_dialog_shot = vm_set_export_variables.SetExportVariables(self)
        self.export_options_stack = QtWidgets.QStackedWidget()
        self.export_options_stack.setFixedSize(QtCore.QSize(45, 25))
        self.top_row.addWidget(self.export_options_stack)
        options_image = self.parent.icon_path + "version_maker__options__v01.png"
        self.export_options_button = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap(options_image)), "", None)
        self.export_options_button.setToolTip("Export global options for the shot.  ")
        self.export_options_stack.addWidget(self.create_empty_label)
        self.export_options_stack.addWidget(self.export_options_button)
        self.export_options_button.clicked.connect(self.export_options)

        self.expanding_spacer_1 = QtWidgets.QSpacerItem(
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
        self.remove_button.clicked.connect(self.remove_self)

        # List Widget Item to add to the parent_list_widget
        self.shot = ShotListWidget(None)

        n_items = self.parent_list_widget.count()
        self.index = n_items - 1
        self.parent_list_widget.insertItem(self.index, self.shot)

        # Set up the shot tree widget
        self.shot_tree = ShotTree(self.parent, self)
        self.shot_tree.index = self.index
        self.shot_tree.item_frame = self.item_frame
        self.shot_tree.shot_combo_box = self.shot_combo_box
        self.shot_tree.task_combo_box = self.task_combo_box
        self.item_layout.addRow(self.shot_tree)
        self.parent_list_widget.setItemWidget(self.shot, self.item_frame)

        self.task_combo_box.currentIndexChanged.connect(self.shot_tree.version_query)
        self.deselect_button.clicked.connect(self.shot_tree.clearSelection)
        self.select_all_button.clicked.connect(self.shot_tree.selectAll)
        self.create_asset_button.clicked.connect(self.shot_tree.create_asset)

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

    def import_selected(self):

        """
        Import the selected assets.
        :return:
        """

        selected_indices = self.shot_tree.selectedIndexes()

        len_selected_indices = len(selected_indices) / 2

        asset_indices = list()
        q_widget_item_widgets = list()
        for int_sel in range(len_selected_indices):

            model_index_0 = selected_indices[int_sel * 2]
            model_index_1 = selected_indices[(int_sel * 2)+1]

            asset_index = model_index_0.row()
            asset_indices.append(asset_index)

            q_widget_item = self.shot_tree.itemFromIndex(model_index_1)
            q_widget_item_widgets.append(q_widget_item)
            import_asset_func = q_widget_item.version_box.import_asset_version_control.import_asset()
            self.parent.import_queue.append(import_asset_func)

    def export_selected(self):

        """
        Exports the selected assets
        :return:
        """

        selected_indices = self.shot_tree.selectedIndexes()

        len_selected_indices = len(selected_indices) / 2

        asset_indices = list()
        q_widget_item_widgets = list()
        for int_sel in range(len_selected_indices):

            model_index_0 = selected_indices[int_sel * 2]
            model_index_1 = selected_indices[(int_sel * 2)+1]

            asset_index = model_index_0.row()
            asset_indices.append(asset_index)

            q_widget_item = self.shot_tree.itemFromIndex(model_index_1)
            q_widget_item_widgets.append(q_widget_item)
            export_asset_func = q_widget_item.version_box.export_asset_version_control.export_asset()

            if export_asset_func not in self.parent.export_func_queue:
                self.parent.export_func_queue.append(export_asset_func)

    def export_options(self):

        """
        Runs the export options dialog box
        :return:
        """

        self._export_options_dialog_shot.exec_()

    def remove_self(self):

        """
        Sets the parent to delete this widget.
        :return:
        """

        self.parent.sequence_combo_box.currentIndexChanged.disconnect(self.shot_combo_box_query)
        self.shot_combo_box.currentIndexChanged.disconnect(self.task_combo_box_query)
        self.parent.task_default_combo_box.currentIndexChanged.disconnect(self.task_combo_box_query)
        self.create_asset_button.clicked.disconnect(self.shot_tree.create_asset)
        self.shot_tree.clear()

        # Remove self from the parents list of available shot widgets
        current_index = self.parent.shot_widgets.index(self)
        self.parent.shot_widgets.pop(current_index)

        # Get the row that we are removing
        current_row = self.parent.data_list.row(self.shot)

        # Weird errors have happened here.  I think whatever goes into the 'takeItem' command
        # needs to be composed into a variable and not set as:
        #       self.parent.data_list.takeItem(self.parent.data_list.row(self.shot))
        # I have been experiencing random crashes from this command otherwise
        self.parent.data_list.takeItem(current_row)

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

        self.shot_folders = list()
        for item in os.listdir(path):
            item_path = "{0}/{1}".format(path, item)
            if os.path.isfile(item_path):
                continue
            else:
                self.shot_folders.append(item)

        if self.shot_folders == list():
            return
        else:
            for folder in self.shot_folders:
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
            for int_folder, fldr in enumerate(folders):
                if fldr.find(text) != -1:
                    index = int_folder
                self.task_combo_box.addItem(fldr)

        self.task_combo_box.setCurrentIndex(index)


class ShotTree(QtWidgets.QTreeWidget):

    def __init__(self, parent, item_setup_widget):

        """

        A wrapper for common Qt QTree tasks.
        :param QtTreeWidget parent:
        :param QtTreeWidget item_setup_widget:
        """

        super(ShotTree, self).__init__(parent)

        self.shot_asset_dict = dict()
        self.asset_version_controls = list()

        self.create_asset_dialog = vm_create_asset_dialog.CreateAsset(self)
        self.create_asset_dialog.list_publishable_scene_objects_func = self.parent().list_publishable_scene_objects_func

        self.item_frame = None
        self.shot_combo_box = None
        self.task_combo_box = None

        # VersionMakerWin
        self.parent = parent
        self.item_setup_widget = item_setup_widget
        self.setColumnCount(2)

        self.shot_box = QtWidgets.QComboBox()

        self.shot_item = QtWidgets.QTreeWidgetItem()
        self.setItemWidget(self.shot_item, 1, self.shot_box)
        self.column_names = ["Asset", "Version"]
        self.setHeaderLabels(self.column_names)
        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.setHeaderHidden(1)

        self.size_policy = QtWidgets.QSizePolicy()
        self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
        self.size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.MinimumExpanding)
        self.setSizePolicy(self.size_policy)

        self.index = -1

    def create_asset(self):

        """
        Runs the create asset dialog.
        :return:
        """

        self.create_asset_dialog.exec_()

        # Get and format the names for the versions we will create
        names = self.create_asset_dialog.cache_object_names.text().split(", ")
        names = [i for i in names if not i == ""]

        self.clear()
        self.shot_asset_dict = dict()
        self.asset_version_controls = list()

        show_folder = self.parent.show_text.text()
        if not os.path.exists(show_folder):
            return

        show_folder_location, slash, show_folder_name = show_folder.rpartition("/")

        production_folder = self.parent.production_combo_box.itemText(self.parent.production_combo_box.currentIndex())
        partition_folder = self.parent.partition_combo_box.itemText(self.parent.partition_combo_box.currentIndex())
        division_folder = self.parent.division_combo_box.itemText(self.parent.division_combo_box.currentIndex())
        sequence_folder = self.parent.sequence_combo_box.itemText(self.parent.sequence_combo_box.currentIndex())

        shot_folder = self.shot_combo_box.itemText(self.shot_combo_box.currentIndex())
        task_folder = self.task_combo_box.itemText(self.task_combo_box.currentIndex())

        shot_folder_split = shot_folder.rpartition("__")[2]
        task_folder_split = task_folder .rpartition("__")[2]

        path = "{0}/{1}/{2}/{3}/{4}/{5}/{6}/{5}__publish/".format(
            show_folder,
            production_folder,
            partition_folder,
            division_folder,
            sequence_folder,
            shot_folder,
            task_folder,
        )
        if not os.path.exists(path):
            return

        # Set everything to the output dict
        ancillary_data = {
            "path": path,
            "show_folder_location": show_folder_location,
            "show_folder_name": show_folder_name,
            "production_folder": production_folder,
            "partition": partition_folder,
            "division": division_folder,
            "sequence": sequence_folder,
            "shot": shot_folder_split,
            "task": task_folder_split
        }

        # List the folders that already exist
        folders = dict()
        for item in os.listdir(path):
            item_path = "{0}{1}".format(path, item)
            print "\t", item_path
            if os.path.isfile(item_path):
                continue
            else:
                # get the type name
                type_folder = folder.return_type_folder(item)

                # Insert the name
                if type_folder not in folders:
                    folders[type_folder] = list()

                folders[type_folder].append(item)

        # Create the folders for the assets you are creating
        for name in names:

            # TODO: Fix this so it is not maya specific
            afp = export_animation.AnimationFilmPublish()
            afp.show_folder_location = show_folder_location
            afp.show_folder = show_folder_name
            afp.partition = partition_folder
            afp.division = division_folder
            afp.sequence = sequence_folder
            afp.shot = shot_folder_split
            afp.task = task_folder_split
            afp.asset = name
            afp()

            if afp.version.type_folder not in folders:
                folders[afp.version.type_folder] = list()

            # TODO: Fix this so it is not maya specific
            print "item broke:", item
            folders[afp.version.type_folder].append(item)

        folder_versions = dict()

        # add top level items to the
        for type_folder, folder_version_names in sorted(folders.items()):

            # set the name
            asset_name = type_folder.split("__")[3]

            # create the item
            item = ShotTaskAssetItem()
            item.folder_path = path
            item.asset = asset_name
            item.type_folder = type_folder
            item()

            # Return the asset versions
            folder_versions[asset_name] = item.version_class
            setattr(item, "ancillary_data", ancillary_data)

            # Set the tree widget
            item.setText(0, asset_name)
            self.addTopLevelItem(item)

            # set the version box widget to the frame
            version_box = AssetVersionControl(self.parent, self, item)
            version_box.set_widget()
            asset_version_controls_dict = {asset_name: version_box}
            self.asset_version_controls.append(asset_version_controls_dict)
            setattr(item, "version_box", version_box)
            version_box.export_asset_version_control.query_scene_func()

            # set the size of the item to the size of the frame
            item.setSizeHint(1, version_box.frame.sizeHint())

            # list in reverse order so the latest versions are listed first
            for ver in reversed(item.version_class.folder_versions):

                index = item.version_class.folder_versions.index(ver)
                ver_num = item.version_class.folder_version_numbers[index]
                version_box.import_asset_version_control.avc_verison_box.addItem(str(ver_num))

        ancillary_data["folder_versions"] = folder_versions

        self.shot_asset_dict[shot_folder] = ancillary_data

        self.parent.import_export_changed()

    def version_query(self):

        """
        Sets the shot combo box on the
        :return:
        """

        self.clear()
        self.shot_asset_dict = dict()
        self.asset_version_controls = list()

        show_folder = self.parent.show_text.text()
        if not os.path.exists(show_folder):
            return

        show_folder_location, slash, show_folder_name = show_folder.rpartition("/")

        production_folder = self.parent.production_combo_box.itemText(self.parent.production_combo_box.currentIndex())
        partition_folder = self.parent.partition_combo_box.itemText(self.parent.partition_combo_box.currentIndex())
        division_folder = self.parent.division_combo_box.itemText(self.parent.division_combo_box.currentIndex())
        sequence_folder = self.parent.sequence_combo_box.itemText(self.parent.sequence_combo_box.currentIndex())

        shot_folder = self.shot_combo_box.itemText(self.shot_combo_box.currentIndex())
        task_folder = self.task_combo_box.itemText(self.task_combo_box.currentIndex())

        shot_folder_split = shot_folder.rpartition("__")[2]
        task_folder_split = task_folder .rpartition("__")[2]

        path = "{0}/{1}/{2}/{3}/{4}/{5}/{6}/{5}__publish/".format(
            show_folder,
            production_folder,
            partition_folder,
            division_folder,
            sequence_folder,
            shot_folder,
            task_folder,
        )
        if not os.path.exists(path):
            return

        # Set everything to the output dict
        ancillary_data = {
            "path": path,
            "show_folder_location": show_folder_location,
            "show_folder_name": show_folder_name,
            "production_folder": production_folder,
            "partition": partition_folder,
            "division": division_folder,
            "sequence": sequence_folder,
            "shot": shot_folder_split,
            "task": task_folder_split
        }

        folders = dict()
        for item in os.listdir(path):
            item_path = "{0}{1}".format(path, item)
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

        folder_versions = dict()

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

            # Return the asset versions
            folder_versions[asset_name] = item.version_class
            setattr(item, "ancillary_data", ancillary_data)

            # Set the tree widget
            item.setText(0, asset_name)
            # item.setCheckState(0, QtCore.Qt.Unchecked)
            self.addTopLevelItem(item)

            # set the version box widget to the frame
            version_box = AssetVersionControl(self.parent, self, item)
            version_box.set_widget()
            asset_version_controls_dict = {asset_name: version_box}
            self.asset_version_controls.append(asset_version_controls_dict)
            setattr(item, "version_box", version_box)
            version_box.export_asset_version_control.query_scene_func()

            # set the size of the item to the size of the frame
            item.setSizeHint(1, version_box.frame.sizeHint())

            # list in reverse order so the latest versions are listed first
            for ver in reversed(item.version_class.folder_versions):

                index = item.version_class.folder_versions.index(ver)
                ver_num = item.version_class.folder_version_numbers[index]
                version_box.import_asset_version_control.avc_verison_box.addItem(str(ver_num))

        ancillary_data["folder_versions"] = folder_versions

        self.shot_asset_dict[shot_folder] = ancillary_data


class ShotListWidget(QtWidgets.QListWidgetItem):

    def __init__(self, parent):

        """
        A wrapper for the list widget item.

        We need this to insert the shot into the shots list.
        """

        super(ShotListWidget, self).__init__(parent)

        # Make object non selectable
        self.setFlags(QtCore.Qt.NoItemFlags)


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
        self.item_layout = QtWidgets.QStackedLayout(self.frame)
        self.item_layout.setSpacing(0)

        self.export_asset_version_control = ExportAssetVersionControlWidget(self, self.parent_tree, self.item)
        self.import_asset_version_control = ImportAssetVersionControlWidget(self, self.parent_tree, self.item)

        self.item_layout.addWidget(self.import_asset_version_control)
        self.item_layout.addWidget(self.export_asset_version_control)

    def set_widget(self):

        """
        Sets the widget to the item's frame
        :return:
        """

        self.parent_tree.setItemWidget(self.item, 1, self.frame)


class ExportAssetVersionControlWidget(QtWidgets.QWidget):

    def __init__(self, parent, parent_tree, item):

        """
        Widget for the export controls in the AssetVersionControl class's stacked layout
        """
        super(ExportAssetVersionControlWidget, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()
        self.setLayout(self.row)

        self.parent_tree = parent_tree
        self.item = item

        self.cache_objects = list()

        # Create Asset
        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.setDefault(True)
        self.export_button_size = QtCore.QSize(125, 25)
        self.export_button.setFixedSize(self.export_button_size)
        self.export_button.clicked.connect(self.export_asset_clicked)
        self.row.addWidget(self.export_button, QtCore.Qt.AlignLeft)

        # Label
        self.asset_label = QtWidgets.QLabel("Scene Nodes:")
        self.asset_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.asset_label.setFixedSize(QtCore.QSize(125, 15))
        self.row.addWidget(self.asset_label, QtCore.Qt.AlignLeft)

        # Label
        self.cache_object_names = QtWidgets.QLineEdit()
        self.cache_object_names.setToolTip('Separate objects by a ", " (comma and space)')
        self.cache_object_names.setFixedSize(QtCore.QSize(400, 25))
        self.row.addWidget(self.cache_object_names, QtCore.Qt.AlignLeft)

        self.replace_button = QtWidgets.QPushButton("Get")
        self.replace_button.setFixedSize(QtCore.QSize(50, 25))
        self.replace_button.setToolTip("Get a new selection")
        self.replace_button.clicked.connect(self.replace_text)
        self.row.addWidget(self.replace_button, QtCore.Qt.AlignLeft)

        self.append_button = QtWidgets.QPushButton("Add")
        self.append_button.setFixedSize(QtCore.QSize(50, 25))
        self.append_button.setToolTip("Append more objects to a selection")
        self.append_button.clicked.connect(self.append_text)
        self.row.addWidget(self.append_button, QtCore.Qt.AlignLeft)

        shot_name = self.parent_tree.shot_combo_box.currentText()
        asset_name = item.text(0)
        self._asset_export_options_dialog_shot = vm_set_export_variables.SetAssetExportVariables(self, shot_name, asset_name)
        options_image = self.parent_tree.parent.icon_path + "version_maker__options__v01.png"
        self.options_button = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap(options_image)), "", None)
        self.options_button.setToolTip("Asset export settings")
        self.options_button.clicked.connect(self.asset_options_button)
        self.row.addWidget(self.options_button, QtCore.Qt.AlignLeft)

        self.row.addStretch()

        self.verbose = False

    def append_text(self):

        """

        :return:
        """

        object_names = self.cache_object_names.text()
        len_object_names = len(object_names)
        selection = self.parent_tree.parent.get_selection_func()

        len_asset_geo_names = len(selection)+len_object_names
        for int_geo, geo in enumerate(selection):
            if int_geo+len_object_names != len_asset_geo_names:
                object_names += ", "
            object_names += geo

        self.cache_object_names.setText(object_names)

    def asset_options_button(self):

        """

        :return:
        """

        self._asset_export_options_dialog_shot.exec_()

    def replace_text(self):

        """

        :return:
        """

        selection = self.parent_tree.parent.get_selection_func()

        len_asset_geo_names = len(selection)
        object_names = ""
        for int_geo, geo in enumerate(selection):
            object_names += geo
            if int_geo+1 != len_asset_geo_names:
                object_names += ", "

        self.cache_object_names.setText(object_names)

    def query_scene_func(self):

        """
        Returns the created assets in the publish folder and which ones you have in the scene.
        :return:
        """

        asset = self.item.asset
        asset_geo_names = list()
        try:
            asset_geo_names = self.parent_tree.parent.get_cache_objects_func(asset_name=asset)
        except NameError:
            err = "Unable to set asset for export: {0};".format(asset)
            self.parent_tree.parent.print_func(err)

        if asset_geo_names is None:
            return

        len_asset_geo_names = len(asset_geo_names)
        object_names = ""
        for int_geo, geo in enumerate(asset_geo_names):
            object_names += geo
            if int_geo+1 != len_asset_geo_names:
                object_names += ", "

        self.cache_object_names.setText(object_names)

        return asset_geo_names

    def export_asset(self):

        """
        returns a the export function and the necessary arguments to call it.
        :return:  export func, ancillary_data, asset, version
        """

        self.return_cachable_object_names()

        # Use the local - per asset - shot variables
        export_variables = self.parent_tree.item_setup_widget._export_options_dialog_shot
        if self._asset_export_options_dialog_shot.use_override_shot_globals_check.isChecked():
            export_variables = self._asset_export_options_dialog_shot

        export_variables.query_rel_frames()

        start_frame = export_variables.start_frame_row.float_box.value()
        end_frame = export_variables.end_frame_row.float_box.value()
        relative_frame_samples = export_variables.relative_frame_samples
        message = export_variables.message_edit.toPlainText()

        if self.verbose:
            self.parent_tree.parent.print_func(
                "start frame: {0}\tend frame: {1}".format(start_frame, end_frame)
            )

        self.item.ancillary_data["message"] = message
        self.item.ancillary_data["start_frame"] = start_frame
        self.item.ancillary_data["end_frame"] = end_frame
        self.item.ancillary_data["relative_frame_samples"] = relative_frame_samples
        self.item.ancillary_data["cache_objects"] = self.cache_objects

        return partial(self.parent_tree.parent.export_func, self.item.ancillary_data, self.item.asset)

    def export_asset_clicked(self):

        """
        Clicked version for exporting only this asset.
        :return:
        """

        func = self.export_asset()
        func()

    def return_cachable_object_names(self):

        """

        :return:
        """

        self.cache_objects = self.cache_object_names.text().replace(" ", "").split(",")


class ImportAssetVersionControlWidget(QtWidgets.QWidget):

    def __init__(self, parent, parent_tree, item):

        """
        Widget for the import controls in the AssetVersionControl class's stacked layout
        """

        super(ImportAssetVersionControlWidget, self).__init__(parent)

        self.row = QtWidgets.QHBoxLayout()
        self.setLayout(self.row)

        self.parent_tree = parent_tree
        self.item = item

        # set up the controls
        # avc = Asset Version Control
        self.avc_verison_label = QtWidgets.QLabel("Version:")
        self.avc_verison_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.avc_verison_label.setFixedSize(QtCore.QSize(75, 15))

        self.avc_verison_box = QtWidgets.QComboBox()
        self.avc_verison_box.setFixedSize(QtCore.QSize(50, 25))

        self.avc_basic_spacer = QtWidgets.QSpacerItem(
            30,
            25,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum
        )

        self.avc_status_label = QtWidgets.QLabel("Status:")
        self.avc_status_label.setFixedSize(QtCore.QSize(50, 25))

        # Layout for the
        self.avc_status_value_frame = QtWidgets.QFrame()
        self.avc_status_value_layout = QtWidgets.QFormLayout(self.avc_status_value_frame)
        self.avc_status_value_layout.setSpacing(0)

        self.avc_status_value_label = QtWidgets.QLabel("Published")
        self.avc_status_value_label.setFixedSize(QtCore.QSize(50, 25))

        # Create Asset
        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.setDefault(True)
        self.import_button.setFixedSize(QtCore.QSize(75, 25))
        self.import_button.clicked.connect(self.import_asset_clicked)

        # STRETCH SPACER
        self.avc_status_spacer = QtWidgets.QSpacerItem(
            10,
            25,
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        # Add the widgets
        self.row.addWidget(self.avc_verison_label)
        self.row.addWidget(self.avc_verison_box)
        self.row.addSpacerItem(self.avc_basic_spacer)
        self.row.addWidget(self.avc_status_label)
        self.row.addWidget(self.avc_status_value_label)
        self.row.addSpacerItem(self.avc_basic_spacer)
        self.row.addWidget(self.import_button, QtCore.Qt.AlignRight)
        self.row.addSpacerItem(self.avc_status_spacer)

        self.avc_verison_label.setBuddy(self.avc_verison_box)

    def import_asset(self):

        """
        set the import button for an asset clicked.
        :return:
        """

        version_number = self.avc_verison_box.itemText(self.avc_verison_box.currentIndex())

        return partial(self.parent_tree.parent.import_func, self.item.ancillary_data, self.item.asset, version_number)

    def import_asset_clicked(self):

        """
        Click the import button in the shot tree
        :return:
        """

        func = self.import_asset()
        func()


class ShotVariablesDialog(QtWidgets.QDialog):

    def __init__(self, shot_item):

        """
        Sets global data for exporting shot data.
        :param ItemSetup (QWidget) shot_item:  The QWidget class that has access to the
        """

        self.start_frame = 1001.0
        self.end_frame = 1101.0
        self.pre_roll_start_frame = 990.0

        self.shot_item = shot_item

    def set_shot_data(self):

        """
        Sets the shot data to each of the ExportAssetVersionControl
        :return:
        """

        self.shot_item.shot_tree

    def query_shot_data(self):

        """
        Returns the generic shot variables as a starting point
        :return:
        """

