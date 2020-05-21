import csv
import numpy as np
import math
import matplotlib.pyplot as plt

class indentAll():
    pass
class indentMed():
    pass
class elastoAll():
    pass
class elastoMed():
    pass
class histo():
    pass
class elastoHisto():
    pass
class bar():
    pass

class plots():
    def __init__(self, parent=None):
        self.workingdir = './'
        self.indentAll = indentAll
        self.indentMed = indentMed
        self.elastoAll = elastoAll
        self.elastoMed = elastoMed
        self.histo = histo
        self.elastoHisto = elastoHisto
        self.bar = bar

    def LoadData(self, fnames):
        objects=[self.indentAll, self.indentMed, self.elastoAll, self.elastoMed, self.histo, self.elastoHisto]
        for i, o in enumerate(objects):
            if fnames[i] is not None:
                with open(fnames[i], newline='') as csvfile:
                    reader=csv.reader(csvfile, delimiter=',')
                    labels=[]
                    data=[]
                    for row in reader:
                        label=row[0]
                        row=np.asarray(row[1:])
                        row=row.astype(float)
                        labels.append(label)
                        data.append(row)
                o.labels=labels
                o.data=data

    def LoadData_Conditions(self, fnames):
        self.elastoMed.datas=[]
        for i in range(len(fnames)):
            with open(fnames[i], newline='') as csvfile:
                reader=csv.reader(csvfile, delimiter=',')
                labels=[]
                data=[]
                for row in reader:
                    label=row[0]
                    row=np.asarray(row[1:])
                    row=row.astype(float)
                    labels.append(label)
                    data.append(row)
            self.elastoMed.labels=labels
            self.elastoMed.datas.append(data)

    def LoadData_BarPlots(self, fname):
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            conds=[]
            labels = []
            data = []
            for i, row in enumerate(reader):
                if i==0:
                    self.bar.mags = row[2:]
                else:
                    cond = row[0]
                    label = row[1]
                    row = np.asarray(row[2:])
                    row = row.astype(float)
                    conds.append(cond)
                    labels.append(label)
                    data.append(row)
            self.bar.conds=conds
            self.bar.labels=labels
            self.bar.data=data

    def LoadData_BarPlots_SingleValues(self, fname):
        with open(fname, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            pos=[]
            val=[]
            std=[]
            for i, row in enumerate(reader):
                if i>=2:
                    row = np.asarray(row[1:])
                    row = row.astype(float)
                    if (i-2)%3==0:
                        pos.append(row)
                    if (i-2-1)%3==0:
                        val.append(row)
                    if (i-2-2)%3==0:
                        std.append(row)
            self.bar.scatterx = pos
            self.bar.scattery = val
            self.bar.scatterstd = std

    def InitiateFigure(self, figstr, figsize):
        fig, axs = plt.subplots(figstr[0], figstr[1], figsize=figsize)
        self.figure=fig
        self.axes=axs
        self.lenax_x = figstr[0]
        self.lenax_y = figstr[1]

    def FindPosition(self, pos):
        if self.lenax_x==1:
            ax = self.axes[int(pos)]
        else:
            pos1=int(math.floor(pos/self.lenax_y))
            pos2=int(pos-pos1*self.lenax_y)
            ax = self.axes[pos1][pos2]
        return ax

    def AdjustAxis_ylim(self, ax, x, y):
        lims = ax.get_xlim()
        i = np.where((x > lims[0]) & (x < lims[1]))[0]
        ax.set_ylim(y[i].min(), y[i].max()*1.1)

    def ForceCurves(self, pos=1, ax_lim=None):
        ax=self.FindPosition(pos)
        Forces=self.indentAll.data[2:]
        HertzFit=self.indentMed.data[0:2]
        maxForceAtXlim = 0
        for i in range(0, len(Forces), 2):
            ax.plot(Forces[i], Forces[i+1], color='black', linewidth=0.1)
            if ax_lim is not None and len(Forces[i+1])>ax_lim[0]:
                if Forces[i+1][ax_lim[0]]>maxForceAtXlim:
                    maxForceAtXlim = Forces[i+1][ax_lim[0]]
                    indMaxCurve = i
        ax.plot(HertzFit[0], HertzFit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('F (nN)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
            else:
                self.AdjustAxis_ylim(ax, Forces[indMaxCurve], Forces[indMaxCurve+1])

    def ForceCurvesWithAverage(self, pos=1, ax_lim=None):
        ax=self.FindPosition(pos)
        Forces=self.indentAll.data[2:]
        MedCurve=self.indentMed.data[0:2]
        MedErr = self.indentMed.data[3:5]
        Fit= self.indentMed.data[5:7]
        maxForceAtXlim = 0
        for i in range(0, len(Forces), 2):
            ax.plot(Forces[i], Forces[i+1], color='black', linewidth=0.1)
            if ax_lim is not None and len(Forces[i+1])>ax_lim[0]:
                if Forces[i+1][ax_lim[0]]>maxForceAtXlim:
                    maxForceAtXlim = Forces[i+1][ax_lim[0]]
                    indMaxCurve = i
        ax.plot(MedCurve[0], MedCurve[1], color='blue', linewidth=1)
        ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color='red', alpha=0.5)
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('F (nN)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
            else:
                self.AdjustAxis_ylim(ax, Forces[indMaxCurve], Forces[indMaxCurve+1])

    def ElastoAll(self, mode=None, pos=2, ax_lim=None):
        ax=self.FindPosition(pos)
        AllData=self.elastoAll.data
        MedCurve=self.elastoMed.data[0:2]
        MedErr = self.elastoMed.data[3:5]
        Fit= self.elastoMed.data[5:]
        for i in range(0, len(AllData), 2):
            ax.plot(AllData[i], AllData[i+1], color='black', linewidth=0.1, alpha=0.25)
        ax.plot(MedCurve[0], MedCurve[1], color='blue', linewidth=1)
        ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color='red', alpha=0.5)
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])

    def ElastoMed_Conditions(self, mode=None, pos=1):
        ax=self.FindPosition(pos)
        colors=['blue', 'red', 'black', 'lime', 'yellow', 'cyan', 'magenta']
        for i in range(len(self.elastoMed.datas)):
            MedCurve=self.elastoMed.datas[i][0:2]
            MedErr = self.elastoMed.datas[i][3:5]
            Fit= self.elastoMed.datas[i][5:]
            ax.plot(MedCurve[0], MedCurve[1], color=colors[i], linewidth=1)
            # ax.fill_between(MedCurve[0], MedErr[0], MedErr[1], color=colors[i], alpha=0.1)
            # ax.plot(Fit[0], Fit[1], color=colors[i], linewidth=2)
            # if mode=='bilayer':
            #     ax.plot(Fit[2], Fit[3], color=colors[i], linewidth=2)
        ax.set_xlim(0,1000)
        ax.set_ylim(0, 12000)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')

    def ElastoNoAverage(self, mode=None, pos=2, ax_lim=None):
        ax=self.FindPosition(pos)
        AllData=self.elastoAll.data
        print(AllData[1])
        Fit= self.elastoMed.data[5:]
        for i in range(0, len(AllData), 2):
            ax.plot(AllData[i], AllData[i+1], color='black', linewidth=0.1, alpha=0.25)
            print(i,AllData[i],AllData[i+1])
        ax.plot(Fit[0], Fit[1], color='lime', linewidth=2)
        ax.set_xlabel('\u03B4 (nm)')
        ax.set_ylabel('E (Pa)')
        if ax_lim is not None:
            ax.set_xlim(0,ax_lim[0])
            if len(ax_lim)>1:
                ax.set_ylim(ax_lim[1], ax_lim[2])
        from matplotlib.ticker import ScalarFormatter
        ax.get_yaxis().get_major_formatter().set_useOffset(False)

    def Histo(self, mode=None, pos=3):
        ax=self.FindPosition(pos)
        FromHertz=self.histo.data[:7]
        FromElasto=self.histo.data[7:]
        ax.hist(FromHertz[2], bins='auto', density=True, color='lime', alpha=0.5)
        ax.plot(FromHertz[5], FromHertz[6], color='lime')
        if mode=='single':
            #ax = ax.twinx()
            ax.hist(FromElasto[2], bins='auto', density=True, color='red', alpha=0.5)
            ax.plot(FromElasto[5], FromElasto[6], color='red')
        ax.set_xlabel('E (Pa)')
        ax.set_ylabel('frequency')

    def BarPlotsInsteadOfHisto(self, pos=3):
        ax = self.FindPosition(pos)
        FromHertz=self.indentMed.data[7:9]
        FromElasto=self.elastoMed.data[7:9]
        print(FromHertz)
        print([FromHertz[0], FromElasto[0]])
        ax.bar(x=[0,1], height=[FromHertz[0][0], FromElasto[0][0]], tick_label=['Hertz', 'Elasto'], yerr=[FromHertz[1][0], FromElasto[1][0]], color=['lime', 'red'], alpha=0.5)

    def BarPlots(self,pos):
        num_conds=int(len(self.bar.conds)/3)
        for i in range(len(self.bar.mags)):
            ax = self.FindPosition(pos+i)
            conds=[]
            means=[]
            stds=[]
            sigs=[]
            colors=[]
            for n in range(0, num_conds*3, 3):
                conds.append(self.bar.conds[n])
                means.append(self.bar.data[n][i])
                stds.append(self.bar.data[n+1][i])
                sigs.append(self.bar.data[n+2][i])
                if self.bar.data[n + 2][i]==0:
                    colors.append('blue')
                else:
                    colors.append('red')
            ax.bar(range(num_conds), means, tick_label=conds, yerr=stds, color=colors)
            ax.set_title(self.bar.mags[i])
            ax.set_xticklabels(labels= conds, rotation=45)
            if i<3:
                ax.set_ylabel('E (Pa)')
            else:
                ax.set_ylabel('d (nm)')
        plt.tight_layout()

    def BarPlots_WithSingleMeasurements(self,pos):
        num_conds=int(len(self.bar.conds)/3)
        for i in range(len(self.bar.mags)):
            ax = self.FindPosition(pos+i)
            conds=[]
            means=[]
            stds=[]
            sigs=[]
            colors=[]
            for n in range(0, num_conds*3, 3):
                conds.append(self.bar.conds[n])
                means.append(self.bar.data[n][i])
                stds.append(self.bar.data[n+1][i])
                sigs.append(self.bar.data[n+2][i])
                if self.bar.data[n + 2][i]==0:
                    colors.append('blue')
                else:
                    colors.append('red')
            ax.bar(range(num_conds), means, tick_label=conds, yerr=stds, color=colors)
            ax.plot(self.bar.scatterx[i], self.bar.scattery[i], 'o', color='black')
            ax.set_title(self.bar.mags[i])
            ax.set_xticklabels(labels= conds, rotation=45)
            if i<3:
                ax.set_ylabel('E (Pa)')
            else:
                ax.set_ylabel('d (nm)')
        plt.tight_layout()

    def ElastoHisto(self, pos=0):
        E0_data=self.elastoHisto.data[:7]
        Eb_data=self.elastoHisto.data[7:14]
        d0_data = self.elastoHisto.data[14:]
        data=[E0_data, Eb_data, d0_data]
        for i in range(3):
            dat=data[i]
            ax = self.FindPosition(pos+i)
            ax.hist(dat[2], bins='auto', density=True, color='lime', alpha=0.5)
            ax.plot(dat[5], dat[6], color='lime')
            if i<3:
                ax.set_xlabel('E (Pa)')
            else:
                ax.set_xlabel('d (nm)')
            ax.set_ylabel('frequency')

    def gauss(x, y):
        def gaussDist(x, x0, w, A):
            return A * np.exp(-((x - x0) / w) ** 2)

        if len(x) == len(y) + 1:
            x = (x[1:] + x[:-1]) / 2.0
        popt, pcov = curve_fit(gaussDist, x, y, p0=[x[np.argmax(y)], (np.max(x) - np.min(x)) / 10.0, np.max(y)],
                               maxfev=100000)
        nx = np.linspace(np.min(x), np.max(x), 100)
        return popt[0], popt[1], popt[2], nx, gaussDist(nx, *popt)

    def SaveFigSvg(self, fname):
        plt.savefig(fname+'.svg')

    def SaveFigPng(self, fname):
        plt.savefig(fname+'.png')



