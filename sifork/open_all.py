from . import segment
import logging

MOMCOR = True

class openWorker():

    def __init__(self,fname):
        self.fname = fname
        self.parameters={}
        self.info={}
        self.segments=[]
    def parseConfigLine(self,cline,newline='\r\n'):
        line = cline[2:-len(newline)]
        # columns: vDeflection strainGaugeHeight
        # fancyNames: "Vertical deflection" "Height (measured)"
        if line.find(':')==-1:
            return False
        fragments = line.split(':')
        name = fragments[0]
        post = ':'.join(fragments[1:]).strip()
        if post.find('"')==-1:
            val = post.split(' ')
        else:
            val = post[1:-1].split('" "')
        if len(val)==1:
            val = val[0]
        return name,val
    def getFile(self):
        in_file = open(str(self.fname),"r")
        righe = in_file.readlines()
        in_file.close()
        self.newline = '\n'
        try:
            if righe[10][-2:]=='\r\n':
                self.newline = '\r\n'
            elif righe[10][-1:]=='\r':
                self.newline = '\r'
        except:
            logging.error('File is not an ascii file')
            return False
        return righe

    def getAll(self):
        return self.parameters,self.info,self.segments
    def open(self):
        return False
    
class opener:
    EXT = ['txt','itx','dat','nano']
    OPN = ['jpktxt','igoritx','igortxt','nanoscopetxt']
    
    def __init__(self,fname):
        self.fname = fname
    def getOpener(self,driver=None):
        if driver == None:
            import os
            extension = os.path.splitext(self.fname)[1][1:].lower()
            for i in range(len(self.EXT)):
                 if self.EXT[i]==extension:
                     dr = eval(self.OPN[i]+'(self.fname)')
                     if dr.open()==True:
                         return dr.getAll()
        else:
            dr = eval(driver+'(self.fname)')
            if dr.open()==True:
                return dr.getAll()
        return [],[],[]

class jpktxt(openWorker):
    def open(self):
        """
        Open JPK exported TXT files
        """
        righe = self.getFile()

        x=[]
        y=[]

        direction = None
        chZ = 0
        chF = 1
        k = 1.0
        parse = True

        try:
            speed = 0.0
            for rigo in righe:
                if rigo[0] != '#' and len(rigo) > len(self.newline) and parse and rigo[0] != ' ':
                    separator = ' '
                    if rigo.find(separator)==-1:
                        separator='\t'
                    datas = rigo[:-len(self.newline)].split(separator)
                    xi = datas[chZ]
                    yi = datas[chF]
                    x.append(float(xi)*1e9)
                    y.append(-1.0*float(yi)*1e12)

                else:
                    ex = self.parseConfigLine(rigo,self.newline)
                    if ex != False:
                        name,val = ex
                        if name == 'units':
                            self.info['units'] = val
                        elif name == 'segmentIndex':
                            if len(x)>0 and len(y)>0:
                                self.segments.append(segment.segment(x,y))
                                self.segments[-1].speed = speed
                                self.segments[-1].k = k
                                if direction != None:
                                    self.segments[-1].direction = direction
                            direction = None
                            speed = 1.0
                            x = []
                            y = []
                        elif name == 'springConstant':
                            self.parameters['k'] = 1000.0*float(val) if not MOMCOR else float(val) #internally k is in pN/nm
                            k = self.parameters['k']
                        elif name=='segment':
                            direction = val
                            if val == 'extend':
                                direction='near'
                                parse = True
                            elif val == 'retract':
                                direction = 'far'
                                parse = True
                            elif val=='pause':
                                parse = False
                        elif name == 'columns':
    # columns: height vDeflection smoothedCapacitiveSensorHeight capacitiveSensorHeight seriesTime time
    # fancyNames: "Height" "Vertical deflection" "Height (measured & smoothed)" "Height (measured)" "Series Time" "Segment Time"
                            zs = ['smoothedCapacitiveSensorHeight','height','capacitiveSensorHeight','strainGaugeHeight']
                            for s in zs[::-1]:
                                if s in val:
                                    chZ = val.index(s)
                            if 'vDeflection' in val:
                                chF = val.index('vDeflection')

                        elif name == 'fzfd':
                            if val == '1' or val == 'True':
                                self.parameters['fzfd'] = True
                        elif name == 'fancyNames':
                            self.info['fancyNames'] = val
                        elif name == 'sensitivity':
                            self.parameters['sensitivity'] = 1.0e9*float(val) if not MOMCOR else float(val) #internally in nm/V
                        elif name == 'speed':
                            speed = 1.0e9*float(val) if not MOMCOR else float(val) #internally in nm/s
        except:
            #if logging.getDEBUG :
            #    logging.error('File cannot be interpreted as JPK FD curve')
            #    return False
            #else:
            raise

        if len(x)>0 and len(y)>0:
            self.segments.append(segment.segment(x,y))
            self.segments[-1].speed = speed
            self.segments[-1].k = k
            if direction != None:
                self.segments[-1].direction = direction

        return True



