from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
import pyqtgraph as pg
import mvexperiment.experiment as experiment
import Ui_Chiaro as view
import engine
import pickle

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class curveWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Chiaro2020')

        self.ui = view.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.b1_selectFolder.clicked.connect(self.b1SelectDir)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.redPen = pg.mkPen( pg.QtGui.QColor(255, 0, 0,30),width=1)
        self.blackPen = pg.mkPen( pg.QtGui.QColor(0, 0, 0,30),width=1)
        self.greenPen = pg.mkPen( pg.QtGui.QColor(0, 255, 0,255),width=2)
        self.nonePen = pg.mkPen(None)
        self.workingdir = './'

        self.b1 = {'phase':1,'forwardSegment':1,'exp':[]}
        self.b2 = {'phase':2,'exp':[],'plit1a':None,'plit1b':None,'plit2':None}
        self.b3 = {'phase':3,'exp':[],'plit1':None,'plit2a':None,'plit2b':None}
        self.b4 = {'phase':4,'exp':[],'Manlio':None,'avcurve':None,'avstress':None}
        self.segmentLength = 100

        self.ui.switcher.setCurrentIndex(0)
        self.ui.sl_load.clicked.connect(self.load_pickle)
        self.ui.b1_generate.clicked.connect(self.generateFake)

    ################################################
    ############## SL actions ######################
    ################################################

    def generateFake(self):
        mysegs = []
        noise = float(self.ui.b1_noise.value())/1000.0
        E1 = float(self.ui.el_emax.value())/1.0e9
        R = 3200.0
        xbase = engine.np.linspace(0,4000,4000)
        for i in range(50):
            mysegs.append(engine.bsegment())
            mysegs[-1].indentation = xbase
            if self.ui.el_one.isChecked() is True:
                mysegs[-1].touch = engine.noisify(engine.standardHertz(xbase,E1,R),noise)
            else:                
                E2 = float(self.ui.el_emin.value())/1.0e9
                h  = float(self.ui.el_h.value())
                if self.ui.el_std.isChecked() is True:
                    mysegs[-1].touch = engine.noisify(engine.LayerStd(xbase,E1,E2,h,R),noise)
                else:
                    mysegs[-1].touch = engine.noisify(engine.LayerRoss(xbase,E1,E2,h,R),noise)
            mysegs[-1].R = R

        self.b3['exp']=mysegs
        self.ui.switcher.setCurrentIndex(2)
        self.b3Init()

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
        self.ui.switcher.setCurrentIndex(data[0].phase-1)

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
        
        fname = QtWidgets.QFileDialog.getSaveFileName(self,'Select the file to save your processing',self.workingdir,"Python object serialization (*.pickle)")
        if fname[0] =='':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        with open(fname[0], 'wb') as f:
            pickle.dump(data, f)
        QtWidgets.QApplication.restoreOverrideCursor()

        if phase == 2:
            self.b2Init()
        elif phase == 3:
            self.b3Init()

    
    ################################################
    ############## b4 actions ######################
    ################################################

    def b4Init(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        
        self.ui.b4_plot.plotItem.clear()
        self.ui.b4_plot.plotItem.setTitle('Force-indentation curves')
        self.ui.b4_plot.plotItem.setLabel('left','Force [nN]')
        self.ui.b4_plot.plotItem.setLabel('bottom','Indentation [nm]')

        xx = []
        yy = []

        for s in self.b4['exp']:
            s.phase = 4
            s.pressure = s.touch/engine.np.pi/s.R/engine.np.abs(s.indentation)           
            plit = pg.PlotCurveItem(clickable=False)
            self.ui.b4_plot.plotItem.addItem(plit)
            xx.append(s.indentation)
            yy.append(s.touch)
            plit.setData( s.indentation,s.touch )
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            #plit.sigClicked.connect(self.b2curveClicked)

        xmed,ymed = engine.getMedCurve(xx,yy)
        self.ui.b4_plot.plotItem.addItem( pg.PlotCurveItem(xmed,ymed,pen=self.greenPen) )
        self.b4['avcurve']=[xmed,ymed]

        #segmentX = xmed[::self.segmentLength]
        #segmentY = ymed[::self.segmentLength]
        #self.ui.b4_plot.plotItem.addItem( pg.PlotDataItem(segmentX,segmentY,pen=None,symbol='o') )
        
        self.b4_stressStrain()
        
        #eps,sig = engine.calculateSS(s,xmed,ymed)
        #elit = pg.PlotCurveItem(100.0*eps[1:],sig[1:]*1e9,pen=pg.mkPen( pg.QtGui.QColor(0, 0, 255,255),width=2))    
        #self.ui.b4_plotElast.plotItem.addItem(elit)

        QtWidgets.QApplication.restoreOverrideCursor()
        #self.ui.b4_doep.clicked.connect(self.b4_stressStrain)
        self.ui.b4_loadManlio.clicked.connect(self.loadManlio)        
        #self.ui.b4_final.clicked.connect(self.b4_manlioNotturno)

    def loadManlio(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,'Select the file to load Manlio data',self.workingdir,"Tab Separated Values (*.tsv)")
        if fname[0] =='':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        

        data = engine.np.loadtxt(fname[0],skiprows=1)

        #self.ui.b3_plotscatter.clear()
        self.b4['Manlio']=[data[:,1],3.0*data[:,0]]
        mlit1 = pg.PlotDataItem(self.b4['Manlio'][0],self.b4['Manlio'][1],pen=None,symbol='o')
        self.ui.b4_plotManlio.addItem(mlit1)
        mlit2 = pg.PlotDataItem(self.b4['Manlio'][0],self.b4['Manlio'][1],pen=None,symbol='o')
        self.ui.b4_plotFinal.addItem(mlit2)

        QtWidgets.QApplication.restoreOverrideCursor()

    def b4_final(self):
        self.ui.b4_plotFinal.clear()

        if self.b4['exp'][0].ElastX is None:
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Performing elastography ...", "Cancel E-analysis", 0, len(self.b4['exp']))
        
        cdown = 10

        grainstep =  float(self.ui.b4_elIncrement.value())
        scaledistance =  float(self.ui.b4_elDash.value())
        maxind = float( self.ui.b4_elMaxind.value() )
        

        pmean = engine.np.linspace(0,10000,100)
        emean = engine.np.zeros(len(pmean))
        howmany = engine.np.zeros(len(pmean))

        for s in self.b4['exp']:  
            #elit = pg.PlotCurveItem(s.pressure[s.IndexDv[1:]]*1e9,s.ElastY*1e9,pen=self.blackPen)    
            x=s.pressure[s.IndexDv[1:]]*1e9
            y=s.ElastY*1e9
            elit = pg.PlotDataItem(x,y,pen=None,symbol='o',symbolPen=None,symbolBrush=pg.mkBrush((0, 0, 0, 5)))            
            imin = engine.np.max([int(engine.np.min(x)/100)+1,0])
            imax = engine.np.min([int(engine.np.max(x)/100)-1,len(pmean)-1])            
            self.ui.b4_plotFinal.plotItem.addItem(elit)            
            emean[imin:imax]+=engine.np.interp(pmean[imin:imax], x, y)
            howmany[imin:imax]+=1
            progress.setValue(progress.value() + 1)
            cdown-=1
            if cdown == 0:
                QtCore.QCoreApplication.processEvents()
                cdown = 10   

        xx = pmean[howmany>0]
        yy = emean[howmany>0]
        hh = howmany[howmany>0]
        yy/=hh

        elit2 = pg.PlotDataItem(xx,yy,pen=None,symbol='o',symbolPen=pg.mkPen((255, 0, 0, 100)),symbolBrush=pg.mkBrush((0, 255, 0, 255)))    
        self.ui.b4_plotFinal.plotItem.addItem(elit2)
        if self.b4['Manlio'] is not None:
            mlit = pg.PlotDataItem(self.b4['Manlio'][0],self.b4['Manlio'][1],pen=None,symbol='o')
            self.ui.b4_plotFinal.addItem(mlit)

        QtWidgets.QApplication.restoreOverrideCursor()

    def b4_manlioNotturno(self):
        self.ui.b4_plotManlio.plotItem.clear()
        self.ui.b4_plotManlio.plotItem.setTitle('Elastography')
        self.ui.b4_plotManlio.plotItem.setLabel('left','Young\'s Modulus [Pa]')
        self.ui.b4_plotManlio.plotItem.setLabel('bottom','Indentation [nm]')

        xx = []
        yy = []

        for s in self.b4['exp']:  
            E = 9*s.touch[1:]/16/engine.np.sqrt(s.R)/(s.indentation[1:])**1.5
            P = s.touch[1:]/engine.np.pi/s.R/s.indentation[1:]
            xx.append(s.indentation[1:])
            yy.append(E)
            #elit = pg.PlotCurveItem(P*1e9,E*1e9,pen=self.blackPen)    
            elit = pg.PlotCurveItem(s.indentation[1:],E*1e9,pen=self.blackPen)    
            elit2 = pg.PlotCurveItem(s.indentation[1:],P*1e9,pen=self.redPen)    
            self.ui.b4_plotManlio.plotItem.addItem(elit)
            self.ui.b4_plotManlio.plotItem.addItem(elit2)

        xmed,ymed = engine.getMedCurve(xx,yy,loose = False)        

        self.ui.b4_plotManlio.addItem( pg.PlotCurveItem(xmed,ymed*1e9,pen=self.greenPen) )   



    def b4_stressStrain(self):
        
        self.ui.b4_plotElast.plotItem.clear()
        self.ui.b4_plotElast.plotItem.setTitle('Stress-Strain curves')
        self.ui.b4_plotElast.plotItem.setLabel('left','Stress [Pa]')
        self.ui.b4_plotElast.plotItem.setLabel('bottom','Strain [%]')
        self.ui.b4_plotElast.plotItem.clear()

        xx = []
        yy = []

        for s in self.b4['exp']:  
            s.epsilon,s.sigma = engine.calculateSS(s)
            xx.append(s.epsilon[1:])
            yy.append(s.sigma[1:])
            elit = pg.PlotCurveItem(100.0*s.epsilon[1:],s.sigma[1:]*1e9,pen=self.blackPen)    
            self.ui.b4_plotElast.plotItem.addItem(elit)
        xmed,ymed = engine.getMedCurve(xx,yy)
        self.ui.b4_plotElast.addItem( pg.PlotCurveItem(100.0*xmed,ymed*1e9,pen=self.greenPen) )        
        self.b4['avstress']=[xmed,ymed]
        self.b4_YoungStrain()

        
        
        #self.ui.b4_plotManlio.addItem( pg.PlotCurveItem(engine.np.log(xmed),ymed*1e9,pen=self.greenPen) )

    def b4_YoungStrain(self):
        self.ui.b4_plotFinal.plotItem.clear()
        xmed,ymed = self.b4['avstress']

        self.ui.b4_plotFinal.plotItem.setTitle('Young-Strain curve')
        self.ui.b4_plotFinal.plotItem.setLabel('left','Young [Pa]')
        self.ui.b4_plotFinal.plotItem.setLabel('bottom','Strain [%]')
        
        discr = int( self.ui.b4_elIncrement.value() )

        ex,ey = engine.ElastoStrain(xmed,ymed,discr)
        self.ui.b4_plotFinal.addItem( pg.PlotCurveItem(ex*100.0,ey*1e9,pen=self.greenPen) )
        ex,ey = engine.ElastoStrainSmart(xmed,ymed,discr)
        self.ui.b4_plotFinal.addItem( pg.PlotCurveItem(ex*100.0,ey*1e9,pen= pg.mkPen((255,0,0),width=2) ) )

    def b4_manliography(self):

        #a = engine.np.random.rand(100,250)
        #img = pg.ImageItem(a)
        #img.scale(0.2, 0.1)
        #self.ui.b1_graph.addItem(img)

        for s in self.b4['exp']:            
            a = engine.np.sqrt(s.R*s.indentation)
            s.sigma = s.touch/(engine.np.pi*a**2)
            s.epsilon = 0.2*a*s.indentation 
            elit = pg.PlotDataItem(s.epsilon[1:],s.sigma[1:],pen=pg.mkPen((0,0,0,10)) )    
            self.ui.b4_plotManlio.plotItem.addItem(elit)
            
    def moodle():
        self.ui.b4_plotManlio.plotItem.clear()
        fmin =  float(self.ui.b4_fmin.value())
        fmax =  float(self.ui.b4_fmax.value())
        fstep = float(self.ui.b4_fstep.value())

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Performing manliography ...", "Cancel MG-analysis", 0, len(self.b4['exp']))
        
        self.ui.b4_plotManlio.plotItem.clear()
        cdown = 10
        for s in self.b4['exp']:            
            index_fmin = engine.np.argmin( ( s.touch-fmin )**2 )
            index_fmax = engine.np.argmin( ( s.touch-fmax )**2 )            
            s.Paxis = s.pressure[index_fmin:index_fmax]*1e9
            s.Eaxis = engine.calcEdeep(s,index_fmin,index_fmax)
            elit = pg.PlotDataItem(s.Paxis,s.Eaxis,pen=None,symbol='s',symbolPen=None,symbolBrush=pg.mkBrush((0, 0, 0, 5))        )    
            self.ui.b4_plotManlio.plotItem.addItem(elit)
            progress.setValue(progress.value() + 1)
            cdown-=1
            if cdown == 0:
                QtCore.QCoreApplication.processEvents()
                cdown = 10
        if self.b4['Manlio'] is not None:
            mlit = pg.PlotDataItem(self.b4['Manlio'][0],self.b4['Manlio'][1],pen=None,symbol='o')
            self.ui.b4_plotManlio.addItem(mlit)
        

        QtWidgets.QApplication.restoreOverrideCursor()


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
            #s.indentation,s.touch = engine.calculateIndentation(s)
            #s.pressure = s.touch/engine.np.sqrt(s.R*engine.np.abs(s.indentation))
            
            iMa.append(engine.np.max(s.indentation))
            fMa.append(engine.np.max(s.touch))

            plit = pg.PlotCurveItem(clickable=False)
            self.ui.b3_plotind.plotItem.addItem(plit)
            plit.setData( s.indentation,s.touch )
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            #plit.sigClicked.connect(self.b2curveClicked)
        
        self.b3['fit']=pg.PlotCurveItem(clickable=False)
        self.b3['fit'].setPen(self.greenPen)
        self.ui.b3_plotind.plotItem.addItem(self.b3['fit'])

        self.b3['indMax']=engine.np.max(iMa)
        self.b3['forMax']=engine.np.max(fMa)
        self.b3updMax()

        self.ui.b3_plotscatter.clear()
        self.b3['plit1'] = pg.PlotDataItem([1,2,3],[0,0,0],pen=None,symbol='o')
        self.ui.b3_plotscatter.addItem(self.b3['plit1'])
        ## compute standard histogram
        self.ui.b3_plothist.clear()
        vals = engine.np.hstack([engine.np.random.normal(size=500), engine.np.random.normal(size=260, loc=4)])
        y,x = engine.np.histogram(vals, bins=engine.np.linspace(-3, 8, 40))
        self.b3['plit2a'] = pg.PlotDataItem(x, y, stepMode=True,pen=pg.mkPen('r'))
        self.ui.b3_plothist.addItem(self.b3['plit2a'])

        e0,w,A,nx,ny = engine.gauss(x,y)        
        self.b3['plit2b'] = pg.PlotDataItem(nx, ny,pen=self.greenPen)
        self.ui.b3_plothist.addItem(self.b3['plit2b'])

        QtWidgets.QApplication.restoreOverrideCursor()

        self.ui.b3_Alpha.valueChanged.connect(self.b3Color)
        self.ui.b3_doCutFit.clicked.connect(self.b3Fit)
        self.ui.b3_maxIndentation.clicked.connect(self.b3updMax)
        self.ui.b3_maxForce.clicked.connect(self.b3updMax)
        self.ui.b3_save.clicked.connect(self.save_pickle)
        self.ui.b3_b3tob4.clicked.connect(self.b3tob4)
        self.ui.b3_doExport.clicked.connect(self.b3Export)
        self.ui.b3_doExport2.clicked.connect(self.b3Export2)
        self.ui.b4_doElas.clicked.connect(self.b3_Alistography)

    def b3_Alistography(self):
        self.ui.b3_long.plotItem.clear()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Performing elastography ...", "Cancel E-analysis", 0, len(self.b4['exp']))
        
        grainstep = int( self.ui.b4_elIncrement.value() )
        scaledistance = float( self.ui.b4_elDash.value() )
        maxind = float( self.ui.b4_elMaxind.value() )

        cdown = 10
        xx=[]
        yy=[]

        E0h=[]
        Ebh=[]
        d0h=[]

        for s in self.b3['exp']:  
            Ex,Ey = engine.Elastography( s,grainstep,scaledistance,maxind)          
            if Ex is None:
                continue
            s.ElastX = Ex
            s.ElastY = Ey

            pars = engine.fitExpDecay(Ex,Ey,s.R)
            if pars is not None:
                E0h.append(pars[0]*1e9)
                Ebh.append(pars[1]*1e9)
                d0h.append(pars[2])

            xx.append(Ex)
            yy.append(Ey)
            elit = pg.PlotCurveItem(Ex,Ey*1e9,pen=self.blackPen)    
            self.ui.b3_long.plotItem.addItem(elit)
            progress.setValue(progress.value() + 1)
            cdown-=1
            if cdown == 0:
                QtCore.QCoreApplication.processEvents()
                cdown = 10        
        
        xmed,ymed = engine.getMedCurve(xx,yy,loose = True)        

        pars = engine.fitExpDecay(xmed,ymed,s.R)
        if pars is not None:
            yfit = engine.ExpDecay(xmed,*pars,s.R)
            self.ui.b3_long.addItem( pg.PlotCurveItem(xmed,yfit*1e9,pen=self.greenPen) )  

        points = pg.PlotDataItem(xmed,ymed*1e9,pen=None,symbol='o')
        self.ui.b3_long.addItem( points )  

        self.ui.b3_plothist_E0.clear()
        self.ui.b3_plothist_Eb.clear()
        self.ui.b3_plothist_d0.clear()

        y,x = engine.np.histogram(E0h, bins='auto',range=(max(0,min(E0h)),min([1000000,max(E0h)])))
        #self.ui.b3_plothist_E0.addItem(pg.PlotDataItem(x, y, stepMode=True,pen=pg.mkPen('r')))
        self.ui.b3_plothist_E0.addItem(pg.PlotCurveItem(x, y, stepMode=True,pen=pg.mkPen('r')))
        val = engine.np.average(E0h)
        err = engine.np.std(E0h)
        self.ui.b3_labE0.setText('<html><head/><body><p><span style=" font-weight:600;">{}&plusmn;{}</span> kPa</p></body></html>'.format(int(val/10)/100.0,int(err/10)/100.0))

        y,x = engine.np.histogram(Ebh, bins='auto',range=(max(0,min(Ebh)),min([100000,max(Ebh)])))
        self.ui.b3_plothist_Eb.addItem(pg.PlotCurveItem(x, y, stepMode=True,pen=pg.mkPen('r')))
        val = engine.np.average(Ebh)
        err = engine.np.std(Ebh)
        self.ui.b3_labEb.setText('<html><head/><body><p><span style=" font-weight:600;">{}&plusmn;{}</span> kPa</p></body></html>'.format(int(val/10)/100.0,int(err/10)/100.0))

        y,x = engine.np.histogram(d0h, bins='auto',range=(max(0,min(d0h)),min([10000,max(d0h)])))
        self.ui.b3_plothist_d0.addItem(pg.PlotCurveItem(x, y, stepMode=True,pen=pg.mkPen('r')))
        val = engine.np.average(d0h)
        err = engine.np.std(d0h)
        self.ui.b3_labd0.setText('<html><head/><body><p><span style=" font-weight:600;">{}&plusmn;{}</span> nm</p></body></html>'.format(int(val),int(err)))        

        QtWidgets.QApplication.restoreOverrideCursor()

        return E0h,Ebh,d0h

    def b3Export(self):
        Earray = self.b3Fit()
        fname = QtWidgets.QFileDialog.getSaveFileName(self,'Select the file to export your E data',self.workingdir,"Data table (*.np.txt)")
        if fname[0] =='':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        engine.np.savetxt(fname[0],Earray)
        QtWidgets.QApplication.restoreOverrideCursor()

    def b3Export2(self):
        E0,Eb,d0 = self.b3_Alistography()
        fname = QtWidgets.QFileDialog.getSaveFileName(self,'Select the file to export your E data',self.workingdir,"Tab Separated Values (*.tsv)")
        if fname[0] =='':
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        with open(fname[0],'w') as f:
            f.write('E0\tEb\td0\n')
            for i in range(len(E0)):
                f.write('{}\t{}\t{}\n'.format(E0[i],Eb[i],d0[i]))
            f.close()
        QtWidgets.QApplication.restoreOverrideCursor()

    def b3updMax(self):
        if self.ui.b3_maxIndentation.isChecked() is True:
            self.ui.b3_threshold.setMaximum(self.b3['indMax'])
        else:
            self.ui.b3_threshold.setMaximum(self.b3['forMax'])

    def b3tob4(self):
        self.b4['exp']=self.b3['exp']
        self.ui.switcher.setCurrentIndex(3)
        self.b4Init()

    def b3Fit(self):
        if self.ui.b3_maxIndentation.isChecked():
            for s in self.b3['exp']:
                if engine.np.max(s.indentation)<float(self.ui.b3_threshold.value()):
                    s.valid = False
                    s.plit.setPen(self.redPen)
                else:
                    s.valid = True
                    s.indMax = engine.np.argmin( (s.indentation - float(self.ui.b3_threshold.value()) )**2 )
                    s.plit.setPen(self.blackPen)
        else:
            for s in self.b3['exp']:
                if engine.np.max(s.touch)<float(self.ui.b3_threshold.value()):
                    s.valid = False
                    s.plit.setPen(self.redPen)
                else:
                    s.valid=True
                    s.plit.setPen(self.blackPen)
                    s.indMax = engine.np.argmin( (s.touch - float(self.ui.b3_threshold.value()) )**2 )
        
        Earray = []
        for s in self.b3['exp']:
            if s.valid is True:
                s.E = engine.fitHertz(s)
                if s.E is not None:
                    Earray.append(s.E*1e9)

        self.b3['plit1'].setData(engine.np.arange(len(Earray)),Earray)
        bins = int(self.ui.b3_bins.value())
        if bins==0:
            bins='auto'
        y,x = engine.np.histogram(Earray, bins=bins)
        self.b3['plit2a'].setData(x,y)
        e0,w,A,nx,ny = engine.gauss(x,y)        
        self.b3['plit2b'].setData(nx,ny)
        w = w/engine.np.sqrt(len(Earray))
        self.ui.b3_results.setText('<html><head/><body><p><span style=" font-weight:600;">{}&plusmn;{}</span> kPa</p></body></html>'.format(int(e0/10)/100.0,int(w/10)/100.0))

        R = self.b3['exp'][0].R
        E = engine.np.average(Earray)/1e9        
        x,y = engine.getHertz(E,R,float(self.ui.b3_threshold.value()),self.ui.b3_maxIndentation.isChecked())
        self.b3['fit'].setData(x,y)
                
        self.ui.b3_Eavg.setText('<html><head/><body><p><span style=" font-weight:600;">{}</span> Pa</p></body></html>'.format(int(engine.np.average(Earray))))
        self.ui.b3_Estd.setText('<html><head/><body><p><span style=" font-weight:600;">{}</span> Pa</p></body></html>'.format(int(engine.np.std(Earray))))

        return Earray


    def b3Color(self):
        alpha = int(self.ui.b3_Alpha.value())
        self.blackPen = pg.mkPen( pg.QtGui.QColor(0, 0, 0,alpha),width=1)
        self.redPen = pg.mkPen( pg.QtGui.QColor(255, 0, 0,alpha),width=1)
        for s in self.b3['exp']:
            if s.valid is True:
                s.plit.setPen(self.blackPen)
            else:
                s.plit.setPen(self.redPen)


    ################################################
    ############## b2 actions ######################
    ################################################

    def b2Init(self):

        self.ui.b2_segment.setMaximum(len(self.b2['exp'])-1)
        
        
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        self.ui.b2_plot_all.plotItem.clear()
        for s in self.b2['exp']:
            s.phase = 2
            plit = pg.PlotCurveItem(clickable=True)
            self.ui.b2_plot_all.plotItem.addItem(plit)
            plit.setData( s.z,s.f )
            plit.setPen(self.blackPen)
            s.plit = plit
            plit.segment = s
            plit.sigClicked.connect(self.b2curveClicked)
        self.b2_view()        
        self.ui.b2_Alpha.setValue(self.ui.b1_Alpha.value())
        
        self.ui.b2_plot_one.plotItem.clear()
        self.ui.b2_plot_two.plotItem.clear()
        s = self.b2['exp'][0]
        self.b2['plit1a'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit1a'].setData(s.z,s.f,pen=pg.mkPen( pg.QtGui.QColor(0, 0, 0,255),width=1))
        self.b2['plit1b'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit1b'].setData(s.z,s.f,pen=pg.mkPen( pg.QtGui.QColor(255, 0, 0,255),width=1))
        self.b2['plit2'] = pg.PlotCurveItem(clickable=True)
        self.b2['plit2'].setData(s.z,s.f, pen=pg.mkPen( pg.QtGui.QColor(0, 0, 0,255),width=1))
        self.ui.b2_plot_one.plotItem.addItem(self.b2['plit1a'])
        self.ui.b2_plot_one.plotItem.addItem(self.b2['plit1b'])
        self.ui.b2_plot_two.plotItem.addItem(self.b2['plit2'])

        QtWidgets.QApplication.restoreOverrideCursor()
        self.ui.b2_Alpha.valueChanged.connect(self.b2Color)
        self.ui.b2_segment.valueChanged.connect(self.b2chSegment)
        self.ui.b2_doFilter.clicked.connect(self.b2Filter)
        self.ui.b2_vFiltered.clicked.connect(self.b2_view)
        self.ui.b2_vOriginal.clicked.connect(self.b2_view)
        self.ui.b2_doOffset.clicked.connect(self.b2OffsetY)
        self.ui.b2_doOffsetX.clicked.connect(self.b2OffsetX)
        self.ui.b2_delete.clicked.connect(self.b2Delete)
        self.ui.b2_b2tob3.clicked.connect(self.b2tob3)
        self.ui.b2_save.clicked.connect(self.save_pickle)

    def b2tob3(self):
        self.b3['exp']=self.b2['exp']
        for s in self.b3['exp']:
            s.indentation,s.touch = engine.calculateIndentation(s)
        self.ui.switcher.setCurrentIndex(2)
        self.b3Init()

    def b2Delete(self):
        index = int(self.ui.b2_segment.value())
        self.b2['exp'][index].plit.clear()
        del(self.b2['exp'][index])
        self.ui.b2_segment.setMaximum(len(self.b2['exp']))
        self.ui.b2_segment.setValue(0)

    def b2curveClicked(self,cv):
        for i in range(len(self.b2['exp'])):
            if cv.segment == self.b2['exp'][i]:
                self.ui.b2_segment.setValue(i)
                break

    def b2_view(self):
        i = 0
        index = int(self.ui.b2_segment.value())
        for s in self.b2['exp']:
            if self.ui.b2_vFiltered.isChecked() is True:
                s.plit.setData(s.z-s.offsetX,s.ffil-s.offsetY)
            else:
                s.plit.setData(s.z,s.f)
            if i==index:
                s.plit.setPen(self.greenPen)
            else:
                s.plit.setPen(self.blackPen)
            i+=1

    def b2Filter(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        pro = float(self.ui.b2_pro.value() )
        winperc = float(self.ui.b2_winperc.value())/10.0
        thresh = int(self.ui.b2_minfreq.value())
        for s in self.b2['exp']:
            s.ffil = engine.filterOsc(s.f,pro=pro,winperc=winperc,threshold=thresh)
        QtWidgets.QApplication.restoreOverrideCursor()
        self.b2Update()
        self.b2_view()

    def b2OffsetY(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for s in self.b2['exp']:
            s.offsetY = engine.calculateOffsetYnew(s,ncMin = float(self.ui.b2_ncMin.value()),ncMax = float(self.ui.b2_ncMax.value()))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.b2Update()
        self.b2_view()

    def b2OffsetX(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for s in self.b2['exp']:
            s.offsetX = engine.calculateOffsetX(s,offset=float(self.ui.b2_xOffset.value()),win1=int(self.ui.b2_win1.value()),win2=int(self.ui.b2_win2.value()))
        QtWidgets.QApplication.restoreOverrideCursor()
        self.b2Update()
        self.b2_view()

    def b2chSegment(self):
        index = int(self.ui.b2_segment.value())
        s = self.b2['exp'][index]
        self.b2['plit1a'].setData(s.z,s.f)
        if s.ffil is None:
            self.b2['plit1b'].setData(s.z,s.f)
        else:
            self.b2['plit1b'].setData(s.z,s.ffil)

        self.b2['plit2'].setData(s.z-s.offsetX,s.f-s.offsetY)
        self.b2_view()

    def b2Color(self):
        alpha = int(self.ui.b2_Alpha.value())
        self.blackPen = pg.mkPen( pg.QtGui.QColor(0, 0, 0,alpha),width=1)
        self.b2Update()

    def b2Update(self):
        for s in self.b2['exp']:
            s.plit.setPen(self.blackPen)
        self.b2chSegment()


    ################################################
    ############## b1 actions ######################
    ################################################

    def b1SelectDir(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self,'Select the root dir','./')
        if fname[0] =='':
            return
        self.workingdir = fname
        self.b1['exp'] = experiment.Chiaro(fname)
        self.b1['exp'].browse()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Opening files...", "Cancel opening", 0, len(self.b1['exp'].haystack))

        self.ui.b1_mainList.clear()
        def attach(node,parent):
            myself = QtWidgets.QTreeWidgetItem(parent)
            node.myTree = myself
            myself.setText(0, node.basename)
            myself.curve = node
            myself.setFlags(myself.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            myself.setCheckState(0,QtCore.Qt.Unchecked)
            for mychild in node:
                attach(mychild,myself)
        for node in self.b1['exp']:
            attach(node,self.ui.b1_mainList)

        for c in self.b1['exp'].haystack:
            c.open()
            progress.setValue(progress.value() + 1)
            QtCore.QCoreApplication.processEvents()
        self.ui.b1_forwardSegment.setMaximum( len(self.b1['exp'].haystack[0])-1 )
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

    def b1_invalid(self):
        threshold = float(self.ui.b1_minmax.value())
        xValue = float(self.ui.b1_yAlign.value())        
        for c in self.b1['exp'].haystack:
            try:
                istart,iend = self.b1GetZF(c[c.forwardSegment].z)
                iPoint = engine.np.argmin((c[c.forwardSegment].z[istart:iend]-xValue)**2)
                yOffset = engine.np.average( c[c.forwardSegment].f[iPoint-10:iPoint+10] )
                if engine.np.max(c[c.forwardSegment].f[istart:iend])<yOffset+threshold:
                    myself = c.myTree
                    newstate = QtCore.Qt.Unchecked
                    myself.setCheckState(0, newstate)
            except IndexError:
                continue

    def b1GetZF(self,z):
        zstart = float(self.ui.b1_start.value())
        zend = float(self.ui.b1_end.value())
        istart = engine.np.argmin( (z-zstart)**2 )
        iend = engine.np.argmin( (z-zend)**2 )
        return istart,iend

    def b1tob2(self):
        mysegs = []
        for c in self.b1['exp'].haystack:
            if c.myTree.checkState(0) == QtCore.Qt.Checked:
                try:
                    istart,iend = self.b1GetZF(c[c.forwardSegment].z)
                    s = engine.bsegment(c,c[c.forwardSegment].z[istart:iend],c[c.forwardSegment].f[istart:iend])
                    mysegs.append(s)                
                except IndexError:
                    continue
        self.b2['exp']=mysegs
        self.ui.switcher.setCurrentIndex(1)
        self.b2Init()

    def b1Color(self):
        alpha = int(self.ui.b1_Alpha.value())
        self.redPen = pg.mkPen( pg.QtGui.QColor(255, 0, 0,alpha),width=1)
        self.blackPen = pg.mkPen( pg.QtGui.QColor(0, 0, 0,alpha),width=1)
        self.b1Update()

    def b1Forward(self):
        num = int(self.ui.b1_forwardSegment.value())
        self.b1['exp'].setForwardSegment(num)
        self.b1Plot()

    def b1Plot(self):
        self.ui.b1_graph.plotItem.clear()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        progress = QtWidgets.QProgressDialog("Plotting all files...", "Cancel plotting", 0, len(self.b1['exp'].haystack))

        for c in self.b1['exp'].haystack:
            plit = pg.PlotCurveItem(clickable=True)
            self.ui.b1_graph.plotItem.addItem(plit)
            if len(c)>c.forwardSegment:
                plit.setData( c[c.forwardSegment].z,c[c.forwardSegment].f )
            else:
                plit.setData( [1000,3000,5000,8000],[0,1,-1,0] )
            plit.setPen(self.b1getPen(c.myTree))
            c.plit = plit
            plit.curve = c
            plit.sigClicked.connect(self.b1curveClicked)
        progress.setValue(len(self.b1['exp'].haystack))
        QtWidgets.QApplication.restoreOverrideCursor()

    def b1getPen(self,myself):

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

    def b1Update(self,myself=None,column=0):
        if myself is None or myself.curve.is_leaf() is False:
            for c in self.b1['exp'].haystack:
                c.plit.setPen(self.b1getPen(c.myTree))
        else:
            myself.curve.plit.setPen(self.b1getPen(myself))


    def b1curveClicked(self,pgCurve):
        myself = pgCurve.curve.myTree
        newstate = QtCore.Qt.Unchecked
        if myself.checkState(0) == QtCore.Qt.Unchecked:
            newstate = QtCore.Qt.Checked
        myself.setCheckState(0, newstate)

    def b1xCut(self):
        for c in self.b1['exp'].haystack:
            try:
                istart,iend = self.b1GetZF(c[c.forwardSegment].z)
                c.plit.setData( c[c.forwardSegment].z[istart:iend],c[c.forwardSegment].f[istart:iend] )
            except IndexError:
                continue


    def b1yAlign(self):
        xValue = float(self.ui.b1_yAlign.value())
        for c in self.b1['exp'].haystack:
            try:
                istart,iend = self.b1GetZF(c[c.forwardSegment].z)
                iPoint = engine.np.argmin((c[c.forwardSegment].z-xValue)**2)
                yOffset = engine.np.average( c[c.forwardSegment].f[iPoint-10:iPoint+10] )
                c.plit.setData( c[1].z[istart:iend],c[1].f[istart:iend]-yOffset)
            except IndexError:
                continue

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Chiaro2020')
    chiaro = curveWindow()
    chiaro.show()
    # QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())