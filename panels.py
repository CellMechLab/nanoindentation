from PyQt5 import QtWidgets, QtGui
from scipy.signal import savgol_filter
import numpy as np
import pyqtgraph as pg
import popup
from scipy.optimize import curve_fit
ALL = []   

# Return False if CP is not evaluated / found correctly 
#Use Threhsold as first guess: 
    #-use threhsold method in Contact Point Class as function 

class CPParameter: #CP parameters class
    def __init__(self, label=None): 
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

    def setType(self, t ):
        if t in self._validTypes:
            self._type = t
            
    def setOptions(self,labels,values):
        self.setValueLabels(labels)
        self.setValues(values)

    def setValues(self,v):
        self._values = v

    def setValueLabels(self,v):
        self._valueLabels = v

    def getValue(self):
        pass

class CPPInt(CPParameter): #CPPInt inherits CPParameter class
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
        self.setType('float') 
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


class ContactPoint: #Contact point class 
    def __init__(self):
        self._parameters = [] 
        self.create() 

    def create(self):
        pass

    def quickTest(self,c):
        return self.getWeight(c)

    def getWeight(self, c):
        return [1,2,3],[2,6,4] 

    def calculate(self,c):
        pass

    def invalidate(self, c, invalid_thresh, j_cp):
        y = c._f  
        for i in y[:j_cp]:
            if i-y[j_cp] <= invalid_thresh:
                return True

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

                     ##Contact Point Finding Algorithms##
#----------------------------------------------------------------------------#

class PrimeContactPoint(ContactPoint): #First Derivative threshold (to change)
    def create(self):
        self.window = CPPInt('Window [nm]')
        self.window.setValue(200) 
        self.threshold = CPPFloat('Threshold [pN]') 
        self.threshold.setValue(0.0005) 
        self.Invalid_thresh = CPPFloat('Invalid Threshold [pN]')
        self.addParameter(self.window)
        self.addParameter(self.threshold)

    def getWeight(self, c): 
        win = self.window.getValue()
        fprime = False 
        if win % 2 == 0:
            win += 1 
        try:
            fprime = savgol_filter(c._f, polyorder=1, deriv=1, window_length=win) 
        except:
            return False
        return c._z , fprime / (1 - fprime)  

    def calculate(self,c):
        win = self.window.getValue()
        z, df = self.getWeight(c)
        threshold = self.threshold.getValue()
        jk = np.argmin( ( df - threshold )**2) 
        if jk < win:
            return False
        for jj in range(jk+5,1,-1):
            if df[jj]>threshold/2 and df[jj-1]<threshold/2:
                break
        if jj < win:
            return False
        return [c._z[jj], c._f[jj]]

class ThRov(ContactPoint): #Ratio of Variances 
    def create(self):
        self.Fthreshold = CPPFloat('Safe Threshold [pN]') #Force threshold
        self.Fthreshold.setValue(10.0) 
        self.Xrange = CPPFloat('X Range [nm]') 
        self.Xrange.setValue(1000.0)
        self.windowr = CPPInt('Window RoV [nm]') #Window used for RoV calculation
        self.windowr.setValue(200)
        self.addParameter( self.Fthreshold )
        self.addParameter( self.Xrange )
        self.addParameter(self.windowr)
        
    def getRange(self,c): 
        x = c._z
        y = c._f
        try:
            jmax = np.argmin((y - self.Fthreshold.getValue()) ** 2)
            jmin = np.argmin((x - (x[jmax] - self.Xrange.getValue())) ** 2)
        except ValueError:
            return False
        return jmin , jmax

    def getWeight(self, c):
        jmin, jmax = self.getRange(c) 
        winr = self.windowr.getValue()
        x = c._z
        y = c._f
        if (winr + jmax) > len(y): #check1
            return False
        if jmin < winr:  #check2
            return False 
        rov = [] 
        for j in range(jmin, jmax): 
            rov.append( (np.var( y[j+1 : j+winr]) )  / (np.var(y[j-winr : j-1] ))) 
        return x[jmin:jmax] , rov  

    def calculate(self,c):
        z = c._z
        f = c._f
        zz_x, rov = self.getWeight(c)
        rov_best_ind = np.argmax(rov)
        j_rov = np.argmin( (z-zz_x[rov_best_ind])**2 )
        return [z[j_rov],f[j_rov]] 


