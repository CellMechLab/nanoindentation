import numpy as np
from . import mvobject
try:
    import savitzky_golay as sg
except:
    from .. import savitzky_golay as sg

class segment(mvobject.mvobject):
    def __init__(self,x,y):   
        #internal units
        #  sensitivity nm/V
        #  k pN/nm
        #  speed nm/s
        #  Z nm
        #  F pN
        #  directions are near | far | hold
        defaults = {'direction':'far','speed':1.0,'k':1.0,'type':'Vconst'}
        self.parseConfig(defaults,'Segment')
        if len(x)==0:
            return False
         
        if x[0]>x[-1]:
            self.direction='near'
            x.reverse()
            y.reverse()
            
        self.show = True

        self.z = np.array(x)
        self.f = np.array(y) 

    def getRelevant(self):
        for i in range(len(self.z)):
            if self.z[i]>=0.0:
                start = i
                break
        return self.z[start:],self.f[start:]
            
    def FZtoFD(self):
        """
        Convert Force versus Displacement to Force versus Distance
        """
        self.z=self.z-self.f/self.k

    def getContactIndex(self, smooth=True):
        y = self.f
        if smooth:
            y = sg.getSG (self.f, len(self.f/100), 2, 0)
        for i in range(len(y)-1):
            if ( ( y[i+1] > 0) and (y[i]<0) ):
                return i+1
        return 0

    def getArea(self):
        """
        :rtype : float
        """
        y = self.f
        x = self.z

        from scipy.integrate import trapz
        i = self.getContactIndex(smooth=False)

        return trapz(y[i:],x[i:])

    def getAdhesion(self):
        return np.max(self.f)

if __name__ == "__main__":
    print ('not for direct use')
