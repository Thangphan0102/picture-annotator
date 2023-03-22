import sys

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget
from src.canvas import Canvas


class UI(QMainWindow):

    def __init__(self):
        super().__init__()
        w = QWidget()
        self.setCentralWidget(w)
        canvas = Canvas('../data/helsinki.jpg')
        grid = QGridLayout(w)
        grid.addWidget(canvas)
        QShortcut(QKeySequence('Ctrl+Z'), self, canvas.undo)
        QShortcut(QKeySequence('Ctrl+R'), self, canvas.reset)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec())
