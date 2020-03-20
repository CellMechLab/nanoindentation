from PyQt5 import QtWidgets
import engine

class uiPanel(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        #Add form elements here 
        widgets = self.setUi()
        for l,w in widgets:
            layout.addRow(l,w)    

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        
    def setUi(self):
        self.setWindowTitle("TITLE")
        return []

class contactPoint(uiPanel):
    def getParams(self):
        return []
    def getCall(self):
        return max

class chiaroPoint(contactPoint):
    def setUi(self):
        self.setWindowTitle("Chiaro contact point")

        self.minY = QtWidgets.QSpinBox()
        self.minY.setMinimum(0)
        self.minY.setMaximum(99999)
        self.minY.setValue(500)

        self.maxY = QtWidgets.QSpinBox()
        self.maxY.setMinimum(0)
        self.maxY.setMaximum(99999)
        self.maxY.setValue(2500)

        self.offset = QtWidgets.QDoubleSpinBox()
        self.offset.setMinimum(-99.0)
        self.offset.setMaximum(99.0)
        self.offset.setDecimals(2)
        self.offset.setValue(0.40)

        self.winLeft = QtWidgets.QSpinBox()
        self.winLeft.setMinimum(1)
        self.winLeft.setMaximum(999)
        self.winLeft.setValue(19)

        self.winRight = QtWidgets.QSpinBox()
        self.winRight.setMinimum(1)
        self.winRight.setMaximum(999)
        self.winRight.setValue(99)

        return[ ['Min Yflat',self.minY],['Max Yflat',self.maxY],['Offset',self.offset],['Left',self.winLeft],['Right',self.winRight]]

    def getParams(self):
        return[ float(self.minY.value()),float(self.maxY.value()),float(self.offset.value()),int(self.winLeft.value()),int(self.winRight.value())]

    def getCall(self):
        return engine.chiaroOffset

class FilterData(uiPanel):
    def setUi(self):
        self.setWindowTitle("Filter parameters")

        self.prominency = QtWidgets.QDoubleSpinBox()
        self.prominency.setMinimum(0.0)
        self.prominency.setMaximum(9.0)
        self.prominency.setValue(0.40)
        self.prominency.setDecimals(2)

        self.minfreq = QtWidgets.QSpinBox()
        self.minfreq.setMinimum(1)
        self.minfreq.setMaximum(999)
        self.minfreq.setValue(25)

        self.band = QtWidgets.QSpinBox()
        self.band.setMinimum(1)
        self.band.setMaximum(999)
        self.band.setValue(30)

        return [ ['Prominency', self.prominency],['MIN cut', self.minfreq],['Model', self.band]]

class Fakedata(uiPanel):
    def setUi(self):
        self.setWindowTitle("Fake data generator")

        self.noiselevel = QtWidgets.QSpinBox()
        self.noiselevel.setMinimum(1)
        self.noiselevel.setMaximum(9999)
        self.noiselevel.setSingleStep(10)
        self.noiselevel.setProperty("value", 100)

        layers = QtWidgets.QGroupBox()
        horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.el_one = QtWidgets.QRadioButton()
        self.el_one.setText('One')
        self.el_one.setChecked(True)
        horizontalLayout_1.addWidget(self.el_one)
        self.el_two = QtWidgets.QRadioButton()
        self.el_two.setText('Two')
        horizontalLayout_1.addWidget(self.el_two)
        layers.setLayout(horizontalLayout_1)

        layers2 = QtWidgets.QGroupBox()
        layers2.setEnabled(False)
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.modAli = QtWidgets.QRadioButton()
        self.modAli.setText('Std')
        self.modAli.setChecked(True)
        horizontalLayout_2.addWidget(self.modAli)
        self.modRos = QtWidgets.QRadioButton()
        self.modRos.setText('Ros')
        horizontalLayout_2.addWidget(self.modRos)
        layers2.setLayout(horizontalLayout_2)

        self.E1 = QtWidgets.QSpinBox()
        self.E1.setMinimum(1)
        self.E1.setMaximum(99999)
        self.E1.setSingleStep(100)
        self.E1.setProperty("value", 18725)

        self.E2 = QtWidgets.QSpinBox()
        self.E2.setEnabled(False)
        self.E2.setMinimum(1)
        self.E2.setMaximum(99999)
        self.E2.setSingleStep(100)
        self.E2.setProperty("value", 6725)

        self.d0 = QtWidgets.QSpinBox()
        self.d0.setEnabled(False)
        self.d0.setMinimum(10)
        self.d0.setMaximum(9999)
        self.d0.setSingleStep(10)
        self.d0.setProperty("value", 298)

        self.length = QtWidgets.QSpinBox()
        self.length.setMinimum(100)
        self.length.setMaximum(99999)
        self.length.setSingleStep(100)
        self.length.setProperty("value", 4000)

        self.el_two.toggled.connect(layers2.setEnabled)
        self.el_two.toggled.connect(self.E2.setEnabled)
        self.el_two.toggled.connect(self.d0.setEnabled)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        return [ ['Noise level [pN]', self.noiselevel],['Layers', layers],['Model', layers2],['E1 [Pa]', self.E1],['E2 [Pa]', self.E2],['d0 [nm]', self.d0],['Lebgth [nm]', self.length]]        