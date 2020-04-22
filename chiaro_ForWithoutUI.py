import sys, os
import mvexperiment.experiment as experiment
import engine
import pickle
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import csv

class curveWindow():
    def __init__(self, parent=None):
        self.workingdir = './'

        self.b1 = {'phase':1,'forwardSegment':1,'exp':[]}
        self.b2 = {'phase':2,'exp':[],'plit1a':None,'plit1b':None,'plit2':None}
        self.b3 = {'phase':3,'exp':[],'plit1':None,'plit2a':None,'plit2b':None}
        self.b4 = {'phase':4,'exp':[],'Manlio':None,'avcurve':None,'avstress':None}
        self.segmentLength = 100
        self.b2_index_invalid = []
        self.MakeInvalidInvisible = False
        self.Switcherindex=0
    ################################################
    ############## SL actions ######################
    ################################################

    def generateFake(self, params=[0, 4000,  20000, 2000, 300, 1, 50]):
        mysegs = []
        mode=params[5]
        num_curves=params[6]
        noise = float(params[0])/1000.0
        R = 3000.0
        N = int(params[1])
        xbase = engine.np.linspace(0,N,N)
        E1 = float(params[2])/1.0e9
        E2 = float(params[3]) / 1.0e9
        h = float(params[4])
        if mode ==1:
            data = engine.np.loadtxt('Lambda_AllDataRos.txt') #'nanoindentation\MyFile.txt')#'nanoindentation\Lambda_AllDataRos.txt')  # ('MyFile.txt')
            for i in range(int(len(data[0,:])/2)):
                mysegs.append(engine.bsegment())
                mysegs[-1].R = R
                mysegs[-1].indentation = xbase
                x = data[:,i*2]
                y = data[:,i*2+1]
                if x[1]<0.000001:
                    x=x*1e9
                if y[1]<0.000001:
                    y=y*1e12
                mysegs[-1].indentation = x
                mysegs[-1].touch = engine.noisify(y/1000.0,noise)
        elif mode==0:
            R = 3200.0
            data = engine.np.loadtxt('alldata3.txt')#('MyFile.txt')
            for i in range(num_curves):
                mysegs.append(engine.bsegment())
                mysegs[-1].R = R
                mysegs[-1].indentation = xbase
                x = data[:, 0]*1e9
                y = data[:, 1]*1e9
                mysegs[-1].indentation = x
                mysegs[-1].touch = engine.noisify(y, noise)
        elif mode==2:
            for i in range(num_curves):
                if num_curves>1:
                    Eact = engine.random.gauss(E1, noise * E1 / 10.0)
                else:
                    Eact= E1
                mysegs.append(engine.bsegment())
                mysegs[-1].R = R
                mysegs[-1].indentation = xbase
                mysegs[-1].touch = engine.noisify(engine.standardHertz(xbase,Eact,R),noise)
        self.b3['exp'] = mysegs

    def load_pickle(self, fname):
        with open(fname, 'rb') as f:
            data = pickle.load(f)
        if data[0].phase == 2:
            self.b2['exp']=data
        elif data[0].phase == 3:
            self.b3['exp']=data
        elif data[0].phase == 4:
            self.b4['exp']=data

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
                s.E, std = engine.fitHertz(s)
                if s.E is not None:
                    Earray.append(s.E*1e9)
        if any(engine.np.isnan(Earray))==False:
            self.Earray=Earray

        bins = 'auto'
        y, x = engine.np.histogram(Earray, bins=bins, density=True)
        if len(y) >= 3:
            self.histox=x
            self.histoy=y
            try:
                e0, w, A, nx, ny = engine.gauss(x, y)
                self.gaussx=nx
                self.gaussy=ny
                w = w / engine.np.sqrt(len(Earray))
                self.gaussE0=e0
                self.gaussE0std=w
            except:
                self.gaussx=None
                self.gaussy=None
                self.gaussE0=None
                self.gaussE0std=None
        else:
            self.histox = engine.np.mean(Earray)
            self.histoy = 1
            self.gaussx = None
            self.gaussy = None
            self.gaussE0 = None
            self.gaussE0std = None
        R = self.R
        E = engine.np.average(Earray) / 1e9
        if mode==0:
            x, y = engine.getHertz(E, R, threshold, indentation=True)
        if mode==1:
            x, y = engine.getHertz(E, R, threshold, indentation=False)
        self.HertzFit_x=x
        self.HertzFit_y=y
        return Earray

    def b3_HertzFitOfAverage(self, params=[0, 1000, 'yeserror']):
        mode=params[0]
        threshold=int(params[1])
        modeError=params[2]
        xx=[]
        yy=[]
        Rs=[]
        for s in self.b3['exp']:
            xx.append(s.indentation[:threshold])
            yy.append(s.touch[:threshold])
            Rs.append(s.R)
        self.R = engine.np.mean(Rs)
        if modeError=='noerror':
            for s in self.b3['exp']:
                s.E, std = engine.fitHertz(s)
                self.Y=s.E
                self.Y_std=std
            self.fxmed = engine.np.asarray(self.b3['exp'][0].indentation[:threshold])
            self.fymed= engine.np.asarray(self.b3['exp'][0].touch[:threshold])
            self.fyerr = engine.np.asarray([0])

            #
            # fxmed= engine.np.asarray(self.b3['exp'][0].indentation[:threshold])
            # fymed= engine.np.asarray(self.b3['exp'][0].touch[:threshold])
            # a= engine.np.isnan(fxmed)
            # b = engine.np.isnan(fymed)
            # print(a, b)
            # self.Y, self.Y_std = engine.fitHertz(self, fxmed, fymed, error=None)
            # #self.fxmed=fxmed
            # #self.fymed=fymed
            # self.fyerr=None
        else:
            self.fxmed, self.fymed, self.fyerr = engine.getMedCurve(xx, yy, loose=True, error=True)
            print(self.fxmed)
            print(self.fymed)
            self.Y, self.Y_std=engine.fitHertz(self, self.fxmed, self.fymed, error=self.fyerr)
        self.avhertzfitx, self.avhertzfity = engine.getHertz(self.Y, self.R, threshold, indentation=True)

    def b3_Alistography(self, params=[30, 500, 2000, 15000, 'yeserror']):
        grainstep = int( params[0] )
        scaledistance = int( params[1] )
        maxind = float( params[2] )
        threshold_oscillation=float(params[3])
        mode=str(params[4])
        xx=[]
        yy=[]
        Rs=[]
        E0h=[]
        Ebh=[]
        d0h=[]
        E0h_std=[]
        Ebh_std=[]
        d0h_std=[]
        self.d01 = []
        self.std_d01 = []
        for s in self.b3['exp']:
            Ex,Ey = engine.Elastography2withMax( s,grainstep,scaledistance,maxind)
            if Ex is None:
                continue
            s.ElastX = Ex
            s.ElastY = Ey
            pars1, covs1= engine.fitExpSimple(Ex,Ey,s.R)
            if pars1 is not None:
                if pars1[0]>0 and pars1[0]<1000000:
                    E0h.append(pars1[0]*1e9)
                    E0h_std.append(covs1[0]*1e9)
                if pars1[1] > 0 and pars1[1] < 1000000:
                    Ebh.append(pars1[1]*1e9)
                    Ebh_std.append(covs1[1] * 1e9)
                if pars1[0] > 0 and pars1[0] < 1000000:
                    d0h.append(pars1[2])
                    d0h_std.append(covs1[2])
                self.d01.append(pars1[2])
                self.std_d01.append(engine.np.sqrt(covs1[2]))
            xx.append(Ex)
            yy.append(Ey)
            Rs.append(s.R)
        self.R=engine.np.mean(Rs)
        if mode=='noerror':
            xmed= engine.np.asarray(Ex)
            ymed= engine.np.asarray(Ey)
            yerr= None
            pars1, covs1 = engine.fitExpSimple(xmed, ymed, self.R)#engine.np.asarray(Ex), engine.np.asarray(Ey), self.R)
            self.fit1 = engine.ExpDecay(xmed, *pars1, self.R)
        else:
            xmed, ymed, yerr = engine.getMedCurve(xx, yy, loose=True, error=True)
            pars1, covs1 = engine.fitExpSimple(xmed, ymed, self.R, sigma=yerr)
            self.fit1 = engine.ExpDecay(xmed, *pars1, self.R)
        self.E0=pars1[0]
        self.Eb=pars1[1]
        self.d0=pars1[2]
        print(self.E0, self.Eb, self.d0)
        if any(engine.np.isnan(xmed))== False and any(engine.np.isnan(ymed))==False:
            self.xmed=xmed
            self.ymed=ymed
            self.yerr=yerr
            self.Emean_elasto=engine.np.mean(ymed)
            if yerr is not None:
                self.Emeanstd_elasto = engine.np.mean(yerr)
            else:
                self.Emeanstd_elasto = engine.np.std(ymed)
        if any(engine.np.isnan(pars1))== False:
            self.pars1=pars1
            self.covs1=covs1
        if any(engine.np.isnan(E0h)) == False:
            self.E0h=E0h
            self.E0h_std=E0h_std
        if any(engine.np.isnan(Ebh)) == False:
            self.Ebh=Ebh
            self.Ebh_std=Ebh_std
        if any(engine.np.isnan(d0h)) == False:
            self.d0h=d0h
            self.d0h_std=d0h_std

        med = engine.np.average(ymed)
        ymedline = engine.np.ones(len(xmed)) * med * 1e9
        self.medlinex = xmed
        self.medliney = ymedline

        bins = 'auto'
        y, x = engine.np.histogram(ymed*1e9, bins=bins, density=True)
        if len(y) >= 3:
            self.elastohistox=x
            self.elastohistoy=y
            try:
                e0, w, A, nx, ny = engine.gauss(x, y)
                self.elastogaussx=nx
                self.elastogaussy=ny
                w = w / engine.np.sqrt(len(ymed*1e9))
                self.elastogaussE0=e0
                self.elastogaussE0std=w
            except:
                self.elastogaussx=None
                self.elastogaussy=None
                self.elastogaussE0=None
                self.elastogaussE0std=None
        else:
            self.elastogaussx = None
            self.elastogaussy = None
            self.elastogaussE0 = None
            self.elastogaussE0std = None
        return pars1, covs1, xmed, ymed*1e9, E0h,Ebh,d0h, self.R

    def b3_AlistographyFromForceMed(self, params=[30, 500, 2000, 15000]):
        grainstep = int( params[0] )
        scaledistance = int( params[1] )
        maxind = float( params[2] )
        threshold_oscillation=float(params[3])
        xx=[]
        yy=[]
        Rs=[]
        for s in self.b3['exp']:
            xx.append(s.indentation)
            yy.append(s.touch)
            Rs.append(s.R)
        self.R = engine.np.mean(Rs)
        fxmed, fymed, fyerr = engine.getMedCurve(xx, yy, loose=True, error=True)
        Ex, Ey = engine.Elastography2ForMedForce(fxmed, fymed, self.R, grainstep, scaledistance, maxind)
        Ex=engine.np.asarray(Ex)
        Ey=engine.np.asarray(Ey)
        pars1, covs1= engine.fitExpSimple(Ex, Ey, self.R)#, sigma=yerr)  # , cutoff=cutoff)
        self.E0 = pars1[0]
        self.Eb = pars1[1]
        self.d0 = pars1[2]
        self.fit1 = engine.ExpDecay(Ex, *pars1, self.R)


        if any(engine.np.isnan(fxmed))== False and any(engine.np.isnan(fymed))==False:
            self.fxmed=fxmed
            self.fymed=fymed
            self.fyerr=fyerr
        if any(engine.np.isnan(Ex))== False and any(engine.np.isnan(Ey))==False:
            self.xmed=Ex
            self.ymed=Ey
            self.yerr=fyerr
        if any(engine.np.isnan(pars1))== False:
            self.pars1=pars1
            self.covs1=covs1

        #return pars1, covs1, pars2, covs2, pars3, covs3, xmed, ymed*1e9, E0h,Ebh,d0h, self.R


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
        with open(fname,'w') as f:
            if fit is True:
                data_Fit = [self.xmed, self.ymed * 1e9, self.pars1, self.covs1]
                data=data_Fit
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 1 params E0, Eb, d0",data[2][0], data[2][1], data[2][2]))
                f.write('{}\t{}\t{}\t{}\n'.format("mean fit 1 std dev E0, Eb, d0", data[3][0], data[3][1], data[3][2]))
                f.write('Ex\tEy\n')
            else:
                data_Bilayer = [self.E0h, self.Ebh, self.d0h]
                data=data_Bilayer
                f.write('E0\tEb\td0\n')
            for i in range(len(data[0])):
                if fit is True:
                    f.write('{}\t{}\n'.format(data[0][i],data[1][i]))
                else:
                    f.write('{}\t{}\t{}\n'.format(data[0][i],data[1][i],data[2][i]))
            f.close()

    def b3ExportToCsvForPlots(self, fnames, settings):
        print('Saving data!')
        #[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData, fname_ElastoHistoData]=fnames
        data1a = []
        data1b = []
        data2a = []
        data2b = []
        for i, s in enumerate(self.b3['exp']):
            label_1a = ['d_' + str(i)]
            label_1b = ['F_' + str(i)]
            data_1a = label_1a + list(s.indentation)
            data_1b = label_1b + list(s.touch)
            label_2a = ['d_' + str(i)]
            label_2b = ['E_' + str(i)]
            data_2a = label_2a + list(s.ElastX)
            data_2b = label_2b + list(s.ElastY*1e9)
            data1a.append(data_1a)
            data1b.append(data_1b)
            data2a.append(data_2a)
            data2b.append(data_2b)
        data1c = ['HertzFit_d'] + list(self.HertzFit_x)
        data1d = ['HertzFit_F'] + list(self.HertzFit_y)
        if settings[5] is True:
            data1ia = ['fxmed'] + list(self.fxmed)
            data1ib = ['fymed'] + list(self.fymed)
            data1ic = ['fyerr'] + list(self.fyerr)
            data1id = ['fy+err'] + list((self.fymed + self.fyerr))
            data1ie = ['fy-err'] + list((self.fymed - self.fyerr))
            data1if = ['fit1x'] + list(self.avhertzfitx)
            data1ig = ['fit1y'] + list(self.avhertzfity)
            data1ih = ['HertzFit_average'] + [self.Y*1e9]
            data1ii = ['HertzFit_averagestd'] + [self.Y_std*1e9]
        data3a = ['xmed'] + list(self.xmed)
        data3b = ['ymed'] + list(self.ymed*1e9)
        if settings[7]=='noerror':
            data3c = ['yerr'] + [0]
            data3d = ['y+err'] + list(self.ymed*1e9)
            data3e = ['y-err'] + list(self.ymed*1e9)
        else:
            data3c = ['yerr'] + list(self.yerr*1e9)
            data3d = ['y+err'] + list((self.ymed + self.yerr)*1e9)
            data3e = ['y-err'] + list((self.ymed - self.yerr)*1e9)
        if settings[6]=='bilayer':
            data3f = ['fit1x'] + list(self.xmed)
            data3g = ['fit1y'] + list(self.fit1*1e9)
        if settings[6]=='single':
            data3f = ['fitlinx'] + list(self.medlinex)
            data3g = ['fitliny'] + list(self.medliney)
        data3h = ['E_mean_Elasto'] + [self.Emean_elasto*1e9]
        data3i = ['E_std_Elasto'] + [self.Emeanstd_elasto*1e9]
        data4a = ['Hertz_E0'] + [self.gaussE0]
        data4b = ['Hertz_E0std'] + [self.gaussE0std]
        data4bc = ['HistoHertz_data'] + list(self.Earray)
        if self.gaussx is not None:
            data4c = ['HistoHertz_x'] + list(self.histox)
            data4d = ['HistoHertz_y'] + list(self.histoy)
            data4e = ['GaussHertz_x'] + list(self.gaussx)
            data4f = ['GaussHertz_y'] + list(self.gaussy)
        else:
            data4c = ['HistoHertz_x']
            data4c.append(self.histox)
            data4d = ['HistoHertz_y']
            data4d.append(self.histoy)
            data4e = ['GaussHertz_x']
            data4f = ['GaussHertz_y']
        data4g = ['Elasto_E0'] + [self.elastogaussE0]
        data4h = ['Elasto_E0std'] + [self.elastogaussE0std]
        data4hi = ['HistoElasto_data'] + list(self.ymed*1e9)
        if self.elastogaussx is not None:
            data4i = ['HistoElasto_x'] + list(self.elastohistox)
            data4j = ['HistoElasto_y'] + list(self.elastohistoy)
            data4k = ['GaussElasto_x'] + list(self.elastogaussx)
            data4l = ['GaussElasto_y'] + list(self.elastogaussy)
        else:
            data4i = ['HistoElasto_x'] + [0]
            data4j = ['HistoElasto_y'] + [0]
            data4k = ['GaussElasto_x'] + [0]
            data4l = ['GaussElasto_y'] + [0]
        if settings[4] is True:
            data5c = ['E0_HistoElasto_dataE0'] + list(self.E0h)
            data5ci = ['E0_HistoElasto_dataE0_std'] + list(self.E0h_std)
            data5cb = ['Eb_HistoElasto_dataE0'] + list(self.Ebh)
            data5cbi = ['Eb_HistoElasto_dataE0_std'] + list(self.Ebh_std)
            data5cc = ['d0_HistoElasto_dataE0'] + list(self.d0h)
            data5cci = ['d0_HistoElasto_dataE0_std'] + list(self.d0h_std)

        if settings[0] is True:
            with open(fnames[0], mode='w', newline='') as f: #fname_IndentResultsData
                w = csv.writer(f)
                w.writerow(data1c)
                w.writerow(data1d)
                for i in range(len(data1a)):
                    w.writerow(data1a[i])
                    w.writerow(data1b[i])
        if settings[1] is True:
            with open(fnames[1], mode='w', newline='') as f: #fname_ElastoAllData
                w = csv.writer(f)
                for i in range(len(data2a)):
                    w.writerow(data2a[i])
                    w.writerow(data2b[i])
        if settings[2] is True:
            with open(fnames[2], mode='w', newline='') as f: #fname_ElastoResultsData
                w = csv.writer(f)
                w.writerow(data3a)
                w.writerow(data3b)
                w.writerow(data3c)
                w.writerow(data3d)
                w.writerow(data3e)
                w.writerow(data3f)
                w.writerow(data3g)
                w.writerow(data3h)
                w.writerow(data3i)
        if settings[3] is True:
            with open(fnames[3], mode='w', newline='') as f: #fname_HistoData
                w = csv.writer(f)
                w.writerow(data4a)
                w.writerow(data4b)
                w.writerow(data4bc)
                w.writerow(data4c)
                w.writerow(data4d)
                w.writerow(data4e)
                w.writerow(data4f)
                w.writerow(data4g)
                w.writerow(data4h)
                w.writerow(data4hi)
                w.writerow(data4i)
                w.writerow(data4j)
                w.writerow(data4k)
                w.writerow(data4l)
        if settings[4] is True:
            with open(fnames[4], mode='w', newline='') as f: #fname_ElastoHistoData
                w = csv.writer(f)
                w.writerow(data5c)
                w.writerow(data5ci)
                w.writerow(data5cb)
                w.writerow(data5cbi)
                w.writerow(data5cc)
                w.writerow(data5cci)
        if settings[5] is True:
            with open(fnames[5], mode='w', newline='') as f: #fname_AvHertzData
                w = csv.writer(f)
                w.writerow(data1ia)
                w.writerow(data1ib)
                w.writerow(data1ic)
                w.writerow(data1id)
                w.writerow(data1ie)
                w.writerow(data1if)
                w.writerow(data1ig)
                w.writerow(data1ih)
                w.writerow(data1ii)


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

    def b2_Alistography(self, fit=False, params=[30, 50, 2000, 301, 15000]):
        grainstep = int(params[0])
        scaledistance = float(params[1])
        maxind = float(params[2])
        filwin = int(params[3])
        thresh_osc = float(params[4])

        print('Filtering curves by rising E(z)!')
        for s in self.b2['exp']:
            if s.invalid is False:
                s.indentation, s.touch = engine.calculateIndentation(s)
                Ex, Ey = engine.Elastography2withMax(s, grainstep, scaledistance, maxind)
                if Ex is None:
                    continue
                s.ElastX = Ex
                s.ElastY = Ey
                s.ElaInvalid, s.filEla =engine.InvalidCurvesFromElasticityRise(s,win=filwin, scaledistance=int(scaledistance), threshold_oscillation=thresh_osc)
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


    def b2_crop(self, params=[100,100]):
        front = params[0]
        back = params[1]
        for s in self.b2['exp']:
            # s.z=s.z_original
            # s.ffil =s.ffil_original
            # s.f=s.f_original
            s.z=s.z[front:-(back+1)]
            s.ffil=s.ffil[front:-(back+1)]
            s.f=s.f[front:-(back+1)]



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

