from .mvFilesystem import MvNode
import numpy as np
from .curve import Segment

class DataSet(MvNode):
    _leaf_ext = ['.txt']

    def __init__(self, filename=None, parent = None):
        super().__init__(parent=parent,filename=filename)
        self._header = None
        self.cantilever_k = 1.0     #elastic constant of the cantilever in nN/nm
        self.cantilever_lever = 1.0 #calibration factor InvOls in nm/V
        self.cantilever_type = 'Colloidal probe'
        self.original_filename = None #the name of the file the text output was created from
        self.tip_radius = 1000.0    #radius of the tip, used for sphere, in nm
        self.tip_shape = 'sphere'   #honest shapes are 'sphere' , 'cone' , 'flat'
        self.data = {'time':[],'force':[],'deflection':[],'z':[]} #store for the full time tracks, add additional channels
        self.protocol = []          #a list of protsegments parameters
        self.protocol_speed = None  #in case a default speed was set and it is not readable from the segment
        self.version = None
        self.forwardSegment = 0
        self.hertz = {}
        self.hertz['threshold']=None
        self.hertz['thresholdType'] = 'indentation'
        self.xpos = None
        self.ypos = None
        self.valid = True

    def setRadius(self,value,recursive = True):
        self.tip_radius = value
        if recursive is True:
            for c in self.haystack:
                c.tip_radius = value

    def setForwardSegment(self,value,recursive=True):
        self.forwardSegment = value
        if recursive is True:
            for c in self.haystack:
                c.forwardSegment=value

    def open(self):
        self.header()
        self.load()
        self.createSegments()

    def check(self):
        #Implement this function to get a signature of the filetype (not only by the extension)
        return True #True = this is a known file, False otherwise

    def header(self):
        #Implement this function to populate the header, see the constructor for critical info
        pass

    def load(self):
        pass

    def createSegments(self):
        pass

    def doOpen(self):
        self.doAll(0)

    def doContact(self):
        self.doAll(1)
        self.doAll(2)

    def doIndentation(self):
        self.doAll(3)

    def doSmooth(self):
        self.doAll(5)

    def doHertz(self,th,tht='indentation'):
        self.hertz['threshold'] = th
        self.hertz['thresholdType'] = tht
        self.doAll(4)

    def doElastography(self,elast):
        iterator = self.haystack
        for c in iterator:
            if c[self.forwardSegment].young is not None:
                c[self.forwardSegment].elastography = elast(c[self.forwardSegment])
                if c[self.forwardSegment].elastography.Elastography() is True:
                    if c[c.forwardSegment].elastography.fitRelativeBilayer() is True:
                        c[c.forwardSegment].elastography.toAbs()

    def doAll(self,step=None):
        if step in [0,1,2,3,4,5]:
            action = ['Opening','Looking for out of contact region','Calculating contact point','Creating indentation','Hertzian fit','Filtering']
        for c in self.haystack:
            if step==0:
                c.open()
            elif step==1:
                c[self.forwardSegment].findOutOfContactRegion()
            elif step == 2:
                c[self.forwardSegment].findContactPoint()
            elif step == 3:
                c[self.forwardSegment].createIndentation()
            elif step == 4:
                if self.hertz['threshold'] is None:
                    c[self.forwardSegment].fitHertz()
                else:
                    c[self.forwardSegment].fitHertz(threshold = self.hertz['threshold'], thresholdType=self.hertz['thresholdType'])
            elif step == 5:
                c[self.forwardSegment].smooth()
            else:
                c.open()
                c[self.forwardSegment].findOutOfContactRegion()
                c[self.forwardSegment].findContactPoint()
                c[self.forwardSegment].createIndentation()
                c[self.forwardSegment].fitHertz()

    def createMap(self,par = 'young',N=50):
        X=[]
        Y=[]
        Z=[]
        for c in self.haystack:
            if c.xpos is not None and c.ypos is not None:
                seg = c[self.forwardSegment]
                if par == 'young':
                    if seg.young is not None:
                        X.append(c.xpos)
                        Y.append(c.ypos)
                        Z.append(seg.young)
                elif par == 'ec':
                    if seg.hasBilayer() is True:
                        X.append(c.xpos)
                        Y.append(c.ypos)
                        Z.append(seg.elastography.Ecortex)
                elif par == 'eb':
                    if seg.hasBilayer() is True:
                        X.append(c.xpos)
                        Y.append(c.ypos)
                        Z.append(seg.elastography.Ebulk)
                elif par == 't':
                    if seg.hasBilayer() is True:
                        X.append(c.xpos)
                        Y.append(c.ypos)
                        Z.append(seg.elastography.Thickness)
        from scipy import interpolate
        F = interpolate.interp2d(X, Y, Z)
        dx = max(X)-min(X)
        dy = max(Y)-min(Y)
        dd = min(dx,dy)/N
        x = np.arange(min(X),max(X),dd)
        y = np.arange(min(Y),max(Y),dd)
        return F(x,y)


