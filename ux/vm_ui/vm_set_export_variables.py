import sys, os
from PySide2 import QtGui, QtCore, QtWidgets

width = 450
height = 250


class SetExportVariables(QtWidgets.QDialog):

    def __init__(self, parent):

        """

        :param <ItemSetup> parent:  parent class of this dialog
        :param is_global:
        """

        super(SetExportVariables, self).__init__(parent)

        self.setWindowTitle("Set Export Variables")

        self.box_layout = QtWidgets.QVBoxLayout(self)

        # Label
        self.top_label = QtWidgets.QLabel("Set global values for the shot", self)
        self.box_layout.addWidget(self.top_label)

        # Start Frame
        self.start_frame_row = LabelFloatRowLayout(self, label="Start Frame:")
        self.box_layout.addLayout(self.start_frame_row)
        self.start_frame_row.float_box.valueChanged.connect(self.start_frame_changed)

        self.end_frame_row = LabelFloatRowLayout(self, label="End Frame:")
        self.box_layout.addLayout(self.end_frame_row)
        self.end_frame_row.float_box.valueChanged.connect(self.end_frame_changed)

        # Relative Frame Samples
        self.relative_frame_samples = list()
        self.rel_frame_row = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.rel_frame_row)
        self.rel_frame_label = QtWidgets.QLabel("Relative Frame Samples:", self)
        self.rel_frame_row.addWidget(self.rel_frame_label)
        self.rel_frame_line = QtWidgets.QLineEdit(self)
        self.rel_frame_line.setText("-0.25, 0.25")
        self.rel_frame_row.addWidget(self.rel_frame_line)

        # Message
        self.message_label = QtWidgets.QLabel("Publish Message:", self)
        self.box_layout.addWidget(self.message_label)
        self.message_edit = QtWidgets.QTextEdit(self)
        self.message_edit.setMinimumSize(QtCore.QSize(width, height))
        self.box_layout.addWidget(self.message_edit)

        # Button Row
        self.button_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.button_row_layout)

        # Buttons
        self.accept_button = QtWidgets.QPushButton("Accept")
        self.button_row_layout.addWidget(self.accept_button)
        self.accept_button.clicked.connect(self.accept)

        self.close_button = QtWidgets.QPushButton("Close")
        self.button_row_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.reject)

        self.setLayout(self.box_layout)

    def accept(self):

        """

        :return:
        """

        self.query_rel_frames()

        super(SetExportVariables, self).accept()

    def end_frame_changed(self):

        """
        change the end frame if it is less than the start frame
        :return:
        """

        end_frame_val = self.end_frame_row.float_box.value()
        start_frame_val = self.start_frame_row.float_box.value()
        if end_frame_val < start_frame_val:
            self.end_frame_row.float_box.setValue(start_frame_val)

    def exec_(self):

        """
        Wrapper for exec_
        :return:
        """

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        super(SetExportVariables, self).exec_()

    def query_rel_frames(self):

        """
        Queries the relative frame samples to the list class attribute.
        :return:
        """

        self.relative_frame_samples = self.rel_frame_line.text().strip().split()

    def start_frame_changed(self):

        """
        change the end frame if it is less than the start frame
        :return:
        """

        start_frame_val = self.start_frame_row.float_box.value()
        if self.end_frame_row.float_box.value() < start_frame_val:
            self.end_frame_row.float_box.setValue(start_frame_val)


