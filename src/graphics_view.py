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

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.zoom_stack = []

        self.wheel_zoom_factor = 1.25
        self.pan_button = Qt.MouseButton.RightButton

        self._is_panning = False
        self._scene_position = QPointF()
        self.start_point = QPoint()
        self.end_point = QPoint()

    def update_view(self):
        if len(self.zoom_stack):
            self.fitInView(self.zoom_stack[-1], self.aspect_ratio_mode)
        else:
            self.fitInView(self.sceneRect(), self.aspect_ratio_mode)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if (self.pan_button is not None) and (event.button() == self.pan_button) and self.VIEW_MODE:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            if self.pan_button == Qt.MouseButton.LeftButton:
                QGraphicsView.mousePressEvent(self, event)
            else:
                self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)
                dummyModifiers = Qt.KeyboardModifier(Qt.KeyboardModifier.ShiftModifier
                                                     | Qt.KeyboardModifier.ControlModifier
                                                     | Qt.KeyboardModifier.AltModifier
                                                     | Qt.KeyboardModifier.MetaModifier)
                dummyEvent = QMouseEvent(QEvent.Type.MouseButtonPress, QPointF(event.pos()), Qt.MouseButton.LeftButton,
                                         event.buttons(), dummyModifiers)
                self.mousePressEvent(dummyEvent)
            scene_view_port = self.mapToScene(self.viewport().rect()).boundingRect().intersected(self.sceneRect())
            self._scene_position = scene_view_port.topLeft()
            self._is_panning = True

        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if (event.button() == Qt.MouseButton.RightButton) and self.VIEW_MODE:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            if len(self.zoom_stack) > 0:
                scene_view_port = self.mapToScene(self.viewport().rect()).boundingRect().intersected(self.sceneRect())
                delta = scene_view_port.topLeft() - self._scene_position
                self.zoom_stack[-1].translate(delta)
                self.zoom_stack[-1] = self.zoom_stack[-1].intersected(self.sceneRect())
            self._is_panning = False

        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_panning:
            QGraphicsView.mouseMoveEvent(self, event)
            if len(self.zoom_stack) > 0:
                scene_view_port = self.mapToScene(self.viewport().rect()).boundingRect().intersected(self.sceneRect())
                delta = scene_view_port.topLeft() - self._scene_position
                self._scene_position = scene_view_port.topLeft()
                self.zoom_stack[-1].translate(delta)
                self.zoom_stack[-1] = self.zoom_stack[-1].intersected(self.sceneRect())
                self.update_view()
        QGraphicsView.mouseMoveEvent(self, event)

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

