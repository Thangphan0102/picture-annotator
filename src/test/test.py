import os
import sys
import unittest
from PIL import Image
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.writer import Writer
from src.utils import *
from src.file_list import *


class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.img = Image.new('RGB', (300, 300))
        cls.img.save('test.jpg')
        cls.writer = Writer('test.jpg', cls.img.width, cls.img.height)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.retain = ['__pycache__', 'test.py']

        for item in os.listdir(Path(__file__).parent):
            if item not in cls.retain:
                os.remove(item)

    def test_export_file_exist(self):
        file_path = self.writer.save('test.xml')
        self.assertTrue(Path(file_path).is_file())
        os.remove(file_path)

    def test_annotations_content(self):
        label, x1, y1, x2, y2 = 'test_object', 100, 50, 200, 250
        label_color_dict = {label: 'ffffff'}

        self.writer.add_object(label, x1, y1, x2, y2)
        self.writer.add_label_color_dict(label, label_color_dict[label])
        file_path = self.writer.save('test.xml')

        result_dict = parse_xml(ET.parse(file_path).getroot())
        result_labels, result_bounding_boxes, result_label_color_dict = parse_annotation_dict(result_dict)

        self.assertEqual(label, result_labels[0])
        self.assertEqual((x1, y1, x2, y2), result_bounding_boxes[0])
        self.assertEqual(label_color_dict, result_label_color_dict)

        os.remove(file_path)


class TestImport(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.img = Image.new('RGB', (300, 300))
        # Valid files
        cls.img.save('test.jpg')
        cls.img.save('test.jpeg')
        cls.img.save('test.png')
        # Non-valid files
        cls.img.save('test.gif')
        os.mkdir('temp_dir')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.retain = ['__pycache__', 'test.py']

        for item in os.listdir(Path(__file__).parent):
            if item not in cls.retain:
                if Path(item).is_file():
                    os.remove(item)
                elif Path(item).is_dir():
                    os.removedirs(item)

    def test_import_file_length(self):
        directory_path = Path(__file__).parent
        _ = QApplication(sys.argv)
        file_list = FileList(None)
        file_list.update_sub_view(directory_path)
        length = file_list.count()

        self.assertEqual(length, 3)


if __name__ == '__main__':
    unittest.main()



