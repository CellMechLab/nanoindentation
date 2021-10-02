"""Main module to run GUI."""

import sys
import os

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import motor
import nano_view as view
import panels
import filter_panel as panfilter
import popup
import json
import engine
from itertools import zip_longest
# import qtmodern.styles
# import qtmodern.windows


pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class NanoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = view.Ui_MainWindow()
        self.ui.setupUi(self)
        self.collection = None
        # set plots style
        self.curve_raw = pg.PlotCurveItem(clickable=False)
        self.curve_raw.setPen(
            pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=1))
        self.ui.g_single.plotItem.showGrid(True, True)
        self.ui.g_single.plotItem.addItem(self.curve_raw)
        self.curve_single = pg.PlotCurveItem(clickable=False)
        self.curve_single.setPen(
            pg.mkPen(pg.QtGui.QColor(0, 0, 0, 200), width=1))
        self.ui.g_single.plotItem.addItem(self.curve_single)
        self.curve_fit = pg.PlotCurveItem(clickable=False)
        self.curve_fit.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=5, style=QtCore.Qt.DashLine))
        self.ui.g_single.plotItem.addItem(self.curve_fit)

        # self.histo_data = pg.PlotCurveItem([0, 0], [
        #                                    0], clickable=False, stepMode='center', fillLevel=0, brush=pg.mkBrush([0, 0, 255, 50]))
        # self.histo_data.setPen(pg.mkPen(pg.QtGui.QColor(0, 0, 255), width=1))
        # self.ui.g_histo.plotItem.addItem(self.histo_data)
        # self.histo_esdata = pg.PlotCurveItem([0, 0], [
        #                                      0], clickable=False, stepMode='center', fillLevel=0, brush=pg.mkBrush([255, 0, 0, 50]))
        # self.histo_esdata.setPen(pg.mkPen(pg.QtGui.QColor(255, 0, 0), width=1))
        # self.ui.g_histo.plotItem.addItem(self.histo_esdata)
        # self.histo_fit = pg.PlotCurveItem(clickable=False)
        # self.histo_fit.setPen(pg.mkPen(pg.QtGui.QColor(
        #     0, 0, 255, 150), width=5))  # ,style=QtCore.Qt.DashLine))
        # self.ui.g_histo.plotItem.addItem(self.histo_fit)
        # self.histo_esfit = pg.PlotCurveItem(clickable=False)
        # self.histo_esfit.setPen(pg.mkPen(pg.QtGui.QColor(
        #     255, 0, 0, 150), width=5))  # ,style=QtCore.Qt.DashLine))
        # self.ui.g_histo.plotItem.addItem(self.histo_esfit)

        #Elasticity spectra
        self.es_top = pg.PlotCurveItem(clickable=False)
        self.es_top.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=1, style=QtCore.Qt.SolidLine))
        self.ui.g_decay.plotItem.addItem(self.es_top)
        self.es_bottom = pg.PlotCurveItem(clickable=False)
        self.es_bottom.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=1, style=QtCore.Qt.SolidLine))
        self.ui.g_decay.plotItem.addItem(self.es_bottom)
        self.es_averageZoom = pg.PlotCurveItem(clickable=False)
        self.es_averageZoom.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=3, style=QtCore.Qt.SolidLine))
        self.ui.g_decay.plotItem.addItem(self.es_averageZoom)
        self.es_averageFit = pg.PlotCurveItem(clickable=False)
        self.es_averageFit.setPen(pg.mkPen(pg.QtGui.QColor(
            0, 0, 0, 250), width=1, style=QtCore.Qt.DashLine))
        self.ui.g_decay.plotItem.addItem(self.es_averageFit)
        self.es_band = pg.FillBetweenItem(self.es_bottom, self.es_top)
        self.es_band.setBrush(pg.mkBrush(pg.QtGui.QColor(255, 0, 0, 50)))
        self.ui.g_decay.plotItem.addItem(self.es_band)
        
        # average hertz data
        self.hertz_average = pg.PlotCurveItem(clickable=False)
        self.hertz_average.setPen(pg.mkPen(pg.QtGui.QColor(
            0, 0, 255, 150), width=3, style=QtCore.Qt.SolidLine))
        self.ui.avg_hertz.plotItem.addItem(self.hertz_average)
        self.hertz_average_top = pg.PlotCurveItem(clickable=False)
        self.hertz_average_top.setPen(pg.mkPen(pg.QtGui.QColor(
            0, 0, 255, 150), width=1, style=QtCore.Qt.SolidLine))
        self.ui.avg_hertz.plotItem.addItem(self.hertz_average_top)
        self.hertz_average_bottom = pg.PlotCurveItem(clickable=False)
        self.hertz_average_bottom.setPen(pg.mkPen(pg.QtGui.QColor(
            0, 0, 255, 150), width=1, style=QtCore.Qt.SolidLine))
        self.ui.avg_hertz.plotItem.addItem(self.hertz_average_bottom)
        self.hertz_band = pg.FillBetweenItem(
            self.hertz_average_bottom, self.hertz_average_top)
        self.hertz_band.setBrush(pg.mkBrush(pg.QtGui.QColor(0, 0, 255, 50)))
        self.ui.avg_hertz.plotItem.addItem(self.hertz_band)
        #avg hertz fit on average F-ind
        self.indentation_fit_avg = pg.PlotCurveItem(clickable=False)
        self.indentation_fit_avg.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=3, style=QtCore.Qt.DashLine))
        self.ui.avg_hertz.plotItem.addItem(self.indentation_fit_avg)

        def title_style(lab):
            return '<span style="font-family: Arial; font-weight:bold; font-size: 10pt;">{}</span>'.format(lab)

        def lab_style(lab):
            return '<span style="">{}</span>'.format(lab)

        self.ui.g_fdistance.plotItem.setTitle(title_style('Raw curves'))
        self.ui.g_indentation.plotItem.setTitle(
            title_style('Indentation curves'))
        self.ui.g_es.plotItem.setTitle(title_style('Elasticity Spectra'))
        self.ui.g_scatter.plotItem.setTitle(title_style('Elasticity values'))
        self.ui.g_single.plotItem.setTitle(title_style('Current curve'))
        # empty title (elasticity stats)
        # self.ui.g_histo.plotItem.setTitle(title_style(''))
        self.ui.g_decay.plotItem.setTitle(title_style('Bilayer model'))

        self.ui.g_fdistance.plotItem.setLabel('left', lab_style('Force [nN]'))
        self.ui.g_single.plotItem.setLabel('left', lab_style('Force [nN]'))
        self.ui.g_indentation.plotItem.setLabel(
            'left', lab_style('Force [nN]'))
        self.ui.g_es.plotItem.setLabel('left', lab_style('Elasticity [Pa]'))
        self.ui.g_scatter.plotItem.setLabel(
            'left', lab_style('Young\'s modulus [Pa]'))
        # self.ui.g_histo.plotItem.setLabel(
        #     'left', lab_style('Probability density'))
        self.ui.g_decay.plotItem.setLabel('left', lab_style('Elasticity [Pa]'))

        self.ui.g_fdistance.plotItem.setLabel(
            'bottom', lab_style('Displacement [nm]'))
        self.ui.g_single.plotItem.setLabel(
            'bottom', lab_style('Displacement [nm]'))
        self.ui.g_indentation.plotItem.setLabel(
            'bottom', lab_style('Indentation [nm]'))
        self.ui.g_es.plotItem.setLabel(
            'bottom', lab_style('Indentation [nm]'))
        self.ui.g_scatter.plotItem.setLabel('bottom', lab_style('Curve #'))
        # self.ui.g_histo.plotItem.setLabel(
        #     'bottom', lab_style('Young\'s modulus [Pa]'))
        self.ui.g_decay.plotItem.setLabel(
            'bottom', lab_style('Indetation [nm]'))
        self.ui.avg_hertz.plotItem.setTitle(title_style('Average F-Ind'))
        self.ui.avg_hertz.plotItem.setLabel(
            'bottom', lab_style('Average indentation [nm]'))
        self.ui.avg_hertz.plotItem.setLabel(
            'left', lab_style('Average force [nN]'))

        for obj in panels.ALL:
            self.ui.comboCP.addItem(obj['label'])
        self.contactPoint = None

        self.ui.comboFsmooth.addItem('-- None --')
        for obj in panfilter.ALL_FILTERS:
            self.ui.comboFsmooth.addItem(obj['label'])
        self.filterMethod = None

        layout = QtWidgets.QFormLayout()
        layout.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.ui.CP_box.setLayout(layout)
        self.changeCP(0)

        layout2 = QtWidgets.QFormLayout()
        layout2.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.ui.FSmooth_box.setLayout(layout2)
        self.changeFS(0)

        self.workingdir = './'
        self.collection = []
        self.experiment = None

        # connect load and open, other connections after load/open
        self.ui.open_selectfolder.clicked.connect(self.loadExperiment)
        self.ui.comboCP.currentIndexChanged.connect(self.changeCP)
        self.ui.comboFsmooth.currentIndexChanged.connect(self.changeFS)

        self.ui.prominency.clicked.connect(self.fmethod_changed)
        self.ui.prominency_prominency.valueChanged.connect(
            self.fmethod_changed)
        self.ui.prominency_minfreq.valueChanged.connect(self.fmethod_changed)
        self.ui.prominency_band.valueChanged.connect(self.fmethod_changed)

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
        self.ui.g_es.plotItem.clear()
        self.ui.g_scatter.plotItem.clear()
        # self.histo_fit.setData(None)
        # self.histo_esfit.setData(None)
        # self.histo_data.setData([0, 0], [0])
        # self.histo_esdata.setData([0, 0], [0])
        self.es_top.setData(None)
        self.es_bottom.setData(None)
        self.es_averageZoom.setData(None)
        self.es_averageFit.setData(None)
        self.hertz_average.setData(None)
        self.hertz_average_bottom.setData(None)
        self.hertz_average_top.setData(None)
        self.hertz_average_error = None
        self.curve_raw.setData(None)
        self.curve_single.setData(None)
        self.curve_fit.setData(None)
        self.experiment = None
        self.collection = []

    # connecting all GUI events (signals) to respective slots (functions)
    def connect_all(self, connect=True):
        slots = []
        handlers = []

        # slots.append(self.ui.curve_segment.valueChanged)
        # handlers.append(self.refill)

        slots.append(self.ui.slid_alpha.valueChanged)
        handlers.append(self.set_alpha)

        slots.append(self.ui.mainlist.currentItemChanged)
        handlers.append(self.change_selected)

        slots.append(self.ui.mainlist.itemChanged)
        handlers.append(self.data_changed)

        slots.append(self.ui.quickView.clicked)
        handlers.append(self.quickCP)

        slots.append(self.ui.fit_indentation.valueChanged)
        handlers.append(self.redostat)

        slots.append(self.ui.es_win.valueChanged)
        handlers.append(self.es_changed)
        slots.append(self.ui.es_order.valueChanged)
        handlers.append(self.es_changed)
        slots.append(self.ui.es_interpolate.clicked)
        handlers.append(self.es_changed)

        cli = [self.ui.view_active, self.ui.view_included, self.ui.view_all]
        for click in cli:
            slots.append(click.clicked)
            handlers.append(self.refresh)

        cli = [self.ui.toggle_activated,
               self.ui.toggle_excluded, self.ui.toggle_included]
        for click in cli:
            slots.append(click.clicked)
            handlers.append(self.toggle)

        # Important: when adding something new to the gui, need to append slots + append handlers
        slots.append(self.ui.save_dataHertz.clicked)
        handlers.append(self.save_dataHertz)

        slots.append(self.ui.save_avg_hertz.clicked)
        handlers.append(self.save_hertz_average)

        slots.append(self.ui.save_dataES.clicked)
        handlers.append(self.save_dataES)

        slots.append(self.ui.reset_all.clicked)
        handlers.append(self.include_exclude_all)

        slots.append(self.ui.analysis.clicked)
        handlers.append(self.hertz_changed)

        slots.append(self.ui.es_analysis.clicked)
        handlers.append(self.es_changed)

        # slots.append(self.ui.crop.clicked)
        # handlers.append(self.crop)

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

    def loadExperiment(self):
        fOpener = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Experiment File", self.workingdir, "JSON curve files (*.json)")
        if fOpener[0] == '' or fOpener[0] is None:
            return
        self.redraw = False
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        filename = fOpener[0]
        self.workingdir = os.path.dirname(filename)

        exp = None
        engine.haystack = []
        structure = json.load(open(filename))
        for cv in structure['curves']:
            engine.haystack.append(engine.curve(cv))
        QtWidgets.QApplication.restoreOverrideCursor()

        self.disconnect_all()
        self.clear()
        self.experiment = engine

        def attach(node, parent):
            myself = QtWidgets.QTreeWidgetItem(parent)
            node.myTree = myself
            myself.setText(0, node.filename)
            myself.curve = node
            myself.setFlags(
                myself.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            myself.setCheckState(0, QtCore.Qt.Checked)
            # for mychild in node:
            #    attach(mychild, myself)
        for node in self.experiment.haystack:
            attach(node, self.ui.mainlist)

        for c in self.experiment.haystack:
            node = motor.Nanoment(c)
            node.setCPFunction(self.contactPoint.calculate)
            node.connect(self, c.myTree)
            c.myTree.nano = node
            self.collection.append(node)
            QtCore.QCoreApplication.processEvents()
        self.refresh()

        self.fdistance_fit = pg.PlotCurveItem(clickable=False)
        self.fdistance_fit.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=5, style=QtCore.Qt.DashLine))
        self.ui.g_fdistance.plotItem.addItem(self.fdistance_fit)
        self.indentation_fit = pg.PlotCurveItem(clickable=False)
        self.indentation_fit.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 150), width=5, style=QtCore.Qt.DashLine))
        self.ui.g_indentation.plotItem.addItem(self.indentation_fit) 
        self.es_average = pg.PlotCurveItem(clickable=False)
        self.es_average.setPen(pg.mkPen(pg.QtGui.QColor(
            255, 0, 0, 255), width=2, style=QtCore.Qt.SolidLine))
        self.ui.g_es.plotItem.addItem(self.es_average)

        # self.ui.curve_segment.setMaximum(len(self.experiment.haystack[0])-1)
        # if len(self.experiment.haystack[0]) > 1:
        #    self.ui.curve_segment.setValue(1)
        self.connect_all()
        self.refill()

        QtWidgets.QApplication.restoreOverrideCursor()

    def quickCP(self):
        for c in self.collection:
            if c.selected is True:
                x0, y0 = None, None
                all = self.contactPoint.calculate(c)
                if all is not None:
                    x0, y0 = all
                a = popup.uiPanel()
                a.setPlots(c._z, c._f, *self.contactPoint.quickTest(c), x0, y0)
                a.exec()

    def changeFS(self, index):
        if self.filterMethod is not None:
            self.filterMethod.disconnect()
        if index == 0:
            self.filterMethod = None
        else:
            self.filterMethod = panfilter.ALL_FILTERS[index-1]['method']()
            self.filterMethod.createUI(self.ui.FSmooth_box.layout())
            self.filterMethod.connect(self.fmethod_changed)
        self.fmethod_changed()

    def changeCP(self, index):
        if self.contactPoint is not None:
            self.contactPoint.disconnect()
        self.contactPoint = panels.ALL[index]['method']()
        self.contactPoint.createUI(self.ui.CP_box.layout())
        self.contactPoint.connect(self.cpoint_changed)
        self.cpoint_changed()

    def include_exclude_all(self):
        if self.ui.reset_activate.isChecked() is True:
            for c in self.collection:
                c.active = True
        else:
            for c in self.collection:
                c.included = False

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

    # def crop(self):
    #     left = self.ui.crop_left.isChecked()
    #     right = self.ui.crop_right.isChecked()
    #     if left is True or right is True:
    #         # indicator = int(self.ui.curve_segment.value())
    #         for i in range(len(self.collection)):
    #             c = self.collection[i]
    #             try:
    #                 x = c._z_raw
    #                 y = c._f_raw
    #                 leftLim = np.min(c._z_raw) + 50
    #                 rightLim = np.max(c._z_raw) - 50
    #                 xnew = []
    #                 ynew = []
    #                 for k in range(len(x)):
    #                     this = True
    #                     if left is True:
    #                         if x[k] < leftLim:
    #                             this = False
    #                     if right is True:
    #                         if x[k] > rightLim:
    #                             this = False
    #                     if this is True:
    #                         xnew.append(x[k])
    #                         ynew.append(y[k])
    #                 self.collection[i].set_XY(xnew, ynew)
    #             except IndexError:
    #                 QtWidgets.QMessageBox.information(
    #                     self, 'Empty curve', 'Problem detected with curve {}, not populated'.format(c.basename))
    #         self.fmethod_changed()
    #     else:
    #         return

    def refill(self):
        # indicator = int(self.ui.curve_segment.value())
        for i in range(len(self.collection)):
            c = self.experiment.haystack[i]
            try:
                # self.collection[i].set_XY(c[indicator].z, c[indicator].f)
                self.collection[i].set_XY(c._Z*1e9, c._F*1e9)
            except IndexError:
                QtWidgets.QMessageBox.information(
                    self, 'Empty curve', 'Problem detected with curve {}, not populated'.format(c.basename))
        self.fmethod_changed()

    def numbers(self):
        E_array = []
        F_data = []
        ind_data = []

        for c in self.collection:
            if c.active is True and c.E is not None:
                E_array.append(c.E)
                # Average Hertz
                F_data.append(c.touch)
                ind_data.append(c.ind)
        if len(E_array) < 2:
            self.ui.data_average.setText('0.00')
            self.ui.data_std.setText('0.00')
            # self.histo_data.setData([0, 0], [0])
            # self.ui.fit_center.setText('0.00')
            # self.ui.fit_std.setText('0.00')
            # self.histo_fit.setData(None)
            # self.histo_esfit.setData(None)
            self.es_average.setData(None)
            self.indentation_fit.setData(None)
            self.indentation_fit_avg.setData(None)
            self.es_averageZoom.setData(None)
            self.es_averageFit.setData(None)
            self.fdistance_fit.setData(None)
            return

        eall = np.array(E_array)
        val = str(int(np.average(eall)/10)/100.0)
        try:
            err = str(int(np.std(eall) / 10) / 100.0)
        except:
            err = 0
        self.ui.data_average.setText(
            '<span>{}&plusmn;{}</span>'.format(val, err))
        self.Yav = str(int(np.average(eall)))
        self.Yav_std = str(int(np.std(eall)))
        bins = 'auto'
        y, x = np.histogram(eall, bins=bins, density=True)
        if len(y) >= 3:
            # self.histo_data.setData(x, y)
            # self.ui.fit_center.setText('0.00')
            # self.ui.fit_std.setText('0.00')
            try:
                x0, w, A, nx, ny = motor.gauss_fit(x, y)
                # self.histo_fit.setData(nx, ny)
                # val = str(int(np.average(x0)/10)/100.0)
                # try:
                #     err = str(int(np.average(w)/10)/100.0)
                # except:
                #     err = 0
                # self.ui.fit_center.setText(
                #     '<span>{}&plusmn;{}</span>'.format(val, err))
                # self.Ygau = str(int(np.average(x0)))
                # self.Ygau_std = str(int(np.average(w)))
                # self.ui.fit_std.setText()
                x, y, z = motor.calc_hertz(x0, self.collection[0].R, self.collection[0].k, float(
                    self.ui.fit_indentation.value()))
                self.indentation_fit.setData(x, y)
                self.indentation_fit_avg.setData(x,y)
                self.fdistance_fit.setData(z, y)
            except:
                self.indentation_fit.setData(None)
                self.fdistance_fit.setData(None)
                self.indentation_fit_avg.setData(None)
                # self.histo_fit.setData(None)
            try:
                x_hertz, y_hertz, er_hertz = motor.getMedCurve(
                    ind_data, F_data, error=True)
                self.hertz_average_error = er_hertz
            except TypeError:
                return
            except ValueError:
                return
            # Setting average hertz data
            if self.ui.analysis.isChecked() is True:
                indmax = float(self.ui.fit_indentation.value())
                self.x_hertz_average = x_hertz
                self.y_hertz_average = y_hertz
                self.hertz_average.setData(x_hertz, y_hertz)
                # jmax_hertz = np.argmin((x_hertz-indmax)**2)
                self.hertz_average.setData(x_hertz, y_hertz)
                self.hertz_average_top.setData(x_hertz, (y_hertz+er_hertz/2))
                self.hertz_average_bottom.setData(
                    x_hertz, (y_hertz-er_hertz/2))
            else:
                self.hertz_average.setData(None)
                self.hertz_average_top.setData(None)
                self.hertz_average_bottom.setData(None)

        # Elasticity Spectra
        if self.ui.es_analysis.isChecked() is True:
            E_data_x = []
            E_data_y = []
            Radius = []
            for c in self.collection:
                if c.active is True and c.E is not None:
                    # Elasticity Spectra
                    Radius.append(c.R)
                    E_data_x.append(c.Ex) #contact radius 
                    E_data_y.append(c.Ey)
            try:
                x, y, er = motor.getMedCurve(E_data_x, E_data_y, error=True)
                self.es_average_error = er*1e9
            except TypeError:
                return
            except ValueError:
                return

            # average E from ES of each curve not accounting ind depth
            # E_no_depth_ES = [np.mean(E_data_y[i]) for i in range(len(E_data_y))]
            # self.E_no_depth_ES = np.array(E_no_depth_ES)*1e9

            x = x**2/np.average(Radius) #ind
            self.es_average.setData(x, y*1e9) # E vs ind
            self.ES_array_x = x
            self.ES_array_y = y*1e9
            indmax = float(self.ui.fit_indentation.value())
            #rmax = np.sqrt(indmax * np.average(Radius))
            jmax = np.argmin((x - indmax)**2)

            # Setting average elasticity spectra data
            self.es_top.setData(x[:jmax], (y[:jmax]+er[:jmax]/2)*1e9)
            self.es_bottom.setData(x[:jmax], (y[:jmax]-er[:jmax]/2)*1e9)
            self.es_averageZoom.setData(x[:jmax], y[:jmax]*1e9)
            all = motor.fitExpSimple(np.sqrt(x[:jmax]*np.average(Radius)), y[:jmax], er[:jmax])
            if all is not None:
                self.es_averageFit.setData(
                    x[:jmax], motor.TheExp(np.sqrt(x[:jmax]*np.average(Radius)), *all[0])*1e9)
                val = str(int((all[0][0]*1e9) / 10) / 100.0)
                try:
                    err = str(int((all[1][0]*1e9) / 10) / 100.0)
                    self.ui.decay_e0.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, err))
                except OverflowError:
                    err = 0
                    self.ui.decay_e0.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, 'XXX'))
                self.E0 = str(int(all[0][0]*1e9))
                self.E0_std = str(int(all[1][0]*1e9))
                val = str(int((all[0][1]*1e9)))
                try:
                    err = str(int((all[1][1]*1e9)))
                    self.ui.decay_eb.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, err))
                except OverflowError:
                    err = 0
                    self.ui.decay_eb.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, 'XXX'))
                self.Eb = str(int(all[0][1]*1e9))
                self.Eb_std = str(int(all[1][1]*1e9))
                val = str(int((all[0][2])))
                try:
                    err = str(int((all[1][2])))
                    self.ui.decay_d0.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, err))
                except OverflowError:
                    self.ui.decay_d0.setText(
                        '<span>{}&plusmn;{}</span>'.format(val, 'XXX'))
                self.d0 = str(int(all[0][2]))
                self.d0_std = str(int(all[1][2]))

            eall = y[:jmax]
            val = str(int(np.average(eall*1e9) / 10) / 100.0)
            err = str(int(np.std(eall*1e9) / 10) / 100.0)
            self.ui.data_std.setText('<span>{}&plusmn;{}</span>'.format(val, err))
            self.ESav = str(int(np.average(eall*1e9)))
            self.ESav_std = str(int(np.std(eall*1e9)))
        else:
            try:
                self.es_top.setData(None)
                self.es_bottom.setData(None)
                self.es_averageZoom.setData(None)
                self.es_averageFit.setData(None)
                self.es_average.setData(None)
                self.ui.data_std.setText('0.00')
                self.ui.decay_e0.setText('0.00')
                self.ui.decay_d0.setText('0.00')
                self.ui.decay_eb.setText('0.00')

            except:
                pass

        # y, x = np.histogram(eall*1e9, bins=bins, density=True)
        # if len(y) >= 3:
        #     self.histo_esdata.setData(x, y)
        #     try:
        #         x0, w, A, nx, ny = motor.gauss_fit(x, y)
        #         # self.histo_esfit.setData(nx, ny)
        #         val = str(int(np.average(x0) / 10) / 100.0)
        #         err = str(int(np.average(w) / 10) / 100.0)
        #         # self.ui.fit_std.setText(
        #         #     '<span>{}&plusmn;{}</span>'.format(val, err))
        #         self.ESgau = str(int(np.average(x0)))
        #         self.ESgau_std = str(int(np.average(w)))
        # except:
        #     self.histo_esfit.setData(None)

    def save_dataHertz(self):
        E_array = []
        # x_pos = []
        for c in self.collection:
            if c.active is True and c.E is not None:
                E_array.append(c.E)
                # x_pos.append(c.xposition)

        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Select the file to export your Hertzian E data', self.workingdir, "Tab Separated Values (*.tsv)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'w') as f:
            f.write(
                '#Hertzian Fit Data exported from Nanoindentation Analysis Software\n')
            f.write('# Repository GitHub Project nanoindentation Branch Master\n')
            f.write('# \n')
            f.write('# Working folder {}\n'.format(self.workingdir))
            f.write('# Tip radius {} nm\n'.format(self.collection[0].R))
            f.write('# Elastic constant {} N/m\n'.format(self.collection[0].k))
            f.write('# Number valid curves {}\n'.format(self.Na))
            f.write('# Max indentation (Hertz Fit) {} nm\n'.format(
                float(self.ui.fit_indentation.value())))
            f.write('# \n')
            f.write(
                '# Young\'s Modulus Hertz, Average {} Pa\n'.format(self.Yav))
            f.write(
                '# Young\'s Modulus Hertz, STD {} Pa\n'.format(self.Yav_std))
            f.write('# \n')
            f.write('# Young\'s Modulus [Pa]\n')
            for x in E_array:
                f.write("{0}\n".format(x))
        f.close()
        f.close()
        QtWidgets.QApplication.restoreOverrideCursor()

    def save_hertz_average(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Select the file to export your average hertz data', self.workingdir, "Tab Separated Values (*.tsv)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'w') as f:
            f.write(
                'Mean Young\'s Modulus Hertz [Pa] # {} \n'.format(self.Yav))
            f.write('Max indentation (Hertz Fit)[nm] # {} \n'.format(
                float(self.ui.fit_indentation.value())))
            f.write('Tip radius [nm] # {} \n'.format(self.collection[0].R))
            f.write(
                'Elastic constant [N/m] #{}\n'.format(self.collection[0].k))
            f.write(
                'Avg Indentation [nm] \t Avg Force [nN] \t Error Force [nN] \n')
            for x in zip(*[self.x_hertz_average, self.y_hertz_average, self.hertz_average_error]):
                f.write("{0}\t{1}\t{2}\n".format(*x))
        f.close()
        QtWidgets.QApplication.restoreOverrideCursor()

    def save_dataES(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Select the file to export your Elasticity Spectra data', self.workingdir, "Tab Separated Values (*.tsv)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'w') as f:
            f.write(
                '# Elasticity Spectra Data exported from Nanoindentation Analysis Software\n')
            f.write('# Repository GitHub Project nanoindentation Branch Master\n')
            f.write('# \n')
            f.write('# Working folder {}\n'.format(self.workingdir))
            f.write('# Tip radius {} nm\n'.format(self.collection[0].R))
            f.write('# Elastic constant {} N/m\n'.format(self.collection[0].k))
            f.write('# Number valid curves {}\n'.format(self.Na))
            f.write('# \n')
            f.write(
                '# Young\'s Modulus ES, Average {} Pa\n'.format(self.ESav))
            f.write('# Young\'s Modulus ES, STD {} Pa\n'.format(
                self.ESav_std))
            f.write('# \n')
            f.write('# E0 from ES fit {} Pa\n'.format(self.E0))
            f.write('# E0 STD {} Pa\n'.format(self.E0_std))
            f.write('# \n')
            f.write('# Eb from ES fit {} Pa\n'.format(self.Eb))
            f.write('# Eb STD {} Pa\n'.format(self.Eb_std))
            f.write('# \n')
            f.write('# d0 from ES fit {} Pa\n'.format(self.d0))
            f.write('# d0 STD {} Pa\n'.format(self.d0_std))
            f.write('# \n')
            f.write(
                '# Mean ES: Indentation [nm] \t Contact Radius [nm] \t Young\'s Modulus [Pa] \t Young\'s Moudlus err [Pa]\n')
            for x in zip_longest(*[self.ES_array_x, np.sqrt(self.ES_array_x * self.collection[0].R), self.ES_array_y, self.es_average_error]):
                f.write("{0}\t{1}\t{2}\t{3}\n".format(*x))
        f.close()
        QtWidgets.QApplication.restoreOverrideCursor()

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
        self.Na = str(Na)
        self.numbers()

    def data_changed(self, item):
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

    def change_selected(self, item):
        for c in self.collection:
            c.selected = False
        try:
            item.nano.selected = True
        except AttributeError:
            pass

    def set_alpha(self, num):
        num = int(num)
        for c in self.collection:
            c.alpha = num

    def fmethod_changed(self):
        if self.collection is None:
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))

        for c in self.collection:
            if self.filterMethod is None:
                c.setFilterFunction(None)
            else:
                c.setFilterFunction(self.filterMethod.calculate)
            c.filter_all()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.count()

    def cpoint_changed(self):
        if self.collection is None:
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))

        if len(self.collection) > 50:
            progress = QtWidgets.QProgressDialog(
                "Computing Contact Point...", "Abort", 0, len(self.collection))

        for i in range(len(self.collection)):
            c = self.collection[i]
            c.setCPFunction(self.contactPoint.calculate)
            c.calculate_contactpoint()
            if len(self.collection) > 50:  # only show progress bar for sets with more than 50 curves
                progress.setValue(progress.value()+1)
                if progress.wasCanceled():
                    return
                if progress.value() % 20 == 0:  # only update progress bar every 20th step
                    QtCore.QCoreApplication.processEvents()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.count()

    def hertz_changed(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        for c in self.collection:
            c.filter_all(False)  # False does not re-compute contact point
        QtWidgets.QApplication.restoreOverrideCursor()
        if self.ui.analysis.isChecked() is False:
            self.hertz_average.setData(None)
            self.hertz_average_top.setData(None)
            self.hertz_average_bottom.setData(None)
        self.count()

    def es_changed(self):
        if self.collection is None:
            return
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))

        if len(self.collection) > 50:
            progress = QtWidgets.QProgressDialog(
                "Computing Elasticity Spectra...", "Abort", 0, len(self.collection))
        for i in range(0, len(self.collection)):
            c = self.collection[i]
            c.filter_all(True)
            if len(self.collection) > 50:  # only show progress bar for sets with more than 50 curves
                progress.setValue(progress.value()+1)
                if progress.wasCanceled():
                    return
                if progress.value() % 20 == 0:  # only update progress bar every 20th step
                    QtCore.QCoreApplication.processEvents()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.count()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Nano2021')
    app.setStyle('Fusion')
    # qtmodern.styles.light(app)
    Chiaro = NanoWindow()
    # mw = qtmodern.windows.ModernWindow(chiaro)
    Chiaro.show()
    sys.exit(app.exec_())
