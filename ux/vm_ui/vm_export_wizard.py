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

        self.ids = list()

        self.progress_bar_class = None

        # Top level layout
        self.box_layout = QtWidgets.QVBoxLayout(self)

        # Label
        self.labels_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.labels_layout)
        self.top_label = QtWidgets.QLabel("Export the following:", self)
        self.labels_layout.addWidget(self.top_label)
        self.drag_label = QtWidgets.QLabel("(Drag and drop to reorder)", self, QtCore.Qt.AlignRight)
        self.labels_layout.addWidget(self.drag_label)

        # Objects to export
        self.shot_asset_list = QtWidgets.QListWidget(self)
        self.shot_asset_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.shot_asset_list.setWindowFlags(QtCore.Qt.NoItemFlags)
        self.box_layout.addWidget(self.shot_asset_list)

        # Button Row
        self.button_row_layout = QtWidgets.QHBoxLayout(self)
        self.box_layout.addLayout(self.button_row_layout)

        # RUN BUTTON
        self.run_button = QtWidgets.QPushButton("Run")
        self.button_row_layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run)

        # CLEAR BUTTON
        self.clear_button = QtWidgets.QPushButton("clear")
        self.button_row_layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear)

        # CLOSE BUTTON
        self.close_button = QtWidgets.QPushButton("Close")
        self.button_row_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.reject)

        self.setLayout(self.box_layout)

        self.setMinimumSize(QtCore.QSize(width, height))

    def clear(self):

        """
        Deletes all queued outputs
        :return:
        """

        count = self.shot_asset_list.count()
        for i in range(count):

            widget = self.shot_asset_list.item(i)
            print widget, widget.id
            index = self.ids.index(widget.id)
            self.ids.pop(index)

            # TODO take item does not take all items
            self.shot_asset_list.takeItem(count - i)

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

        print self.progress_bar_class

        for int_exp, exp in enumerate(self.parent().export_queue):

            id = "{0}_{1}_{2}_{3}".format(exp["sequence"], exp["shot"], exp["task"], exp["asset"])
            if id in self.ids:
                continue

            self.ids.append(id)

            print exp["asset"]

            item = ExportTaskItem(self.shot_asset_list)
            item.id = id
            # print item
            item.exp_task_widget.sequence.setText(exp["sequence"])
            item.exp_task_widget.shot.setText(exp["shot"])
            item.exp_task_widget.task.setText(exp["task"])
            item.exp_task_widget.asset.setText(exp["asset"])

            if self.progress_bar_class is not None:
                item.exp_task_widget.progress_bar_class = self.progress_bar_class

            # print "\t", self.parent().export_func_queue[int_exp].args[0].keys()

            # print exp.keys()

        self.progress_bar_class

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

            start_frame = self.parent().export_func_queue[int_exp].args[0]["start_frame"]
            end_frame = self.parent().export_func_queue[int_exp].args[0]["end_frame"]
            relative_frame_samples = self.parent().export_func_queue[int_exp].args[0]["relative_frame_samples"]
            min_sample = min(*relative_frame_samples)
            max_sample = max(*relative_frame_samples)
            self.progress_bar_class.min_frame = start_frame + min_sample
            self.progress_bar_class.max_frame = end_frame + max_sample

            print int_exp, exp
            print "\t", dir(self.parent().export_func_queue[int_exp])
            print "\t", self.parent().export_func_queue[int_exp].func
            print "\targs; ", self.parent().export_func_queue[int_exp].args
            print "\targ keys; ", self.parent().export_func_queue[int_exp].args[0].keys()
            print "\trelative_frame_samples: ", self.parent().export_func_queue[int_exp].args[0]["relative_frame_samples"]
            # self.parent().export_func_queue[int_exp]()

        # if self.progress_bar_class is not None:
        #     item.exp_task_widget.progress_bar_class = self.progress_bar_class


class ExportTaskWidget(QtWidgets.QWidget):

    def __init__(self, parent):

        """
        A wrapper for the list widget item.

        We need this to insert the shot into the shots list.
        """

        super(ExportTaskWidget, self).__init__(parent)

        self.progress_bar_class = None

        # Labels
        self.column_names = ["Sequence", "Shot", "Task", "Asset", "Progress"]  # To show you the order
        self.sequence = QtWidgets.QLabel("Sequence")
        self.shot = QtWidgets.QLabel("Shot")
        self.task = QtWidgets.QLabel("Task")
        self.asset = QtWidgets.QLabel("Asset")

        # Create the layout
        self.frame = QtWidgets.QFrame()
        self.frame.setLineWidth(0)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.item_layout = QtWidgets.QHBoxLayout(self.frame)

        # Add the widgetes
        self.item_layout.addWidget(self.sequence)
        self.item_layout.addWidget(self.shot)
        self.item_layout.addWidget(self.task)
        self.item_layout.addWidget(self.asset)

        self.progress_bar = QtWidgets.QProgressBar()
        self.item_layout.addWidget(self.progress_bar)

        self.setLayout(self.item_layout)

    def __call__(self, *args, **kwargs):

        """
        Set the progress bar to the Progress classes qt_widget
        :param args:
        :param kwargs:
        :return:
        """

        self.progress_bar_class.qt_widget = self.progress_bar


class ExportTaskItem(QtWidgets.QListWidgetItem):

    def __init__(self, parent):

        """
        A wrapper for the list widget item, we need this to insert the frame and information about the asset
        into the shots list.
        """

        super(ExportTaskItem, self).__init__(parent)

        self.exp_task_widget = ExportTaskWidget(parent)
        parent.parent().shot_asset_list.setItemWidget(self, self.exp_task_widget)

        self.id = ""

        self.setSizeHint(self.exp_task_widget.item_layout.sizeHint())
