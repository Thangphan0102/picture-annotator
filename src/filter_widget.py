from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class FilterWidget(QWidget):
    def __init__(self, main_window):
        super(FilterWidget, self).__init__(None)

        # Class variable
        self.main_window = main_window
        self.label_item_dict = {}
        self.label_list = QListWidget(None)

        # Set layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel('Label list'))
        self.layout.addWidget(self.label_list)

        # Config
        self.setFixedWidth(200)

        # Interactions
        self.label_list.itemChanged.connect(self.label_item_changed)

    def add_label(self, label, color):
        item = QListWidgetItem(label)
        self.label_item_dict[label] = item
        item.setBackground(QBrush(color))
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)
        self.label_list.addItem(item)

    def undo(self, label):
        item = self.label_item_dict[label]
        self.label_list.takeItem(self.label_list.row(item))

    def reset(self):
        self.label_list.clear()

    def label_item_changed(self, item):
        label = item.text()
        self.main_window.canvas.change_visible_boxes(label, item.checkState() == Qt.CheckState.Checked)