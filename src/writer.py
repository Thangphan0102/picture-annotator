import os
import xml.etree.ElementTree as ET
from pathlib import Path


class Writer:
    def __init__(self, image_path: str, width, height, depth=3):
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

    def addObject(self, label, x1, y1, x2, y2):
        # annotation/object
        object = ET.SubElement(self.annotation, 'object')

        # annotation/object/name
        name = ET.SubElement(object, 'name')
        name.text = f'{label}'

        # annotation/object/bndbox
        bndbox = ET.SubElement(object, 'bnbbox')

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

    def save(self, export_path):
        # XML tree
        tree = ET.ElementTree(self.annotation)
        ET.indent(tree)

        if os.path.exists(export_path):
            os.remove(export_path)

        tree.write(export_path, encoding='utf-8')