##################################
##### Optics11 Chiaro ############
##################################

def cross(x1,x2,th,dth):
    th1 = th+dth
    th2 = th-dth
    if np.sign(x1-th1) != np.sign(x2-th1):
        return True
    if np.sign(x1-th2) != np.sign(x2-th2):
        return True
    return False

class ChiaroBase(DataSet):

    def check(self):
        f = open(self.filename)
        signature = f.readline()
        f.close()
        if signature[0:5] == 'Date\t':
            return True
        return False

    def header(self):
        f = open(self.filename)
        targets=['Tip radius (um)','Calibration factor','k (N/m)','SMDuration (s)','Piezo Indentation Sweep Settings','Profile:','E[eff] (Pa)','X-position (um)','Y-position (um)']
        reading_protocol = False
        for line in f:
            if reading_protocol is False:
                if line[0:len(targets[0])] == targets[0]:
                    self.tip_radius = float(line.strip().replace(',','.').split('\t')[1])*1000.0 #NB: internal units are nm
                elif line[0:len(targets[1])] == targets[1]:
                    self.cantilever_lever = float(line.strip().replace(',','.').split('\t')[1]) #NB: so called geometric factor
                elif line[0:len(targets[2])] == targets[2]:
                    self.cantilever_k = float(line.strip().replace(',','.').split('\t')[1])
                elif line[0:len(targets[3])] == targets[3]:
                    delay = float(line.strip().replace(',','.')[len(targets[3]):])
                    self.protocol.append([0, delay])
                elif line[0:len(targets[6])] == targets[6]:
                    self.youngProvided = float(line.strip().replace(',','.').split('\t')[1])/1.0e9 #saved in Pa, internally in GPa; this is Eeff (i.e. including 1-\nu^2)
                elif line[0:len(targets[7])] == targets[7]:
                    self.xpos = float(line[len(targets[7]):].strip())
                elif line[0:len(targets[8])] == targets[8]:
                    self.ypos = float(line[len(targets[8]):].strip())
                elif line[0:len(targets[5])] == targets[5]:
                    reading_protocol = True
                elif line[0:len(targets[4])] == targets[4]:
                    reading_protocol = True
            else:
                if line.strip() == '':
                    reading_protocol = False
                else:
                    slices = line.strip().replace(',', '.').split('\t')
                    self.protocol.append([float(slices[1]),float(slices[3])])
        f.close()

    def load(self):
        f = open(self.filename)
        stopLine = 'Time (s)'
        numeric = False
        data = []
        for riga in f:
            if numeric is False:
                if riga[0:len(stopLine)] == stopLine:
                    numeric = True
            else:
                line = riga.strip().replace(',','.').split('\t')
                # Time (s)	Load (uN)	Indentation (nm)	Cantilever (nm)	Piezo (nm)	Auxiliary
                data.append([float(line[0]),float(line[1]),float(line[3]),float(line[4])]) #skip 2 = indentation and #5 auxiliary if present
        f.close()
        data = np.array(data)
        self.data['time'] = data[:, 0]
        self.data['force'] = data[:, 1]*1000.0
        self.data['deflection'] = data[:, 2]
        self.data['z'] = data[:, 3]
        
    def toggleIndCal(self,value=False):
        for c in self:
            if c.basename == 'Calib' or c.basename == 'Indentations':
                for s in c.haystack:
                    s.active = value

    def see_segmentation(self):
        import matplotlib.pyplot as plt
        t = self.data['time']
        z = self.data['z']
        plt.plot(t,z,color='red')
        col = True
        for i in range(len(self.nodi) - 1):
            z = self.data['z'][self.nodi[i]:self.nodi[i + 1]]
            t = self.data['time'][self.nodi[i]:self.nodi[i + 1]]
            if col is True:
                plt.plot(t,z,color='blue')
            else:
                plt.plot(t,z,color='yellow')
            col = not col

