from PySide2 import QtWidgets
import pymel.all as pm
import os

from jbeamMayaTools.core.Vehicle import Vehicle
from jbeamMayaTools.core.maya_builders import build_truss
from jbeamMayaTools.core import jbeam_import
# from jbeamMayaTools.core import jbeam_import

CAR_NAME = 'howiezoom'
ROOT_PATH = os.path.abspath(__file__ + '/../../../')
MAYA_SRC_PATH = os.path.join(ROOT_PATH, 'maya_src', 'hello_car.mb')
BEAM_VEHICLES_PATH = os.path.join(
    os.path.expanduser('~'), 'BeamNG.drive', 'vehicles')
TEST_VEHICLE_PATH = os.path.join(BEAM_VEHICLES_PATH, CAR_NAME)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout(self)

        import_btn = QtWidgets.QPushButton('Import')
        test_export_btn = QtWidgets.QPushButton('Export')
        open_test_btn = QtWidgets.QPushButton('Open Test')
        build_nodes_btn = QtWidgets.QPushButton('Build Nodes')

        for btn in [test_export_btn, build_nodes_btn, open_test_btn, import_btn]:
            btn.setFixedHeight(40)

        mainLayout.addWidget(import_btn)
        mainLayout.addWidget(open_test_btn)
        mainLayout.addWidget(build_nodes_btn)
        mainLayout.addWidget(test_export_btn)

        mainLayout.addStretch()

        # logic
        test_export_btn.clicked.connect(self.export_cmd)
        open_test_btn.clicked.connect(self.open_test)
        build_nodes_btn.clicked.connect(self.build_btn)
        import_btn.clicked.connect(self.import_cmd)

    def build_btn(self):
        build_truss(car_name=CAR_NAME)

    def open_test(self):
        """ Open the test file
        """
        pm.openFile(MAYA_SRC_PATH, force=True)

    def export_cmd(self):
        """ Export
        """

        if not os.path.exists(TEST_VEHICLE_PATH):
            os.makedirs(TEST_VEHICLE_PATH)

        # Make the vehicle
        group = pm.ls(sl=True)[0]
        v = Vehicle(beam_vehicles_path=BEAM_VEHICLES_PATH,
                    name=CAR_NAME, group=group)

        # Export it
        v.export()

    def import_cmd(self):
        print('import')
        jbeam_import.import_vehicle()