########################## OLD ##################
class NanoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = view.Ui_MainWindow()
        self.ui.setupUi(self)

        self.workingdir = './'
        self.collection = []

        # connect load and open, other connections after load/open

        self.ui.open_load.clicked.connect(self.load_pickle)
        self.ui.open_selectfolder.clicked.connect(self.open_folder)

        QtCore.QMetaObject.connectSlotsByName(self)

    ################################################
    ############## OPEN / LOAD #####################
    ################################################

    def load_pickle(self):

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select the file to load your processing', self.workingdir,
                                                      "Python object serialization (*.pickle)")
        if fname[0] == '':
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'rb') as f:
            data = pickle.load(f)
        QtWidgets.QApplication.restoreOverrideCursor()

        if data[0].phase == 2:
            self.b2['exp'] = data
            self.b2Init()
        elif data[0].phase == 3:
            self.b3['exp'] = data
            self.b3Init()
        elif data[0].phase == 4:
            self.b4['exp'] = data
            self.b4Init()
        self.ui.switcher.setCurrentIndex(data[0].phase - 1)

    def save_pickle(self):
        phase = self.ui.switcher.currentIndex() + 1
        if phase == 2:
            data = self.b2['exp'].copy()
        elif phase == 3:
            data = self.b3['exp'].copy()
        elif phase == 4:
            data = self.b4['exp'].copy()
        for s in data:
            s.plit = None
            s.elit = None

        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Select the file to save your processing', self.workingdir,
                                                      "Python object serialization (*.pickle)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'wb') as f:
            pickle.dump(data, f)
        QtWidgets.QApplication.restoreOverrideCursor()

        # if phase == 2:
        #    self.b2Init()
        # elif phase == 3:
        #    self.b3Init()

    def open_folder(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select the root dir', './')
        if fname == '' or fname is None or fname[0] == '':
            return
        self.workingdir = fname
        if self.ui.open_o11new.isChecked() is True:
            self.b1['exp'] = experiment.Chiaro(fname)
        elif self.ui.open_o11old.isChecked() is True:
            self.b1['exp'] = experiment.ChiaroGenova(fname)
        elif self.ui.open_nanosurf.isChecked() is True:
            self.b1['exp'] = experiment.NanoSurf(fname)

        self.b1['exp'].browse()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, len(self.b1['exp'].haystack))

        self.ui.b1_mainList.clear()

        def attach(node, parent):
            myself = QtWidgets.QTreeWidgetItem(parent)
            node.myTree = myself
            myself.setText(0, node.basename)
            myself.curve = node
            myself.setFlags(myself.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            myself.setCheckState(0, QtCore.Qt.Unchecked)
            for mychild in node:
                attach(mychild, myself)

        for node in self.b1['exp']:
            attach(node, self.ui.b1_mainList)

        for c in self.b1['exp'].haystack:
            c.open()
            progress.setValue(progress.value() + 1)
            QtCore.QCoreApplication.processEvents()
        self.ui.b1_forwardSegment.setMaximum(len(self.b1['exp'].haystack[0]) - 1)
        self.ui.b1_forwardSegment.setValue(1)
        progress.setValue(len(self.b1['exp'].haystack))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.b1Forward()
        self.ui.b1_mainList.itemChanged.connect(self.b1Color)
        self.ui.b1_mainList.itemClicked.connect(self.b1Color)
        self.ui.b1_mainList.itemSelectionChanged.connect(self.b1Color)
        self.ui.b1_yAlignButton.clicked.connect(self.b1yAlign)
        self.ui.b1_forwardSegment.valueChanged.connect(self.b1Forward)
        self.ui.b1_red.clicked.connect(self.b1Color)
        self.ui.b1_black.clicked.connect(self.b1Color)
        self.ui.b1_redblack.clicked.connect(self.b1Color)
        self.ui.b1_Alpha.valueChanged.connect(self.b1Color)
        self.ui.b1tob2.clicked.connect(self.b1tob2)
        self.ui.b1_end.valueChanged.connect(self.b1xCut)
        self.ui.b1_start.valueChanged.connect(self.b1xCut)
        self.ui.b1_doInvalidate.clicked.connect(self.b1_invalid)

    ################################################
    ################# Actions ######################
    ################################################

    def curve_clicked(self, curve):
        for c in self.collection:
            c.nano.selected = False
        curve.nano.selected = True

    ################################################
    ############## b3 actions ######################
    ################################################

    def b3Init(self):

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        iMa = []
        fMa = []

        self.ui.b3_plotind.plotItem.clear()
        for s in self.b3['exp']:
            s.phase = 3

            iMa.append(engine.np.max(s.indentation))
            fMa.append(engine.np.max(s.touch))

            plit = pg.PlotCurveItem(clickable=False)
            self.ui.b3_plotind.plotItem.addItem(plit)
            plit.setData(s.indentation, s.touch)
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            # plit.sigClicked.connect(self.b2curveClicked)

        self.b3['fit'] = pg.PlotCurveItem(clickable=False)
        self.b3['fit'].setPen(self.greenPen)
        self.ui.b3_plotind.plotItem.addItem(self.b3['fit'])

        self.b3['indMax'] = engine.np.max(iMa)
        self.b3['forMax'] = engine.np.max(fMa)
        self.b3updMax()

        self.ui.b3_plotscatter.clear()
        self.ui.b3_plothist.clear()
        # prepare plots for histo data - standard
        self.b3['plit1'] = pg.PlotDataItem(pen=None, symbolBrush=pg.mkBrush('b'), symbol='o')
        self.ui.b3_plotscatter.addItem(self.b3['plit1'])
        self.b3['plit2a'] = pg.PlotDataItem(stepMode=True, pen=pg.mkPen('b'))
        self.b3['plit2b'] = pg.PlotDataItem(pen=pg.mkPen((0, 0, 255, 100), width=4))
        self.ui.b3_plothist.addItem(self.b3['plit2a'])
        self.ui.b3_plothist.addItem(self.b3['plit2b'])
        # prepare plots for histo data - elastography
        self.b3['pela1'] = pg.PlotDataItem(pen=None, symbolBrush=pg.mkBrush('r'), symbol='o')
        self.ui.b3_plotscatter.addItem(self.b3['pela1'])
        self.b3['pela2a'] = pg.PlotDataItem(stepMode=True, pen=pg.mkPen('r'))
        self.b3['pela2b'] = pg.PlotDataItem(pen=pg.mkPen((255, 0, 0, 100), width=4))
        self.ui.b3_plothist.addItem(self.b3['pela2a'])
        self.ui.b3_plothist.addItem(self.b3['pela2b'])

        QtWidgets.QApplication.restoreOverrideCursor()

        self.ui.b3_Alpha.valueChanged.connect(self.b3Color)
        self.ui.b3_ShiftCurves.clicked.connect(self.b3_ShiftAllCurves)
        self.ui.b3_doCutFit.clicked.connect(self.b3Fit)
        self.ui.b3_maxIndentation.clicked.connect(self.b3updMax)
        self.ui.b3_maxForce.clicked.connect(self.b3updMax)
        self.ui.b3_save.clicked.connect(self.save_pickle)
        self.ui.b3_doExport.clicked.connect(self.b3Export)
        self.ui.b3_doExport2.clicked.connect(lambda: self.b3Export2(fit=False))
        self.ui.b3_doExport2fit.clicked.connect(lambda: self.b3Export2(fit=True))
        self.ui.b4_doElas.clicked.connect(self.b3_Alistography)
        self.ui.b3_CreateCpShiftArray.clicked.connect(self.b3_CreateCpShiftArray)

    def b3_Alistography(self, fit=True):
        self.ui.b3_long.plotItem.clear()
        self.ui.b3_plotRed.plotItem.clear()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        progress = QtWidgets.QProgressDialog("Performing elastography ...", "Cancel E-analysis", 0, len(self.b4['exp']))
        grainstep = int(self.ui.b4_elIncrement.value())
        scaledistance = float(self.ui.b4_elDash.value())
        maxind = float(self.ui.b4_elMaxind.value())

        cdown = 10
        xx = []
        yy = []
        Rs = []

        # E0h=[]
        # Ebh=[]
        # d0h=[]

        # self.d01=[]
        # self.std_d01=[]
        # self.d02=[]
        # self.std_d02=[]
        # self.d03=[]
        # self.std_d03=[]
        # self.d04=[]
        # self.std_d04=[]

        # print('singles>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        for s in self.b3['exp']:
            Ex, Ey = engine.Elastography2withMax(s, grainstep, scaledistance, maxind)
            if Ex is None:
                continue
            s.ElastX = Ex
            s.ElastY = Ey

            # getall = engine.fitExpSimple(Ex,Ey)
            # if getall is None:
            #    continue
            # pars1, covs1, pars2, covs2, pars3, covs3, pars4, covs4, i_dhalf, i_cut = getall
            # if pars1 is not None:
            #    E0h.append(pars2[0]*1e9)
            #    Ebh.append(pars3[1]*1e9)
            #    d0h.append(pars2[2])
            # self.d01.append(pars1[2])
            # self.std_d01.append(engine.np.sqrt(covs1[2]))
            # self.d02.append(pars2[2])
            # self.std_d02.append(engine.np.sqrt(covs2[2]))
            # self.d03.append(pars3[2])
            # self.std_d03.append(engine.np.sqrt(covs3[2]))
            # self.d04.append(pars4[2])
            # self.std_d04.append(engine.np.sqrt(covs4[2]))

            xx.append(Ex)
            yy.append(Ey)
            elit = pg.PlotCurveItem(Ex, Ey * 1e9, pen=self.blackPen)
            self.ui.b3_long.plotItem.addItem(elit)
            progress.setValue(progress.value() + 1)
            cdown -= 1
            if cdown == 0:
                QtCore.QCoreApplication.processEvents()
                cdown = 10
            Rs.append(s.R)
        self.R = engine.np.mean(Rs)
        xmed, ymed, yerr = engine.getMedCurve(xx, yy, loose=True, error=True)
        # points = pg.PlotDataItem(xmed,ymed*1e9,pen=None,symbol='o')
        # points1 = pg.PlotCurveItem(xmed,ymed*1e9,pen=pg.mkPen( pg.QtGui.QColor(0, 0, 255,200),width=2))
        # self.ui.b3_long.plotItem.addItem( points1 )

        points = pg.PlotCurveItem(xmed, ymed * 1e9, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 255, 200), width=2))
        y_uperror = ymed + yerr
        y_downerror = ymed - yerr
        yup_curve = pg.PlotCurveItem(xmed, y_uperror * 1e9, pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        ydown_curve = pg.PlotCurveItem(xmed, y_downerror * 1e9, pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        errorzone = pg.FillBetweenItem(ydown_curve, yup_curve, brush='r')
        self.ui.b3_plotRed.plotItem.addItem(points)
        self.ui.b3_plotRed.plotItem.addItem(errorzone)

        if any(engine.np.isnan(xmed)) == False and any(engine.np.isnan(ymed)) == False:
            self.xmed = xmed
            self.ymed = ymed

        if self.ui.b3_sinfit.isChecked() is True:
            med = engine.np.average(ymed)
            ymedline = engine.np.ones(len(xmed)) * med * 1e9
            medline = pg.PlotCurveItem(xmed, ymedline, pen=pg.mkPen('g', width=2, style=QtCore.Qt.DashLine))
            self.ui.b3_plotRed.plotItem.addItem(medline)
            self.ui.b3_labE0.setText(
                '<html><head/><body><p><span style=" font-weight:600;">{}</span> kPa</p></body></html>'.format(
                    int(med * 1e8) / 100.0))

            # self.b3['pela1'].setData(engine.np.arange(len(ymed)),ymed*1e9)
            bins = int(self.ui.b3_bins.value())
            if bins == 0:
                bins = 'auto'
            y, x = engine.np.histogram(ymed * 1e9, bins=bins, density=True)
            if len(y) >= 3:
                self.b3['pela2a'].setData(x, y)
                try:
                    e0, w, A, nx, ny = engine.gauss(x, y)
                    self.b3['pela2b'].setData(nx, ny)
                    w = w / engine.np.sqrt(len(ymed * 1e9))
                except:
                    e0 = 0
                    w = 0
            else:
                e0 = s.E
                w = 0

        else:
            # print('bilayer>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            getall = engine.fitExpSimple(xmed, ymed, R=self.R, sigma=yerr)

            if getall is not None:
                pars1, covs1 = getall
                # pars1, covs1, pars2, covs2, pars3, covs3, pars4, covs4, i_dhalf, i_cut = getall
                # print(i_dhalf)
                # print(pars1[2], pars2[2], pars3[2], pars4[2])
                if pars1 is not None:
                    yfit0 = engine.ExpDecay(xmed, *pars1, self.R)
                    # yfit1 = engine.ExpDecay(xmed[:i_dhalf],*pars2, self.R)
                    # yfit2 = engine.ExpDecay(xmed[i_dhalf:], *pars3, self.R)
                    # yfit3 = engine.ExpDecay(xmed[:i_cut], *pars4, self.R)
                    self.ui.b3_plotRed.addItem(pg.PlotCurveItem(xmed, yfit0 * 1e9, pen=self.greenPen))
                    # self.ui.b3_plotRed.addItem( pg.PlotCurveItem(xmed[:i_dhalf:],yfit1 * 1e9,pen=self.greenPen) )
                    # self.ui.b3_plotRed.addItem(pg.PlotCurveItem(xmed[i_dhalf:], yfit2 * 1e9, pen=self.greenPen))
                    # self.ui.b3_plotRed.addItem(pg.PlotCurveItem(xmed[:i_cut], yfit3 * 1e9,pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=3)))
                    self.ui.b3_labE0.setText(
                        '<html><head/><body><p><span style=" font-weight:600;">{}</span> kPa</p></body></html>'.format(
                            int(pars1[0] * 1e8) / 100.0))
                    self.ui.b3_labEb.setText(
                        '<html><head/><body><p><span style=" font-weight:600;">{}</span> kPa</p></body></html>'.format(
                            int(pars1[1] * 1e8) / 100.0))
                    self.ui.b3_labd0.setText(
                        '<html><head/><body><p><span style=" font-weight:600;">{}</span> nm</p></body></html>'.format(
                            int(pars1[2])))

        QtWidgets.QApplication.restoreOverrideCursor()

        if self.ui.b3_sinfit.isChecked() is True:
            return xmed, ymed * 1e9, ymedline
        else:
            return xmed, ymed * 1e9, pars1, covs1  # , pars2, covs2, pars3, covs3

    def b3Export(self):
        Earray = self.b3Fit()
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Select the file to export your E data', self.workingdir,
                                                      "Data table (*.np.txt)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        engine.np.savetxt(fname[0], Earray)
        QtWidgets.QApplication.restoreOverrideCursor()

    def b3Export2(self, fit=False):
        # fit = False
        data = self.b3_Alistography(fit)
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Select the file to export your E data', self.workingdir,
                                                      "Tab Separated Values (*.tsv)")
        if fname[0] == '':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        with open(fname[0], 'w') as f:
            if fit is True:
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 1 params E0, Eb, d0", data[2][0], data[2][1], data[2][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 1 std dev E0, Eb, d0", data[3][0], data[3][1], data[3][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 2 params E0, Eb, d0", data[4][0], data[4][1], data[4][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 2 std dev E0, Eb, d0", data[5][0], data[5][1], data[5][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 3 params E0, Eb, d0", data[6][0], data[6][1], data[6][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 3 std dev E0, Eb, d0", data[7][0], data[7][1], data[7][2]))
                f.write('Ex\tEy\n')
            else:
                f.write('E0\tEb\td0\n')
            for i in range(len(data[0])):
                if fit is True:
                    f.write('{}\t{}\n'.format(data[0][i], data[1][i]))
                else:
                    f.write('{}\t{}\t{}\n'.format(data[0][i], data[1][i], data[2][i]))
            f.close()
        QtWidgets.QApplication.restoreOverrideCursor()

    def b3updMax(self):
        if self.ui.b3_maxIndentation.isChecked() is True:
            self.ui.b3_threshold.setMaximum(self.b3['indMax'])
        else:
            self.ui.b3_threshold.setMaximum(self.b3['forMax'])

    def b3tob4(self):
        self.b4['exp'] = self.b3['exp']
        self.ui.switcher.setCurrentIndex(3)
        self.b4Init()

    def b3_ShiftAllCurves(self, shift=None):
        if shift == False:
            shift = int(self.ui.b3_ShiftValue.value())
        self.shift = shift
        # changed the way this works!!!
        for s in self.b3['exp']:
            # s.offsetX=s.offsetX_original
            # s.offsetY=s.offsetY_original
            s.offsetX = s.offsetX + shift
            ind = engine.np.argmin(engine.np.abs(s.z - s.offsetX))
            s.offsetY = s.ffil[ind]
            s.indentation, s.touch = engine.calculateIndentation(s)
        self.b3Update()
        self.b3Fit()
        self.b3_Alistography()

    def b3_CreateCpShiftArray(self):
        min_shift = int(self.ui.b3_ShiftArrayMin.value())
        max_shift = int(self.ui.b3_ShiftArrayMax.value())
        step_shift = int(self.ui.b3_ShiftArrayStep.value())
        file = str(self.ui.b3_ShiftArrayFile.text())
        shifts = range(min_shift, max_shift + step_shift, step_shift)
        Eys_norm = []
        len_Ey_norm = []
        folder = str(os.path.dirname(os.path.abspath(__file__)))
        fname = folder + '\ArrayData' + '\ArrayData_' + file + '.csv'
        header = ['shift', 'E0', 'Eb', 'd0', 'Ex', 'Ey']
        with open(fname, 'w', newline='') as myfile:
            wr = csv.writer(myfile, delimiter=',')
            wr.writerow(header)
            for shift in shifts:
                self.b3_ShiftAllCurves(shift)
                tosave_i = [shift, self.E0h, self.Ebh, self.d0h, list(self.xmed), list(self.ymed)]
                wr.writerow(tosave_i)
                start_norm = int(float(self.ui.b4_elDash.value()) / int(self.ui.b4_elIncrement.value())) - 1
                ymed_min = min(self.ymed[start_norm:])
                ymed_max = max(self.ymed[start_norm:])
                ymed_norm = []
                ymed_norm_means = []
                for y in self.ymed[start_norm:]:
                    ymed_norm_i = float((y - ymed_min) / (ymed_max - ymed_min))
                    for i in range(10):
                        ymed_norm.append(ymed_norm_i)
                if len(ymed_norm) > 1000:
                    for i in range(0, len(ymed_norm) - 1, 200):
                        ymed_norm_i = engine.np.mean(ymed_norm[i:i + 1])
                        ymed_norm_means.append(ymed_norm_i)
                    ymed_norm = ymed_norm_means
                # ymed_norm=[(y-ymed_min)/(ymed_max-ymed_min) for y in self.ymed]
                for i in range(10):
                    Eys_norm.append(ymed_norm)  # engine.np.asarray(ymed_norm))
                    len_Ey_norm.append(len(ymed_norm))
        min_len = min(len_Ey_norm)
        for i, x in enumerate(Eys_norm):
            Eys_norm[i] = Eys_norm[i][:min_len]
        imname = folder + '\ArrayData' + '\ArrayData_' + file + '.png'
        plt.imsave(imname, engine.np.asarray(Eys_norm), cmap=cm.jet)
        self.ui.b3_ShiftArrayImage.setPixmap(QtGui.QPixmap(imname))

    def b3Fit(self):
        if self.ui.b3_maxIndentation.isChecked():
            for s in self.b3['exp']:
                if s.plit is not None:
                    if engine.np.max(s.indentation) < float(self.ui.b3_threshold.value()):
                        s.valid = False
                        s.plit.setPen(self.redPen)
                    else:
                        s.valid = True
                        s.indMax = engine.np.argmin((s.indentation - float(self.ui.b3_threshold.value())) ** 2)
                        s.plit.setPen(self.blackPen)
        else:
            for s in self.b3['exp']:
                if engine.np.max(s.touch) < float(self.ui.b3_threshold.value()):
                    s.valid = False
                    s.plit.setPen(self.redPen)
                else:
                    s.valid = True
                    s.plit.setPen(self.blackPen)
                    s.indMax = engine.np.argmin((s.touch - float(self.ui.b3_threshold.value())) ** 2)

        Earray = []
        for s in self.b3['exp']:
            if s.valid is True:
                s.E, std = engine.fitHertz(s)

                if s.E is not None:
                    Earray.append(s.E * 1e9)

        self.b3['plit1'].setData(engine.np.arange(len(Earray)), Earray)
        bins = int(self.ui.b3_bins.value())
        if bins == 0:
            bins = 'auto'
        y, x = engine.np.histogram(Earray, bins=bins, density=True)
        if len(y) >= 3:
            self.b3['plit2a'].setData(x, y)
            try:
                e0, w, A, nx, ny = engine.gauss(x, y)
                self.b3['plit2b'].setData(nx, ny)
                w = w / engine.np.sqrt(len(Earray))
            except:
                e0 = 0
                w = 0
        else:
            e0 = s.E
            w = 0
        self.ui.b3_results.setText(
            '<html><head/><body><p><span style=" font-weight:600;">{}&plusmn;{}</span> kPa</p></body></html>'.format(
                int(e0 / 10) / 100.0, int(w / 10) / 100.0))

        R = self.b3['exp'][0].R
        E = engine.np.average(Earray) / 1e9
        x, y = engine.getHertz(E, R, float(self.ui.b3_threshold.value()), self.ui.b3_maxIndentation.isChecked())
        self.b3['fit'].setData(x, y)

        self.ui.b3_Eavg.setText(
            '<html><head/><body><p><span style=" font-weight:600;">{}</span> Pa</p></body></html>'.format(
                int(engine.np.average(Earray))))
        self.ui.b3_Estd.setText(
            '<html><head/><body><p><span style=" font-weight:600;">{}</span> Pa</p></body></html>'.format(
                int(engine.np.std(Earray))))

        if any(engine.np.isnan(Earray)) == False:
            self.Earray = Earray
        return Earray

    def b3Color(self):
        alpha = int(self.ui.b3_Alpha.value())
        self.blackPen = pg.mkPen(pg.QtGui.QColor(0, 0, 0, alpha), width=1)
        self.redPen = pg.mkPen(pg.QtGui.QColor(255, 0, 0, alpha), width=1)
        for s in self.b3['exp']:
            if s.valid is True:
                s.plit.setPen(self.blackPen)
            else:
                s.plit.setPen(self.redPen)

    def b3Update(self):
        iMa = []
        fMa = []

        self.ui.b3_plotind.plotItem.clear()
        for s in self.b3['exp']:
            s.phase = 3

            iMa.append(engine.np.max(s.indentation))
            fMa.append(engine.np.max(s.touch))

            plit = pg.PlotCurveItem(clickable=False)
            self.ui.b3_plotind.plotItem.addItem(plit)
            plit.setData(s.indentation, s.touch)
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            # plit.sigClicked.connect(self.b2curveClicked)

        self.b3['fit'] = pg.PlotCurveItem(clickable=False)
        self.b3['fit'].setPen(self.greenPen)
        self.ui.b3_plotind.plotItem.addItem(self.b3['fit'])

        self.b3['indMax'] = engine.np.max(iMa)
        self.b3['forMax'] = engine.np.max(fMa)
        self.b3updMax()

    ################################################
    ############## b2 actions ######################
    ################################################

    def b2Init(self):
        self.ui.b2_segment.setMaximum(len(self.b2['exp']) - 1)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.ui.b2_plot_all.plotItem.clear()
        for s in self.b2['exp']:
            s.phase = 2
            plit = pg.PlotCurveItem(clickable=True)
            self.ui.b2_plot_all.plotItem.addItem(plit)
            s.z_original = s.z
            s.f_original = s.f
            plit.setData(s.z, s.f)
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            plit.sigClicked.connect(self.b2curveClicked)
            s.bol_deriv = None
            s.invalid = False
            s.bol = True
            s.ElastX = None
            s.x_CPderiv = engine.np.array([0])
            s.y_CPderiv = engine.np.array([0])
            s.threshold_exp = 0
            s.quot = None
        self.b2_view()
        self.ui.b2_Alpha.setValue(self.ui.b1_Alpha.value())

        self.ui.b2_plot_one.plotItem.clear()
        self.ui.b2_plot_two.plotItem.clear()
        s = self.b2['exp'][0]

        self.b2['plit1a'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit1a'].setData(s.z, s.f, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
        self.b2['plit1b'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit1b'].setData(s.z, s.f, pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=1))
        self.b2['plit1c'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit1c'].setData([0, 0], [min(s.f), max(s.f)], pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        self.b2['plit2'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit2'].setData(s.z, s.f, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
        self.b2['plit2a'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit2a'].setData([0, 0], [0, 1], pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        self.b2['plit2b'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit2b'].setData([0, 0], [0, 1], pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        self.b2['plit2c'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit2c'].setData([0, 0], [0, 1], pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        self.b2['plit3'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit3'].setData(s.z, s.f, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=2))
        self.b2['plit3b'] = pg.PlotCurveItem()
        self.b2['plit3b'].setData(s.z, s.f, pen=pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=1))

        self.ui.b2_plot_one.plotItem.addItem(self.b2['plit1a'])
        self.ui.b2_plot_one.plotItem.addItem(self.b2['plit1b'])
        self.ui.b2_plot_one.plotItem.addItem(self.b2['plit1c'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2a'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2b'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2c'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2c'])
        self.ui.b2_plot_three.plotItem.addItem(self.b2['plit3'])
        self.ui.b2_plot_three.plotItem.addItem(self.b2['plit3b'])

        QtWidgets.QApplication.restoreOverrideCursor()
        self.ui.b2_Alpha.valueChanged.connect(self.b2Color)
        self.ui.b2_segment.valueChanged.connect(self.b2chSegment)
        self.ui.b2_doFilter.clicked.connect(self.b2Filter)
        self.ui.b2_vFiltered.clicked.connect(self.b2_view)
        self.ui.b2_vOriginal.clicked.connect(self.b2_view)
        self.ui.b2_CropCurves.clicked.connect(self.b2_crop)
        self.ui.b2_doContactPoint.clicked.connect(self.b2_contactPoint)
        self.ui.b2_delete.clicked.connect(self.b2Delete)
        self.ui.b2_deleteAllInvalid.clicked.connect(self.b2DeleteAllInvalid)
        self.ui.b2_b2tob3.clicked.connect(self.b2tob3)
        self.ui.b2_save.clicked.connect(self.save_pickle)
        self.ui.b2_DoElasto.clicked.connect(self.b2_Alistography)

    def b2tob3(self):
        self.b3['exp'] = []
        for s in self.b2['exp']:
            if s.invalid is False:
                self.b3['exp'].append(s)
        for s in self.b3['exp']:
            s.indentation, s.touch = engine.calculateIndentation(s)
            s.offsetX_original = s.offsetX
            # s.indentation_original=s.indentation
            # s.touch_original=s.touch
        self.ui.switcher.setCurrentIndex(2)
        self.b3Init()

    def b2_Alistography(self, fit=False):
        self.ui.b2_plot_elasto.plotItem.clear()

        a = panels.b2_Elasto()
        if a.exec() == 0:
            return
        grainstep, scaledistance, maxind, filwin, thresh_osc = a.getParams()

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # progress = QtWidgets.QProgressDialog("Performing elastography ...", "Cancel E-analysis", 0, len(self.b4['exp']))

        cdown = 10
        xx = []
        yy = []

        E0h = []
        Ebh = []
        d0h = []

        for s in self.b2['exp']:
            if s.invalid is False:
                s.indentation, s.touch = engine.calculateIndentation(s)
                Ex, Ey = engine.Elastography2withMax(s, grainstep, scaledistance, maxind)
                if Ex is None:
                    continue
                s.ElastX = Ex
                s.ElastY = Ey
                xx.append(Ex)
                yy.append(Ey)
                elit = pg.PlotCurveItem(Ex, Ey * 1e9, pen=self.blackPen, clickable=True)
                self.ui.b2_plot_elasto.plotItem.addItem(elit)
                elit.sigClicked.connect(self.b2curveClicked)
                elit.segment = s
                s.elit = elit
                # progress.setValue(progress.value() + 1)
                cdown -= 1
                if cdown == 0:
                    QtCore.QCoreApplication.processEvents()
                    cdown = 10

                s.ElaInvalid, s.filEla = engine.InvalidCurvesFromElasticityRise(s, win=filwin,
                                                                                scaledistance=int(scaledistance),
                                                                                threshold_oscillation=thresh_osc)
                if s.ElaInvalid == True:
                    s.invalid = True

        # xmed, ymed = engine.getMedCurve(xx, yy, loose=True)
        # # points = pg.PlotDataItem(xmed,ymed*1e9,pen=None,symbol='o')
        # points = pg.PlotCurveItem(xmed, ymed * 1e9, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 255, 200), width=2))
        # self.ui.b2_plot_elasto.plotItem.addItem(points)
        #
        # if any(engine.np.isnan(xmed)) == False and any(engine.np.isnan(ymed)) == False:
        #     self.xmed = xmed
        #     self.ymed = ymed
        # if any(engine.np.isnan(E0h)) == False:
        #     self.E0h = E0h
        # if any(engine.np.isnan(Ebh)) == False:
        #     self.Ebh = Ebh
        # if any(engine.np.isnan(d0h)) == False:
        #     self.d0h = d0h
        #
        # pars1, covs1, pars2, covs2, pars3, covs3, pars4, covs4, i_dhalf, i_cut = engine.fitExpDecay(xmed, ymed, s.R)
        # if pars1 is not None:
        #     yfit = engine.ExpDecay(xmed, pars2[0], pars1[1], pars1[2], s.R)
        #     self.ui.b2_plot_elasto.addItem(pg.PlotCurveItem(xmed, yfit * 1e9, pen=self.greenPen))

        QtWidgets.QApplication.restoreOverrideCursor()

    def b2Delete(self):
        index = int(self.ui.b2_segment.value())
        self.b2['exp'][index].plit.clear()
        del (self.b2['exp'][index])
        self.ui.b2_segment.setMaximum(len(self.b2['exp']))
        # self.ui.b2_segment.setValue(0)
        self.ui.b2_segment.setValue(index - 1)

    def b2DeleteAllInvalid(self):
        self.MakeInvalidInvisible = True
        # for i, s in enumerate(self.b2['exp']):
        #     if s.invalid is True:
        #         self.b2['exp'][i].plit.clear()
        # self.ui.b2_segment.setMaximum(len(self.b2['exp']))
        # self.ui.b2_segment.setValue(0)
        # self.b2_index_invalid=[]
        self.b2_view()
        print("Removed all invalid curves!")

    def b2curveClicked(self, cv):
        for i in range(len(self.b2['exp'])):
            if cv.segment == self.b2['exp'][i]:
                self.ui.b2_segment.setValue(i)
                break

    def b2_view(self):
        index = int(self.ui.b2_segment.value())
        for i, s in enumerate(self.b2['exp']):
            if self.ui.b2_vFiltered.isChecked() is True:
                s.plit.setData(s.z - s.offsetX, s.ffil - s.offsetY)
            else:
                s.plit.setData(s.z, s.f)
            if i == index:
                s.plit.setPen(self.greenPen)
                try:
                    s.elit.setPen(self.greenPen)
                except:
                    pass
            else:
                s.plit.setPen(self.blackPen)
                try:
                    s.elit.setPen(self.blackPen)
                except:
                    pass
                if s.invalid is True:
                    s.plit.setPen(self.redPen)
                    try:
                        s.elit.setPen(self.redPen)
                    except:
                        pass
                    if self.MakeInvalidInvisible == True:
                        s.plit.setPen(self.nonePen)

    def b2Filter(self):

        if self.ui.comboFilter.currentText() == 'Prominency':
            a = panels.FilterData()
            if (a.exec() == 0):
                return
        elif self.ui.comboFilter.currentText() == 'SmoothFFT':
            a = panels.FilterSavData()
            if (a.exec() == 0):
                return
        else:
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        pars = a.getParams()
        summative = pars[0]
        del (pars[0])
        fun = a.getCall()
        for s in self.b2['exp']:
            if summative is True:
                s.ffil = fun(s.ffil, *pars)
            else:
                s.ffil = fun(s.f, *pars)
            s.ffil_original = s.ffil

        QtWidgets.QApplication.restoreOverrideCursor()
        self.b2Update()
        self.b2_view()

    def b2_crop(self):
        a = panels.CropCurves()
        if (a.exec() == 0):
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        front = int(a.CropStart.value())
        back = int(a.CropEnd.value())
        for s in self.b2['exp']:
            s.z = s.z_original
            s.ffil = s.ffil_original
            s.f = s.f_original
            s.z = s.z[front:-(back + 1)]
            s.ffil = s.ffil[front:-(back + 1)]
            s.f = s.f[front:-(back + 1)]
        self.b2Update()
        self.b2_view()

    def b2_contactPoint(self):
        p = None
        f = None

        if self.ui.comboContact.currentText() == 'Chiaro':
            a = panels.chiaroPoint()
            if a.exec() == 0:
                return
            p = a.getParams()
            f = a.getCall()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            if f is not None:
                for s in self.b2['exp']:
                    s.invalid = False
                    s.offsetX, s.offsetY = f(s, *p)
                    if (s.offsetX, s.offsetY) == (0, 0):
                        s.invalid = True
        elif self.ui.comboContact.currentText() == 'eeff':
            a = panels.eeffPoint()
            a.setSegment(self.b2['exp'][0])
            if a.exec() == 0:
                return
            p = a.getParams()
            self.threshold_quot = p[1]
            f = a.getCall()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            if f is not None:
                for s in self.b2['exp']:
                    s.invalid = False
                    s.offsetX, s.offsetY, s.quot = f(s, *p[:-1])
                    s.bol2 = engine.Nanosurf_FindInvalidCurves(s, p[-1])
                    if (s.offsetX, s.offsetY) == (0, 0) or s.bol2 == False:
                        s.invalid = True

        elif self.ui.comboContact.currentText() == 'Nanosurf':
            a = panels.NanosurfPoint()
            if a.exec() == 0:
                return
            p = a.getParams()
            f = a.getCall()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            if f is not None:
                for s in self.b2['exp']:
                    s.invalid = False
                    s.bol, s.offsetX, s.offsetY, s.x_CPderiv, s.y_CPderiv = f(s, *p)
                    s.offsetX_original = s.offsetX
                    s.offsetY_original = s.offsetY
                    if s.bol is True:
                        s.bol2 = engine.Nanosurf_FindInvalidCurves(s, p[-1])
                    else:
                        s.bol2 = None
                    if s.bol is False or s.bol2 is False:
                        s.invalid = True
        elif self.ui.comboContact.currentText() == 'Nanosurf Deriv':
            a = panels.NanosurfPointDeriv()
            if a.exec() == 0:
                return
            p = a.getParams()
            f = a.getCall()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            if f is not None:
                for s in self.b2['exp']:
                    s.invalid = False
                    s.bol_deriv, s.offsetX, s.offsetY, s.z0s, s.ymax, s.x_slopes, s.slopes = f(s, *p)
                    s.offsetX_original = s.offsetX
                    s.offsetY_original = s.offsetY
                    # if s.bol_deriv is True:
                    #     s.bol2=engine.Nanosurf_FindInvalidCurves(s, p[-1])
                    # else:
                    #     s.bol2=None
                    if s.bol_deriv is False:  # or s.bol2 is False:
                        s.invalid = True

        QtWidgets.QApplication.restoreOverrideCursor()
        self.b2Update()
        self.b2_view()

    def b2chSegment(self):
        index = int(self.ui.b2_segment.value())
        s = self.b2['exp'][index]
        self.b2['plit1a'].setData(s.z, s.f)
        if s.bol == None or s.bol == False:
            if s.ffil is None:
                self.b2['plit1b'].setData(s.z, s.f)
                self.b2['plit1c'].setData([0, 0], [min(s.f), max(s.f)],
                                          pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=2))
            else:
                self.b2['plit1b'].setData(s.z, s.ffil)
                self.b2['plit1c'].setData([0, 0], [min(s.f), max(s.f)],
                                          pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=2))

        if s.bol == True:
            if s.ffil is None:
                self.b2['plit1a'].setData(s.z - s.offsetX, s.f - s.offsetY)
                self.b2['plit1b'].setData(s.z - s.offsetX, s.f - s.offsetY)
                self.b2['plit1c'].setData([0, 0], [min(s.f), max(s.f)],
                                          pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            else:
                self.b2['plit1a'].setData(s.z - s.offsetX, s.f - s.offsetY)
                self.b2['plit1b'].setData(s.z - s.offsetX, s.ffil - s.offsetY)
                self.b2['plit1c'].setData([0, 0], [min(s.f), max(s.f)],
                                          pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))

        if s.bol is not None and s.x_CPderiv[0] != 0:
            self.b2['plit2'].setData(s.x_CPderiv - s.offsetX, s.y_CPderiv,
                                     pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
            self.b2['plit2b'].setData([min(s.x_CPderiv - s.offsetX), max(s.x_CPderiv - s.offsetX)],
                                      [s.threshold_exp, s.threshold_exp],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
        if s.bol_deriv is not None:
            self.b2['plit2'].setData(s.z0s - s.offsetX, s.ymax, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
            self.b2['plit2a'].setData([0, 0], [min(s.ymax), max(s.ymax)],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            self.b2['plit2b'].setData([min(s.z0s - s.offsetX), max(s.z0s - s.offsetX)],
                                      [s.threshold_slopes, s.threshold_slopes],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            slopes = engine.np.asarray(s.slopes) * 10000
            self.b2['plit2c'].setData(s.x_slopes - s.offsetX, slopes,
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=1))
        if s.quot is not None:
            self.b2['plit2'].setData(s.z - s.offsetX, s.quot, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
            self.b2['plit2a'].setData([0, 0], [min(s.quot), max(s.quot)],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            self.b2['plit2b'].setData([min(s.z - s.offsetX), max(s.z - s.offsetX)],
                                      [self.threshold_quot, self.threshold_quot],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            self.b2['plit2c'].setData([0, 0], [min(s.quot), max(s.quot)],
                                      pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=2))
            if s.invalid == True:
                self.b2['plit2'].setData(s.z - s.offsetX, s.quot,
                                         pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=1))
        if s.ElastX != None:
            if s.E0 is not None and s.E0 > s.Eb:
                self.b2['plit3'].setData(s.ElastX, s.ElastY * 1e9, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
            else:
                self.b2['plit3'].setData(s.ElastX, s.ElastY * 1e9,
                                         pen=pg.mkPen(pg.QtGui.QColor(255, 0, 0, 255), width=1))
            if s.ElaInvalid != None:
                if s.ElaInvalid == False:
                    self.b2['plit3b'].setData(s.ElastX, s.filEla,
                                              pen=pg.mkPen(pg.QtGui.QColor(0, 255, 0, 255), width=1))
                if s.ElaInvalid == True:
                    self.b2['plit3b'].setData(s.ElastX, s.filEla, pen=pg.mkPen(pg.QtGui.QColor(0, 0, 0, 255), width=1))
            else:
                self.b2['plit3b'].setData([0, 0], [0, 0])
        else:
            # self.b2['plit2'].setData(s.z - s.offsetX, s.f - s.offsetY,pen=pg.mkPen( pg.QtGui.QColor(255, 0, 0,255),width=1))
            self.b2['plit3'].setData([0, 0], [0, 0])
            self.b2['plit3b'].setData([0, 0], [0, 0])

        self.b2_view()

    def b2Color(self):
        alpha = int(self.ui.b2_Alpha.value())
        self.blackPen = pg.mkPen(pg.QtGui.QColor(0, 0, 0, alpha), width=1)
        self.redPen = pg.mkPen(pg.QtGui.QColor(255, 0, 0, alpha), width=1)
        self.b2Update()

    def b2Update(self):
        for s in self.b2['exp']:
            if s.invalid is True:
                s.plit.setPen(self.redPen)
            else:
                s.plit.setPen(self.blackPen)
        self.b2chSegment()

    ################################################
    ############## b1 actions ######################
    ################################################

    def b1_invalid(self):
        threshold = float(self.ui.b1_minmax.value())
        xValue = float(self.ui.b1_yAlign.value())
        for c in self.b1['exp'].haystack:
            try:
                istart, iend = self.b1GetZF(c[c.forwardSegment].z)
                iPoint = engine.np.argmin((c[c.forwardSegment].z[istart:iend] - xValue) ** 2)
                yOffset = engine.np.average(c[c.forwardSegment].f[iPoint - 10:iPoint + 10])
                if engine.np.max(c[c.forwardSegment].f[istart:iend]) < yOffset + threshold:
                    myself = c.myTree
                    newstate = QtCore.Qt.Unchecked
                    myself.setCheckState(0, newstate)
            except IndexError:
                continue

    def b1GetZF(self, z):
        zstart = float(self.ui.b1_start.value())
        zend = float(self.ui.b1_end.value())
        istart = engine.np.argmin((z - zstart) ** 2)
        iend = engine.np.argmin((z - zend) ** 2)
        return istart, iend

    def b1tob2(self):
        mysegs = []
        for c in self.b1['exp'].haystack:
            if c.myTree.checkState(0) == QtCore.Qt.Checked:
                try:
                    istart, iend = self.b1GetZF(c[c.forwardSegment].z)
                    s = engine.bsegment(c, c[c.forwardSegment].z[istart:iend], c[c.forwardSegment].f[istart:iend])
                    mysegs.append(s)
                except IndexError:
                    continue
        self.b2['exp'] = mysegs
        self.ui.switcher.setCurrentIndex(1)
        self.b2Init()

    def b1Color(self):
        alpha = int(self.ui.b1_Alpha.value())
        self.redPen = pg.mkPen(pg.QtGui.QColor(255, 0, 0, alpha), width=1)
        self.blackPen = pg.mkPen(pg.QtGui.QColor(0, 0, 0, alpha), width=1)
        self.b1Update()

    def b1Forward(self):
        num = int(self.ui.b1_forwardSegment.value())
        self.b1['exp'].setForwardSegment(num)
        self.b1Plot()

    def b1Plot(self):
        self.ui.b1_graph.plotItem.clear()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Plotting all files...", "Cancel plotting", 0,
                                             len(self.b1['exp'].haystack))

        for c in self.b1['exp'].haystack:
            plit = pg.PlotCurveItem(clickable=True)
            self.ui.b1_graph.plotItem.addItem(plit)
            if len(c) > c.forwardSegment:
                plit.setData(c[c.forwardSegment].z, c[c.forwardSegment].f)
            else:
                plit.setData([1000, 3000, 5000, 8000], [0, 1, -1, 0])
            plit.setPen(self.b1getPen(c.myTree))
            c.plit = plit
            plit.curve = c
            plit.sigClicked.connect(self.b1curveClicked)
        progress.setValue(len(self.b1['exp'].haystack))
        QtWidgets.QApplication.restoreOverrideCursor()

    def b1getPen(self, myself):

        if myself.isSelected() is True:
            return self.greenPen

        red = False
        black = False
        if self.ui.b1_redblack.isChecked() is True:
            red = True
            black = True
        elif self.ui.b1_red.isChecked() is True:
            red = True
        elif self.ui.b1_black.isChecked() is True:
            black = True

        isRed = (myself.checkState(0) == QtCore.Qt.Unchecked)
        if isRed is True:
            if red is True:
                return self.redPen
            else:
                return self.nonePen
        else:
            if black is True:
                return self.blackPen
            else:
                return self.nonePen

    def b1Update(self, myself=None, column=0):
        if myself is None or myself.curve.is_leaf() is False:
            for c in self.b1['exp'].haystack:
                c.plit.setPen(self.b1getPen(c.myTree))
        else:
            myself.curve.plit.setPen(self.b1getPen(myself))

    def b1curveClicked(self, pgCurve):
        myself = pgCurve.curve.myTree
        newstate = QtCore.Qt.Unchecked
        if myself.checkState(0) == QtCore.Qt.Unchecked:
            newstate = QtCore.Qt.Checked
        myself.setCheckState(0, newstate)

    def b1xCut(self):
        for c in self.b1['exp'].haystack:
            try:
                istart, iend = self.b1GetZF(c[c.forwardSegment].z)
                c.plit.setData(c[c.forwardSegment].z[istart:iend], c[c.forwardSegment].f[istart:iend])
            except IndexError:
                continue

    def b1yAlign(self):
        xValue = float(self.ui.b1_yAlign.value())
        for c in self.b1['exp'].haystack:
            try:
                istart, iend = self.b1GetZF(c[c.forwardSegment].z)
                iPoint = engine.np.argmin((c[c.forwardSegment].z - xValue) ** 2)
                yOffset = engine.np.average(c[c.forwardSegment].f[iPoint - 10:iPoint + 10])
                c.plit.setData(c[1].z[istart:iend], c[1].f[istart:iend] - yOffset)
            except IndexError:
                continue
