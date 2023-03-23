from PyQt6.QtWidgets import QDockWidget


class DockBar(QDockWidget):
    def __init__(self, title='Dock', main_window=None):
        super().__init__()
        self.title = title
        self.main_window = main_window
        self.config()

    def config(self):
        self.setFixedWidth(200)
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
