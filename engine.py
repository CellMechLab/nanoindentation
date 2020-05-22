import numpy as np
import random
from scipy.signal import savgol_filter,medfilt

def gauss(x,y):
    def gaussDist(x,x0,w,A):
        return A*np.exp( -((x-x0)/w)**2 )
    if len(x)==len(y)+1:
        x = (x[1:]+x[:-1])/2.0
    popt, pcov = curve_fit(gaussDist, x,y , p0=[x[np.argmax(y)],(np.max(x)-np.min(x))/10.0,np.max(y)], maxfev=100000)
    nx = np.linspace(np.min(x),np.max(x),100)
    return popt[0],popt[1],popt[2],nx,gaussDist(nx,*popt)

def getHertz(E,R,threshold,indentation=True):
    poisson = 0.5
    if indentation is True:
        x = np.linspace(0,threshold,200)
    else:
        xmax = (((3.0/4.0) * ((1 - poisson ** 2)/E)  * threshold)**2/R ) **(1/3)
        x = np.linspace(0,xmax,200)

    return x,(4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)
