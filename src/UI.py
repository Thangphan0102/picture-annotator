import os
import sys
import glob
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QMenuBar, QFileDialog, QDockWidget, \
    QTextEdit, QHBoxLayout, QScrollArea, QListWidget, QVBoxLayout
from src.canvas import Canvas
from config import *


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._create_menu_bar()
        self._create_dock()
        self._create_canvas()

        self.setWindowTitle('Picture annotator')
        self.setGeometry(1200, 300, 1400, 1000)

    def _create_canvas(self):
        self.main_widget = QWidget()
        self.canvas = Canvas('../data/helsinki.jpg')
        self.grid = QHBoxLayout()
        self.grid.addWidget(self.canvas)

        self.main_widget.setLayout(self.grid)
        self.setCentralWidget(self.main_widget)

        # Add shortcut
        QShortcut(QKeySequence('Ctrl+Z'), self, self.canvas.undo)
        QShortcut(QKeySequence('Ctrl+R'), self, self.canvas.reset)
        QShortcut(QKeySequence('Ctrl+D'), self, self.canvas.print_labels)

    def _create_menu_bar(self):
        # Define open action
        open_action = QAction(QIcon(None), 'Open file..', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open a new file')
        open_action.triggered.connect(self._show_dialog)

        # Define help action
        help_action = QAction(QIcon(None), 'Show help text', self)
        help_action.setShortcut('Ctrl + H')
        help_action.setStatusTip('Show the help guide')
        help_action.triggered.connect(self._show_help)

        # Create menubar
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu = menu_bar.addMenu('&Help')
        file_menu.addAction(help_action)
        self.setMenuBar(menu_bar)

    def _create_dock(self):
        # Create dock
        dock_widget = QDockWidget('Dock', self)
        dock_widget.setWidget(QTextEdit())

        # Disable dock widget's movable features
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

    def _show_dialog(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Select a directory')

    def _show_help(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
