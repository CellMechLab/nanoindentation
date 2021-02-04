import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

def hertz(x, young, radius, nu=0.5):
    x = np.abs(x)
    return 4*young/3/(1-nu**2)*np.sqrt(radius)*x**1.5

def setCP(th, delta=0):
    iContact = np.argmin((th['z']-th['cp']-delta) ** 2)
    Yf = th['F'][iContact:]
    Xf = th['z'][iContact:]-th['cp']-delta
    ind = Xf - Yf / k
    return ind, Yf

def Young(th, indmax=2e-6):
    jj = np.argmin((th['ind']-indmax)**2)
    #plt.plot(th['ind'][:jj], th['touch'][:jj])
    popt, pcov = curve_fit(hertz, th['ind'][:jj], th['touch'][:jj], p0=[
                           3000], maxfev=100000)
    return popt[0]

def ES_direct(c, win=30e-9, order=1, cp =2000e-9, k = 1.0, R = 1e-6):
    rF = c.f*1e-9
    z = c.z*1e-9

    iContact = np.argmin((z-cp) ** 2)
    F = rF[iContact:]
    Xf = z[iContact:]-cp
    delta = Xf - F / k

    rdelta = np.linspace(min(delta), max(delta), len(delta))
    rF = np.interp(rdelta, delta, F)
    space = rdelta[1]-rdelta[0]
    iwin = int(win/space)
    if iwin % 2 == 0:
        iwin += 1
    dFdd = savgol_filter(rF, iwin, order, deriv=1, delta=space)
    ES = 3*dFdd/8/np.sqrt(R*rdelta)
    return rdelta[iwin:-iwin], ES[iwin:-iwin]

def ES_prime(c, win=30e-9, order=1, delta=0, cp =2000e-9, k = 1.0, R = 1e-6, capped = False):
    F = c.f*1e-9
    z = c.z*1e-9

    rz = np.linspace(min(z), max(z), len(z))
    rF = np.interp(rz, z, F)
    space = rz[1]-rz[0]
    iwin = int(win/space)
    if iwin % 2 == 0:
        iwin += 1
    S = savgol_filter(rF, iwin, order, deriv=1, delta=space)

    iContact = np.argmin((rz-cp-delta) ** 2)
    Yf = rF[iContact:]
    Xf = rz[iContact:]-cp-delta
    ind = Xf - Yf / k
    ES = 3*S[iContact:]/(1-S[iContact:]/k)/8/np.sqrt(R*ind)
    if capped is False:
        Scap = S[iContact:]/k<2
    else:
        Scap = S[iContact:]/k<0.95

    return ind[Scap][iwin:-iwin], ES[Scap][iwin:-iwin]

def Prime(c, win=30e-9, order=1):
    F = c.f*1e-9
    z = c.z*1e-9

    rz = np.linspace(min(z), max(z), len(z))
    rF = np.interp(rz, z, F)
    space = rz[1]-rz[0]
    iwin = int(win/space)
    if iwin % 2 == 0:
        iwin += 1
    S = savgol_filter(rF, iwin, order, deriv=1, delta=space)

    return rz, S

from mvexperiment import experiment
exp = experiment.Chiaro('../tmpdata/matrix_scan01/')
exp.browse()
for c in tqdm(exp.haystack):
    c.open()


for c in tqdm(exp.haystack):
    c[1].S = Prime(c[1])

    c[1].cp = 0
    jmax = np.argmin((c[1].S[1]-0.3)**2)
    jcp = 0
    for j in range(jmax,0,-1):
        if c[1].S[1][j]<=0:
            jcp = j
            break
    c[1].cp = c[1].S[0][jcp]
    #plt.plot(z,S/c.cantilever_k)
    #plt.plot(z,S/(1-S/c.cantilever_k))

plt.subplot(211)
for c in tqdm(exp.haystack):
    #c[1].E = ES_prime(c[1],cp = c[1].cp,k=c.cantilever_k,R=c.tip_radius*1e-9)
    c[1].Ecap = ES_prime(c[1],cp = c[1].cp,k=c.cantilever_k,R=c.tip_radius*1e-9,capped=False)
    plt.plot(c[1].Ecap[0],c[1].Ecap[1])
plt.subplot(212)
for c in tqdm(exp.haystack):
    #c[1].E = ES_prime(c[1],cp = c[1].cp,k=c.cantilever_k,R=c.tip_radius*1e-9)
    c[1].Ecap = ES_direct(c[1],cp = c[1].cp,k=c.cantilever_k,R=c.tip_radius*1e-9)
    plt.plot(c[1].Ecap[0],c[1].Ecap[1])

if False:
    j = 0
    s = exp.haystack[j][1]
    plt.subplot(311)
    x = s.z-s.cp*1e9
    plt.plot(x,s.f,'o')
    plt.plot(x[x>0],exp.haystack[j].cantilever_k*x[x>0])
    plt.subplot(312)
    x = s.S[0]*1e9-s.cp*1e9
    plt.plot(x,s.S[1]/exp.haystack[j].cantilever_k)
    plt.plot([0,max(x)],[1,1],'k--')
    plt.subplot(313)
    plt.plot(s.E[0],s.E[1])
    plt.plot(s.Ecap[0],s.Ecap[1])

plt.show()
