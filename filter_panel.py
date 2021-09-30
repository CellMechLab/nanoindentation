"""Algorithms for filtering F-z nanoindentation data."""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtWidgets
from scipy.signal import savgol_filter, medfilt, detrend
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import popup

ALL_FILTERS = []


#########################################################
#####################DO NOT CHANGE#######################
#########################################################


class FilterParameter:  
    def __init__(self, label=None):
        self._label = label
        self._defaultValue = None
        self._validTypes = ['int', 'float', 'combo']
        self._type = 'int'
        self._values = []
        self._valueLabels = []
        self._widget = None
        self.triggered = None

    def getLabel(self):
        return self._label

    def getWidget(self):
        return self._widget

    def setType(self, t):
        if t in self._validTypes:
            self._type = t

    def setOptions(self, labels, values):
        self.setValueLabels(labels)
        self.setValues(values)

    def setValues(self, v):
        self._values = v

    def setValueLabels(self, v):
        self._valueLabels = v

    def getValue(self):
        pass


class FilterInt(FilterParameter):  
    def __init__(self, label=None):
        super().__init__(label)
        self._defaultValue = 0
        self.setType('int')
        widget = QtWidgets.QLineEdit()
        valid = QtGui.QIntValidator()
        widget.setValidator(valid)
        self._widget = widget
        self.setValue(self._defaultValue)
        self.triggered = self._widget.editingFinished

    def setValue(self, num):
        self._widget.setText(str(int(num)))

    def getValue(self):
        return int(self._widget.text())


class FilterFloat(FilterParameter):  
    def __init__(self, label=None):
        super().__init__(label)
        self._defaultValue = 0.0
        self.setType('float')
        widget = QtWidgets.QLineEdit()
        valid = QtGui.QDoubleValidator()
        widget.setValidator(valid)
        self._widget = widget
        self.setValue(self._defaultValue)
        self.triggered = self._widget.editingFinished

    def setValue(self, num):
        self._widget.setText(str((num)))

    def getValue(self):
        return float(self._widget.text())


class FilterCombo(FilterParameter): 
    def __init__(self, label, labels, values):
        super().__init__(label)
        self._defaultValue = 0
        self.setType('combo')

        self._values = values
        self._valueLabels = labels

        widget = QtWidgets.QComboBox()
        for v in labels:
            widget.addItem(v)
        widget.setCurrentIndex(0)
        self._widget = widget
        self.triggered = self._widget.currentIndexChanged

    def getValue(self):
        who = int(self._widget.currentIndex())
        return float(self._values[who])

    def setValue(self, num):
        self._widget.setCurrentIndex(num)


class Filter:  
    def __init__(self):
        self._parameters = []
        self.create()

    def create(self):
        pass

    def quickTest(self, c):
        return self.getWeight(c)

    def getWeight(self, c):
        return [1, 2, 3], [2, 6, 4]

    def calculate(self, c):
        pass

    def disconnect(self):
        for p in self._parameters:
            try:
                p.triggered.disconnect()
            except TypeError:
                pass

    def connect(self, callback):
        for p in self._parameters:
            p.triggered.connect(callback)

    def addParameter(self, P):
        self._parameters.append(P)

    def createUI(self, layout):
        for i in range(layout.rowCount()):
            layout.removeRow(0)
        for widget in self._parameters:
            layout.addRow(widget.getLabel(), widget.getWidget())


#################################################
#####################Filters#####################
#################################################

class SavGolFilter(Filter):
    """
    Filters data with the Savitzky-Golay filter from the Scipy Library.
    doi: https://doi.org/10.1038/s41592-019-0686-2
    """  
    def create(self):
        self.win = FilterInt('Window Length [nm]')
        self.win.setValue(25)
        self.polyorder = FilterInt('Polynomical Order (Int)')
        self.polyorder.setValue(3)
        self.addParameter(self.win)
        self.addParameter(self.polyorder)

    def calculate(self, c):
        y = c._f
        win = self.win.getValue()
        polyorder = self.polyorder.getValue()
        if win % 2 == 0:
            win += 1
        if polyorder > win:
            return False
        y_smooth = savgol_filter(y, win, polyorder)
        return y_smooth


class MedianFilter(Filter):
    """
    Filters data with the median filter from the Scipy Library.
    doi: https://doi.org/10.1038/s41592-019-0686-2
    """  
    def create(self):
        self.win = FilterInt('Window Length [nm]')
        self.win.setValue(25)
        self.addParameter(self.win)

    def calculate(self, c):
        y = c._f
        win = self.win.getValue()
        if win % 2 == 0:
            win += 1
        y_smooth = medfilt(y, win)
        return y_smooth

ALL_FILTERS.append({'label': 'Savitzky Golay', 'method': SavGolFilter})
ALL_FILTERS.append({'label': 'Median Filter', 'method': MedianFilter})
