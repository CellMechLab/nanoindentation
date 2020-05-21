from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
import pyqtgraph as pg
from scipy.signal import savgol_filter,medfilt,find_peaks
from scipy.interpolate import interp1d

PEN_GREEN = pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=2)

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

class Nanoment(object):
    def __init__(self,curve = None):
        self.basename = None
        self._xcontactpoint = 0
        self._ycontactpoint = 0
        self._z = None
        self._f = None
        self._z_raw = None
        self._f_raw = None
        self._ind = None
        self._touch = None
        self.R = None
        self.k = None
        self.curve_single = None
        self.curve_raw = None
        self._g_fdistance = None
        self._g_indentation = None
        self._active = True
        self._included = True
        self._alpha = 100
        self._selected = False
        self._tree = None
        self._ui = None
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

        self._curve_single = nanowin.curve_single
        self._curve_raw = nanowin.curve_raw

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
        self._tree = None
        self._ui = None
        self._curve_single = None
        self._curve_raw = None

    def update_view(self):
        if self._g_fdistance is not None:
            if self.z is not None and self.force is not None:
                if len(self.z) == len(self.force):
                    self._g_fdistance.setData(self.z,self.force)
                    if self.selected is True:
                        self._curve_raw.setData(self._z_raw-self.x_contact_point,self._f_raw-self.y_contact_point)
                        self._curve_single.setData(self.z,self.force)
            self._g_fdistance.setPen(self.getPen('dist') )

        if self._g_indentation is not None:
            if self.ind is not None and self.touch is not None:
                if len(self.ind) == len(self.touch):
                    self._g_indentation.setData(self.ind, self.touch)
            self._g_indentation.setPen(self.getPen('ind'))
        if self.selected is True:
            self._ui.stats_R.setText(str(self.R))
            self._ui.stats_k.setText(str(self.k))


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
        if self.selected is True:
            pen = PEN_GREEN
        return pen

    def set_indentation(self):
        if self.k is None:
            return

        z = self.z
        f = self.force
        iContact = np.argmin((z ** 2))

        Yf = f[iContact:]
        Xf = z[iContact:]
        self.ind = Xf - Yf / self.k
        self.touch = Yf

    def reset_contactpoint(self):
        self._xcontactpoint = 0
        self._ycontactpoint = 0

    def rewind_data(self):
        self._ind = None
        self._touch = None
        self.z = self._z_raw
        self.force = self._f_raw

    def reset_data(self):
        self._z = None
        self._f = None
        self._ind = None
        self._touch = None

    def set_XY(self,x,y):
        self.reset_data()
        self.reset_contactpoint()
        self._included = True
        self._active = True
        self._z_raw = x
        self._f_raw = y
        self.z = x
        self.force = y
        # calculate contact point
        # set indentation

    def filter_prominence(self, pro=0.2, winperc=1, threshold=25):
        # threshold is the minimum frequency to be eventually filtered
        # winperc is the width around the filtered frequency in % of the position
        # pro is the peak prominency
        y = self.force
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
            return y
        xf = np.arange(0, len(ff.real))
        yinterpreal = interp1d(xf[xgood], ff.real[xgood], kind='linear')
        yinterpimag = interp1d(xf[xgood], ff.imag[xgood], kind='linear')
        ff.real = yinterpreal(xf)
        ff.imag = yinterpimag(xf)
        self.force = np.fft.irfft(ff, n=len(y))

    def filter_fsmooth(self, win, method):
        if win % 2 == 0:
            win += 1
        y = self.force
        df = np.fft.rfft(y)
        if method == 'SG':
            df.real[win:-win] = savgol_filter(df.real, win, 3)[win:-win]
            df.imag[win:-win] = savgol_filter(df.imag, win, 3)[win:-win]
        elif method == 'MM':
            df.real[win:-win] = medfilt(df.real, win)[win:-win]
            df.imag[win:-win] = medfilt(df.imag, win)[win:-win]
        self.force = np.fft.irfft(df, n=len(y))

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
        return self._active

    @active.setter
    def active(self, x):
        if self._active is x:
            return
        self._active = x
        if self._active is True:
            self.included = True
        self.update_view()

    @property
    def included(self):
        return self._included

    @included.setter
    def included(self, x):
        if self._included is x:
            return
        self._included = x
        if self._included is True:
            self._tree.setCheckState( 0,QtCore.Qt.Checked )
        else:
            self._tree.setCheckState(0,QtCore.Qt.Unchecked)
        if x is False:
            self.active = False
        self.update_view()

    @property
    def x_contact_point(self):
        return self._xcontactpoint

    @x_contact_point.setter
    def x_contact_point(self, x):
        if self._xcontactpoint == x:
            return
        self._xcontactpoint = x
        self.update_view()

    @property
    def y_contact_point(self):
        return self._ycontactpoint

    @y_contact_point.setter
    def y_contact_point(self, x):
        if self._ycontactpoint == x:
            return
        self._ycontactpoint = x
        self.update_view()

    @property
    def z(self):
        if self._z is None:
            return None
        return self._z-self.x_contact_point

    @z.setter
    def z(self, x):
        if sames(self._z,x) is False:
            x = np.array(x)
            self._z = x
            self.update_view()

    @property
    def force(self):
        if self._f is None:
            return None
        return self._f - self.y_contact_point

    @force.setter
    def force(self, x):
        if sames(self._f, x) is False:
            x = np.array(x)
            self._f = x
            self.update_view()

    @property
    def ind(self):
        return self._ind

    @ind.setter
    def ind(self, x):
        if sames(self._ind, x) is False:
            x = np.array(x)
            self._ind = x
            self.update_view()

    @property
    def touch(self):
        return self._touch

    @touch.setter
    def touch(self, x):
        if sames(self._touch, x) is False:
            x = np.array(x)
            self._touch = x
            self.update_view()
