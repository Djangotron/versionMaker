import sys, os
from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools
from ...lib_vm import images
from functools import partial
from ...version import utilities


class ItemSetup(QtWidgets.QWidget):

    def __init__(self, parent_list_widget, parent):

        """
        Class to setup a shot tree & shot list widget.
        :param parent_list_widget:
        """

        self.parent_list_widget = parent_list_widget
        self.parent = parent

        self.index = self.parent_list_widget

        # The frame is the widget that can hold the layout
        self.item_frame = QtWidgets.QFrame()
        self.item_frame.setLineWidth(0)
        self.item_frame.setFrameShape(QtWidgets.QFrame.NoFrame)

        # the layout can hold the widgets
        self.item_layout = QtWidgets.QFormLayout(self.item_frame)
        self.item_layout.setSpacing(0)

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

        # delete
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.setDefault(True)
        self.delete_button_size = QtCore.QSize(75, 25)
        self.delete_button.setFixedSize(self.delete_button_size)
        self.top_row.addWidget(self.delete_button, QtCore.Qt.AlignRight)

        # Connect
        self.parent.sequence_combo_box.currentIndexChanged.connect(self.shot_combo_box_query)
        self.shot_combo_box.currentIndexChanged.connect(self.task_combo_box_query)
        self.parent.task_default_combo_box.currentIndexChanged.connect(self.task_combo_box_query)
        self.delete_button.clicked.connect(lambda: self.delete_self())

        #
        self.shot = ShotListWidget(None)

        n_items = self.parent_list_widget.count()
        self.index = n_items - 1
        self.parent_list_widget.insertItem(self.index, self.shot)

        # Set up the shot tree widget
        self.shot_tree = ShotTree(self.parent)
        self.shot_tree.index = self.index
        self.shot_tree.shot_combo_box = self.shot_combo_box
        self.shot_tree.task_combo_box = self.task_combo_box
        self.item_layout.addRow(self.shot_tree)
        self.parent_list_widget.setItemWidget(self.shot, self.item_frame)

        self.task_combo_box.currentIndexChanged.connect(self.shot_tree.version_query)

        # Set the size
        self.size = QtCore.QSize(-1, 100)
        self.shot.setSizeHint(self.size)

        self.shot_combo_box_query()

    def delete_self(self):

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

        self.shot_combo_box = None
        self.task_combo_box = None

        # VersionMakerWin
        self.parent = parent
        self.setColumnCount(1)

        self.shot_box = QtWidgets.QComboBox()

        self.shot_item = QtWidgets.QTreeWidgetItem()
        self.setItemWidget(self.shot_item, 1, self.shot_box)
        self.setHeaderHidden(1)
        self.addTopLevelItem(self.shot_item)

        self.size_policy = QtWidgets.QSizePolicy()
        self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(self.size_policy)

        self.index = -1

    def version_query(self):

        """
        Sets the shot combo box on the
        :return:
        """

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
                print folder
                item = ShotTaskAssetItem()
                item.setText(0, folder)
                self.shot_item.addChild(item)


class ShotListWidget(QtWidgets.QListWidgetItem):

    def __init__(self, parent):

        """
        A wrapper for common Qt QList tasks.
        """

        super(ShotListWidget, self).__init__(parent)


class ShotTaskAssetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self):

        """
        A wrapper for common Qt QTree tasks.
        """

        super(ShotTaskAssetItem, self).__init__()

        self.addChild(QtWidgets.QTreeWidgetItem())
