from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class FilterWidget(QWidget):
    """ The rightmost widget of the main window containing a list of check boxes to hide or show annotations

    Attributes:
        main_window (QMainWindow): The parent main window of this widget.
        label_item_dict (Dict[str, QListWidgetItem]): The dictionary contains the labels as keys and QListWidgetItem as
            values.
        label_list (QListWidget): The QListWidget.
    """
    def __init__(self, main_window: QMainWindow):
        """ Initialize the instance. Define the class variable, set layout, set fixed width, and add interactions.

        Args:
            main_window (QMainWindow): The parent main window of this widget.
        """
        super(FilterWidget, self).__init__(None)

        # Class variable
        self.main_window = main_window
        self.label_item_dict = {}
        self.label_list = QListWidget(None)

        # Set layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Label list'))
        layout.addWidget(self.label_list)

        # Config
        self.setFixedWidth(200)

        # Interactions
        self.label_list.itemChanged.connect(self.label_item_changed)

    def add_label(self, label: str, color: QColor) -> None:
        """ Add a checkbox corresponds to the annotated label and color in the canvas

        Args:
            label (str): The name of the label
            color (QColor): The selected color for that label

        Returns:
            None
        """

        # Create a new item
        item = QListWidgetItem(label)
        self.label_item_dict[label] = item

        # Add settings to the item
        item.setBackground(QBrush(color))
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)

        # Add the item to the list
        self.label_list.addItem(item)

    def undo(self, label: str) -> None:
        """ Remove the checkbox if all the corresponding labels are removed

        Args:
            label (str): The name of the label

        Returns:
            None
        """
        # Remove the item
        item = self.label_item_dict[label]
        self.label_list.takeItem(self.label_list.row(item))

    def reset(self) -> None:
        """ Remove all the checkboxes.

        Returns:
            None
        """
        self.label_list.clear()

    def label_item_changed(self, item: QListWidgetItem) -> None:
        """ Change the visibility of the bounding box(es) in the canvas area when the check status of a checkbox is
            changed

        Args:
            item (QListWidgetItem): The checkbox selected

        Returns:
            None
        """
        label = item.text()
        self.main_window.canvas.change_visible_boxes(label, item.checkState() == Qt.CheckState.Checked)
