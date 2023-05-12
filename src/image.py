from typing import List, Tuple

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QPoint


class Image(QPixmap):
    """ A class that contains information about the images such as its path, its
     labels, and its bounding_box.

     Attributes:
        image_path (str): A string represents the directory containing the images.
        labels (List[str]): A list of string contains the label names.
        bounding_boxes (List[Tuple[int, int, int, int]]): A list of int contains the bounding boxes.
        label_color_dict (Dict[str, QColor]): A dictionary contains the labels as keys and colors as values
            to store which colors correspond to a given label.
    """

    def __init__(self, image_path: str) -> object:
        """ Initializes the instance based on the image path.

        Args:
            image_path (str): The absolute path to the directory containing the images.
        """
        super(Image, self).__init__(image_path)

        self.image_path = image_path
        self.labels = []
        self.bounding_boxes = []
        self.label_color_dict = {}

    def get_path(self) -> str:
        """ Get the path of the image.

        Returns:
            image_path (str): A string represents the image path.
        """
        return self.image_path

    def get_label(self) -> List[str]:
        """ Get the labels of the image.

        Returns:
            labels (List[str]): A list contains the labels.
        """
        return self.labels

    def get_bounding_box(self) -> List[Tuple[int, int, int, int]]:
        """ Get the bounding boxes of the image.

        Returns:
            bounding_boxes (List[Tuple[int, int, int, int])): A list of a list contains the bounding boxes.
        """
        return self.bounding_boxes

    def add_label(self, label: str) -> None:
        """ Add the given label to the labels list.

        Args:
            label (str): A string represent an object name

        Returns:
            None
        """
        self.labels.append(label)

    def add_bounding_box(self, start_point: QPoint, end_point: QPoint) -> None:
        """ Turn start_point and end_point into a tuple of [xmin, ymin, xmax, ymax] then
        add to the bounding boxes attribute.

        Returns:
            None
        """
        self.bounding_boxes.append((start_point.x(), start_point.y(), end_point.x(), end_point.y()))
