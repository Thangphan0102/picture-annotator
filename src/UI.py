import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QGraphicsScene, QGraphicsView

from dock_bar import DockBar
from file_list import FileList
from menu_bar import MenuBar
from file_view import FileView


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._config()
        self._create_menu_bar()
        self._create_dock_bar()
        self._create_file_view()
        self._create_main_view()

    def _create_main_view(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Canvas area
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Set layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.file_view)
        self.layout.addWidget(self.view)
        self.central_widget.setLayout(self.layout)

    def _create_file_view(self):
        self.file_view = FileView(self)

    def _create_menu_bar(self):
        self.setMenuBar(MenuBar(self))

    def _create_dock_bar(self):
        self.dock_bar = DockBar('Dock', self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_bar)

    def _config(self):
        self.setWindowTitle('Picture annotator')
        self.setGeometry(1000, 300, 1400, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
