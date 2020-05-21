import numpy as np
import random
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter,medfilt

def getMedCurve(xar,yar,loose = True,threshold=3, error=False):
    if loose is False:
        xmin = -np.inf
        xmax = np.inf
        deltax = 0
        for x in xar:
            xmin = np.max([xmin,np.min(x)])
            xmax = np.min([xmax,np.max(x)])
            deltax += ((np.max(x)-np.min(x))/len(x))
        deltax /= len(xar)
        xnew = np.linspace(xmin,xmax,int( (xmax-xmin)/deltax) )
        ynew = np.zeros(len(xnew))
        for i in range(len(xar)):
            ycur = np.interp(xnew, xar[i], yar[i])
            ynew += ycur
        ynew/=len(xar)
    else:
        xmin = np.inf
        xmax = -np.inf
        deltax = 0
        for x in xar:
            xmin = np.min([xmin, np.min(x)])
            xmax = np.max([xmax, np.max(x)])
            deltax += ((np.max(x) - np.min(x)) / (len(x) - 1))
        deltax /= len(xar)
        xnewall = np.linspace(xmin, xmax, int((xmax - xmin) / deltax))
        ynewall = np.zeros(len(xnewall))
        count = np.zeros(len(xnewall))
        ys = np.zeros([len(xnewall), len(xar)])
        for i in range(len(xar)):
            imin = np.argmin((xnewall - np.min(xar[i])) ** 2)  # +1
            imax = np.argmin((xnewall - np.max(xar[i])) ** 2)  # -1
            ycur = np.interp(xnewall[imin:imax], xar[i], yar[i])
            ynewall[imin:imax] += ycur
            count[imin:imax] += 1
            for j in range(imin, imax):
                ys[j][i] = ycur[j-imin]
        cc = count >= threshold
        xnew = xnewall[cc]
        ynew = ynewall[cc] / count[cc]
        yerrs_new = ys[cc]
        yerr = []
        for j in range(len(yerrs_new)):
            squr_sum = 0
            num = 0
            std = 0
            for i in range(0, len(yerrs_new[j])):
                if yerrs_new[j][i] != 0:
                    squr_sum += (yerrs_new[j][i] - ynew[j]) ** 2
                    num += 1
            if num > 0:
                std = np.sqrt(squr_sum / num)
            yerr.append(std)
        yerr = np.asarray(yerr)
    if error == False:
        return xnew[:-1], ynew[:-1]
    elif error == True:
        return xnew[:-1], ynew[:-1], yerr[:-1]

def gauss(x,y):
    def gaussDist(x,x0,w,A):
        return A*np.exp( -((x-x0)/w)**2 )
    if len(x)==len(y)+1:
        x = (x[1:]+x[:-1])/2.0
    popt, pcov = curve_fit(gaussDist, x,y , p0=[x[np.argmax(y)],(np.max(x)-np.min(x))/10.0,np.max(y)], maxfev=100000)
    nx = np.linspace(np.min(x),np.max(x),100)
    return popt[0],popt[1],popt[2],nx,gaussDist(nx,*popt)

    
def eeffOffset(s,win,threshold):
    quot = getEEE(s,win,threshold)
    jj=0
    for j in range(len(quot)-1,1,-1):
        if quot[j]>threshold and quot[j-1]<threshold:
            jj=j
            break
    oX = s.z[jj]
    oY = s.ffil[jj]
    if jj>4 and jj<len(s.z)-4:
        oX = np.average(s.z[jj-4:jj+4])
        oY = np.average(s.ffil[jj-4:jj+4])    #it might be extended to use a little average of F around point jj
    return oX,oY,quot

def P_derivative(s, z0=0, win=20, savgol_mode='interp'):
    z = s.z-min(s.z)
    P = s.f-min(s.f)+10
    coeff = 3 / 8 / np.sqrt(s.R)
    down = np.sqrt(abs(z - z0 - P / s.k))
    if win % 2 == 0:
        win += 1
    pdot = savgol_filter(P, win, 1, delta=z[1] - z[0], deriv=1, mode=savgol_mode)
    blob = pdot / (1 - pdot / s.k)
    return coeff * blob / down

def IndentationForDerivative(s, z0=0):
    z=s.z-min(s.z)
    i0 = np.argmin((z - z0) ** 2)
    ind = z[i0:] - z0 - s.f[i0:] / s.k
    return ind, i0

def Nanosurf_FindInvalidCurves(s, threshold_invalid=10):
    s.bol2=None
    ind=np.argmin(abs(s.z-s.offsetX))
    if ind<=200:
        s.bol2 = False
    else:
        f_abs = np.absolute(s.ffil[200:ind])
        val=max(f_abs)
        f_abs2=np.absolute(s.ffil[-1000:-100])
        val2=max(f_abs2)
        if val>threshold_invalid or val2<0.5*threshold_invalid:
            s.bol2=False
        else:
            s.bol2=True
    return s.bol2

def InvalidCurvesFromElasticityRise(s, win=301, scaledistance=500, threshold_oscillation=15000):
    ElaInvalid = False
    if len(s.ElastY)<=win:
        ElaInvalid = True
        filEla= None
    else:
        filEla = savgol_filter(s.ElastY * 1e9, win, 1, 0)
        start=np.mean(filEla[:20])
        median=np.median(filEla[200:])
        if start<median:
            ElaInvalid=True
        else:
            for val in s.ElastY[scaledistance:]:
                if np.abs(val*1e9-median)-threshold_oscillation>0:
                    ElaInvalid = True
    return ElaInvalid, filEla


def getHertz(E,R,threshold,indentation=True):
    poisson = 0.5
    if indentation is True:
        x = np.linspace(0,threshold,200)
    else:
        xmax = (((3.0/4.0) * ((1 - poisson ** 2)/E)  * threshold)**2/R ) **(1/3)
        x = np.linspace(0,xmax,200)

    return x,(4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

def fitHertz(s,x=None,y=None, error=None):
    if x is None:
        x = s.indentation[:s.indMax]
        y = s.touch[:s.indMax]
    seeds = [1000.0/1e9]
    #NB the curve is forced to have F=0 at indentation 0
    try:
        R = s.R
        def Hertz(x,E):
            x = np.abs(x)
            poisson = 0.5
            # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
            return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)
        if error is not None:
            popt, pcov = curve_fit(Hertz, x[1:],y[1:] , p0=seeds, maxfev=10000, sigma=error[1:])
        else:
            popt, pcov = curve_fit(Hertz, x,y , p0=seeds, maxfev=10000)
        Einternal = popt[0]
        E_std = np.sqrt(pcov[0][0])
        return Einternal, E_std
    except (RuntimeError,ValueError):
        return None

def noisify(y,intensity=1.0):
    random.seed()
    for i in range(len(y)):
        y[i]=y[i]+2*(random.random()-0.5)*intensity
    return y

def standardHertz(x,E,R,poisson=0.5):
    return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)