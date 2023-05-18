import os
import xml.etree.ElementTree as ET
from pathlib import Path

from src.config import *


class Writer:
    """ A class helps to write annotations into a xml file

    """

    def __init__(self, image_path: str, width: int, height: int, depth: int = 3):
        """ Initialize the instance

        Args:
            image_path (str): The absolute path to the image
            width (int): The width of the image
            height (int): The height of the image
            depth (int ): Number of color channel(s), default is 3 for color images
        """
        # root
        self.image_path = Path(image_path)

        # annotation
        self.annotation = ET.Element('annotation')

        # annotation/folder
        self.folder = ET.SubElement(self.annotation, 'folder')
        self.folder.text = f'{Path(image_path).parent.name}'

        # annotation/filename
        self.filename = ET.SubElement(self.annotation, 'filename')
        self.filename.text = f'{Path(image_path).name}'

        # annotation/path
        self.path = ET.SubElement(self.annotation, 'path')
        self.path.text = f'{image_path}'

        # annotation/size
        self.size = ET.SubElement(self.annotation, 'size')
        # annotation/size/width
        self.width = ET.SubElement(self.size, 'width')
        self.width.text = f'{width}'
        # annotation/size/height
        self.height = ET.SubElement(self.size, 'height')
        self.height.text = f'{height}'
        # annotation/size/depth
        self.depth = ET.SubElement(self.size, 'depth')
        self.depth.text = f'{depth}'

    def add_object(self, label: str, x1: int, y1: int, x2: int, y2: int) -> None:
        """ Write the information of a bounding box into the xml file

        Args:
            label (str): The label name
            x1 (int): X-coordinate of the top-left point of the rectangle
            y1 (int): Y-coordinate of the top-left point of the rectangle
            x2 (int): X-coordinate of the bottom-right point of the rectangle
            y2 (int): Y-coordinate of the bottom-right point of the rectangle

        Returns:
            None
        """
        # annotation/object
        object = ET.SubElement(self.annotation, 'object')

        # annotation/object/name
        name = ET.SubElement(object, 'name')
        name.text = f'{label}'

        # annotation/object/bndbox
        bndbox = ET.SubElement(object, 'bndbox')

        # annotation/object/bndbox/xmin
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = f'{x1}'

        # annotation/object/bndbox/ymin
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = f'{y1}'

        # annotation/object/bndbox/xmax
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = f'{x2}'

        # annotation/object/bndbox/ymax
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = f'{y2}'

    def add_label_color_dict(self, label: str, color: str) -> None:
        """ Write the information of the selected color corresponding to the label.

        Args:
            label (str): The label name
            color (str): The hexadecimal color code. For example "ffffff" represents the color white.

        Returns:
            None
        """
        # annotation/color_dict
        color_dict = ET.SubElement(self.annotation, 'color_dict')
        color_dict.set(label, color)

    def save(self, path: str = None) -> str:
        """ Save the annotated xml file

        Args:
            path (str): The specified path to save the annotation file. The default is None and the xml file will be
                saved into y2_2023_08713_picture_annotator/data/annotations.

        Returns:
            saved_path (str): The path to the saved xml file.
        """
        # XML tree
        tree = ET.ElementTree(self.annotation)
        ET.indent(tree, space='    ')

        if path is None:
            save_path = ANNOTATION_DIR.joinpath(self.image_path.with_suffix('.xml').name)
            tree.write(save_path, encoding='utf-8')
        else:
            save_path = path
            tree.write(path, encoding='utf-8')

        return save_path
