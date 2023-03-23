from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QFileDialog


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.config()
        # Create menubar
        self.main_window = main_window

    def config(self):
        self.open_action = QAction('Open file..', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setStatusTip('Open a new file')
        self.open_action.triggered.connect(self._show_dialog)

        # Define help action
        self.help_action = QAction('Show help text', self)
        self.help_action.setShortcut('Ctrl+H')
        self.help_action.setStatusTip('Show the help guide')
        self.help_action.triggered.connect(self._show_help)

        file_menu = self.addMenu('&File')
        file_menu.addAction(self.open_action)
        file_menu = self.addMenu('&Help')
        file_menu.addAction(self.help_action)

    def _show_dialog(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        self.main_window.file_view.update_sub_view(self.directory_path)

    def _show_help(self):
        pass


