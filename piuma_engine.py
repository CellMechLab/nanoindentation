import os
import numpy as np

def getLine(f,file=True):
    if file:
        text = f.readline()
    else:
        text = f
    return text.replace('\n','').replace('\r','').split('\t')

def getTarget(f,target):
    while True:
        dx = getLine(f)
        if dx[0][:len(target)]==target:
            return dx

class protsegment(object):
    def __init__(self,line = None):
        if line is None:
            self.aim = None
            self.duration = None
        else:
            self.aim = float(line[1].replace(',','.'))
            self.duration = float(line[3].replace(',','.'))

class psegment(object):
    def __init__(self,x=None,y=None):
        if (x[-1]<x[0]):
            x.reverse()
            y.reverse()
        x = np.array(x)
        y = np.array(y)
        #x,y = np.sort(np.array([x,y]),axis=1) #simplify curve
        self.z = x
        self.f = y
        self.poisson = 0.5
        self.tipradius = 0.0
        self.E = 0.0

    def hertz(self,x, E=None):
        if E is None:
            E = self.E
        radius = self.tipradius*1000.0 #express everything in nm
        Eeff = E/1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
        y = (4.0/3.0) * (Eeff /(1-self.poisson**2)) * np.sqrt(radius * x**3 )
        return y #y will be in nN

    def getJ(self,xmin=None,xmax=None):
        if xmin is None:
            jmin = 0
        else:
            jmin = self.getPoint(xmin,mode='nearest',getindex=True)
        if xmax is None:
            jmax = 0
        else:
            jmax = self.getPoint(xmax,mode='nearest',getindex=True)
        return jmin,jmax

    def getE(self,xmin=None,xmax=None):
        from scipy.optimize import curve_fit
        jmin,jmax = self.getJ(xmin,xmax)

        seeds = [1000.0]
        #NB the curve is forced to have F=0 at indentation 0
        popt, pcov = curve_fit(self.hertz, np.abs(self.z[jmin:jmax]-self.z[jmin]), self.f[jmin:jmax]-self.f[jmin] , p0=seeds,maxfev=10000)
        self.E = popt[0]
        return self.E

    def getPoint(self,val,dir='X',order=0,win=None,mode='left',ret=0,getindex=False):
        #modes are left, right, nearest
        #ret is the order of the derivative from which to return the point
        if dir == 'X':
            check = self.z
        else:
            if order == 0:
                check = self.f
            else:
                check = self.getDerivative(order,win)
        if mode == 'left':
            got = -1
        else:
            got = 0
        if mode == 'left':
            for i in range(len(check)-1):
                if (check[i]<=val<check[i+1]) or (check[i]>=val>check[i+1]):
                    got = i
                    break
        elif mode == 'right':
            for i in range(len(check),1,-1):
                if (check[i]<=val<check[i-1]) or (check[i]>=val>check[i-1]):
                    got = i
                    break
        else:
            check = np.array(check)
            got = np.argmin(np.abs(check-val))
        if getindex:
            return got
        x = self.z[got]
        if ret == 0:
            y = self.f[got]
        else:
            y = self.getDerivative(ret,win)[got]
        return (x,y)

    def getDerivative(self,order,win=None):
        from scipy.signal import savgol_filter as sg
        if win is None:
           win = max(len(self.f)/100,10)
        if win % 2 == 0:
            win+=1
        return sg(self.f,win,order+2,deriv=order,mode='nearest')

    def getZ(self,force):
        for i in range(len(self.f)-1):
            if ( self.f[i]<=force and self.f[i+1]>force ) or (self.f[i]>=force and self.f[i+1]<force):
                return self.z[i]
        return self.z[-1]

