from PyQt5 import QtWidgets
import pyqtgraph as pg
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

class FilterSavData(contactPoint):
    def setUi(self):
        self.setWindowTitle("Filter FFT-Savitzky")

        self.sumup = QtWidgets.QCheckBox()
        self.sumup.setChecked(False)

        self.win = QtWidgets.QSpinBox()
        self.win.setMinimum(5)
        self.win.setMaximum(99)
        self.win.setValue(25)
        self.win.setSingleStep(2)

        self.methodSG = QtWidgets.QRadioButton()
        self.methodSG.setText('Savitzky')
        self.methodSG.setChecked(True)

        self.methodMM = QtWidgets.QRadioButton()
        self.methodMM.setText('Median')

        return [ ['Cumulative', self.sumup],['Window', self.win],[self.methodSG,self.methodMM]]
    
    def getParams(self):
        win = int(self.win.value() )
        if win%2 == 0:
            win+=1
        if self.methodSG.isChecked() == True:
            method = 'SG'
        else:
            method = 'MM'
        return [ self.sumup.isChecked(),win ,method]

    def getCall(self):
        return engine.filterSav

class FilterData(contactPoint):
    def setUi(self):
        self.setWindowTitle("Filter parameters")

        self.sumup = QtWidgets.QCheckBox()
        self.sumup.setChecked(False)

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

        return [ ['Cumulative', self.sumup],['Prominency', self.prominency],['MIN cut', self.minfreq],['Model', self.band]]
    
    def getParams(self):
        pro = float(self.prominency.value() )
        winperc = float(self.band.value())/10.0
        thresh = int(self.minfreq.value())

        return [ self.sumup.isChecked(),pro,winperc,thresh ]

    def getCall(self):
        return engine.filterOsc

class eeffPoint(contactPoint):
    def setSegment(self,s):
        self.s = s
        self.curve = pg.PlotCurveItem( s.z,s.ffil,pen=pg.mkPen(pg.QtGui.QColor(0, 0, 255, 255), width=2))
        self.plot.addItem( self.curve )
        self.updatePlot()

    def updatePlot(self):
        #self.curve.setData(self.s.z,1000.0*engine.getEEE(self.s,int(self.minY.value()),float(self.offset.value())/1000.0))
        p = self.getParams()
        oX,oY,q = engine.eeffOffset(self.s,p[0],p[1])
        self.curve.setData(self.s.z-oX,self.s.ffil-oY)

    def setUi(self):
        self.setWindowTitle("Eeff contact point")

        self.minY = QtWidgets.QSpinBox()
        self.minY.setMinimum(0)
        self.minY.setMaximum(9999)
        self.minY.setValue(500)
        self.minY.setSingleStep(100)

        self.offset = QtWidgets.QDoubleSpinBox()
        self.offset.setMinimum(-1000)
        self.offset.setMaximum(1000)
        self.offset.setDecimals(2)
        self.offset.setValue(1.50)
        self.offset.setSingleStep(0.1)

        self.threshold_invalid = QtWidgets.QDoubleSpinBox()
        self.threshold_invalid.setMinimum(0)
        self.threshold_invalid.setMaximum(999)
        self.threshold_invalid.setDecimals(2)
        self.threshold_invalid.setValue(10.00)
        self.threshold_invalid.setSingleStep(0.5)

        self.plot = pg.PlotWidget()

        self.minY.valueChanged.connect(self.updatePlot)
        self.offset.valueChanged.connect(self.updatePlot)

        return[ ['Window length',self.minY],['Threshold CP',self.offset],['Preview',self.plot],['Threshold Invalid', self.threshold_invalid]]

    def getParams(self):
        return[ int(self.minY.value()),float(self.offset.value())/1000.0, float(self.threshold_invalid.value())]

    def getCall(self):
        return engine.eeffOffset

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


class NanosurfPoint(contactPoint):
    def setUi(self):
        self.setWindowTitle("Nanosurf contact point")

        self.step = QtWidgets.QSpinBox()
        self.step.setMinimum(0)
        self.step.setMaximum(1000)
        self.step.setValue(50)

        self.length = QtWidgets.QSpinBox()
        self.length.setMinimum(0)
        self.length.setMaximum(10000)
        self.length.setValue(500)

        self.threshold_exp = QtWidgets.QDoubleSpinBox()
        self.threshold_exp.setMinimum(-99.0)
        self.threshold_exp.setMaximum(99.0)
        self.threshold_exp.setDecimals(3)
        self.threshold_exp.setValue(0.100)

        self.threshold_len_straight = QtWidgets.QSpinBox()
        self.threshold_len_straight.setMinimum(0)
        self.threshold_len_straight.setMaximum(10000)
        self.threshold_len_straight.setValue(1000)

        self.thresholdfactor_mean_exp_before_CP = QtWidgets.QDoubleSpinBox()
        self.thresholdfactor_mean_exp_before_CP.setMinimum(0)
        self.thresholdfactor_mean_exp_before_CP.setMaximum(1)
        self.thresholdfactor_mean_exp_before_CP.setDecimals(3)
        self.thresholdfactor_mean_exp_before_CP.setValue(0.500)

        self.threshold_invalid = QtWidgets.QDoubleSpinBox()
        self.threshold_invalid.setMinimum(0)
        self.threshold_invalid.setMaximum(10000)
        self.threshold_invalid.setDecimals(2)
        self.threshold_invalid.setValue(5.00)

        return[ ['Step Size',self.step],['Section Length',self.length],['CP Threshold of Derivative',self.threshold_exp],['Min Straight before CP',self.threshold_len_straight],['Threshold Factor for Mean Exp before CP', self.thresholdfactor_mean_exp_before_CP], ['Threshold for invalidity in linear region [nN]', self.threshold_invalid]]

    def getParams(self):
        return[ int(self.step.value()),int(self.length.value()),float(self.threshold_exp.value()),int(self.threshold_len_straight.value()), float(self.thresholdfactor_mean_exp_before_CP.value()), float(self.threshold_invalid.value())]

    def getCall(self):
        return engine.NanosurfOffset