class ThRovFirst(ContactPoint): #Ratio of variances First peak 
    def create(self):
        self.Fthreshold = CPPFloat('Safe Threshold [pN]') #Force threshold
        self.Fthreshold.setValue(10.0) 
        self.Xrange = CPPFloat('X Range [nm]') 
        self.Xrange.setValue(1000.0)
        self.windowr = CPPInt('Window RoV [nm]') #Window used for RoV calculation
        self.windowr.setValue(200)
        self.addParameter( self.Fthreshold )
        self.addParameter( self.Xrange )
        self.addParameter(self.windowr)
        
    def getRange(self,c): 
        x = c._z
        y = c._f
        try:
            jmax = np.argmin((y - self.Fthreshold.getValue()) ** 2)
            jmin = np.argmin((x - (x[jmax] - self.Xrange.getValue())) ** 2)
        except ValueError:
            return False
        return jmin , jmax

    def getWeight(self, c):
        jmin, jmax = self.getRange(c)
        winr = self.windowr.getValue()
        x = c._z
        y = c._f
        if (len(y) - jmax) < int(winr/2): 
            return False
        if (jmin) < int(winr/2): 
            return False
        rov = []
        for j in range(jmin, jmax):
            rov.append( (np.var( y[j+1 : j+winr]))  / (np.var(y[j-winr : j-1])) ) 
        return x[jmin:jmax], rov

    def calculate(self,c):
        z = c._z
        f = c._f
        zz_x, rov = self.getWeight(c)
        rov_best_ind = np.argmax(rov)
        j_rov = np.argmin( (z-zz_x[rov_best_ind])**2 )
        return [z[j_rov], f[j_rov]] 
        
