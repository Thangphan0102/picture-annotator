import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QGraphicsScene, QGraphicsView

from file_list import FileList
from menu_bar import MenuBar
from file_view import FileView
from filter_widget import FilterWidget
from canvas import Canvas


class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        self._config()

        # Set central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set layout
        self.layout = QHBoxLayout(self.central_widget)

        # File view area
        self.file_view = FileView(self)
        self.layout.addWidget(self.file_view)

        # Canvas area
        self.scene = QGraphicsScene()
        self.canvas = Canvas(None, self)
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Filter area
        self.filter_widget = FilterWidget(self)
        self.layout.addWidget(self.filter_widget)

        # Create menubar
        self.setMenuBar(MenuBar(self))

    def _config(self):
        self.setWindowTitle('Picture annotator')
        self.setGeometry(1000, 300, 1400, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
