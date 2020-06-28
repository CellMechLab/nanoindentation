from PyQt5 import QtWidgets, QtGui
from scipy.signal import savgol_filter
import numpy as np
import pyqtgraph as pg

ALL = []

class CPParameter(object):
    def __init__(self,label=None):
        self._label=label
        self._defaultValue = None
        self._validTypes = ['int','float','combo']
        self._type = 'int'
        self._values = []
        self._valueLabels = []
        self._widget = None
        self.triggered = None

    def getLabel(self):
        return self._label

    def getWidget(self):
        return self._widget

    def setType(self,t):
        if t in self._validTypes:
            self._type = t
            
    def setOptions(self,labels,values):
        self.setValues(values)
        self.setValueLabels(labels)

    def setValues(self,v):
        self._values = v

    def setValueLabels(self,v):
        self._valueLabels = v

    def getValue(self):
        pass


class CPPInt(CPParameter):
    def __init__(self,label=None):
        super().__init__(label)
        self._defaultValue = 0
        self.setType( 'int' )
        widget = QtWidgets.QLineEdit()
        valid = QtGui.QIntValidator()
        widget.setValidator(valid)
        self._widget = widget
        self.setValue(self._defaultValue)
        self.triggered = self._widget.editingFinished

    def setValue(self,num):
        self._widget.setText(str(int(num)))

    def getValue(self):
        return int(self._widget.text())

class CPPFloat(CPParameter):
    def __init__(self, label=None):
        super().__init__(label)
        self._defaultValue = 0
        self.setType('int')
        widget = QtWidgets.QLineEdit()
        valid = QtGui.QDoubleValidator()
        widget.setValidator(valid)
        self._widget = widget
        self.setValue(self._defaultValue)
        self.triggered = self._widget.editingFinished

    def setValue(self,num):
        self._widget.setText(str((num)))

    def getValue(self):
        return float(self._widget.text())

class CPPCombo(CPParameter):
    def __init__(self, label,labels,values):
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

    def setValue(self,num):
        self._widget.setCurrentIndex(num)


class ContactPoint(object):
    def __init__(self):
        self._parameters = []
        self.create()

    def create(self):
        pass

    def quickTest(self,c):
        all = self.getWeight(c)
        if all is None or all[0] is None:
            return
        pg.plot(all[0],all[1])

    def getWeight(self, c):
        return [1,2,3],[2,6,4]

    def calculate(self,c):
        pass

    def disconnect(self):
        for p in self._parameters:
            p.triggered.disconnect()

    def connect(self,callback):
        for p in self._parameters:
            p.triggered.connect(callback)

    def addParameter(self,P):
        self._parameters.append(P)

    def createUI(self,layout):
        for i in range(layout.rowCount()):
            layout.removeRow(0)
        for widget in self._parameters:
            layout.addRow(widget.getLabel(), widget.getWidget())


class PrimeContactPoint(ContactPoint):
    def create(self):
        self.window = CPPInt('Window')
        self.window.setValue(200)
        self.threshold = CPPFloat('Threshold')
        self.threshold.setValue(0.0)
        self.addParameter( self.window )
        self.addParameter( self.threshold )

    def getWeight(self,c):
        win = self.window.getValue()
        xprime = None
        if win % 2 == 0:
            win += 1
        try:
            xprime = savgol_filter(c._f, polyorder=1, deriv=1, window_length=win)
        except:
            return None

        return c._z,xprime / (1 - xprime)

    def calculate(self,c):
        x,quot = self.getWeight(c)
        threshold = self.threshold.getValue()
        jk = np.argmin(np.abs(quot-threshold))
        for jj in range(jk,1,-1):
            if quot[jk]>threshold and quot[jk-1]<threshold:
                break
        return [c._z[jj], c._f[jj]]


class ThRov(ContactPoint):
    def create(self):
        self.Fthreshold = CPPFloat('Safe Threshold')
        self.Fthreshold.setValue(10.0)
        self.Xrange = CPPFloat('X Range')
        self.Xrange.setValue(2000.0)
        self.windowr = CPPInt('Window R')
        self.windowr.setValue(200)
        self.addParameter( self.Fthreshold )
        self.addParameter( self.Xrange )
        self.addParameter(self.windowr)

    def getWeight(self, c):
        jmin, jmax = self.getRange(c)
        winr = self.windowr.getValue()
        x = c._z
        y = c._f
        if (len(y) - jmax) < winr + 1:
            return None
        if (jmin) < winr + 1:
            return None
        rov = []
        for j in range(jmin, jmax + 1):
            rov.append(np.var(y[j + 1:j + winr + 1] / np.var(y[j - winr:j])))
        return x[jmin:jmax+1],rov

    def getRange(self,c):
        x = c._z
        y = c._f
        jmax = np.argmin((y - self.Fthreshold.getValue()) ** 2)
        jmin = np.argmin((x - (x[jmax] - self.Xrange.getValue())) ** 2)
        return jmin,jmax

    def calculate(self,c):
        jmin,jmax = self.getRange(c)
        winr = self.windowr.getValue()
        x = c._z
        y = c._f
        if (len(y) - jmax) < winr + 1:
            return None
        if (jmin) < winr + 1:
            return None
        rov = []
        for j in range(jmin,jmax+1):
            rov.append(np.var(y[j+1:j+winr+1]/np.var(y[j-winr:j])))
        jrov = np.argmax(rov) + jmin

        return [x[jrov],y[jrov]]


class DDer(ContactPoint):
    def create(self):
        self.window = CPPInt('Window P')
        self.window.setValue(20)
        self.Xrange = CPPFloat('X Range')
        self.Xrange.setValue(200.0)
        self.Fthreshold = CPPFloat('Safe Threshold')
        self.Fthreshold.setValue(10.0)
        self.addParameter(self.window)
        self.addParameter(self.Xrange)
        self.addParameter(self.Fthreshold)

    def getRange(self, c):
        x = c._z
        y = c._f
        jmax = np.argmin((y - self.Fthreshold.getValue()) ** 2)
        jmin = np.argmin((x - (x[jmax] - self.Xrange.getValue())) ** 2)
        return jmin, jmax

    def getWeight(self, c):
        jmin, jmax = self.getRange(c)
        if jmin is None:
            return None

        win = self.window.getValue()
        if win % 2 == 0:
            win += 1
        xsecond = savgol_filter(c._f / c.k, polyorder=4, deriv=2, window_length=win)
        return(c._z[jmin:jmax],xsecond[jmin:jmax])

    def calculate(self, c):
        jmin, jmax = self.getRange(c)
        if jmin is None:
            return None

        win = self.window.getValue()
        if win % 2 == 0:
            win += 1
        xsecond = savgol_filter(c._f / c.k, polyorder=4, deriv=2, window_length=win)
        jrov = np.argmax(np.abs(xsecond[jmin:jmax])) + jmin
        return [c._z[jrov], c._f[jrov]]

class Threshold(ContactPoint):
    def create(self):
        self.Fthreshold = CPPFloat('Threshold')
        self.Fthreshold.setValue(1.0)
        self.addParameter( self.Fthreshold )

    def calculate(self,c):
        yth = self.Fthreshold.getValue()
        x = c._z
        y = c._f
        jrov = np.argmin( (y-yth)**2 )

        return [x[jrov],y[jrov]]

ALL.append( { 'label':'Prime function', 'method':PrimeContactPoint} )
ALL.append( { 'label':'Threshold', 'method':Threshold} )
ALL.append( { 'label':'Ratio of Variances', 'method':ThRov} )
ALL.append( { 'label':'Second derivative', 'method':DDer} )