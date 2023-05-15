from typing import List, Tuple, Dict
import xml.etree.ElementTree as ET

try:
    from PyQt6.QtGui import QPixmap, QColor
    from PyQt6.QtCore import QPoint
except ImportError:
    raise ImportError("Requires PyQt6")

from config import *
from utils import parse_xml, parse_annotation_dict


class Image(QPixmap):
    """ A class that contains information about the images such as its path, its
     labels, and its bounding_box.

     Attributes:
        image_path (str): A string represents the directory containing the images.
        labels (List[str]): A list of string contains the label names.
        bounding_boxes (List[Tuple[int, int, int, int]]): A list of int contains the bounding boxes.
        label_color_dict (Dict[str, str]): A dictionary contains the labels as keys and colors as hex strings
            to store which colors correspond to a given label.
    """

    def __init__(self, image_path: str) -> object:
        """ Initializes the instance based on the image path.

        Args:
            image_path (str): The absolute path to the directory containing the images.
        """
        super(Image, self).__init__(image_path)

        self.image_path = image_path
        self.annotation_path = None
        self.labels = []
        self.bounding_boxes = []
        self.label_color_dict = {}
        self.visible = {}

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

    def get_color_dict(self) -> Dict[str, str]:
        return self.label_color_dict

    def get_visible(self) -> Dict[str, bool]:
        return self.visible

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

    def is_existed_annotation(self) -> bool:
        """ Return a boolean indicating if the image has the corresponding annotation file.

        Returns:
            bool: True if existed else False
        """
        annotation_path = Path(ANNOTATION_DIR, Path(self.image_path).with_suffix('.xml').name)

        if annotation_path.is_file():
            self.annotation_path = annotation_path
            return True
        return False

    def load_annotation(self):
        if self.is_existed_annotation():
            result_dict = parse_xml(ET.parse(self.annotation_path).getroot())
            self.labels, self.bounding_boxes, self.label_color_dict = parse_annotation_dict(result_dict)
            self.visible = {label: True for label in self.label_color_dict.keys()}
            return True
        return False
