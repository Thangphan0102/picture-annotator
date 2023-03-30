from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QAction
from PyQt6.QtWidgets import QWidget, QInputDialog


class Canvas(QWidget):
    def __init__(self, photo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = QImage(photo)
        self.setFixedSize(self.image.width(), self.image.height())
        self.pressed = self.moving = False
        self.revisions = []
        self.labels = []

        self.set_pen()
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

    def draw_rectangle(self, qp):
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setPen(self.pen)
        qp.drawRect(self.start_point.x(), self.start_point.y(), self.rectangle_width, self.rectangle_height)

    def undo(self):
        if self.revisions and self.labels:
            self.image = self.revisions.pop()
            self.labels.pop()
            self.update()

    def reset(self):
        if self.revisions and self.labels:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.labels.clear()
            self.update()

    def save(self):
        pass

    def print_labels(self):
        print(self.labels)

    def add_label(self):
        qp = QPainter(self.image)
        label, ok = QInputDialog.getText(self, 'Class label', 'Enter class label')
        if ok:
            self.revisions.append(self.image.copy())
            self.draw_rectangle(qp)
            self.labels.append(
                [[self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y()], label]
            )

    def set_pen(self):
        self.pen = QPen()
        self.pen.setBrush(QColor(255, 0, 0))
        self.pen.setWidth(3)

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
