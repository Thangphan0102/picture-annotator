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

    def get_path(self):
        return self.image_path

    def get_label(self):
        return self.labels

    def get_bounding_box(self):
        return self.bounding_boxes

    def add_label(self, label):
        self.labels.append(label)

    def add_bounding_box(self, start_point, end_point):
        self.bounding_boxes.append([start_point.x(), start_point.y(), end_point.x(), end_point.y()])
