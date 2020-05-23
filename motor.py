from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
import pyqtgraph as pg
from scipy.signal import savgol_filter,medfilt,find_peaks
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

PEN_GREEN = pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=2)
ST_RED = 1
ST_BLU = 2
ST_BLK = 3

def sames(ar1,ar2):
    if (ar1 is None) or (ar2 is None):
        return False
    if len(ar1) != len(ar2):
        return False
    ar1 = np.array(ar1)
    ar2 = np.array(ar2)
    if np.sum(ar1-ar2) == 0:
        return True
    return False


def hertz (x, E, R, poisson=0.5):
    return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)


def Gauss(x,x0,w,A):
    return A*np.exp( -((x-x0)/w)**2 )


def calc_hertz(E,R,k,maxvalue):
    x = np.linspace(0,maxvalue,int(maxvalue))
    y = hertz(x,E/1e9,R)
    z = x + y/k
    return x,y,z


def gauss_fit(x,y):
    if len(x)==len(y)+1:
        x = (x[1:]+x[:-1])/2.0
    popt, pcov = curve_fit(Gauss, x,y , p0=[x[np.argmax(y)],(np.max(x)-np.min(x))/10.0,np.max(y)], maxfev=1000)
    nx = np.linspace(np.min(x),np.max(x),100)
    x0,w,A = popt
    return x0,w,A,nx,Gauss(nx,*popt)

