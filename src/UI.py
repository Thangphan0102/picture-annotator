import sys

try:
    from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QGraphicsScene
except ImportError:
    raise ImportError("Requires PyQt6")

from src.file_list import FileList
from src.menu_bar import MenuBar
from src.file_view import FileView
from src.filter_widget import FilterWidget
from src.canvas import Canvas
from src.graphics_view import CustomGraphicsView
import src.config


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

        # View area
        self.scene = QGraphicsScene()
        self.view = CustomGraphicsView(self.scene, self)

        # File view area
        self.file_view = FileView(self)

        # Filter area
        self.filter_widget = FilterWidget(self)

        # Create menubar
        self.setMenuBar(MenuBar(self))

        # Set layout
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.addWidget(self.file_view)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.filter_widget)

    def _config(self) -> None:
        """ Add configurations to the main window

        Returns:
            None
        """
        self.setWindowTitle('Picture annotator')
        self.setGeometry(1000, 300, 1400, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
