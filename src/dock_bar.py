from PyQt6.QtWidgets import QDockWidget, QListWidget


class DockBar(QDockWidget):
    def __init__(self, title='Dock', main_window=None):
        super(DockBar, self).__init__()
        self.title = title
        self.main_window = main_window
        self.config()

    def config(self):
        self.setWindowTitle(self.title)
        self.setMinimumWidth(300)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
