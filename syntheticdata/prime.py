import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

E = 6245
N = 40
R = 3400e-9
cp = 3.0e-6
indmax = 7e-6
cpoint = 1000
indpoint = 7000
noiselevel = 100e-12
noisewidth = 1e-9
k = 0.032

def hertz(x,young=E,radius=R,nu=0.5):
    x = np.abs(x)
    return 4*young/3/(1-nu**2)*np.sqrt(radius)*x**1.5

xpost = np.linspace(0,indmax,indpoint)
Fpost = hertz(xpost)
zpost = xpost+Fpost/k

FDcurves = []

for i in range(N):
    this = {}
    realcp = cp + 100.0e-9*np.random.normal(scale=1)
    zpre = np.linspace(0,realcp,cpoint)
    Fpre = np.zeros(len(zpre))
    F = np.append(Fpre,Fpost)
    z = np.append(zpre,zpost+realcp)
    noise = noiselevel * np.random.normal(scale=.1,size=F.shape)
    F += noise
    properz = np.linspace(0,max(z),int(max(z)*1e9))
    properF = np.interp(properz, z, F)
    this['z']=properz
    this['F']=properF
    this['cp'] = realcp
    FDcurves.append(this)


def setCP(th,delta = 0):
    iContact = np.argmin((th['z']-th['cp']-delta )** 2)
    Yf = th['F'][iContact:]
    Xf = th['z'][iContact:]-th['cp']-delta
    ind = Xf - Yf / k
    return ind,Yf

def Young(th,indmax = 2e-6):
    jj = np.argmin((th['ind']-indmax)**2)
    #plt.plot(th['ind'][:jj], th['touch'][:jj])
    popt, pcov = curve_fit(hertz, th['ind'][:jj], th['touch'][:jj], p0=[3000], maxfev=100000)
    return popt[0]

for i in range(len(FDcurves)):
    th = FDcurves[i]
    FDcurves[i]['ind'],FDcurves[i]['touch']=setCP(th)
    Eth = Young(FDcurves[i])

if False:
    delta = np.linspace(-200e-9,200e-9,400)
    Eall = []
    for j in tqdm(range(len(delta))):
        Enow=[]
        for i in range(len(FDcurves)):
            th = FDcurves[i]
            FDcurves[i]['ind'],FDcurves[i]['touch']=setCP(th,delta[j])
            Enow.append(Young(FDcurves[i]))
        Eall.append(np.average(Enow))
    plt.plot(delta,Eall,'o')
    Eth = []
    for j in tqdm(range(len(delta))):
        i=12
        th = FDcurves[i]
        FDcurves[i]['ind'],FDcurves[i]['touch']=setCP(th,delta[j])
        Eth.append(Young(FDcurves[i]))
    plt.plot(delta,Eth,'--')


def ES_direct(th,win=30e-9,order=1):
    # E = 3*dFdd/8a ; dFdd = derivative of force vs delta
    F = th['touch']
    delta = th['ind']

    rdelta = np.linspace(min(delta),max(delta),len(delta))
    rF = np.interp(rdelta, delta, F)
    space = rdelta[1]-rdelta[0]
    iwin = int(win/space)
    if iwin%2 == 0:
        iwin += 1
    dFdd = savgol_filter(rF,iwin,order,deriv=1,delta=space)
    ES = 3*dFdd/8/np.sqrt(R*rdelta)
    return rdelta[iwin:-iwin],ES[iwin:-iwin]

def ES_prime(th,win=30e-9,order=1,delta=0):
    F = th['F']
    z = th['z']

    rz = np.linspace(min(z),max(z),len(z))
    rF = np.interp(rz, z, F)
    space = rz[1]-rz[0]
    iwin = int(win/space)
    if iwin%2 == 0:
        iwin += 1
    S = savgol_filter(rF,iwin,order,deriv=1,delta=space)

    iContact = np.argmin((rz-th['cp']-delta )** 2)
    Yf = rF[iContact:]
    Xf = rz[iContact:]-th['cp']-delta
    ind = Xf - Yf / k
    ES = 3*S[iContact:]/(1-S[iContact:]/k)/8/np.sqrt(R*ind)

    return ind[iwin:-iwin],ES[iwin:-iwin]

def Prime(th,win=30e-9,order=1):
    F = th['F']
    z = th['z']

    rz = np.linspace(min(z),max(z),len(z))
    rF = np.interp(rz, z, F)
    space = rz[1]-rz[0]
    iwin = int(win/space)
    if iwin%2 == 0:
        iwin += 1
    S = savgol_filter(rF,iwin,order,deriv=1,delta=space)

    return rz,S

if False:
    myTH = FDcurves[12]
    myTH['ind'],myTH['touch']=setCP(myTH,0)

    plt.subplot(211)
    for order in [1,2,3,4,5,6]:
        Ex,Ey=ES_direct(myTH,order=order)
        plt.plot(Ex,Ey,label=str(order))

    #plt.plot([0,200e-9],[E,E],'--')
    plt.legend()

    plt.subplot(212)

    for size in [1,2,3,4,5,6]:
        Ex,Ey=ES_direct(myTH,win=size*10*1e-9,order=4)
        plt.plot(Ex,Ey,label=str(size*10))
    plt.plot([0,max(Ex)],[E,E],'--')
    plt.legend()


order = 4
win = 30e-9

myTH = FDcurves[12]

#plt.plot(*Prime(myTH))

if True:
    plt.subplot(211)
    plt.title('Direct')
    delta = [-100e-9,-50e-9,0,50e-9,100e-9]
    for j in range(len(delta)):
        myTH['ind'],myTH['touch']=setCP(myTH,delta[j])
        Ex,Ey=ES_direct(myTH,win=30e-9,order=4)
        plt.plot(Ex,Ey,label=str(delta[j]*1e9))
    plt.xlim((0,500e-9))
    plt.ylim((0,20000))
    plt.legend()

    plt.subplot(212)
    plt.title('Prime')
    delta = [-100e-9,-50e-9,0,50e-9,100e-9]
    for j in range(len(delta)):
        Ex,Ey=ES_prime(myTH,win=30e-9,order=4,delta=delta[j])
        plt.plot(Ex,Ey,label=str(delta[j]*1e9))
    plt.xlim((0,500e-9))
    plt.ylim((0,20000))
    plt.legend()

if False:
    myTH['ind'],myTH['touch']=setCP(myTH)
    Ex,Ey=ES_direct(myTH,win=30e-9,order=4)
    plt.plot(Ex,Ey,label='direct')

    Ex,Ey=ES_prime(myTH,win=30e-9,order=4)
    plt.plot(Ex,Ey,label='prime')

    plt.legend()

#plt.plot([100e-9],[E],'ro')




plt.show()