class Chiaro(ChiaroBase):

    def createSegments(self, bias = 30):
        sign = +1
        actualPos = 1
        nodi = []
        nodi.append(0)
        wait = 0
        for nextThreshold,nextTime in self.protocol:
            for j in range(actualPos,len(self.data['z'])):
                if self.data['time'][j] > wait + nextTime:
                    if (cross(self.data['z'][j],self.data['z'][j-1],nextThreshold,bias)) is True:
                        nodi.append(j)
                        wait = self.data['time'][j]
                        break
            actualPos = j
        nodi.append(len(self.data['z'])-1)
        self.nodi=nodi
        for i in range(len(nodi) - 1):
            z = self.data['z'][nodi[i]:nodi[i + 1]]
            f = self.data['force'][nodi[i]:nodi[i + 1]]
            t = self.data['time'][nodi[i]:nodi[i + 1]]
            self.append(Segment(self, z, f))
            beg = int(len(z) / 3)
            end = int(2 * len(z) / 3)
            # for future reference maybe worth adding a fit ?
            self[-1].speed = (z[end] - z[beg]) / (t[end] - t[beg])

class ChiaroGenova(ChiaroBase):
    #this procedure works for old text curves from Genova, not last version
    #waiting for the feedback from Optics11 to get it corrected
    def createSegments(self):
        vs = self.protocol
        nodi = []
        nodi.append(0)
        j = 0
        nexttime = vs[j][1]
        nextvalue = vs[j][0]
        timefound = False
        valuefound = False
        for i in range(len(self.data['time'])):
            if i == len(self.data['time']) - 1:
                nodi.append(i)
            else:
                if self.data['time'][i] <= nexttime and self.data['time'][i + 1] > nexttime:
                    timefound = True
                if (self.data['z'][i] <= nextvalue and self.data['z'][i + 1] > nextvalue) or (
                        self.data['z'][i] >= nextvalue and self.data['z'][i + 1] < nextvalue):
                    valuefound = True
            if timefound and valuefound:
                nodi.append(i)
                nexttime = self.data['time'][i]
                timefound = False
                valuefound = False
                if (j + 1 == len(vs)):
                    nodi.append(len(self.data['time']) - 1)
                    break
                else:
                    j += 1
                    nexttime += vs[j][1]
                    nextvalue = vs[j][0]
        self.nodi = nodi
        for i in range(len(nodi)-1):
            z = self.data['z'][nodi[i]:nodi[i+1]]
            f = self.data['force'][nodi[i]:nodi[i+1]]
            t = self.data['time'][nodi[i]:nodi[i+1]]
            self.append(Segment(self,z,f))
            beg = int(len(z)/3)
            end = int(2*len(z)/3)
            #for future reference maybe worth adding a fit ?
            self[-1].speed = (z[end]-z[beg])/(t[end]-t[beg])