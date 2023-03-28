from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from file_list import FileList


class FileView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.file_list = FileList(self.main_window)
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('List of images'))
        self.layout.addWidget(self.file_list)

        self.setLayout(self.layout)
        self.setMaximumWidth(300)

