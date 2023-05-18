import sys
from typing import Union

try:
    from PyQt6.QtGui import QPaintEvent, QPainter, QPen, QColorConstants, QEnterEvent, QMouseEvent, QColor, QAction
    from PyQt6.QtCore import QRect, QEvent, Qt, QPoint
    from PyQt6.QtWidgets import QWidget, QInputDialog, QColorDialog, QMainWindow
except ImportError:
    raise ImportError("Requires PyQt6")

from image import Image
from writer import Writer
from config import *


class Canvas(QWidget):
    """ The canvas to draw annotations on.

    Attributes:
        VIEW_MODE (bool): The indicator of whether the canvas is in view mode (True) or drawing mode (False). True by
            default
        image (Image): The custom pixmap displayed on the canvas.
        drawing (bool): The indicator of whether the user is started drawing a bounding box or not. False by default
        idle (bool): The indicator of whether the canvas is free for adding a new bounding box. True by default
        guile_line_on (bool): The indicator of whether to display the guidelines or not. True by default
        mouse_pos (QPoint): The position of the mouse on the canvas for displaying the guidelines.
        visible (Dict[str, bool]): The mapping of which annotations to display.

    """

    VIEW_MODE = True

    def __init__(self, image_path: str, main_window: QMainWindow, *args: object, **kwargs: object) -> None:
        """ Initialize the instance given the arguments

        The canvas add the image to the scene and create a "drawable canvas" on top of it.

        Args:
            image_path (str): The string represents the path to the image.
            main_window (QMainWindow): The parent main window of the widget.
            *args (object):
            **kwargs (object):
        """
        super(Canvas, self).__init__(*args, **kwargs)

        # Class variable
        self.main_window = main_window
        self.image = Image(image_path)
        self.drawing = False
        self.idle = True
        self.guide_line_on = True
        self.mouse_pos = None

        # Display the image
        self.main_window.scene.setSceneRect(self.image.rect().toRectF())
        self.main_window.scene.addPixmap(self.image)

        # Add the loaded annotations to the filter widget
        if self.image.load_annotation():
            self.main_window.filter_widget.add_labels_from_dict(self.image.get_color_dict())

        # Set configurations
        self.setFixedSize(self.image.width(), self.image.height())
        self.setStyleSheet("background-color: transparent;")

        # Create shortcuts
        self.create_shortcuts()

    def paintEvent(self, event: QPaintEvent) -> None:
        """ Handle the drawing event.

        This method handle:
            Displaying the image and their annotations.
            Displaying guidelines.
            Displaying temporary drawing rectangle.

        Args:
            event (QPaintEvent): The paint event when called self.update()

        Returns:
            None
        """

        # Painter instance
        p = QPainter(self)

        # Display annotations including bounding boxes and label texts (if visible)
        for label, bounding_box in zip(self.image.get_label(), self.image.get_bounding_box()):
            if self.image.get_visible()[label]:
                x1, y1, x2, y2 = bounding_box
                bounding = QRect(x1, y1, x2 - x1, y2 - y1)
                color = self.image.label_color_dict[label]
                self.draw_rectangle(p, bounding, color, fill=False)
                self.draw_text(p, label, x1, y1, x2, y2)

        # Display drawing
        if not self.VIEW_MODE:

            # Display guidelines
            if self.guide_line_on and self.mouse_pos is not None:
                # Initialize pen instance
                p.setPen(QPen(QColorConstants.White, 1))

                # Draw horizontal guide line
                p.drawLine(0, self.mouse_pos.y(), self.image.width(), self.mouse_pos.y())

                # Draw vertical guide line
                p.drawLine(self.mouse_pos.x(), 0, self.mouse_pos.x(), self.image.height())

            # Display a temporary bounding box
            if self.drawing:
                self.draw_rectangle(p)

    def enterEvent(self, event: QEnterEvent) -> None:
        """ Handle the event when the user move the mouse into the image.

        Get the mouse position if it is on the image and the canvas is in draw mode.

        Args:
            event (QEnterEvent): The event when moved the mouse into the widget.

        Returns:
            None
        """
        if self.idle and not self.VIEW_MODE:
            self.mouse_pos = event.position().toPoint()

    def leaveEvent(self, event: QEvent) -> None:
        """ Handle the event when the user move the mouse out of the image.

        Remove the mouse position if it moves out of the image and repaint the canvas.

        Args:
            event (QEvent): The event when moved the mouse of the widget.

        Returns:
            None
        """
        self.mouse_pos = None
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """ Handle the event when the user pressed mouse buttons.

        Record the start position when the user left-clicked the mouse to draw a temporary bounding box.

        Args:
            event (QMouseEvent): The event created by mouse device.

        Returns:
            None
        """
        if self.idle and not self.VIEW_MODE:
            if event.button() == Qt.MouseButton.LeftButton:
                self.start_point = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """ Handle the event when the user move the mouse.

        Record the mouse position used draw the guidelines and the current position used to draw the temporary bounding
        box.

        Args:
            event (QMouseEvent): The event created by mouse device.

        Returns:
            None
        """
        if self.idle and not self.VIEW_MODE:
            self.mouse_pos = event.pos()
            self.update()

            if event.buttons() & Qt.MouseButton.LeftButton:
                self.drawing = True
                self.end_point = event.pos()
                self.check_mouse(event)
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """ Handle the event when the user release clicked buttons.

        Stop drawing a temporary bounding box and call the `insert_label` method.

        Args:
            event (QMouseEvent): The event created by mouse device

        Returns:
            None
        """
        if self.idle and self.drawing and not self.VIEW_MODE:
            if event.button() == Qt.MouseButton.LeftButton:
                self.insert_label()
                self.drawing = False
                self.update()

    def draw_rectangle(
            self,
            p: QPainter,
            rect: QRect = None,
            color: Union[QColor, QColorConstants] = QColorConstants.Red,
            fill: bool = True
    ) -> None:
        """ Draw a temporary bounding box on the canvas.

        Args:
            p (QPainter): The QPainter instance.
            rect (QRect(int, int, int, int)): The bounding box.
            color (str): The string represents the hex color of the line and filled rectangle.
            fill (bool): Indicator of whether to fill the rectangle.
        """
        # Painter setting
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(color), 3))

        # Draw a bounding box
        if rect is None:
            rect = QRect(
                self.start_point.x(), self.start_point.y(),
                self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y()
            )
        p.drawRect(rect)
        if fill:
            p.fillRect(rect, QColor(255, 0, 0, 30))

    def insert_label(self) -> None:
        """ Handle actions when adding annotations. This method opens an input dialog asking the user for the label of
        the annotations. If canceled, do nothing. If the user types in a label and presses ok, it opens a color dialog
        (if the label first introduced) asking for a color related to that label. If the user presses ok, it will add
        the annotation to the image.

        Returns:
            None
        """
        self.idle = False
        label, ok = QInputDialog.getText(None, 'Class label', 'Enter class label')
        if ok:
            if label not in self.image.label_color_dict.keys():
                color = QColorDialog.getColor(
                    initial=QColorConstants.Red,
                    options=QColorDialog.ColorDialogOption.DontUseNativeDialog
                )
                self.image.label_color_dict[label] = color.name()
            if label not in set(self.image.get_label()):
                self.main_window.filter_widget.add_label(label, QColor(color))
                self.image.visible[label] = True
            self.image.add_label(label)
            self.image.add_bounding_box(self.start_point, self.end_point)
        self.idle = True

    def draw_text(self, p, text, x1, y1, x2, y2):
        """ Display the label in the bottom-left corner of the bounding box.

        Args:
            p (QPainter): The QPainter instance
            text (str): The label
            x1 (int): The x-coordinate of the first point of the bounding box
            y1 (int): The y-coordinate of the first point of the bounding box
            x2 (int): The x-coordinate of the second point of the bounding box
            y2 (int): The y-coordinate of the second point of the bounding box

        Returns:
            None
        """
        # Set the font
        font = p.font()
        font.setPixelSize(14)
        p.setFont(font)

        # Define position to draw on
        x_position = min(x1, x2) + 3
        y_position = max(y1, y2) - 3

        # Drawing action
        p.drawText(QPoint(x_position, y_position), text)

    def check_mouse(self, event: QMouseEvent) -> None:
        """ Check if the mouse moved outside the image.

        Args:
            event (QMouseEvent): The event created by mouse device.

        Returns:
            None
        """

        # 1 |   2   | 3
        # ==|=======|==
        # 4 | Image | 5
        # ==|=======|==
        # 6 |   7   | 8
        image_x1, image_y1, image_x2, image_y2 = self.image.rect().getCoords()
        if event.pos().x() < image_x1:                                          # 4
            self.end_point = QPoint(image_x1 + 1, event.pos().y())
        if event.pos().y() < image_y1:                                          # 2
            self.end_point = QPoint(event.pos().x(), image_y1 + 1)
        if (event.pos().x() < image_x1) and (event.pos().y() < image_y1):       # 1
            self.end_point = QPoint(image_x1 + 1, image_y1 + 1)
        if event.pos().x() > image_x2:                                          # 5
            self.end_point = QPoint(image_x2, event.pos().y())
        if event.pos().y() > image_y2:                                          # 7
            self.end_point = QPoint(event.pos().x(), image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() > image_y2):       # 8
            self.end_point = QPoint(image_x2, image_y2)
        if (event.pos().x() < image_x1) and (event.pos().y() > image_y2):       # 6
            self.end_point = QPoint(image_x1 + 1, image_y2)
        if (event.pos().x() > image_x2) and (event.pos().y() < image_y1):       # 3
            self.end_point = QPoint(image_x2, image_y1 + 1)

    def change_visible_boxes(self, label: str, value: bool) -> None:
        """ Change the visibility of the bounding boxes corresponding to the given label.

        Args:
            label (str): The label name
            value (bool): The indicator of visibility

        Returns:
            None
        """
        self.image.visible[label] = value
        self.repaint()

    """
    ============================================================================
    Actions and shortcuts
    ============================================================================
    """

    def undo(self) -> None:
        """ Undo action.

        Remove the last drawn bounding box.

        Returns:
            None
        """
        if self.image.get_label():
            label = self.image.get_label().pop()
            self.image.bounding_boxes.pop()
            if label not in self.image.get_label():
                self.image.label_color_dict.pop(label)
                self.main_window.filter_widget.undo(label)
                self.image.visible.pop(label)
            self.update()

    def reset(self):
        """ Reset action.

        Remove all the bounding boxes.

        Returns:
            None
        """
        if self.image.get_label():
            self.image.get_label().clear()
            self.image.bounding_boxes.clear()
            self.image.label_color_dict.clear()
            self.image.visible.clear()
            self.main_window.filter_widget.reset()
            self.update()

    def save(self) -> None:
        """ Save action.

        Save the drawn bounding boxes as annotations into a .xml file.

        Returns:
            None
        """
        writer = Writer(self.image.get_path(), self.image.width(), self.image.height())

        for label, bounding_box in zip(self.image.get_label(), self.image.get_bounding_box()):
            x1, y1, x2, y2 = bounding_box
            writer.add_object(label, x1, y1, x2, y2)

        for label, color in self.image.get_color_dict().items():
            writer.add_label_color_dict(label, color)

        writer.save()

    def print_labels(self) -> None:
        """ Display annotations action.

        Print the labels, bounding boxes, and their visibility into the console.

        Returns:
            None
        """
        print(self.image.get_label())
        print(self.image.get_bounding_box())
        print(self.image.get_color_dict())
        print(self.image.get_visible())

    def change_to_draw(self) -> None:
        """ Change to draw mode action.

        Returns:
            None
        """
        if self.VIEW_MODE:
            self.VIEW_MODE = False
            self.setMouseTracking(True)

    def change_to_view(self) -> None:
        """ Change to view mode action.

        Returns:
            None
        """
        if not self.VIEW_MODE:
            self.VIEW_MODE = True
            self.setMouseTracking(False)
            self.repaint()

    def create_shortcuts(self) -> None:
        """ Assign the shortcuts for actions.

        Returns:
            None
        """
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
        print_labels_action.setShortcut('Ctrl+G')
        print_labels_action.triggered.connect(self.print_labels)

        change_to_draw_action = QAction('Change to draw', self)
        change_to_draw_action.setShortcut('Ctrl+D')
        change_to_draw_action.triggered.connect(self.change_to_draw)

        change_to_view_action = QAction('Change to view', self)
        change_to_view_action.setShortcut('Ctrl+V')
        change_to_view_action.triggered.connect(self.change_to_view)

        self.addAction(undo_action)
        self.addAction(reset_action)
        self.addAction(save_action)
        self.addAction(print_labels_action)
        self.addAction(change_to_draw_action)
        self.addAction(change_to_view_action)
