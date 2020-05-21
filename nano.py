from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import pyqtgraph as pg
import mvexperiment.experiment as experiment
import nano_view as view
import motor
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
        self.ui.mainlist.clear()
        self.ui.g_fdistance.plotItem.clear()
        self.ui.g_indentation.plotItem.clear()
        #self.ui.g_histo.plotItem.clear()
        #self.ui.g_scatter.plotItem.clear()
        self.curve_raw.setData(None)
        self.curve_single.setData(None)

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
            self.experiment = experiment.Chiaro(fname)
        elif self.ui.open_o11old.isChecked() is True:
            self.experiment = experiment.ChiaroGenova(fname)
        elif self.ui.open_nanosurf.isChecked() is True:
            self.experiment = experiment.NanoSurf(fname)

        self.experiment.browse()
        if len(self.experiment) == 0:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.information(self,'Empty folder','I did not find any valid file in the folder, please check file format and folder')
            return

        self.disconnect_all()
        self.clear()

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

        self.ui.slid_curve.setValue(0)
        self.ui.slid_curve.setMaximum(len(self.collection)-1)
        self.ui.slid_curve.setValue(0)
        self.ui.curve_segment.setMaximum(len(self.experiment.haystack[0])-1)
        self.connect_all()
        if len(self.experiment.haystack[0])>1:
            self.ui.slid_curve.setValue(1)
            #self.ui.curve_segment.setValue(1)
        else:
            self.refill()
        self.refill()

    def refill(self):
        indicator = int(self.ui.curve_segment.value())
        for i in range(len(self.collection)):
            c = self.experiment.haystack[i]
            self.collection[i].set_XY(c[indicator].z,c[indicator].f)

    def data_changed(self,item):
        included = item.checkState(0) == QtCore.Qt.Checked
        try:
            item.nano.included = included
        except AttributeError:
            pass

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

    def filter_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for c in self.collection:
            c.rewind_data()
        if self.ui.prominency.isChecked() is True:
            for c in self.collection:
                pro = float(self.ui.prominency_prominency.value())/100.0
                winperc = int( self.ui.prominency_band.value() )
                threshold = int( self.ui.prominency_minfreq.value() )
                c.filter_prominence(pro, winperc, threshold)
        if self.ui.fsmooth.isChecked() is True:
            for c in self.collection:
                win = int(self.ui.fsmooth_window.value())
                method = 'SG'
                if self.ui.fsmooth_median.isChecked() is True:
                    method = 'MM'
                c.filter_fsmooth(win, method)
        QtWidgets.QApplication.restoreOverrideCursor()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Nano2020')
    chiaro = NanoWindow()
    chiaro.show()
    # QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
