import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore

from jbeamMayaTools.gui import main_widget

__maintainer__ = 'Bryan Howard'
__email__ = 'bhowiebkr@gmail.com'

WINDOW_TITLE = 'JBeam Maya Tools'
WINDOW_OBJECT = 'jbeam_maya_tools'


def _maya_delete_ui():
    """Delete existing UI in Maya"""
    if cmds.window(WINDOW_OBJECT, q=True, exists=True):
        cmds.deleteUI(WINDOW_OBJECT)  # Delete window
    if cmds.dockControl('MayaWindow|' + WINDOW_TITLE, q=True, ex=True):
        cmds.deleteUI('MayaWindow|' + WINDOW_TITLE)  # Delete docked window


def _maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class JbeamUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(JbeamUI, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Settings
        self.settings = QtCore.QSettings(
            'jbeam_maya_tools', 'jbeam_maya_tools')

        # Flags
        self.setObjectName(WINDOW_OBJECT)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumSize(10, 10)
        self.setProperty("saveWindowPref", True)

        # Main widgets
        self.main_widget = main_widget.MainWidget(self)
        self.setCentralWidget(self.main_widget)

    def closeEvent(self, event):
        """ Save the GUI settings
        """
        geometry = self.saveGeometry()
        try:
            self.settings.setValue('geometry', geometry)
            super(JbeamUI, self).closeEvent(event)
        except Exception:
            pass


def start():
    _maya_delete_ui()  # Delete any existing existing UI
    GUI = JbeamUI(parent=_maya_main_window())
    GUI.show()  # Show the UI
    return GUI
