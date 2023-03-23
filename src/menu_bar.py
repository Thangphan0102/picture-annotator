from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QFileDialog


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.config()

    def config(self):
        # Define open action
        open_action = QAction('Open file..', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self._show_dialog)

        # Define help action
        help_action = QAction('Show help text', self)
        help_action.setShortcut('Ctrl+H')
        help_action.triggered.connect(self._show_help)

        file_menu = self.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu = self.addMenu('&Help')
        file_menu.addAction(help_action)

    def _show_dialog(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        self.main_window.file_view.file_list.update_sub_view(self.directory_path)

    def _show_help(self):
        pass


