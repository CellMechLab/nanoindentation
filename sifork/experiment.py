import os
import logging
from . import curve
from . import mvobject

logging.basicConfig(level=logging.DEBUG)

class experiment(mvobject.mvobject):
    def __init__(self):
        defaults = {'current':None}
        self.parseConfig(defaults,'Experiment')
        self.curves = [] #store for curves
        self.locations = [] #store for full pathnames
        self.basenames = [] #store for names

    def __iter__(self):
        return self.curves.__iter__()

    def __getitem__(self, index):
        if index in self.locations:
            index = self.locations.index(index)
        elif index in self.basenames:
            index = self.basenames.index(index)
        return self.curves[index]
    def __setslice__(self,imin,imax,vals):
        i = imin
        for v in vals:
            self.__setitem__(i,v)
            i+=1
        if i < imax:
            del self.curves[i:imax]
            del self.locations[i:imax]
            del self.basenames[i:imax]
    def __setitem__(self,index,curve):
        self.curves[index]=curve
        self.locations[index] = curve.filename
        self.basenames[index] = curve.basename
    def __len__(self):
        return len(self.curves)

    def __delitem__(self,index):
        if index in self.locations:
            index = self.locations.index(index)
        elif index in self.basenames:
            index = self.basenames.index(index)
        del self.curves[index]
        del self.locations[index]
        del self.basenames[index]
    def index(self,valore):
        if valore in self.locations:
            return self.locations.index(valore)
        elif valore in self.basenames:
            return self.basenames.index(valore)
        raise ValueError('Not found')

    def size(self):
        return len([e for e in self.curves if e])

    def append(self,obj):
        if isinstance(obj,curve.curve):
            if obj:
                if obj.filename in self.locations:
                    logging.warn('Curve {0} is already in the experiment. File NOT appended'.format(obj.filename))
                    return False
                elif obj.basename in self.basenames:
                    logging.error('Curve with basename {0} is already in the experiment. File NOT appended'.format(obj.basename))
                    return False
                else:
                    self.curves.append(obj)
                    self.locations.append(obj.filename)
                    self.basenames.append(obj.basename)
                    return True
            else:
                logging.warn('Curve {0} is NOT relevant to the experiment or broken. Curve NOT appended')
                return False
        else:
            return self.append(curve.curve(obj))

    def addFiles(self, fnames = None):
        if fnames == None:
            return False
        for fname in fnames:
            if os.path.isfile(fname):
                self.append(fname)

    def addDirectory(self,dirname=None):
        if dirname == None:
            return False
        if not os.path.isdir(dirname):
            logging.warn('The selected path {0} is not a valid directory'.format(dirname))
            return False
        logging.debug("Opening DIR {0}".format(dirname))

        i=0
        pmax = len(os.listdir(dirname))
        step = max(pmax/100,10)
        for fnamealone in os.listdir(dirname):
            if i % step == 0:
                logging.debug( "{0}% {1}/{2}".format(100*i/pmax,i,pmax))
            fname = os.path.join(str(dirname), fnamealone)
            if os.path.isfile(fname):
                self.append(fname)
            i+=1

    def saveCurves(self, dirname = None):
        if dirname==None:
            return False
        if not os.path.isdir(dirname):
            logging.warn('The selected path {0} is not a valid directory'.format(dirname))
            return False
        for c in self.curves:
            if c:
                name = os.path.join(str(dirname), 'exp_'+c.basename)
                c.save(name)


if __name__ == "__main__":
    print ('not for direct use')
