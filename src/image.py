from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Image(QPixmap):
    def __init__(self, image_path):
        super(Image, self).__init__(image_path)

        self.image_path = image_path
        self.labels = []
        self.bounding_boxes = []
        self.label_color_dict = {}

    def add_label(self, label):
        self.labels.append(label)

    def add_bounding_box(self, start_point, end_point):
        self.bounding_boxes.append([start_point.x(), start_point.y(), end_point.x(), end_point.y()])
