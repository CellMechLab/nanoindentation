from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import pyqtgraph as pg
import mvexperiment.experiment as experiment
import nano_view as view
import motor
import numpy as np
import pickle

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class NanoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = view.Ui_MainWindow()
        self.ui.setupUi(self)

        self.curve_raw = pg.PlotCurveItem(clickable=False)
        self.curve_raw.setPen(pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=2))
        self.ui.g_single.plotItem.addItem(self.curve_raw)
        self.curve_single = pg.PlotCurveItem(clickable=False)
        self.curve_single.setPen(pg.mkPen(pg.QtGui.QColor(0, 0, 0, 200), width=1))
        self.ui.g_single.plotItem.addItem(self.curve_single)
        self.curve_fit = pg.PlotCurveItem(clickable=False)
        self.curve_fit.setPen(pg.mkPen(pg.QtGui.QColor(255, 0, 0, 150), width=2, style=QtCore.Qt.DashLine ))
        self.ui.g_single.plotItem.addItem(self.curve_fit)
        self.histo_data = pg.PlotCurveItem([0,0],[0],clickable=False,stepMode=True,fillLevel=0,brush=pg.mkBrush([0,0,255,50]))
        self.histo_data.setPen(pg.mkPen(pg.QtGui.QColor(0, 0, 255), width=1))
        self.ui.g_histo.plotItem.addItem(self.histo_data)
        self.histo_fit = pg.PlotCurveItem(clickable=False)
        self.histo_fit.setPen(pg.mkPen(pg.QtGui.QColor(255, 0, 0, 150), width=2, style=QtCore.Qt.DashLine))
        self.ui.g_histo.plotItem.addItem(self.histo_fit)

        self.workingdir = './'
        self.collection = []
        self.experiment = None

        # connect load and open, other connections after load/open
        self.ui.open_load.clicked.connect(self.load_pickle)
        self.ui.open_selectfolder.clicked.connect(self.open_folder)

        QtCore.QMetaObject.connectSlotsByName(self)

    ################################################
    ############## OPEN / LOAD #####################
    ################################################

    def clear(self):
        self.collection = []
        self.experiment = None
        self.ui.mainlist.clear()
        self.ui.g_fdistance.plotItem.clear()
        self.ui.g_indentation.plotItem.clear()
        self.histo_fit.setData(None)
        self.histo_data.setData([0,0],[0])
        self.curve_raw.setData(None)
        self.curve_single.setData(None)
        self.curve_fit.setData(None)

        self.collection = []

    def connect_all(self,connect=True):
        slots=[]
        handlers=[]

        slots.append(self.ui.curve_segment.valueChanged)
        handlers.append(self.refill)

        slots.append(self.ui.slid_alpha.valueChanged)
        handlers.append(self.set_alpha)

        slots.append(self.ui.mainlist.currentItemChanged)
        handlers.append(self.change_selected)

        slots.append(self.ui.mainlist.itemChanged)
        handlers.append(self.data_changed)

        cli = [self.ui.prominency,self.ui.fsmooth,self.ui.fsmooth_savitzky,self.ui.fsmooth_median]
        vch = [self.ui.prominency_minfreq,self.ui.prominency_band,self.ui.prominency_prominency,self.ui.fsmooth_window  ]
        for click in cli:
            slots.append(click.clicked)
            handlers.append(self.filter_changed)
        for chan in vch:
            slots.append(chan.valueChanged)
            handlers.append(self.filter_changed)

        slots.append(self.ui.contact_threshold.valueChanged)
        handlers.append(self.cpoint_changed)
        slots.append(self.ui.contact_window.valueChanged)
        handlers.append(self.cpoint_changed)

        slots.append(self.ui.fit_indentation.valueChanged)
        handlers.append(self.redostat)

        cli = [self.ui.view_active, self.ui.view_included, self.ui.view_all]
        for click in cli:
            slots.append(click.clicked)
            handlers.append(self.refresh)

        cli = [self.ui.toggle_activated, self.ui.toggle_excluded, self.ui.toggle_included]
        for click in cli:
            slots.append(click.clicked)
            handlers.append(self.toggle)

        vch = [ self.ui.histogram_max,self.ui.histogram_min,self.ui.histogram_bins ]
        for chan in vch:
            slots.append(chan.valueChanged)
            handlers.append(self.count)
        slots.append(self.ui.histogram.clicked)
        handlers.append(self.count)

        for i in range(len(slots)):
            if connect is True:
                slots[i].connect(handlers[i])
            else:
                try:
                    slots[i].disconnect(handlers[i])
                except TypeError:
                    pass

    def disconnect_all(self):
        self.connect_all(False)

    def load_pickle(self):

        fname = QtWidgets.QFileDialog.getOpenFileName(self,'Select the file to load your processing',self.workingdir,"Python object serialization (*.pickle)")
        if fname[0] =='':
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        with open(fname[0], 'rb') as f:
            data = pickle.load(f)
        QtWidgets.QApplication.restoreOverrideCursor()

        if data[0].phase == 2:
            self.b2['exp']=data
            self.b2Init()
        elif data[0].phase == 3:
            self.b3['exp']=data
            self.b3Init()
        elif data[0].phase == 4:
            self.b4['exp']=data
            self.b4Init()

    def save_pickle(self):
        phase = self.ui.switcher.currentIndex()+1
        if phase == 2:
            data = self.b2['exp'].copy()
        elif phase == 3:
            data = self.b3['exp'].copy()
        elif phase == 4:
            data = self.b4['exp'].copy()
        for s in data:
            s.plit = None
            s.elit = None
        
        fname = QtWidgets.QFileDialog.getSaveFileName(self,'Select the file to save your processing',self.workingdir,"Python object serialization (*.pickle)")
        if fname[0] =='':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        with open(fname[0], 'wb') as f:
            pickle.dump(data, f)
        QtWidgets.QApplication.restoreOverrideCursor()

    def open_folder(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self,'Select the root dir','./')
        if fname =='' or fname is None or fname[0] =='':
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.workingdir = fname
        if self.ui.open_o11new.isChecked() is True:
            exp = experiment.Chiaro(fname)
        elif self.ui.open_o11old.isChecked() is True:
            exp = experiment.ChiaroGenova(fname)
        elif self.ui.open_nanosurf.isChecked() is True:
            exp = experiment.NanoSurf(fname)

        exp.browse()
        if len(exp) == 0:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.information(self,'Empty folder','I did not find any valid file in the folder, please check file format and folder')
            return

        self.disconnect_all()
        self.clear()
        self.experiment = exp

        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, len(self.experiment.haystack))


        def attach(node,parent):
            myself = QtWidgets.QTreeWidgetItem(parent)
            node.myTree = myself
            myself.setText(0, node.basename)
            myself.curve = node
            myself.setFlags(myself.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            myself.setCheckState(0,QtCore.Qt.Checked)
            for mychild in node:
                attach(mychild,myself)
        for node in self.experiment:
            attach(node,self.ui.mainlist)

        for c in self.experiment.haystack:
            c.open()
            node = motor.Nanoment(c)
            node.connect(self,c.myTree)
            c.myTree.nano = node
            self.collection.append(node)
            progress.setValue(progress.value() + 1)
            QtCore.QCoreApplication.processEvents()

        progress.setValue(len(self.experiment.haystack))
        QtWidgets.QApplication.restoreOverrideCursor()

        self.fdistance_fit = pg.PlotCurveItem(clickable=False)
        self.fdistance_fit.setPen(pg.mkPen(pg.QtGui.QColor(255, 0, 0, 150), width=2, style=QtCore.Qt.DashLine))
        self.ui.g_fdistance.plotItem.addItem(self.fdistance_fit)
        self.indentation_fit = pg.PlotCurveItem(clickable=False)
        self.indentation_fit.setPen(pg.mkPen(pg.QtGui.QColor(255, 0, 0, 150), width=2, style=QtCore.Qt.DashLine))
        self.ui.g_indentation.plotItem.addItem(self.indentation_fit)

        self.ui.slid_curve.setValue(0)
        self.ui.slid_curve.setMaximum(len(self.collection)-1)
        self.ui.slid_curve.setValue(0)
        self.ui.curve_segment.setMaximum(len(self.experiment.haystack[0])-1)
        self.connect_all()
        if len(self.experiment.haystack[0])>1:
            self.ui.slid_curve.setValue(1)
            self.ui.curve_segment.setValue(1)
        #else:
        #    self.refill()
        self.refill()

    def redostat(self):
        for c in self.collection:
            c.reset_E()
        self.refresh()

    def refresh(self):
        for c in self.collection:
            c.update_view()
        self.count()

    def toggle(self):
        current = 0
        for i in range(len(self.collection)):
            if self.collection[i].selected is True:
                current = i
                break
        if self.ui.toggle_activated.isChecked() is True:
            self.collection[current].active = True
        else:
            if self.ui.toggle_excluded.isChecked() is True:
                self.collection[current].included = False
            else:
                self.collection[current].active = False
        self.count()

    def refill(self):
        indicator = int(self.ui.curve_segment.value())
        for i in range(len(self.collection)):
            c = self.experiment.haystack[i]
            try:
                self.collection[i].set_XY(c[indicator].z,c[indicator].f)
            except IndexError:
                QtWidgets.QMessageBox.information(self, 'Empty curve','Problem detected with curve {}, not populated'.format(c.basename))
        self.filter_changed()

    def numbers(self):
        E_array=[]
        for c in self.collection:
            if c.active is True and c.E is not None:
                E_array.append(c.E)
        eall = np.array(E_array)
        self.ui.data_average.setText( str(int(np.average(eall)/10)/100.0) )
        self.ui.data_std.setText(str(int(np.std(eall) / 10) / 100.0))

        bins = 'auto'
        rng = None
        if self.ui.histogram.isChecked() is True:
            nm = int(self.ui.histogram_bins.value())
            if nm > 0:
                bins = nm
            rmin = float( self.ui.histogram_min.value() )
            rmax = float( self.ui.histogram_max.value() )
            if rmin != 0 and rmax != 0:
                rng = (rmin,rmax)
        if rng is None:
            y,x = np.histogram(eall, bins=bins, density=True)
        else:
            y, x = np.histogram(eall, bins=bins, density=True, range=rng)
        if len(y)>=3:
            self.histo_data.setData(x,y)
            self.ui.fit_center.setText('0.00')
            self.ui.fit_std.setText('0.00')

            #try:
            x0, w, A, nx, ny = motor.gauss_fit(x, y)
            self.histo_fit.setData(nx,ny)
            self.ui.fit_center.setText(str(int(np.average(x0)/10)/100.0))
            self.ui.fit_std.setText(str(int(np.average(w)/10)/100.0))

            x,y,z = motor.calc_hertz(x0,self.collection[0].R,self.collection[0].k,float(self.ui.fit_indentation.value()))
            self.indentation_fit.setData(x,y)
            self.fdistance_fit.setData(z,y)

            #except:
            #    pass


    def count(self):
        Ne = 0
        Na = 0
        Ni = 0
        for c in self.collection:
            if c.active is True:
                Na += 1
            elif c.included is False:
                Ne += 1
            else:
                Ni += 1
        self.ui.stats_ne.setText(str(Ne))
        self.ui.stats_ni.setText(str(Ni))
        self.ui.stats_na.setText(str(Na))

        self.numbers()

    def data_changed(self,item):
        included = item.checkState(0) == QtCore.Qt.Checked
        try:
            item.nano.included = included
        except AttributeError:
            pass
        self.count()

    def curve_clicked(self, curve):
        for c in self.collection:
            c.selected = False
        curve.nano.selected = True

    def change_selected(self,item):
        for c in self.collection:
            c.selected = False
        try:
            item.nano.selected = True
        except AttributeError:
            pass

    def set_alpha(self,num):
        num = int(num)
        for c in self.collection:
            c.alpha = num

    def cpoint_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for c in self.collection:
            c.calculate_contactpoint()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.count()

    def filter_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for c in self.collection:
            c.filter_all()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.count()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Nano2020')
    chiaro = NanoWindow()
    chiaro.show()
    # QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
