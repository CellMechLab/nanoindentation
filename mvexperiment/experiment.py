from .mvFilesystem import MvNode
import numpy as np
from .curve import Segment
from .curve import MODE_DIRECTION_BACKWARD,MODE_DIRECTION_FORWARD,MODE_DIRECTIONS_PAUSE

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

##################################
##### Nanosurf ###################
##################################


class NanoSurf(DataSet):

    def check(self):
        f = open(self.filename)
        signature = f.readline()
        f.close()
        if signature[0:9] == '#Filename':
            return True
        return False

    def header(self):
        f = open(self.filename)
        targets=['#Cantilever=','#Spring-Constant=','#Deflection-Sensitivity=','#Filename=','#SpecMap','#SpecMode']

        def outNum(text):
            s = ''
            for c in text:
                if c.isdigit() or c in ['.','e','-','+']:
                    s+=c
                else:
                    break
            return float(s)
        map_dim = [None,None]
        map_size = [None,None]
        isMap = False
        for line in f:
            if line[0:len(targets[2])] == targets[2]: #1.4736e-07m/V
                self.cantilever_lever = outNum(line[len(targets[2]):])*1e9 #NB: internal units are nm/V
            elif line[0:len(targets[1])] == targets[1]:
                self.cantilever_k = outNum(line[len(targets[1]):]) #NB: internal units are nm/V
            elif line[0:len(targets[0])] == targets[0]:
                self.cantilever_type = line[len(targets[0]):].strip() #guess the radius
                data = self.cantilever_type.strip().split('-')
                if len(data)>1:
                    if 'um' in data[1]:
                        radius = float(data[1].replace('um',''))*1000.0
                        self.tip_radius = radius
                    if len(data)>2:
                        if 'um/s' in data[2]:
                            speed = float(data[1].replace('um/s', '')) * 1000.0
                            self.protocol_speed = speed
            elif line[0:len(targets[3])] == targets[3]:
                self.original_filename = line[len(targets[3]):].strip()
            elif line[0:len(targets[5])] == targets[5]:
                if line[line.find('=')+1:].strip()=='Map':
                    isMap = True
            elif (line[0:len(targets[4])] == targets[4]) and (isMap is True):
                tp = line[line.find('-')+1:line.find('=')]
                if tp == 'Dim':
                    map_dim = line[line.find('=')+1:].split(';')
                elif tp=='Size':
                    map_size = line[line.find('=')+1:].split(';')
                elif tp == 'CurIndex':
                    curindex = int(line[line.find('=') + 1:])
                    nx = int(map_size[0])
                    ny = int(map_size[1])
                    coordinates = []
                    dx = (float(map_dim[1]) - float(map_dim[0]))/(nx-1)
                    dy = (float(map_dim[3]) - float(map_dim[2]))/(ny-1)
                    for i in range(nx):
                        for j in range(ny):
                            coordinates.append((i*dx,j*dy))
                    self.xpos,self.ypos = coordinates[curindex]
            elif line[0] != '#':
                break
        f.close()

    def load(self):
        data = []
        dummy = True
        collected = 0
        f = open(self.filename)
        for line in f:
            if dummy is True:
                if line[0:10] == '#Spec-Data':
                    dummy = False
                    self.protocol.append(collected)
                    #Note the header line
                    #Spec-Data=Z-Axis Sensor [m];Deflection [V];Z-Axis-Out [m]
                    #Spec-Data=Z-Axis Sensor [m];Deflection [N];Z-Axis-Out [m]
                    #Units for Deflection can be either V or N !
                    self.data_channels = line[11:].strip().split(';')
                elif line[0:11] == '#Spec-Phase':
                    self.append(Segment(self))
                elif line[0:10] == '#Spec-Name':
                    if line[16:].strip() == 'forward':
                        self[-1].direction = MODE_DIRECTION_FORWARD
                    elif line[16:].strip() == 'backward':
                        self[-1].direction = MODE_DIRECTION_BACKWARD
                    else:
                        self[-1].direction = MODE_DIRECTIONS_PAUSE
                elif line[0:10] == '#Spec-Data':
                    self[-1].header = line[11:].strip()
            elif dummy is False:
                if line.strip() == '':
                    dummy = True
                else:
                    data.append([i for i in map(float,line.strip().split(';'))])
                    collected += 1
        self.protocol.append(len(data))
        f.close()
        data = np.array(data)
        # Now get as much information as possible out of the curves
        # Spec-Data=Z-Axis Sensor [m];Deflection [N];Z-Axis-Out [m]
        #mmmm, try to guess it

        check = np.abs(np.mean(data[:100, 1])*1e9)
        if check<1000:
            self.data['force'] = data[:,1]*1e9
        else :
            self.data['force'] = data[:, 1] * self.cantilever_lever
        self.data['z'] = data[:, 0]*1e9

    def createSegments(self):
        for i in range(len(self.protocol)-1):
            z = self.data['z'][self.protocol[i]:self.protocol[i+1]]
            f = self.data['force'][self.protocol[i]:self.protocol[i+1]]
            self[i].setData(z,f,reorder=True)