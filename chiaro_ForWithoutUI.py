import sys, os
import mvexperiment.experiment as experiment
import engine
import pickle
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import csv

class curveWindow():
    def __init__(self, parent=None):

        # self.redPen = pg.mkPen( pg.QtGui.QColor(255, 0, 0,30),width=1)
        # self.blackPen = pg.mkPen( pg.QtGui.QColor(0, 0, 0,30),width=1)
        # self.greenPen = pg.mkPen( pg.QtGui.QColor(0, 255, 0,255),width=2)
        # self.nonePen = pg.mkPen(None)
        self.workingdir = './'

        self.b1 = {'phase':1,'forwardSegment':1,'exp':[]}
        self.b2 = {'phase':2,'exp':[],'plit1a':None,'plit1b':None,'plit2':None}
        self.b3 = {'phase':3,'exp':[],'plit1':None,'plit2a':None,'plit2b':None}
        self.b4 = {'phase':4,'exp':[],'Manlio':None,'avcurve':None,'avstress':None}
        self.segmentLength = 100
        self.b2_index_invalid = []
        self.MakeInvalidInvisible = False

        self.Switcherindex=0
        #self.ui.sl_load.clicked.connect(self.load_pickle)
        #self.ui.b1_generate.clicked.connect(self.generateFake)

    ################################################
    ############## SL actions ######################
    ################################################

    def generateFake(self):
        a = panels.Fakedata()
        if a.exec() == 0:
            return

        mysegs = []
        noise = float(a.noiselevel.value())/1000.0
        E1 = float(a.E1.value())/1.0e9
        R = 3000.0
        N = int(a.length.value())
        xbase = engine.np.linspace(0,N,N)
        for i in range(50):
            mysegs.append(engine.bsegment())
            mysegs[-1].R = R
            mysegs[-1].indentation = xbase
            if a.el_one.isChecked() is True:
                mysegs[-1].touch = engine.noisify(engine.standardHertz(xbase,E1,R),noise)
            else:                
                E2 = float(a.E2.value())/1.0e9
                h  = float(a.d0.value())
                if a.modAli.isChecked() is True:
                    mysegs[-1].touch = engine.noisify(engine.LayerStd(xbase,E1,E2,h,R),noise)
                else:
                    #mysegs[-1].touch = engine.noisify(engine.LayerRoss(xbase,E1,E2,h,R),noise)
                    data = engine.np.loadtxt('MyFile.txt')
                    x = data[:, 0]
                    y = data[:, 1]
                    mysegs[-1].indentation = x
                    mysegs[-1].touch = engine.noisify(y / 1000.0, noise)
                    # mysegs[-1].touch = engine.noisify(engine.LayerRoss(xbase,E1,E2,h,R),noise)

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
    ############## b3 actions ######################
    ################################################

    
    #def b3Init(self):
        #print('why b3init?')
        #pass
        #vals = engine.np.hstack([engine.np.random.normal(size=500), engine.np.random.normal(size=260, loc=4)])
        #y,x = engine.np.histogram(vals, bins=engine.np.linspace(-3, 8, 40))
        #e0,w,A,nx,ny = engine.gauss(x,y)

        ##self.b3_ShiftAllCurves()
        #self.b3Fit()
        #self.b3_Alistography
        #self.b3_CreateCpShiftArray
        ##self.save_pickle
        #self.b3Export
        #self.b3Export2(fit=False)
        #self.b3Export2(fit=True)

    def b3_Alistography(self, params=[30, 500, 2000]):
        grainstep = int( params[0] )
        scaledistance = float( params[1] )
        maxind = float( params[2] )
        xx=[]
        yy=[]
        E0h=[]
        Ebh=[]
        d0h=[]
        for s in self.b3['exp']:
            Ex,Ey = engine.Elastography2withMax( s,grainstep,scaledistance,maxind)
            if Ex is None:
                continue
            s.ElastX = Ex
            s.ElastY = Ey
            pars_i, covs_i = engine.fitExpDecay(Ex,Ey,s.R)
            if pars_i is not None:
                E0h.append(pars_i[0]*1e9)
                Ebh.append(pars_i[1]*1e9)
                d0h.append(pars_i[2])
            xx.append(Ex)
            yy.append(Ey)
        xmed,ymed, yerr = engine.getMedCurve(xx,yy,loose = True, error=True)
        pars, covs = engine.fitExpDecay(xmed, ymed, s.R, sigma=yerr)
        if any(engine.np.isnan(xmed))== False and any(engine.np.isnan(ymed))==False:
            self.xmed=xmed
            self.ymed=ymed
        if any(engine.np.isnan(pars))== False:
            self.pars=pars
            self.covs=covs
        if any(engine.np.isnan(E0h)) == False:
            self.E0h=E0h
        if any(engine.np.isnan(Ebh)) == False:
            self.Ebh=Ebh
        if any(engine.np.isnan(d0h)) == False:
            self.d0h=d0h
        return pars, covs, xmed, ymed*1e9, E0h,Ebh,d0h

    def b3Export(self, fname=None):
        if fname is None:
            pass
        elif self.Earray is None:
            pass
        else:
            print('Saving data!')
            Earray = self.Earray
            engine.np.savetxt(fname,Earray)

    def b3Export2(self, fit=False, fname=None):
        data_Bilayer=[self.E0h, self.Ebh, self.d0h]
        data_Fit= [self.xmed, self.ymed*1e9, self.pars, self.covs]
        with open(fname,'w') as f:
            if fit is True:
                data=data_Fit
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit params E0, Eb, d0",data[2][0], data[2][1], data[2][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit std dev E0, Eb, d0", data[3][0], data[3][1], data[3][2]))
                f.write('Ex\tEy\n')
            else:
                data=data_Bilayer
                f.write('E0\tEb\td0\n')
            for i in range(len(data[0])):
                if fit is True:
                    f.write('{}\t{}\n'.format(data[0][i],data[1][i]))
                else:
                    f.write('{}\t{}\t{}\n'.format(data[0][i],data[1][i],data[2][i]))
            f.close()

    def b3_ShiftAllCurves(self, shift=None):
        if shift == False:
            shift=int(self.ui.b3_ShiftValue.value())
        self.shift=shift
        #changed the way this works!!!
        for s in self.b3['exp']:
            #s.offsetX=s.offsetX_original
            #s.offsetY=s.offsetY_original
            s.offsetX=s.offsetX+shift
            ind=engine.np.argmin(engine.np.abs(s.z - s.offsetX))
            s.offsetY=s.ffil[ind]
            s.indentation, s.touch = engine.calculateIndentation(s)
        self.b3Update()
        self.b3Fit()
        self.b3_Alistography()

    def b3_CreateCpShiftArray(self):
        min_shift=int(self.ui.b3_ShiftArrayMin.value())
        max_shift = int(self.ui.b3_ShiftArrayMax.value())
        step_shift = int(self.ui.b3_ShiftArrayStep.value())
        file=str(self.ui.b3_ShiftArrayFile.text())
        shifts=range(min_shift,max_shift+step_shift,step_shift)
        Eys_norm=[]
        len_Ey_norm=[]
        folder=str(os.path.dirname(os.path.abspath(__file__)))
        fname =folder + '\ArrayData' + '\ArrayData_' + file + '.csv'
        header=['shift', 'E0', 'Eb', 'd0', 'Ex','Ey']
        with open(fname, 'w', newline='') as myfile:
            wr = csv.writer(myfile, delimiter=',')
            wr.writerow(header)
            for shift in shifts:
                self.b3_ShiftAllCurves(shift)
                tosave_i=[shift, self.E0h, self.Ebh, self.d0h, list(self.xmed), list(self.ymed)]
                wr.writerow(tosave_i)
                start_norm = int(float(self.ui.b4_elDash.value()) / int(self.ui.b4_elIncrement.value())) - 1
                ymed_min=min(self.ymed[start_norm:])
                ymed_max=max(self.ymed[start_norm:])
                ymed_norm=[]
                ymed_norm_means=[]
                for y in self.ymed[start_norm:]:
                    ymed_norm_i=float((y-ymed_min)/(ymed_max-ymed_min))
                    for i in range(10):
                        ymed_norm.append(ymed_norm_i)
                if len(ymed_norm) > 1000:
                    for i in range(0, len(ymed_norm)-1, 200):
                        ymed_norm_i=engine.np.mean(ymed_norm[i:i+1])
                        ymed_norm_means.append(ymed_norm_i)
                    ymed_norm=ymed_norm_means
                #ymed_norm=[(y-ymed_min)/(ymed_max-ymed_min) for y in self.ymed]
                for i in range(10):
                    Eys_norm.append(ymed_norm)#engine.np.asarray(ymed_norm))
                    len_Ey_norm.append(len(ymed_norm))
        min_len=min(len_Ey_norm)
        for i,x in enumerate(Eys_norm):
            Eys_norm[i]=Eys_norm[i][:min_len]
        imname = folder + '\ArrayData' + '\ArrayData_' + file + '.png'
        plt.imsave(imname, engine.np.asarray(Eys_norm), cmap=cm.jet)
        self.ui.b3_ShiftArrayImage.setPixmap(QtGui.QPixmap(imname))

    def b3Fit(self, params=[0, 1000]):
        mode=params[0]
        threshold=float(params[1])
        if mode==0: #maxIndentation
            for s in self.b3['exp']:
                if engine.np.max(s.indentation)<threshold:
                    s.valid = False
                else:
                    s.valid = True
                    s.indMax = engine.np.argmin((s.indentation - threshold)**2 )
        else: #maxForce
            for s in self.b3['exp']:
                if engine.np.max(s.touch)<threshold:
                    s.valid = False
                else:
                    s.valid=True
                    s.indMax = engine.np.argmin( (s.touch - threshold)**2 )
        Earray = []
        for s in self.b3['exp']:
            if s.valid is True:
                s.E = engine.fitHertz(s)
                if s.E is not None:
                    Earray.append(s.E*1e9)
        if any(engine.np.isnan(Earray))==False:
            self.Earray=Earray
        return Earray


    ################################################
    ############## b2 actions ######################
    ################################################

    def b2Init(self):
        for s in self.b2['exp']:
            s.phase = 2
            s.z_original=s.z
            s.f_original=s.f
            s.bol_deriv = None
            s.invalid = False
            s.bol=True
            s.ElastX= None
            s.x_CPderiv=[0]
            s.y_CPderiv=[0]
            s.threshold_exp = 0

        ##s = self.b2['exp'][0]
        ##self.save_pickle()
        # self.b2Filter()
        # #self.b2_crop()
        # self.b2_contactPoint()
        # self.b2_Alistography()
        # self.b2tob3()

    def b2tob3(self):
        for s in self.b2['exp']:
            if s.invalid is False:
                self.b3['exp'].append(s)
        print('Calculating indentation!')
        for s in self.b3['exp']:
            s.indentation,s.touch = engine.calculateIndentation(s)
            s.offsetX_original=s.offsetX
            # s.indentation_original=s.indentation
            # s.touch_original=s.touch
        self.SwitcherIndex = 2

    def b2_Alistography(self, fit=False, params=[30, 50, 2000, 301]):
        grainstep = int(params[0])
        scaledistance = float(params[1])
        maxind = float(params[2])
        filwin = int(params[3])

        cdown = 10
        xx = []
        yy = []

        E0h = []
        Ebh = []
        d0h = []
        print('Filtering curves by rising E(z)!')
        for s in self.b2['exp']:
            if s.invalid is False:
                s.indentation, s.touch = engine.calculateIndentation(s)
                Ex, Ey = engine.Elastography2withMax(s, grainstep, scaledistance, maxind)
                if Ex is None:
                    continue
                s.ElastX = Ex
                s.ElastY = Ey
                s.ElaInvalid, s.filEla =engine.InvalidCurvesFromElasticityRise(s,win=filwin)
                if s.ElaInvalid == True:
                    s.invalid=True

    def b2Filter(self, params=[0.4, 30, 25]):
        pro = float(params[0])
        winperc = float(params[1])/10.0
        thresh = int(params[2])
        print("Filtering curves!")
        for s in self.b2['exp']:
            s.ffil = engine.filterOsc(s.f,pro=pro,winperc=winperc,threshold=thresh)
            s.ffil_original=s.ffil

    # def b2_crop(self):
    #     a = panels.CropCurves()
    #     if(a.exec()==0):
    #         return
    #     QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    #     front = int(a.CropStart.value())
    #     back = int(a.CropEnd.value())
    #     for s in self.b2['exp']:
    #         s.z=s.z_original
    #         s.ffil =s.ffil_original
    #         s.f=s.f_original
    #         s.z=s.z[front:-(back+1)]
    #         s.ffil=s.ffil[front:-(back+1)]
    #         s.f=s.f[front:-(back+1)]

    def b2_contactPoint(self, mode, params=[100, 1.5, 10]):
        minY=int(params[0])
        offset=float(params[1])/1000.0
        threshold_invalid=float(params[2])

        if mode==0: #=='Chiaro':
            pass
            # a = panels.chiaroPoint()
            # if a.exec()==0:
            #     return
            # p = a.getParams()
            # f = a.getCall()
            # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # if f is not None:
            #     for s in self.b2['exp']:
            #         s.invalid = False
            #         s.offsetX, s.offsetY = f(s, *p)
            #         if (s.offsetX, s.offsetY) == (0,0):
            #             s.invalid = True
        elif mode==1: #=='eeff':
            self.threshold_quot=offset
            print("Finding Contact Point by Eeff!")
            for s in self.b2['exp']:
                s.invalid = False
                s.offsetX, s.offsetY, s.quot = engine.eeffOffset(s, minY, offset)
                s.bol2 = engine.Nanosurf_FindInvalidCurves(s, threshold_invalid)
                if (s.offsetX, s.offsetY) == (0,0) or s.bol2==False:
                    s.invalid = True

        elif mode==2: #=='Nanosurf':
            pass
            # a = panels.NanosurfPoint()
            # if a.exec()==0:
            #     return
            # p = a.getParams()
            # f = a.getCall()
            # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # if f is not None:
            #     for s in self.b2['exp']:
            #         s.invalid = False
            #         s.bol, s.offsetX, s.offsetY, s.x_CPderiv, s.y_CPderiv = f(s,*p)
            #         s.offsetX_original=s.offsetX
            #         s.offsetY_original=s.offsetY
            #         if s.bol is True:
            #             s.bol2=engine.Nanosurf_FindInvalidCurves(s, p[-1])
            #         else:
            #             s.bol2=None
            #         if s.bol is False or s.bol2 is False:
            #             s.invalid = True
        elif mode==3: #=='Nanosurf Deriv':
            pass
            # a = panels.NanosurfPointDeriv()
            # if a.exec()==0:
            #     return
            # p = a.getParams()
            # f = a.getCall()
            # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # if f is not None:
            #     for s in self.b2['exp']:
            #         s.invalid = False
            #         s.bol_deriv, s.offsetX, s.offsetY, s.z0s, s.ymax, s.x_slopes, s.slopes = f(s,*p)
            #         s.offsetX_original=s.offsetX
            #         s.offsetY_original=s.offsetY
            #         # if s.bol_deriv is True:
            #         #     s.bol2=engine.Nanosurf_FindInvalidCurves(s, p[-1])
            #         # else:
            #         #     s.bol2=None
            #         if s.bol_deriv is False:# or s.bol2 is False:
            #             s.invalid = True







    ################################################
    ############## b1 actions ######################
    ################################################

    def b1SelectDir(self, fname=None, mode=None, forward_segment=0):
        if fname[0] =='':
            return
        self.workingdir = fname
        if mode==0:
            self.b1['exp'] = experiment.Chiaro(fname)
        elif mode==1:
            self.b1['exp'] = experiment.ChiaroGenova(fname)
        elif mode==2:
            self.b1['exp'] = experiment.NanoSurf(fname)
        self.b1['exp'].browse()
        print("Opening files!")
        for c in self.b1['exp'].haystack:
            c.open()
        self.b1Forward(forward_segment=forward_segment)
        self.b1tob2()

    def b1tob2(self):
        mysegs = []
        for c in self.b1['exp'].haystack:
            try:
                s = engine.bsegment(c,c[c.forwardSegment].z,c[c.forwardSegment].f)
                mysegs.append(s)
            except IndexError:
                continue
        self.b2['exp']=mysegs
        self.Switcherindex=1
        self.b2Init()

    def b1Forward(self, forward_segment=0):
        self.b1['exp'].setForwardSegment(forward_segment)
