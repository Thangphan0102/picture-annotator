import glob
import os
from pathlib import Path

from PyQt6.QtWidgets import QListWidget, QGridLayout

from canvas import Canvas
from config import IMAGE_EXTENSIONS


class FileList(QListWidget):
    def __init__(self, main_window):
        super().__init__()

        # self.config()
        self.main_window = main_window
        self.directory_path = None

    def update_sub_view(self, directory_path=None):
        self.directory_path = directory_path

        image_file_paths = []
        for extension in IMAGE_EXTENSIONS:
            image_file_paths.extend(glob.glob(os.path.join(directory_path, extension)))

        for index, image_file_path in enumerate(image_file_paths):
            self.insertItem(index, Path(image_file_path).name)

        self.itemSelectionChanged.connect(self._select_item)

    def _select_item(self):
        item = self.currentItem()
        self.main_window.scene.clear()
        canvas = Canvas(os.path.join(self.directory_path, item.text()))
        self.main_window.scene.addWidget(canvas)
