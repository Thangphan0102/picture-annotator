import os
from config import IMAGE_EXTENSIONS
import glob
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, \
    QGraphicsView, QWidget, QApplication, QDockWidget, QFileDialog, \
    QTextEdit, QMenuBar, QLabel, QHBoxLayout, QScrollArea, QVBoxLayout, QListWidget, QListView, QGraphicsPixmapItem, \
    QGraphicsItem
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import Qt
import sys


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._create_menu_bar()
        self._create_dock()
        self._create_main_view()

        self.setWindowTitle('Picture annotator')
        self.setGeometry(300, 300, 1400, 800)

    def _list_images(self, directory_path=None):
        self.list_widget = QListWidget()
        self.vbox = QVBoxLayout()

        image_filenames = []
        for extension in IMAGE_EXTENSIONS:
            image_filenames.extend(glob.glob(os.path.join(directory_path, extension)))

        for index, image_filename in enumerate(image_filenames):
            self.list_widget.insertItem(index, image_filename.split('/')[-1])

        self.list_widget.itemSelectionChanged.connect(self._select_item)
        self.vbox.addWidget(self.list_widget)
        self.scroll.setLayout(self.vbox)

    def _create_main_view(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Main area
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Scroll area
        self.scroll = QScrollArea()

        # Scroll setting
        self.scroll.setFixedWidth(300)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.view)
        self.main_widget.setLayout(self.layout)

    def _create_menu_bar(self):
        # Open action
        open_file = QAction(QIcon(None), 'Open file..', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Open a new file')
        open_file.triggered.connect(self._show_dialog)

        # Help action
        help_act = QAction(QIcon(None), '&Show help text', self)
        help_act.setShortcut('Ctrl+H')
        help_act.setStatusTip('Show the help guide')
        help_act.triggered.connect(self._show_help)

        # Create menubar
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_file)
        file_menu = menu_bar.addMenu("&Help")
        file_menu.addAction(help_act)
        self.setMenuBar(menu_bar)

    def _create_dock(self):
        # Create dock
        dock_widget = QDockWidget('Dock', self)
        dock_widget.setWidget(QTextEdit())

        # Disable dock widget's movable feature
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

    def _show_dialog(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Select a directory')
        self._list_images(self.directory_path)

    def _show_help(self):
        pass

    def _select_item(self):
        item = self.list_widget.currentItem()
        self.scene.clear()
        pixmap = QPixmap(self.directory_path + '/' + item.text()).scaledToWidth(800)
        self.scene.addPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