class GoodnessOfFit(ContactPoint): #Goodness of Fit (GoF)
     def create(self): 
        self.windowr = CPPFloat('Window Fit [nm]') 
        self.windowr.setValue(200.0)
        self.Xrange = CPPFloat('X Range [nm]')
        self.Xrange.setValue(1000.0)
        self.Fthreshold = CPPFloat('Safe Threshold [pN]')
        self.Fthreshold.setValue(10.0) 
        self.addParameter(self.windowr)
        self.addParameter(self.Xrange)
        self.addParameter(self.Fthreshold)
        
     #Returns min and max indices of f-z data considered
     def getRange(self,c): 
        x = c._z
        y = c._f
        try:
            jmax = np.argmin((y - self.Fthreshold.getValue()) ** 2)  
            jmin = np.argmin((x - (x[jmax] - self.Xrange.getValue())) ** 2) 
        except ValueError: 
            return False 
        return jmin, jmax 
        
     #Retunrs weight array (R**2) and corresponding index array. Uses get_indentation and fit methods defined below
     def getWeight(self, c):
         jmin, jmax = self.getRange(c) 
         if jmin is False or jmax is False:
              return False 
          
         zwin = self.windowr.getValue()
         zstep = (max(c._z) - min(c._z)) / (len(c._z) - 1)
         win = int(zwin / zstep) 
    
         R_squared = []
         j_x = np.arange(jmin, jmax) 
         for j in j_x: 
             ind, Yf = self.get_indentation(c, j, win) 
             E_std = self.fit(c, ind, Yf)
             R_squared.append(E_std) 
         return c._z[jmin:jmax], R_squared
     
     #Retunrs indentation (ind) and f from z vs f data
     def get_indentation(self, c, iContact, win):
         z = c._z 
         f = c._z
         R = c.R
         if (iContact + win) > len(z):  
             return False 
         Zf = z[iContact : iContact + win] - z[iContact]
         Yf = f[iContact: iContact + win] - f[iContact]
         ind = Zf - Yf / c.k 
         ind = ind[ind<=0.1*R] #fit only for small indentations
         return ind, Yf                
        
     def fit(self, c, ind, f):
        seeds = [1000.0 / 1e9]
        try:
            R = c.R
            def Hertz(x, E):
                x = np.abs(x)
                poisson = 0.5
                return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)
            popt, pcov = curve_fit(Hertz, ind, f, p0=seeds, maxfev=100000)
            #E_std = np.sqrt(pcov[0][0]) #R**2
            residuals = f - Hertz(ind, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((f-np.mean(f))**2)
            R_squared = 1 - (ss_res / ss_tot)
            return R_squared
        except (RuntimeError, ValueError):
            return False 
        
     #Retunrs contact point (z0, f0) based on max R**2
     def calculate(self,c):
         z = c._z 
         f = c._f 
         zz_x, R_squared = self.getWeight(c)
         R_best_ind = np.argmax(R_squared)
         j_GoF = np.argmin( (z-zz_x[R_best_ind])**2 )
         return [z[j_GoF],f[j_GoF]] 

class DDer(ContactPoint): #Second Derivative 
    def create(self):
        self.window = CPPInt('Window P')
        self.window.setValue(20)
        self.Xrange = CPPFloat('X Range')
        self.Xrange.setValue(1000.0)
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
        if jmin is False:
            return False
        win = self.window.getValue()
        if win % 2 == 0:
            win += 1
        fsecond = savgol_filter(c._f, polyorder=4, deriv=2, window_length=win)
        return c._z[jmin:jmax], fsecond[jmin:jmax]

    def calculate(self, c):
        z = c._z 
        f = c._f 
        zz_x, ddf = self.getWeight(c)
        ddf_best_ind = np.argmin(ddf)
        jdd = np.argmin(( z - zz_x[ddf_best_ind] )**2 )
        return [c._z[jdd], c._f[jdd]] 
    
class Threshold(ContactPoint): #Threshold 
    def create(self):
        self.Athreshold = CPPFloat('Align Threshold [pN]')
        self.Athreshold.setValue(10.0)
        self.deltaX = CPPFloat('Align left step [nm]')
        self.deltaX.setValue(2000.0)
        self.Fthreshold = CPPFloat('AVG area [nm]')
        self.Fthreshold.setValue(100.0)
        self.addParameter(self.Athreshold )
        self.addParameter(self.deltaX)
        self.addParameter(self.Fthreshold)
    
    def calculate(self,c):
        yth = self.Athreshold.getValue()
        x = c._z
        y = c._f
        if yth > np.max(y) or yth < np.min(y): 
            return None 
        jrov = 0
        for j in range(len(y)-1,1,-1): 
            if y[j]>yth and y[j-1]<yth: 
                jrov = j 
                break
        x0 = x[jrov]
        dx = self.deltaX.getValue()
        ddx = self.Fthreshold.getValue() 
        if ddx <= 0:
            jxalign = np.argmin((x - (x0 - dx)) ** 2)
            f0 = y[jxalign] 
        else:
            jxalignLeft = np.argmin( (x-(x0-dx-ddx))**2 )
            jxalignRight = np.argmin( (x-(x0-dx+ddx))**2 )
            f0 = np.average(y[jxalignLeft:jxalignRight])
        jcp = jrov
        for j in range(jrov,1,-1):
            if y[j]>f0 and y[j-1]<f0:
                jcp = j
                break
        return [x[jcp], y[jcp]] 

ALL.append( { 'label':'Threshold', 'method':Threshold} )
ALL.append( { 'label':'Gooodness of Fit', 'method':GoodnessOfFit} ) 
ALL.append( { 'label':'Prime function', 'method':PrimeContactPoint} ) 
ALL.append( { 'label':'Ratio of Variances', 'method':ThRov} )
ALL.append( { 'label':'Ratio of Variances - First Peak', 'method':ThRovFirst} )
ALL.append( { 'label':'Second derivative', 'method':DDer} )