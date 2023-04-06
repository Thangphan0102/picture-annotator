import os
from pathlib import Path

from pascal_voc_writer import Writer
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QAction, QTextItem, QColorConstants
from PyQt6.QtWidgets import QWidget, QInputDialog, QColorDialog


class Canvas(QWidget):
    def __init__(self, image_path, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)
        self.image_path = image_path
        self.image = QImage(self.image_path)
        self.setFixedSize(self.image.width(), self.image.height())

        self.revisions = []
        self.labels = []
        self.bounding_boxes = []
        self.label_color_dict = {}

        self.pen = QPen()
        self.pen.setColor(QColorConstants.Red)
        self.pen.setWidth(3)

        self.moving = False

        self.start_point = None
        self.end_point = None
        self.rectangle_width = None
        self.rectangle_height = None

        self.create_shortcuts()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.moving = True
            self.end_point = event.pos()
            self.check_mouse(event)
            self.rectangle_width = self.end_point.x() - self.start_point.x()
            self.rectangle_height = self.end_point.y() - self.start_point.y()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.add_label()
            self.moving = False
            self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = event.rect()
        qp.drawImage(rect, self.image, rect)
        if self.moving:
            self.draw_rectangle(qp)

    def draw_rectangle(self, qp, color=QColorConstants.Red):
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.pen.setColor(color)
        qp.setPen(self.pen)
        qp.drawRect(self.start_point.x(), self.start_point.y(), self.rectangle_width, self.rectangle_height)

    def add_text(self, qp, text):
        font = qp.font()
        font.setPixelSize(14)
        qp.setFont(font)
        x_position = min(self.start_point.x(), self.end_point.x()) + 3
        y_position = max(self.start_point.y(), self.end_point.y()) - 3
        qp.drawText(QPoint(x_position, y_position), text)

    def undo(self):
        if self.revisions and self.labels:
            self.image = self.revisions.pop()
            label = self.labels.pop()
            self.bounding_boxes.pop()
            if label not in self.labels:
                self.label_color_dict.pop(label)
            self.update()

    def reset(self):
        if self.revisions and self.labels:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.labels.clear()
            self.bounding_boxes.clear()
            self.label_color_dict.clear()
            self.update()

    def save(self):
        self.writer = Writer(self.image_path, self.image.width(), self.image.height())

        for label, bounding_box in zip(self.labels, self.bounding_boxes):
            xmin, ymin, xmax, ymax = bounding_box
            self.writer.addObject(label, xmin, ymin, xmax, ymax)

        data_path = Path(self.image_path).parent.parent
        file_name = Path(self.image_path).name
        export_file_name = Path(file_name).with_suffix('.xml')
        export_path = Path(data_path).joinpath('annotations').joinpath(export_file_name)
        self.writer.save(export_path)

    def print_labels(self):
        print(self.labels, self.bounding_boxes)
        print(self.label_color_dict)

    def add_label(self):
        qp = QPainter(self.image)
        label, ok = QInputDialog.getText(self, 'Class label', 'Enter class label')
        if ok:
            if label not in self.label_color_dict.keys():
                color = QColorDialog.getColor(options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
                self.label_color_dict[label] = color
            else:
                color = self.label_color_dict[label]
            self.revisions.append(self.image.copy())
            self.draw_rectangle(qp, color)
            self.add_text(qp, label)
            self.labels.append(label)
            self.bounding_boxes.append(
                [self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y()]
            )

    def check_mouse(self, event):
        # Check if mouse move outside of image
        # 1 |   2   | 3
        # ==|=======|==
        # 4 | Image | 5
        # ==|=======|==
        # 6 |   7   | 8
        image_x1, image_y1, image_x2, image_y2 = self.image.rect().getCoords()
        if event.pos().x() < image_x1:                                      # 4
            self.end_point = QPoint(image_x1 + 1, event.pos().y())
        if event.pos().y() < image_y1:                                      # 2
            self.end_point = QPoint(event.pos().x(), image_y1 + 1)
        if (event.pos().x() < image_x1) and (event.pos().y() < image_y1):   # 1
            self.end_point = QPoint(image_x1 + 1, image_y1 + 1)
        if event.pos().x() > image_x2:                                      # 5
            self.end_point = QPoint(image_x2, event.pos().y())
        if event.pos().y() > image_y2:                                      # 7
            self.end_point = QPoint(event.pos().x(), image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() > image_y2):   # 8
            self.end_point = QPoint(image_x2, image_y2)
        if (event.pos().x() < image_x1) and (event.pos().y() > image_y2):   # 6
            self.end_point = QPoint(image_x1 + 1, image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() < image_y1):   # 3
            self.end_point = QPoint(image_x2, image_y1 + 1)

    def create_shortcuts(self):
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.undo)

        reset_action = QAction('Reset', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.triggered.connect(self.reset)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        print_labels_action = QAction('Print labels', self)
        print_labels_action.setShortcut('Ctrl+D')
        print_labels_action.triggered.connect(self.print_labels)

        self.addAction(undo_action)
        self.addAction(reset_action)
        self.addAction(save_action)
        self.addAction(print_labels_action)