class pscan(object):
    def __init__(self,filename = None):
        self.snumber = 0
        self.xi = 0
        self.yi = 0
        self.dx = 0.0
        self.dy = 0.0
        self.tipradius=0.0
        self.curves = []
        self.matrix = []
        if filename is not None:
            self.dir = os.path.dirname(str(filename))
            self.guess(str(filename))

    def guessDir(self):
        import glob
        fili = glob.glob(os.path.join (self.dir,self.basename + ' S-{0} X-*'.format(self.snumber)))

        for f in fili:
            self.add(f)
        xis=[]
        yis=[]
        for cv in self.curves:
            xis.append(cv.xi)
            yis.append(cv.yi)
        self.xi = max(xis)
        self.yi = max(yis)
        for i in range(self.xi):
            riga = []
            for j in range(self.yi):
                riga.append(None)
            self.matrix.append(riga)
        for cv in self.curves:
            self.matrix[cv.xi-1][cv.yi-1]=cv
        hm = 0.0
        dx = 0.0
        for j in range(self.yi):
            for i in range(1,self.xi):
                if (self.matrix[i][j] is not None) and (self.matrix[i-1][j] is not None):
                    dx+=self.matrix[i][j].x-self.matrix[i-1][j].x
                    hm+=1.0
        if hm > 0:
            self.dx = dx/hm
        hm = 0.0
        dy = 0.0
        for i in range(self.xi):
            for j in range(1,self.yi):
                if (self.matrix[i][j] is not None) and (self.matrix[i][j-1] is not None):
                    dy+=self.matrix[i][j].y-self.matrix[i][j-1].y
                    hm+=1.0
        if hm > 0:
            self.dy = dy/hm

    def guess(self,filename):
        try:
            f = open(filename,'r')
            self.date = getLine(f)[1]
            self.basename = getLine(f)[0]
            self.snumber = int(getLine(f)[1].replace(',','.'))
            self.k = float(getTarget(f,'k (N/m)')[1].replace(',','.'))
            self.tipradius = float(getTarget(f,'Tip radius (um)')[1].replace(',','.'))
            self.calib = float(getTarget(f, 'Calibration factor')[1].replace(',','.'))

            getTarget(f,'Piezo Indentation Sweep Settings')
            self.protocol = []
            for i in range(7):
                riga = getLine(f)
                if riga[1]!='NaN':
                    self.protocol.append( protsegment( riga ) )
            f.close()

        except:
            print('An error occurred while opening the file')
            raise

    def add(self,filename,load=False):
        p = pcurve(filename,load=load)
        self.curves.append(p)

class pcurve(object):
        def __init__(self,filename=None,load=True):
            #Time (s)	Load (uN)	Indentation (nm)	Cantilever (nm)	Piezo (nm)
            self.time = [] #from the beginning, in s
            self.f = [] #load, to be stored in nN while they are saved in uN
            self.d = [] #cantilever deflection in nm ; load and cantilever are the same but a multiplication coefficient
            self.z = [] #piezo position, in nm
            self.xi=0
            self.yi=0
            self.x=0.0
            self.y=0.0
            self.color = None
            self.filename = filename
            if filename is not None:
                self.guess()
            if load is True:
                self.load()

        def guess(self,filename = None):
            if filename is not None:
                self.filename = filename
            self.filename = str(self.filename)
            basename = os.path.basename(self.filename)
            f = open(self.filename,'r')
            self.date = getLine(f)[1]
            self.basename = getLine(f)[0]
            iii = getLine(f)
            self.si = int(iii[1].replace(',','.'))
            self.xi = int(iii[3].replace(',','.'))
            self.yi = int(iii[5].replace(',','.'))
            self.ii = int(iii[7].replace(',','.')) #index of the indentation
            self.x = float(getTarget(f,'X-position (um)')[1].replace(',','.'))
            self.y = float(getTarget(f,'Y-position (um)')[1].replace(',','.'))
            self.k = float(getTarget(f,'k (N/m)')[1].replace(',','.'))
            self.tipradius = float(getTarget(f,'Tip radius (um)')[1].replace(',','.'))
            self.calib = float(getTarget(f, 'Calibration factor')[1].replace(',','.'))
            f.close()

        def load(self):
            f = open(self.filename)
            getTarget(f,'Time (s)')
            while True:
                line = f.readline()
                if line == '':
                    break
                self.parseLine(line)

        def createSegments(self,protocol):
            nodi = self.getNodes(protocol)
            self.segments = []
            for i in range(len(nodi)-1):
                self.segments.append(psegment(self.z[nodi[i]:nodi[i+1]],self.f[nodi[i]:nodi[i+1]]))
            for s in self.segments:
                s.tipradius = self.tipradius

        def getNodes(self,protocol):
            vs = []
            for s in protocol:
                vs.append([s.aim,s.duration])
            nodi = []
            nodi.append(0)
            j=0
            nexttime = vs[j][1]
            nextvalue = vs[j][0]
            timefound = False
            valuefound = False
            for i in range(len(self.time)):
                if i==len(self.time)-1:
                    nodi.append(i)
                else:
                    if self.time[i]<=nexttime and self.time[i+1]>nexttime:
                        timefound = True
                    if (self.z[i]<=nextvalue and self.z[i+1]>nextvalue) or (self.z[i]>=nextvalue and self.z[i+1]<nextvalue):
                        valuefound = True
                if timefound and valuefound:
                    nodi.append(i)
                    nexttime = self.time[i]
                    timefound=False
                    valuefound=False
                    if (j+1 == len(vs)):
                        nodi.append(len(self.time)-1)
                        break
                    else:
                        j+=1
                        nexttime += vs[j][1]
                        nextvalue = vs[j][0]
            return nodi

        def parseLine(self,line):
            p = getLine(line,False)
            self.time.append(float(p[0].replace(',','.')))
            self.f.append(float(p[1].replace(',','.'))*1000.0) #convert uN to nN
            self.d.append(float(p[3].replace(',','.')))
            self.z.append(float(p[4].replace(',','.')))
