import sys, os
from PySide2 import QtCore, QtWidgets


width = 450
height = 450


class CreateAsset(QtWidgets.QDialog):

    def __init__(self, parent):

        """
        Get an asset name from a user input.
        """

        super(CreateAsset, self).__init__(parent)

        # self.setMinimumWidth(width)
        # self.setMinimumHeight(height)
        self.setWindowTitle("Create Asset Cache")

        self.get_cachable_objects_func = None
        self.list_publishable_scene_objects_func = None

        self.publishable_assets_dict = list()
        self.publishable_objects = list()

        self.box_layout = QtWidgets.QVBoxLayout(self)

        # Label
        self.available_names_label = QtWidgets.QLabel("Available Assets From Scene (double click)", self)
        self.box_layout.addWidget(self.available_names_label)

        # List assets
        self.available_names_list = AssetListWidget()
        self.box_layout.addWidget(self.available_names_list)
        self.available_names_list.itemSelectionChanged.connect(self.selection_changed)

        # Name of the asset
        self.name_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.name_row_layout)
        self.names_label = QtWidgets.QLabel("Name:", self)
        self.name_row_layout.addWidget(self.names_label)
        self.cache_object_names = QtWidgets.QLineEdit(self)
        self.name_row_layout.addWidget(self.cache_object_names)

        self.button_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.button_row_layout)

        # Buttons
        self.create_button = QtWidgets.QPushButton("Create")
        self.button_row_layout.addWidget(self.create_button)
        self.create_button.clicked.connect(self.accept)

        self.close_button = QtWidgets.QPushButton("Close")
        self.button_row_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.reject)

    def accept(self):

        """

        :return:
        """

        super(CreateAsset, self).accept()

    def double_click(self, *args):

        """
        Wrapper for double clicked
        :param args:
        :return:
        """

        self.available_names_list.clearSelection()
        self.cache_object_names.setText("")

    def exec_(self):

        self.populate()
        super(CreateAsset, self).exec_()

    def populate(self):

        """
        Populate the list of assets that are available in scene.
        :return:
        """

        if self.list_publishable_scene_objects_func is None:
            return

        self.publishable_assets_dict = self.list_publishable_scene_objects_func()

        self.available_names_list.clear()
        self.publishable_objects = list()
        for asset_name, cache_dict in self.publishable_assets_dict.items():

            self.publishable_objects.append(asset_name)
            item = QtWidgets.QListWidgetItem(asset_name, self.available_names_list)
            self.available_names_list.itemDoubleClicked.connect(self.double_click)

    def selection_changed(self):

        """
        Modifies the line edit to match the selection in the window
        :return:
        """

        selected_items = self.available_names_list.selectedItems()

        len_selected_items = len(selected_items)
        if len_selected_items == 0:
            return

        line_edit_string = ""
        for int_item in range(len_selected_items):

            asset_name = self.available_names_list.selectedItems()[int_item].text()
            line_edit_string += "{}, ".format(asset_name)

        self.cache_object_names.setText(line_edit_string)


class AssetListWidget(QtWidgets.QListWidget):

    def __init__(self):

        """ Reimplementing class for customization """
        
        super(AssetListWidget, self).__init__()

        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.q_size = QtCore.QSize(width, 200)
        self.setFixedSize(self.q_size)
