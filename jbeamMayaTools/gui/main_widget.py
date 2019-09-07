from PySide2 import QtWidgets


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # Layouts
        mainLayout = QtWidgets.QVBoxLayout(self)
