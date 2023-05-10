from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os

from canvas import Canvas


class CustomGraphicsView(QGraphicsView):

    VIEW_MODE = True

    def __init__(self, scene: QGraphicsScene, main_window: QMainWindow):
        super(CustomGraphicsView, self).__init__(scene)

        self.main_window = main_window
        self.aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio

        self.zoom_stack = []
        self.wheel_zoom_factor = 1.25

    def update_view(self):
        if len(self.zoom_stack):
            self.fitInView(self.zoom_stack[-1], self.aspect_ratio_mode)
        else:
            self.fitInView(self.sceneRect(), self.aspect_ratio_mode)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            # Zoom in
            if len(self.zoom_stack) == 0:
                self.zoom_stack.append(self.sceneRect())
            elif len(self.zoom_stack) > 1:
                del self.zoom_stack[:-1]
            zoom_rect = self.zoom_stack[-1]
            center = zoom_rect.center()
            zoom_rect.setWidth(zoom_rect.width() / self.wheel_zoom_factor)
            zoom_rect.setHeight(zoom_rect.height() / self.wheel_zoom_factor)
            zoom_rect.moveCenter(center)
            self.zoom_stack[-1] = zoom_rect.intersected(self.sceneRect())
            self.update_view()
        else:
            # Zoom out
            if len(self.zoom_stack) == 0:
                return
            elif len(self.zoom_stack) > 1:
                del self.zoom_stack[:-1]
            zoom_rect = self.zoom_stack[-1]
            center = zoom_rect.center()
            zoom_rect.setWidth(zoom_rect.width() * self.wheel_zoom_factor)
            zoom_rect.setHeight(zoom_rect.height() * self.wheel_zoom_factor)
            zoom_rect.moveCenter(center)
            self.zoom_stack[-1] = zoom_rect.intersected(self.sceneRect())
            if self.zoom_stack[-1] == self.sceneRect():
                self.zoom_stack = []
            self.update_view()

