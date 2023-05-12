from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QFileDialog, QMainWindow


class MenuBar(QMenuBar):
    """ The menubar of the program.

    Attributes:
        main_window (QMainWindow): The parent main window of the widget.
    """
    def __init__(self, main_window: QMainWindow):
        """ Initialize the instance given the main window and add configurations.

        Args:
            main_window (QMainWindow): The parent main window of the widget.
        """
        super().__init__()
        self.main_window = main_window
        self.config()

    def config(self) -> None:
        """ Add items and their action when selected to the widget

        Returns:
            None
        """
        # Open action
        open_action = QAction('Open file..', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self._show_dialog)

        # Help action
        help_action = QAction('Show help text', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self._show_help)

        file_menu = self.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu = self.addMenu('&Help')
        file_menu.addAction(help_action)

    def _show_dialog(self) -> None:
        """ Open a dialog asking the user to select a directory. Given the selected directory, it updates the FileList
        widget to show all the images in that directory.

        Returns:
            None
        """
        directory_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        self.main_window.file_view.file_list.update_sub_view(directory_path)

    def _show_help(self):
        pass
