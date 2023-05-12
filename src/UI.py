import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QGraphicsScene, QGraphicsView
from PyQt6.QtGui import QWheelEvent

from file_list import FileList
from menu_bar import MenuBar
from file_view import FileView
from filter_widget import FilterWidget
from canvas import Canvas
from graphics_view import CustomGraphicsView
import config


class UI(QMainWindow):
    """ The UI of the program.

    Attributes:
        central_widget (QWidget): The central widget of the UI.
        layout (QLayout): The layout of the widgets inside UI.
        file_view (FileView): The file view instance.
        canvas (Canvas): The canvas instance.
        scene (QGraphicsScene): The graphics scene of the UI.
        view (CustomGraphicsView): The custom graphics view instance.
        filter_widget (FilterWidget): The filter widget instace.
    """

    def __init__(self) -> None:
        """ Initialize all the elements and add them into the UI.

        """
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

        # View area
        self.canvas = None
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self.scene, self)
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
