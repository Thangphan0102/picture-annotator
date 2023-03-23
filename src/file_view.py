import glob
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QListWidget, QVBoxLayout

from src.canvas import Canvas
from src.config import IMAGE_EXTENSIONS


class FileView(QScrollArea):
    def __init__(self, main_window):
        super().__init__()

        self.config()
        self.main_window = main_window
        self.directory_path = None

    def config(self):
        self.setFixedWidth(200)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def update_sub_view(self, directory_path=None):
        self.list_widget = QListWidget()
        self.directory_path = directory_path
        vbox = QVBoxLayout()

        image_file_paths = []
        for extension in IMAGE_EXTENSIONS:
            image_file_paths.extend(glob.glob(os.path.join(directory_path, extension)))

        for index, image_file_path in enumerate(image_file_paths):
            self.list_widget.insertItem(index, image_file_path.split('/')[-1])

        self.list_widget.itemSelectionChanged.connect(self._select_item)
        vbox.addWidget(self.list_widget)
        self.main_window.file_view.setLayout(vbox)

    def _select_item(self):
        item = self.list_widget.currentItem()
        # self.main_window.create_canvas(os.path.join(self.directory_path, item.text()))
        self.main_window.scene.clear()
        canvas = Canvas(os.path.join(self.directory_path, item.text()))
        self.main_window.scene.addWidget(canvas)