class Nanoment(object):
    def __init__(self,curve = None):
        self.basename = None
        self._contactpoint = [0,0]
        self._z = None
        self._f = None
        self._z_raw = None
        self._f_raw = None
        self._ind = None
        self._touch = None
        self.R = None
        self.k = None
        self._E = 5
        self._curve_single = None
        self._curve_raw = None
        self._curve_fit = None
        self._g_fdistance = None
        self._g_indentation = None
        self._g_scatter = None
        self._state = ST_BLK = 3
        self._alpha = 100
        self._selected = False
        self._tree = None
        self._ui = None
        self._Eindex = 0
        if curve is not None:
            self.R = curve.tip_radius
            self.k = curve.cantilever_k
            self.basename = curve.basename

    def connect(self,nanowin,node = False):
        self._ui=nanowin.ui
        #Plot F(z)
        self._g_fdistance = pg.PlotCurveItem(clickable=True)
        nanowin.ui.g_fdistance.plotItem.addItem(self._g_fdistance)
        self._g_fdistance.sigClicked.connect(nanowin.curve_clicked)
        self._g_fdistance.nano = self
        # Plot F(delta)
        self._g_indentation = pg.PlotCurveItem(clickable=True)
        nanowin.ui.g_indentation.plotItem.addItem(self._g_indentation)
        self._g_indentation.sigClicked.connect(nanowin.curve_clicked)
        self._g_indentation.nano = self
        # Plot E
        self._g_scatter = pg.PlotDataItem(clickable=True,pen=None,symbol='o',symbolPen=None,symbolBrush=None)
        self._Eindex = len(nanowin.ui.g_scatter.plotItem.items)
        self._g_scatter.setSymbolPen(None)
        self._g_scatter.setSymbolBrush(None)
        nanowin.ui.g_scatter.plotItem.addItem(self._g_scatter)
        self._g_scatter.sigClicked.connect(nanowin.curve_clicked)
        self._g_scatter.nano = self

        self._curve_single = nanowin.curve_single
        self._curve_raw = nanowin.curve_raw
        self._curve_fit = nanowin.curve_fit

        if node is not False:
            self._tree = node
        else:
            myself = QtWidgets.QTreeWidgetItem(nanowin.ui.mainlist)
            myself.setText(0, self.basename)
            myself.curve = self
            myself.setFlags(myself.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            myself.setCheckState(0, QtCore.Qt.Checked)

    def disconnect(self):
        self._g_fdistance = None
        self._g_indentation = None
        self._g_scatter = None
        self._tree = None
        self._ui = None
        self._curve_single = None
        self._curve_raw = None
        self._curve_fit = None

    def update_view(self):
        if self._g_fdistance is not None:
            if self.z is not None and self.force is not None:
                if len(self.z) == len(self.force):
                    self._g_fdistance.setData(self.z,self.force)
                    if self.selected is True:
                        self._curve_raw.setData(self.z_raw,self.f_raw)
                        self._curve_single.setData(self.z,self.force)
                        if self.E is not None:
                            ex,ey = self.getFitted()
                            self._curve_fit.setData(ex,ey)
                        else:
                            self._curve_fit.setData(None)
            self._g_fdistance.setPen(self.getPen('dist') )

        if self._g_indentation is not None:
            if self.ind is not None and self.touch is not None:
                if len(self.ind) == len(self.touch):
                    self._g_indentation.setData(self.ind, self.touch)
            self._g_indentation.setPen(self.getPen('ind'))

        if self._g_scatter is not None:
            if self.active is True and self.E is not None:
                self._g_scatter.setData(x=[self._Eindex],y=[self.E])
                self._g_scatter.setSymbolPen('k')
                self._g_scatter.setSymbolBrush('b')
            else:
                self._g_scatter.setSymbolPen(None)
                self._g_scatter.setSymbolBrush(None)

        if self.selected is True:
            self._ui.stats_R.setText(str(self.R))
            self._ui.stats_k.setText(str(self.k))
            if self.active is True:
                self._ui.toggle_activated.setChecked(True)
                if self.E is not None:
                    self._g_scatter.setSymbolPen(PEN_GREEN)
            elif self.included is False:
                self._ui.toggle_excluded.setChecked(True)
            else:
                self._ui.toggle_included.setChecked(True)

    def getPen(self,curve='ind'):
        PEN_BLACK = pg.mkPen(pg.QtGui.QColor(0, 0, 0, self.alpha), width=1)
        PEN_RED = pg.mkPen(pg.QtGui.QColor(255, 0, 0, self.alpha), width=1)
        PEN_BLUE = pg.mkPen(pg.QtGui.QColor(0, 0, 255, self.alpha), width=1)

        if curve == 'ind':
            if self.ind is None or self.touch is None:
                return None
            if len(self.ind) != len(self.touch):
                return None
            if self.active is False:
                return None
            pen = PEN_BLACK
        else:
            if self.z is None or self.force is None:
                return None
            if len(self.z) != len(self.force):
                return None
            if self.active is True:
                pen = PEN_BLACK
            else:
                if self.included is True:
                    pen = PEN_BLUE
                else:
                    pen = PEN_RED
        if self._ui.view_all.isChecked() is False and self.active is False:
            if self._ui.view_active.isChecked() is True:
                if self.active is False:
                    pen = None
            else:
                if self.included is False:
                    pen = None
        if self.selected is True:
            pen = PEN_GREEN
        return pen

    def set_indentation(self):
        if self._ui.analysis.isChecked() is False:
            return
        if self.k is None:
            return
        if self. active is False:
            return
        z = self.z
        f = self.force
        iContact = np.argmin((z ** 2))

        Yf = f[iContact:]
        Xf = z[iContact:]
        self.ind = Xf - Yf / self.k
        self.touch = Yf

    def reset_E(self):
        self._E = None

    def reset_contactpoint(self):
        self._contactpoint = [0,0]
        self._E=None

    def rewind_data(self):
        self._ind = None
        self._touch = None
        self._z = self._z_raw
        self._f = self._f_raw
        self._E = None

    def reset_data(self):
        self._z = None
        self._f = None
        self._ind = None
        self._touch = None
        self._E = None

    def set_XY(self,x,y):
        self.reset_data()
        self.reset_contactpoint()
        self._included = True
        self._active = True
        self.z_raw = x
        self.f_raw = y
        self._E = None

    def filter_all(self):
        self.rewind_data()
        if self._ui.prominency.isChecked() is True:
            pro = float(self._ui.prominency_prominency.value()) / 100.0
            winperc = int(self._ui.prominency_band.value())
            threshold = int(self._ui.prominency_minfreq.value())
            self.filter_prominence(pro, winperc, threshold)
        if self._ui.fsmooth.isChecked() is True:
            win = int(self._ui.fsmooth_window.value())
            method = 'SG'
            if self._ui.fsmooth_median.isChecked() is True:
                method = 'MM'
            self.filter_fsmooth(win, method)
        self.calculate_contactpoint()

    def filter_prominence(self, pro=0.2, winperc=1, threshold=25):
        if self.included is False:
            return
        # threshold is the minimum frequency to be eventually filtered
        # winperc is the width around the filtered frequency in % of the position
        # pro is the peak prominency
        y = self._f
        ff = np.fft.rfft(y, norm=None)
        idex = find_peaks(np.log(np.abs(ff)), prominence=pro)
        xgood = np.ones(len(ff.real)) > 0.5
        for imax in idex[0]:
            jwin = int(imax * winperc / 100)
            if imax > threshold and jwin == 0:
                xgood[imax] = False
            elif imax > threshold:
                ext1 = np.max([imax - jwin, 0])
                ext2 = np.min([imax + jwin + 1, len(xgood) - 1])
                for ii in range(ext1, ext2):
                    xgood[ii] = False
        if np.sum(xgood) < 50:
            return
        xf = np.arange(0, len(ff.real))
        yinterpreal = interp1d(xf[xgood], ff.real[xgood], kind='linear')
        yinterpimag = interp1d(xf[xgood], ff.imag[xgood], kind='linear')
        ff.real = yinterpreal(xf)
        ff.imag = yinterpimag(xf)
        self._f = np.fft.irfft(ff, n=len(y))

    def filter_fsmooth(self, win, method):
        if self.included is False:
            return
        if win % 2 == 0:
            win += 1
        y = self._f
        df = np.fft.rfft(y)
        if method == 'SG':
            df.real[win:-win] = savgol_filter(df.real, win, 3)[win:-win]
            df.imag[win:-win] = savgol_filter(df.imag, win, 3)[win:-win]
        elif method == 'MM':
            df.real[win:-win] = medfilt(df.real, win)[win:-win]
            df.imag[win:-win] = medfilt(df.imag, win)[win:-win]
        self._f = np.fft.irfft(df, n=len(y))

    def calculate_contactpoint(self):
        self.reset_contactpoint()
        if self.included is False:
            return
        off = float(self._ui.contact_offset.value())
        win = int(self._ui.contact_window.value())
        threshold = float(self._ui.contact_threshold.value())/ 1000.0
        if self.z is None or self.force is None or (len(self.z) != len(self.force)):
            return
        self._state = ST_BLK
        xprime = None
        if win % 2 == 0:
            win += 1
        try:
            xprime = savgol_filter(self._f, polyorder=1, deriv=1, window_length=win)
        except:
            self.active = False
            return
        quot = xprime / (1 - xprime)
        jj = 0
        for j in range(len(quot) - 1, 1, -1):
            if quot[j] > threshold and quot[j - 1] < threshold:
                jj = j
                break
        if (jj==0) or (jj==len(quot) - 1):
            self.active = False
            return
        oX = self._z[jj]
        oY = self._f[jj]
        if jj > 4 and jj < len(self._z) - 4:
            oX = np.average(self._z[jj - 4:jj + 4])
            oY = np.average(self._f[jj - 4:jj + 4])  # it might be extended to use a little average of F around point jj
        if oX is None or oY is None:
            self.active = False
            return
        self._contactpoint = [oX,oY]
        self.set_indentation()
        self.update_view()

    def getFitted(self):
        if self._ui.analysis.isChecked() is False:
            return
        x = np.linspace(0,float(self._ui.fit_indentation.value()),int(self._ui.fit_indentation.value()))
        y = hertz(x,self.E/1e9,self.R)

        x = x + y/self.k

        return x,y

    def fitHertz(self):
        if self._ui.analysis.isChecked() is False:
            return
        if self.ind is None or self.touch is None or (len(self.ind) != len(self.touch)):
            return
        seeds = [1000.0 / 1e9]
        try:
            R = self.R

            def Hertz(x, E):
                x = np.abs(x)
                poisson = 0.5
                # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
                return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

            indmax = float(self._ui.fit_indentation.value())
            jj = np.argmin((self.ind-indmax)**2)
            if jj < 5:
                return
            popt, pcov = curve_fit(Hertz, self.ind[:jj], self.touch[:jj], p0=seeds, maxfev=100000)
            #E_std = np.sqrt(pcov[0][0])
            self._E = popt[0]*1e9
        except (RuntimeError, ValueError):
            return

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, x):
        if x == self._selected:
            return
        self._selected = x
        if x is True:
            self._ui.mainlist.setCurrentItem(self._tree)
        self.update_view()

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, x):
        if x == self._alpha:
            return
        self._alpha = x
        self.update_view()

    @property
    def active(self):
        return self._state == ST_BLK

    @active.setter
    def active(self, x):
        if x is False:
            if self._state < ST_BLK:
                return
            self._state = ST_BLU
        else:
            if self._state == ST_BLK:
                return
            self._state = ST_BLK
            self._tree.setCheckState(0, QtCore.Qt.Checked)
        self.update_view()

    @property
    def included(self):
        return self._state > ST_RED

    @included.setter
    def included(self, x):
        if x is False:
            if self._state == ST_RED:
                return
            else:
                self._state = ST_RED
                self._tree.setCheckState(0, QtCore.Qt.Unchecked)
        else:
            if self._state > ST_RED:
                return
            self._state = ST_BLK
            self._tree.setCheckState(0, QtCore.Qt.Checked)
        self.update_view()

    @property
    def E(self):
        if self._E is None:
            self.fitHertz()
        return self._E

    @E.setter
    def E(self, x):
        if self._E == x:
            return
        self._E = x
        self.update_view()

    @property
    def x_contact_point(self):
        return self._contactpoint[0]

    @x_contact_point.setter
    def x_contact_point(self, x):
        if self._contactpoint[0] == x:
            return
        self._contactpoint[0] = x
        self.set_indentation()

    @property
    def y_contact_point(self):
        return self._contactpoint[1]

    @y_contact_point.setter
    def y_contact_point(self, x):
        if self._contactpoint[1] == x:
            return
        self._contactpoint[1] = x
        self.set_indentation()

    @property
    def z_raw(self):
        if self._z_raw is None:
            return None
        return self._z_raw - self.x_contact_point

    @z_raw.setter
    def z_raw(self, x):
        if x is not None:
            x = np.array(x)
        self._z_raw = x
        self.z = x

    @property
    def f_raw(self):
        if self._f_raw is None:
            return None
        return self._f_raw - self.y_contact_point

    @f_raw.setter
    def f_raw(self, x):
        if x is not None:
            x = np.array(x)
        self._f_raw = x
        self.force = x

    @property
    def z(self):
        if self._z is None:
            return None
        delta = self._z - self.x_contact_point
        return delta

    @z.setter
    def z(self, x):
        if sames(self._z,x) is False:
            if x is None:
                self._z = None
            else:
                x = np.array(x)
            self._z = x
            self.filter_all()

    @property
    def force(self):
        if self._f is None:
            return None
        return self._f - self.y_contact_point

    @force.setter
    def force(self, x):
        if sames(self._f, x) is False:
            if x is not None:
                x = np.array(x)
            self._f = x
            self.update_view()
            self.filter_all()

    @property
    def ind(self):
        return self._ind

    @ind.setter
    def ind(self, x):
        if sames(self._ind, x) is False:
            if x is not None:
                x = np.array(x)
            self._ind = x
            self.update_view()

    @property
    def touch(self):
        return self._touch

    @touch.setter
    def touch(self, x):
        if sames(self._touch, x) is False:
            if x is not None:
                x = np.array(x)
            self._touch = x
            self.update_view()
