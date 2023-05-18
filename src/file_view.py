try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow
except ImportError:
    raise ImportError("Requires PyQt6")

from file_list import FileList


class FileView(QWidget):
    """ The leftmost widget of the main window containing the text and the FileList widget.

    Attributes:
        main_window (QMainWindow): The parent main window of this widget.
        label (QLabel): The text label.
        file_list (FileList): The file list widget.
    """
    def __init__(self, main_window):
        """ Initialize the instance given the main_window. Create and add the label and the file list widget
        respectively to the widget.

        Args:
            main_window (QMainWindow):
        """
        super().__init__()

        # Set attributes
        self.main_window = main_window

        # Initialize widgets
        self.label = QLabel('List of images')
        self.file_list = FileList(self.main_window)

        # Define layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)

        # Set configuration
        self.setLayout(layout)
        self.setMaximumWidth(300)
