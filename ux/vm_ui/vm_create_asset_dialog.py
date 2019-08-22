import sys, os
from PySide2 import QtCore, QtWidgets


class CreateAsset(QtWidgets.QDialog):

    def __init__(self, parent):

        """
        Get an asset name from a user input.
        """

        super(CreateAsset, self).__init__(parent)

        self._h = 450
        self._w = 450

        # self.setMinimumWidth(self._w)
        # self.setMinimumHeight(self._h)
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
        self.available_names_list = QtWidgets.QListWidget(self)
        self.box_layout.addWidget(self.available_names_list)
        self.available_names_size = QtCore.QSize(self._w, 200)
        self.available_names_list.setFixedSize(self.available_names_size)

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
            item = CreateAssetListWidget(asset_name, self.available_names_list)


class CreateAssetListWidget(QtWidgets.QListWidgetItem):

    def __init__(self, *args):

        super(CreateAssetListWidget, self).__init__(*args)

        print "size hint:", self.parent().sizeHint()
        self.setSizeHint()