class igoritx(openWorker):
    def open(self):
        """
        Open internal Igor Text File ITX
        """
        self.parameters['k'] = 1.0        
        speed = 0.0
        
        righe = self.getFile()
        newline = self.newline
        
        y1=[]
        y2=[]
        x1=[]
        x2=[]
        
        speed = 0.0
        del righe[0:3]
        for rigo in righe:
            r = rigo.strip(newline)
            if r.strip() =='END':
                break
            (ffb,eeb,fff,eef)= r.split()
            if ffb.strip()=='ffb':
                continue
            if eef.strip() != 'NAN':
                x1.append(float(eef))
                y1.append(float(fff))
            if eeb.strip() != 'NAN':
                x2.append(float(eeb))            
                y2.append(float(ffb))
    
        self.segments.append(segment.segment(x1, y1))
        self.segments.append(segment.segment(x2, y2))
        
        r = righe[-1].strip(newline)
        r = r[r.find('"')+1:-1]
        sl = r.split(';')
        for var in sl:
            nm,val = var.split('=')
            if nm.strip() =='SC(pN/nm)':
                self.parameters['k'] = float(val)
            if nm.strip() == 'PullingRate(nm/s)':
                speed = float(val)/1.0e9
        
        for p in self.segments:
            p.speed = speed
        return True
    
class igortxt(openWorker):
    def open(self):
        """
        Open Igor exported TXT files
        """
        self.parameters['k'] = 1.0        
        speed = 0.0
        
        righe = self.getFile()
        newline = self.newline
        
        y1=[]
        y2=[]
        x1=[]
        x2=[]
        
        for rigo in righe:
            r = rigo.strip(newline)
            (ffb,eeb,fff,eef)= r.split()
            if ffb.strip()=='ffb':
                continue
            if eef.strip() != 'NAN':
                x1.append(float(eef))
                y1.append(float(fff))
            if eeb.strip() != 'NAN':
                x2.append(float(eeb))            
                y2.append(float(ffb))
        
        
        self.segments.append(segment.segment(x1, y1))
        self.segments.append(segment.segment(x2, y2))
    
        for p in self.segments:
            p.speed = speed
            
        return True

class nanoscopetxt(openWorker):
    def open(self):
        import numpy as np
        """
        Open exported text files from nanoscope (versions ? Implementation is not robust)
        """
        self.parameters['k'] = 1.0        
        
        righe = self.getFile()
        newline = self.newline
        
        o = 0
        i = 0
        
        r = righe[0].strip(newline)
        r = r.strip('"')
        r = r.strip('\\')
        
        while r != '*File list end':
            r = righe[i].strip(newline)
            r = r.strip('"')
            r = r.strip('\\')
    
            if o==0 and r=='*Scanner list':
                o+=1
            elif o==1 and r=='*Ciao scan list':
                o+=1
            elif o==2 and r=='*Ciao force list':
                o+=1
            elif o==3 and r=='*Ciao force image list':
                o+=1
            
            if r.find(':') > 0:
                g = r.split(':')
                if len(g)==2:
                    (pre,post) = g 
                else:
                    pre=g[0]+':'+g[1]
                    post=g[2]  
                pre = pre.strip()
                post=post.strip()
                                    
                if o == 1:
                    if pre == '@Sens. Zsens':
                        post=post.split()
                        zsens = float(post[-2])
                        self.info['zsens']=zsens
                elif o==2:
                    if pre=='@Sens. DeflSens':
                        post=post.split()
                        deflsens = float(post[-2])
                        self.info['deflsens']=deflsens
                elif o==3:
                    if pre == 'Scan rate':
                        scanrate = float(post)
                        self.info['scanrate']=scanrate                        
                    elif pre=='@4:Ramp size Zsweep':
                        post=post.split()
                        rampsize = float(post[-2])
                    elif pre=='@Z scan start':
                        post=post.split()
                        zstart = float(post[-2])
                        self.info['zstart']=zstart
                    elif pre=='@Z scan size':
                        post=post.split()
                        zsize = float(post[-2])
                        self.info['zsize']=zsize
                    if pre == 'Forward vel.':
                        fspeed = float(post)
                        self.info['fspeed']=fspeed
                    if pre == 'Reverse vel.':
                        bspeed = float(post)
                        self.info['bspeed']=bspeed
                elif o==4:
                    if pre=='Samps/line':
                        post=post.split()
                        sampline = int(post[-1])
                    elif pre=='Spring Constant':
                        self.parameters['k'] = 1000.0*float(post)                        
                    elif pre=='@4:Z scale':
                        post=post.split()
                        zscale = float(post[-2])
                        self.info['zscale']=zscale
            i+=1
        y1=[]
        y2=[]
        x=[]
                
        for j in range(i+2,len(righe)):
            rigo = righe[j].split()
            x.append((j-i-2)*zsens*rampsize/float(sampline))            
            y1.append(-self.parameters['k']*float(rigo[0]))
            y2.append(-self.parameters['k']*float(rigo[1]))
        
        x = np.array(x)
        y1.reverse()
        y1 = np.array(y1)
        y2 = np.array(y2)
        
        #test whether some points at the end/beginning of the curves are saturating
        if y1[0]==y1[1]:
            a = y1[0]
            i=0
            for yy in y1:
                i+=1
                if yy!=a:
                    break
            y1 = y1[i:]
            y2 = y2[i:]
            x = x[i:]
        
        
        self.segments.append(segment.segment(x, y1))
        self.segments.append(segment.segment(x, y2))
    
        self.segments[0].speed = fspeed
        self.segments[1].speed = bspeed
            
        return True
if __name__ == "__main__":
    print ('not for direct use')