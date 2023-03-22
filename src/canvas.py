import sys

from PyQt6.QtCore import Qt, QKeyCombination
from PyQt6.QtGui import QImage, QPainter, QPen, QKeyEvent
from PyQt6.QtWidgets import QWidget, QInputDialog


class Canvas(QWidget):
    def __init__(self, photo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = QImage(photo)
        self.setFixedSize(self.image.width(), self.image.height())
        self.pressed = self.moving = False
        self.revisions = []
        self.labels = []

        self.start_point = None
        self.end_point = None
        self.rectangle_width = None
        self.rectangle_height = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
            self.start_point = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.moving = True
            self.end_point = event.pos()
            self.rectangle_width = self.end_point.x() - self.start_point.x()
            self.rectangle_height = self.end_point.y() - self.start_point.y()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.revisions.append(self.image.copy())
            qp = QPainter(self.image)
            self.draw_rectangle(qp) if self.moving else self.draw_point(qp)
            self.pressed = self.moving = False
            self.update()

            self.add_label()

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = event.rect()
        qp.drawImage(rect, self.image, rect)
        if self.moving:
            self.draw_rectangle(qp)
        elif self.pressed:
            self.draw_point(qp)

    def draw_point(self, qp):
        qp.setPen(QPen())
        qp.drawPoint(self.start_point)

    def draw_rectangle(self, qp):
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setPen(QPen())
        qp.drawRect(self.start_point.x(), self.start_point.y(), self.rectangle_width, self.rectangle_height)

    def undo(self):
        if self.revisions:
            self.image = self.revisions.pop()
            self.update()

    def reset(self):
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()

    def add_label(self):
        label, ok = QInputDialog.getText(self, 'Class label', 'Enter class label')
        if ok:
            print(f'Bounding box [{self.start_point, self.end_point}]', label)