class SetAssetExportVariables(QtWidgets.QDialog):

    def __init__(self, parent, shot_name="", asset_name=""):

        """
        A UI for setting specific overrides for the exporting assets.

        This should be the same as SetExportVariables because some of the queried attributes in the vm_shot_tree
        need to query the same variables.

        :param <ItemSetup> parent:  parent class of this dialog
        :param <QtWidgets> parent:  Parent widget of this dialog
        :param <string> shot_name:  Name of the shot to display at the top of this dialog
        :param <string> asset_name:  Name of the asset to display at the top of this dialog
        """

        super(SetAssetExportVariables, self).__init__(parent)

        self.relative_frame_samples = list()

        self.shot_name = shot_name
        self.asset_name = asset_name

        self.setWindowTitle("Set Export Variables for:    {0}/{1}".format(shot_name, asset_name))

        self.box_layout = QtWidgets.QVBoxLayout(self)

        # Label
        self.top_label = QtWidgets.QLabel("Set global values for the shot", self)
        self.box_layout.addWidget(self.top_label)

        self.shot_globals_layout = QtWidgets.QHBoxLayout()
        self.use_shot_globals_label = QtWidgets.QLabel("Override Shot Variables:")
        self.use_override_shot_globals_check = QtWidgets.QCheckBox()
        self.use_override_shot_globals_check.stateChanged.connect(self.enable_check_box)
        self.shot_globals_layout.addWidget(self.use_shot_globals_label)
        self.shot_globals_layout.addWidget(self.use_override_shot_globals_check)
        self.box_layout.addLayout(self.shot_globals_layout)

        # Start Frame
        self.start_frame_row = LabelFloatRowLayout(self, label="Start Frame:")
        self.box_layout.addLayout(self.start_frame_row)
        self.start_frame_row.float_box.valueChanged.connect(self.start_frame_changed)
        self.start_frame_row.float_box.setEnabled(False)

        # End Frame
        self.end_frame_row = LabelFloatRowLayout(self, label="End Frame:")
        self.box_layout.addLayout(self.end_frame_row)
        self.end_frame_row.float_box.valueChanged.connect(self.end_frame_changed)
        self.end_frame_row.float_box.setEnabled(False)

        # Relative Frame Samples
        self.relative_frame_samples = list()
        self.rel_frame_row = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.rel_frame_row)
        self.rel_frame_label = QtWidgets.QLabel("Relative Frame Samples:", self)
        self.rel_frame_row.addWidget(self.rel_frame_label)
        self.rel_frame_line = QtWidgets.QLineEdit(self)
        self.rel_frame_line.setText("-0.25, 0.25")
        self.rel_frame_row.addWidget(self.rel_frame_line)

        # Message
        self.message_label = QtWidgets.QLabel("Publish Message:", self)
        self.box_layout.addWidget(self.message_label)
        self.message_edit = QtWidgets.QTextEdit(self)
        self.message_edit.setMinimumSize(QtCore.QSize(width, height))
        self.box_layout.addWidget(self.message_edit)
        self.message_edit.setEnabled(False)

        # Button Row
        self.button_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.button_row_layout)

        # Buttons
        self.accept_button = QtWidgets.QPushButton("Accept")
        self.button_row_layout.addWidget(self.accept_button)
        self.accept_button.clicked.connect(self.accept)

        self.close_button = QtWidgets.QPushButton("Close")
        self.button_row_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.reject)

    def accept(self):

        """

        :return:
        """

        self.query_rel_frames()

        super(SetAssetExportVariables, self).accept()

    def end_frame_changed(self):

        """
        change the end frame if it is less than the start frame
        :return:
        """

        end_frame_val = self.end_frame_row.float_box.value()
        start_frame_val = self.start_frame_row.float_box.value()
        if end_frame_val < start_frame_val:
            self.end_frame_row.float_box.setValue(start_frame_val)

    def enable_check_box(self):

        """
        Sets all controls enabled based on the state of the use shot globals
        :return:
        """

        is_checked = self.use_override_shot_globals_check.isChecked()
        if is_checked:
            self.start_frame_row.float_box.setEnabled(True)
            self.end_frame_row.float_box.setEnabled(True)
            self.message_edit.setEnabled(True)
        else:
            self.start_frame_row.float_box.setEnabled(False)
            self.end_frame_row.float_box.setEnabled(False)
            self.message_edit.setEnabled(False)

    def exec_(self):

        """
        Wrapper for exec_
        :return:
        """

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        super(SetAssetExportVariables, self).exec_()

    def query_rel_frames(self):

        """
        Queries the relative frame samples to the list class attribute.
        :return:
        """

        self.relative_frame_samples = [float(i) for i in self.rel_frame_line.text().strip().split()]

    def start_frame_changed(self):

        """
        change the end frame if it is less than the start frame
        :return:
        """

        start_frame_val = self.start_frame_row.float_box.value()
        if self.end_frame_row.float_box.value() < start_frame_val:
            self.end_frame_row.float_box.setValue(start_frame_val)

    def use_asset_overrides(self):

        """
        Use the asset override
        :return:
        """

        return self.use_override_shot_globals_check.isChecked()


class LabelFloatRowLayout(QtWidgets.QHBoxLayout):

    def __init__(self, parent, label="", float_value=1001.0):

        """ Simple class to wrap a few widgets together """

        super(LabelFloatRowLayout, self).__init__(parent)

        self.label = QtWidgets.QLabel(label)
        self.addWidget(self.label)

        self.float_box = QtWidgets.QDoubleSpinBox()
        self.float_box.setMinimum(0)
        self.float_box.setMaximum(1000000)
        self.float_box.setDecimals(2)
        self.float_box.setValue(1001.0)
        self.addWidget(self.float_box)
