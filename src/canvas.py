import sys
from pathlib import Path
from pascal_voc_writer import Writer

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from image import *


class Canvas(QWidget):
    def __init__(self, image_path, main_window, *args, **kwargs):
        super(Canvas, self).__init__(*args, **kwargs)

        self.main_window = main_window
        self.image = Image(image_path)
        self.main_window.scene.addPixmap(self.image)

        self.drawing = False
        self.idle = True
        self.guide_line_on = True
        self.mouse_pos = None
        self.visible = {}

        self.create_shortcuts()
        self.setMouseTracking(True)
        self.setFixedSize(self.image.width(), self.image.height())
        self.setStyleSheet("background-color: transparent;")

    def paintEvent(self, event: QPaintEvent):
        p = QPainter(self)

        for label, bounding_box in zip(self.image.labels, self.image.bounding_boxes):
            if self.visible[label]:
                x1, y1, x2, y2 = bounding_box
                bounding = QRect(x1, y1, x2 - x1, y2 - y1)
                color = self.image.label_color_dict[label]
                self.draw_rectangle(p, bounding, color, fill=False)
                self.draw_text(p, label, x1, y1, x2, y2)

        if self.guide_line_on and self.mouse_pos is not None:
            p.setPen(QPen(QColorConstants.White, 1))

            # Draw horizontal guide line
            p.drawLine(0, self.mouse_pos.y(), self.image.width(), self.mouse_pos.y())

            # Draw vertical guide line
            p.drawLine(self.mouse_pos.x(), 0, self.mouse_pos.x(), self.image.height())

        if self.drawing:
            self.draw_rectangle(p)

    def enterEvent(self, event: QEnterEvent) -> None:
        if self.idle:
            self.mouse_pos = event.position().toPoint()

    def leaveEvent(self, event: QEvent) -> None:
        self.mouse_pos = None
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if self.idle:
            if event.button() == Qt.MouseButton.LeftButton:
                self.start_point = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.idle:
            self.mouse_pos = event.pos()
            self.update()

            if event.buttons() & Qt.MouseButton.LeftButton:
                self.drawing = True
                self.end_point = event.pos()
                self.check_mouse(event)
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.idle and self.drawing:
            if event.button() == Qt.MouseButton.LeftButton:
                self.insert_label()
                self.drawing = False
                self.update()

    def draw_rectangle(self, p, rect=None, color=QColorConstants.Red, fill=True):
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(color, 3))
        if rect is None:
            rect = QRect(
                self.start_point.x(), self.start_point.y(),
                self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y()
            )
        p.drawRect(rect)
        if fill:
            p.fillRect(rect, QColor(255, 0, 0, 30))

    def insert_label(self):
        self.idle = False
        label, ok = QInputDialog.getText(None, 'Class label', 'Enter class label')
        if ok:
            if label not in self.image.label_color_dict.keys():
                color = QColorDialog.getColor(
                    initial=QColorConstants.Red,
                    options=QColorDialog.ColorDialogOption.DontUseNativeDialog
                )
                self.image.label_color_dict[label] = color
            if label not in set(self.image.labels):
                self.main_window.filter_widget.add_label(label, color)
                self.visible[label] = True
            self.image.add_label(label)
            self.image.add_bounding_box(self.start_point, self.end_point)
        self.idle = True

    def draw_text(self, p, text, x1, y1, x2, y2):
        font = p.font()
        font.setPixelSize(14)
        p.setFont(font)
        x_position = min(x1, x2) + 3
        y_position = max(y1, y2) - 3
        p.drawText(QPoint(x_position, y_position), text)

    def check_mouse(self, event):
        # Check if mouse move outside of image
        # 1 |   2   | 3
        # ==|=======|==
        # 4 | Image | 5
        # ==|=======|==
        # 6 |   7   | 8
        image_x1, image_y1, image_x2, image_y2 = self.image.rect().getCoords()
        if event.pos().x() < image_x1:  # 4
            self.end_point = QPoint(image_x1 + 1, event.pos().y())
        if event.pos().y() < image_y1:  # 2
            self.end_point = QPoint(event.pos().x(), image_y1 + 1)
        if (event.pos().x() < image_x1) and (event.pos().y() < image_y1):  # 1
            self.end_point = QPoint(image_x1 + 1, image_y1 + 1)
        if event.pos().x() > image_x2:  # 5
            self.end_point = QPoint(image_x2, event.pos().y())
        if event.pos().y() > image_y2:  # 7
            self.end_point = QPoint(event.pos().x(), image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() > image_y2):  # 8
            self.end_point = QPoint(image_x2, image_y2)
        if (event.pos().x() < image_x1) and (event.pos().y() > image_y2):  # 6
            self.end_point = QPoint(image_x1 + 1, image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() < image_y1):  # 3
            self.end_point = QPoint(image_x2, image_y1 + 1)

    ###########
    # Actions and shortcuts
    ###########
    def undo(self):
        if self.image.labels:
            label = self.image.labels.pop()
            self.image.bounding_boxes.pop()
            if label not in self.image.labels:
                self.image.label_color_dict.pop(label)
                self.main_window.filter_widget.undo(label)
                self.visible.pop(label)
            self.update()

    def reset(self):
        if self.image.labels:
            self.image.labels.clear()
            self.image.bounding_boxes.clear()
            self.image.label_color_dict.clear()
            self.visible.clear()
            self.main_window.filter_widget.reset()
            self.update()

    def save(self):
        writer = Writer(self.image.image_path, self.image.width(), self.image.height())

        for label, bounding_box in zip(self.image.labels, self.image.bounding_boxes):
            x1, y1, x2, y2 = bounding_box
            writer.addObject(label, x1, y1, x2, y2)

        data_path = Path(self.image.image_path).parent.parent
        file_name = Path(self.image.image_path).name
        export_file_name = Path(file_name).with_suffix('.xml')
        export_path = Path(data_path).joinpath('annotations').joinpath(export_file_name)
        writer.save(export_path)

    def print_labels(self):
        print(self.image.labels)
        print(self.image.bounding_boxes)
        print(self.image.label_color_dict)
        print(self.visible)

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

    def change_visible_boxes(self, label, value):
        self.visible[label] = value
        self.repaint()