class NanosurfPointDeriv(contactPoint):
    def setUi(self):
        self.setWindowTitle("Nanosurf contact point")

        self.win = QtWidgets.QSpinBox()
        self.win.setMinimum(0)
        self.win.setMaximum(99999)
        self.win.setValue(100)

        self.step_z = QtWidgets.QSpinBox()
        self.step_z.setMinimum(0)
        self.step_z.setMaximum(99999)
        self.step_z.setValue(50)

        self.factor = QtWidgets.QSpinBox()
        self.factor.setMinimum(0)
        self.factor.setMaximum(999)
        self.factor.setValue(2)

        self.threshold_slopes = QtWidgets.QDoubleSpinBox()
        self.threshold_slopes.setMinimum(0)
        self.threshold_slopes.setMaximum(1)
        self.threshold_slopes.setDecimals(3)
        self.threshold_slopes.setValue(0.200)

        self.threshold_len_straight = QtWidgets.QSpinBox()
        self.threshold_len_straight.setMinimum(0)
        self.threshold_len_straight.setMaximum(10000)
        self.threshold_len_straight.setValue(1000)

        self.threshold_invalid = QtWidgets.QDoubleSpinBox()
        self.threshold_invalid.setMinimum(0)
        self.threshold_invalid.setMaximum(10000)
        self.threshold_invalid.setDecimals(2)
        self.threshold_invalid.setValue(5.00)

        return[ ['Derivative Window',self.win],['Step Size',self.step_z],['Multiply step for slope',self.factor],['CP Threshold of Slope',self.threshold_slopes],['Min Straight before CP',self.threshold_len_straight], ['Threshold for invalidity in linear region [nN]', self.threshold_invalid]]

    def getParams(self):
        return[ int(self.win.value()),int(self.step_z.value()),int(self.factor.value()),float(self.threshold_slopes.value()), float(self.threshold_len_straight.value()), float(self.threshold_invalid.value())]

    def getCall(self):
        return engine.NanosurfOffsetDeriv

class b2_Elasto(uiPanel):
    def setUi(self):
        self.setWindowTitle("Elastography parameters")

        self.grainstep = QtWidgets.QSpinBox()
        self.grainstep.setMinimum(0)
        self.grainstep.setMaximum(999)
        self.grainstep.setValue(30)

        self.scaledistance = QtWidgets.QSpinBox()
        self.scaledistance.setMinimum(1)
        self.scaledistance.setMaximum(99999)
        self.scaledistance.setValue(500)

        self.maxind = QtWidgets.QSpinBox()
        self.maxind.setMinimum(1)
        self.maxind.setMaximum(99999)
        self.maxind.setValue(2000)

        self.filwin = QtWidgets.QSpinBox()
        self.filwin.setMinimum(1)
        self.filwin.setMaximum(99999)
        self.filwin.setValue(301)

        self.threshold_oscillation = QtWidgets.QSpinBox()
        self.threshold_oscillation.setMinimum(0)
        self.threshold_oscillation.setMaximum(9999999)
        self.threshold_oscillation.setValue(15000)

        return [ ['Increment', self.grainstep],['Dash Depth', self.scaledistance],['Max Indent', self.maxind], ['Filter Window', self.filwin], ['Threshold Oscillation', self.threshold_oscillation]]

    def getParams(self):
        return[ int(self.grainstep.value()),float(self.scaledistance.value()),float(self.maxind.value()), int(self.filwin.value()), float(self.threshold_oscillation.value())]




class CropCurves(uiPanel):
    def setUi(self):
        self.setWindowTitle("Crop start & end of all curves (nm)")

        self.CropStart = QtWidgets.QSpinBox()
        self.CropStart.setMinimum(0)
        self.CropStart.setMaximum(99999)
        self.CropStart.setValue(200)

        self.CropEnd = QtWidgets.QSpinBox()
        self.CropEnd.setMinimum(0)
        self.CropEnd.setMaximum(99999)
        self.CropEnd.setValue(100)

        return [ ['Crop Length Front', self.CropStart],['Crop Length End', self.CropEnd]]

# class ShiftArray(uiPanel):
#     def setUi(self):
#         self.setWindowTitle("Create elastography array for shifted CPs")
#
#         self.MinShift = QtWidgets.QSpinBox()
#         self.MinShift.setMinimum(-99999)
#         self.MinShiftt.setMaximum(99999)
#         self.MinShift.setValue(-500)
#
#         self.MaxShift = QtWidgets.QSpinBox()
#         self.MaxShift.setMinimum(-99999)
#         self.MaxShift.setMaximum(99999)
#         self.MaxShift.setValue(1500)
#
#         self.StepSize = QtWidgets.QSpinBox()
#         self.StepSize.setMinimum(-99999)
#         self.StepSize.setMaximum(99999)
#         self.StepSize.setValue(50)



        return [ ['Crop Length Front', self.CropStart],['Crop Length End', self.CropEnd]]

class Fakedata(uiPanel):
    def setUi(self):
        self.setWindowTitle("Fake data generator")

        self.noiselevel = QtWidgets.QSpinBox()
        self.noiselevel.setMinimum(0)
        self.noiselevel.setMaximum(9999)
        self.noiselevel.setSingleStep(10)
        self.noiselevel.setProperty("value", 10)

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