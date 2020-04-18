# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

def ExpSimple(x,E0,Eb,d0):
    R = 3200
    weight = np.exp(-np.sqrt(R*x)/d0)
    return Eb+(E0-Eb)*weight

def fitExpSimple(x,y):
    seeds=[10000/1e9,1000/1e9,200]
    x=np.array(x)
    popt1, pcov1 = curve_fit(ExpSimple, x,y, p0=seeds, maxfev=10000)
    return popt1

def Elastography2withMax(x,y,grainstep = 11,maxindentation=800):
    R = 3200
    yi = interp1d(x,y)
    max_x=np.min([np.max(x), maxindentation])
    min_x=1
    if np.min(x)>1:
        min_x=np.min(x)
    xx = np.arange(min_x,max_x,1.0)
    yy = yi(xx)
    coeff = 3/8/np.sqrt(R)
    win = grainstep
    if win%2 == 0:
        win+=1
    deriv = savgol_filter(yy,win,3,delta=1.0,deriv=1)
    Ey = coeff*deriv/np.sqrt(xx)
    Ex = list(xx)
    dwin = int(win-1) #int((win-1)/2)
    Ex=Ex[dwin:-dwin]
    Ey=Ey[dwin:-dwin]
    return np.array(Ex),np.array(Ey)    

E2 = 2000.0
Lamb = 2.0/1.08

# E1
Nmax = 22
d0 = 300.0
dtrue = []
E1true = []
E2true = []
E1 = []
for i in range(3,Nmax+1):
    E1.append(i*1000)
    data = np.loadtxt('../ros/fc{}.txt'.format(i*1000))
    indentation = data[:,0]*1e9
    force = data[:,1]*1e9
    ex,ey = Elastography2withMax(indentation,force)
    coe = fitExpSimple(ex,ey)
    dtrue.append(coe[2])
    E1true.append(coe[0]*1e9)
    E2true.append(coe[1]*1e9)
    
for i in range(3,8):
    E1.append(i*10000)
    data = np.loadtxt('../ros/fc{}0000.txt'.format(i))
    indentation = data[:,0]*1e9
    force = data[:,1]*1e9
    ex,ey = Elastography2withMax(indentation,force)
    coe = fitExpSimple(ex,ey)
    dtrue.append(coe[2])
    E1true.append(coe[0]*1e9)
    E2true.append(coe[1]*1e9)

E1true=np.array(E1true)
E2true=np.array(E2true)
dtrue=np.array(dtrue)
E1 = np.array(E1).astype(float)

plt.figure()
plt.subplot(231)
plt.plot(E1/E2,(E1true/E1),'o')
plt.plot((E1/E2)[6:20],(E1true/E1)[6:20],'o')
plt.ylabel('E1apparent/trueE1')
plt.xlabel('Ratio TrueE1/E2')
plt.title('$E1_{apparent}$ for d0=300')
plt.subplot(232)
plt.plot((E1/E2),(E2true/E2),'o')
plt.plot((E1/E2)[6:20],(E2true/E2)[6:20],'o')
plt.ylabel('E2apparent/trueE2')
plt.xlabel('Ratio TrueE1/E2')
plt.title('$E2_{apparent}$ for d0=300')
plt.subplot(233)
plt.plot((E1/E2),(Lamb*dtrue/d0),'o')
plt.plot((E1/E2)[6:20],(Lamb*dtrue/d0)[6:20],'o')
plt.ylabel('Dapparent/Dtrue')
plt.xlabel('Ratio TrueE1/E2')
plt.title('$d_{apparent}$  for d0=300')

# thickness
E1 = 20000.0
dtrue = []
E1true = []
E2true = []
d0=[]
for i in range(100,520,50):
    data = np.loadtxt('../ros/fc20{}.txt'.format(i))
    d0.append(float(i))
    indentation = data[:,0]*1e9
    force = data[:,1]*1e9
    ex,ey = Elastography2withMax(indentation,force)
    coe = fitExpSimple(ex,ey)
    dtrue.append(coe[2])
    E1true.append(coe[0]*1e9)
    E2true.append(coe[1]*1e9)

for i in range(6,10):
    data = np.loadtxt('../ros/fc20{}00.txt'.format(i))
    d0.append(float(i*100))
    indentation = data[:,0]*1e9
    force = data[:,1]*1e9
    ex,ey = Elastography2withMax(indentation,force)
    coe = fitExpSimple(ex,ey)
    dtrue.append(coe[2])
    E1true.append(coe[0]*1e9)
    E2true.append(coe[1]*1e9)

E1true=np.array(E1true)
E2true=np.array(E2true)
dtrue=np.array(dtrue)

d0 = np.array(d0)
plt.subplot(234)
plt.plot(d0,(E1true/E1),'o')
plt.plot(d0[2:6],(E1true/E1)[2:6],'o')
plt.ylabel('E1apparent/trueE1')
plt.xlabel('Thickness d0 [nm]')
plt.title('$E1_{apparent}$ for E1=20000')
plt.subplot(235)
plt.plot(d0,E2true/E2,'o')
plt.plot(d0[2:6],(E2true/E2)[2:6],'o')
plt.ylabel('E2apparent/trueE2')
plt.xlabel('Thickness d0 [nm]')
plt.title('$E2_{apparent}$ for E1=20000')
plt.subplot(236)
plt.plot(d0,Lamb*dtrue/d0,'o')
plt.plot(d0[2:6],(Lamb*dtrue/d0)[2:6],'o')
plt.ylabel('Dapparent/Dtrue')
plt.xlabel('Thickness d0 [nm]')
plt.title('$d_{apparent}$ for E1=20000')
plt.show()