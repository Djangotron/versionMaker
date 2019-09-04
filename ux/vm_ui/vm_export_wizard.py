from PySide2 import QtGui, QtCore, QtWidgets, QtUiTools

width = 600
height = 450


class GetterOuttaHere(QtWidgets.QDialog):

    def __init__(self, parent):

        """
        Open a wizard to list all of the outputs and visualize them as the cache / output
        """

        super(GetterOuttaHere, self).__init__(parent)

        self.setWindowTitle("Version Maker Export Wizard")

        # Top level layout
        self.box_layout = QtWidgets.QVBoxLayout(self)

        # Label
        self.top_label = QtWidgets.QLabel("Export the following:", self)
        self.box_layout.addWidget(self.top_label)

        # Objects to export
        self.shot_asset_list = QtWidgets.QListWidget(self)
        self.box_layout.addWidget(self.shot_asset_list)

        # Button Row
        self.button_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.button_row_layout)

        # RUN BUTTON
        self.run_button = QtWidgets.QPushButton("Run")
        self.button_row_layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run)

        # CLOSE BUTTON
        self.close_button = QtWidgets.QPushButton("Close")
        self.button_row_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.reject)

        self.setLayout(self.box_layout)

        self.setMinimumSize(QtCore.QSize(width, height))

    def exec_(self):
        """
        Wrapper for exec_
        :return:
        """

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        super(GetterOuttaHere, self).exec_()

    def query_export_queue(self):

        """
        Query the parent UI's export queue
        :return:
        """

        # Convert the selected partial functions into queue exports
        self.parent().return_partial_shot_export()

        for int_exp, exp in enumerate(self.parent().export_queue):

            id = "{0}_{1}_{2}_{3}".format(exp["sequence"], exp["shot"], exp["task"], exp["asset"])

            item = ExportTaskItem(self.shot_asset_list)
            item.exp_task_widget.sequence.setText(exp["sequence"])
            item.exp_task_widget.shot.setText(exp["shot"])
            item.exp_task_widget.task.setText(exp["task"])
            item.exp_task_widget.asset.setText(exp["asset"])

    def run(self):

        """
        Run the export of the queue items
        :return:
        """

        # # Get all of the items for the list
        # self.query_export_queue()

        # print len(self.parent().export_func_queue)
        # print len(self.parent().export_queue)
        for int_exp, exp in enumerate(self.parent().export_queue):

            # print int_exp, exp
            # print "\t", dir(self.parent().export_func_queue[int_exp])
            # print "\t", self.parent().export_func_queue[int_exp].func
            # print "\t", self.parent().export_func_queue[int_exp].args
            self.parent().export_func_queue[int_exp]()


class ExportTaskWidget(QtWidgets.QWidget):

    def __init__(self, parent):

        """
        A wrapper for the list widget item.

        We need this to insert the shot into the shots list.
        """

        super(ExportTaskWidget, self).__init__(parent)

        # Labels
        self.column_names = ["Sequence", "Shot", "Task", "Asset", "Progress"]  # To show you the order
        self.sequence = QtWidgets.QLabel("Sequence")
        self.shot = QtWidgets.QLabel("Shot")
        self.task = QtWidgets.QLabel("Task")
        self.asset = QtWidgets.QLabel("Asset")

        # Create the layout
        self.item_frame = QtWidgets.QFrame()
        self.item_layout = QtWidgets.QHBoxLayout(self.item_frame)

        # Add the widgetes
        self.item_layout.addWidget(self.sequence)
        self.item_layout.addWidget(self.shot)
        self.item_layout.addWidget(self.task)
        self.item_layout.addWidget(self.asset)

        self.setLayout(self.item_layout)


class ExportTaskItem(QtWidgets.QListWidgetItem):

    def __init__(self, parent):

        """
        A wrapper for the list widget item.

        We need this to insert the shot into the shots list.
        """

        super(ExportTaskItem, self).__init__(parent)

        self.exp_task_widget = ExportTaskWidget(parent)
        parent.parent().shot_asset_list.setItemWidget(self, self.exp_task_widget.item_frame)

        self.setSizeHint(self.exp_task_widget.item_layout.sizeHint())
