from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os

from canvas import Canvas


class CustomGraphicsView(QGraphicsView):
    """ The graphics view of the program.

    Attributes:
        main_window (QMainWindow): The parent main window of the widget.
        aspect_ratio_mode (Qt.AspectRatioMode): The defined ratio mode when displaying images
        zoom_stack (List[QRectF]): The placeholder of the rectangles when zooming in and out.
        wheel_zoom_factor (int): The ratio handles how much to zoom.

    """

    def __init__(self, scene: QGraphicsScene, main_window: QMainWindow) -> None:
        """ Initialize the instance of the super class.

        Args:
            scene (QGraphicsScene): The graphic scene behind the view.
            main_window (QMainWindow): The parent main window of the widget.
        """
        super(CustomGraphicsView, self).__init__(scene)

        self.main_window = main_window
        self.aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio

        self.zoom_stack = []
        self.wheel_zoom_factor = 1.25

    def update_view(self) -> None:
        """ Update the view when zooming in and out.

        Returns:
            None
        """
        if len(self.zoom_stack):
            self.fitInView(self.zoom_stack[-1], self.aspect_ratio_mode)
        else:
            self.fitInView(self.sceneRect(), self.aspect_ratio_mode)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """ Handle the actions when the user scroll the wheel. If the user scroll forward, zoom in the image. If the
        user scroll back, zoom out.

        Args:
            event (QWheelEvent): The event when the user scroll the wheel.

        Returns:
            None
        """
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

