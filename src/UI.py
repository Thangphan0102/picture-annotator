import sys

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from src.canvas import Canvas


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        canvas = Canvas('../data/helsinki.jpg')
        self.setCentralWidget(canvas)
        self.setGeometry(1200, 300, 300, 300)
        QShortcut(QKeySequence('Ctrl+Z'), self, canvas.undo)
        QShortcut(QKeySequence('Ctrl+R'), self, canvas.reset)
        QShortcut(QKeySequence('Ctrl+D'), self, canvas.print_labels)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
