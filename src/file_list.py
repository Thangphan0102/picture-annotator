import glob
import os
from pathlib import Path

try:
    from PyQt6.QtWidgets import QListWidget, QGridLayout, QMainWindow
except ImportError:
    raise ImportError("Requires PyQt6")

from canvas import Canvas
from config import IMAGE_EXTENSIONS


class FileList(QListWidget):
    """ A custom list widget to select images

    Attributes:
        main_window (QMainWindow): The parent main window of the widget
        directory_path (str): The string represents the opened directory containing the images
    """
    def __init__(self, main_window: QMainWindow):
        """ Initialize the instance given the main_window

        Args:
            main_window (QMainWindow): The parent main window of the widget
        """
        super().__init__()

        self.main_window = main_window
        self.directory_path = None

    def update_sub_view(self, directory_path=None):
        """ List all the images of the formats '.jpg', '.jpeg', '.png' (these can be modified in the src/config.py)
        whenever the user select or change the directory

        Args:
            directory_path (str): A string represents the opened directory containing the images
        """

        # Set attribute
        self.directory_path = directory_path

        # Find all images in the given directory
        image_file_paths = []
        for extension in IMAGE_EXTENSIONS:
            image_file_paths.extend(glob.glob(os.path.join(directory_path, extension)))

        # Add the images to the widget
        for index, image_file_path in enumerate(image_file_paths):
            self.insertItem(index, Path(image_file_path).name)

        # Add action when the selected item changes
        self.itemSelectionChanged.connect(self._select_item)

    def _select_item(self) -> None:
        """ Display the image to the scene in the canvas area whenever the user select or change the image

        Returns:
            None
        """

        # Define the selected item
        item = self.currentItem()

        # Clean the scene and the filter_widget
        self.main_window.scene.clear()
        self.main_window.filter_widget.reset()

        # Update the canvas to display the new selected image
        canvas = Canvas(os.path.join(self.directory_path, item.text()), self.main_window)
        self.main_window.canvas = canvas
        self.main_window.scene.addWidget(canvas)
        self.main_window.view.update_view()
