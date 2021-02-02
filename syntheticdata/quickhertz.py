import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

E = 6245
N = 40
R = 3400e-9
cp = 3.0e-6
indmax = 7e-6
cpoint = 1000
indpoint = 7000
noiselevel = 1e-12
noisewidth = 1e-9
k = 0.032

print(E)

def hertz(x,R,E,nu=0.5):
    return 4*E/3/(1-nu**2)*np.sqrt(R)*x**1.5

xpost = np.linspace(0,indmax,indpoint)
Fpost = hertz(xpost,R,E)
zpost = xpost+Fpost/k

Enew=[]
colors=['c','k','r','y','g','b']
for i in range(N):
    col = colors[i%len(colors)]
    f = open('./tmp/fake_{}_{}.tsv'.format(E,i),'w')
    f.write('#easy_tsv\n')
    f.write('#k: {} \n'.format(k))
    f.write('#R: {} \n'.format(R*1e9))
    f.write('#displacement [nm] \t #force [nN] \n')

    realcp = cp #+ 100.0e-9*np.random.normal(scale=1)
    zpre = np.linspace(0,realcp,cpoint)
    Fpre = np.zeros(len(zpre))

    F = np.append(Fpre,Fpost)
    z = np.append(zpre,zpost+realcp)

    #now randomize it
    noise = noiselevel * np.random.normal(scale=.1,size=F.shape)
    F += noise

    properz = np.linspace(0,max(z),int(max(z)*1e9))
    properF = np.interp(properz, z, F)

    #plt.plot(properz,properF,'o')
    iContact = np.argmin((properz-realcp )** 2)
    Yf = properF[iContact:]
    Xf = properz[iContact:]-realcp
    ind = Xf - Yf / k
    def Hertz(x, E):
        x = np.abs(x)
        poisson = 0.5
        return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

    #plt.plot(ind,Yf,'o',color=col)

    indmax = 2000
    jj = np.argmin((ind-indmax)**2)
    popt, pcov = curve_fit(Hertz, ind[:jj], Yf[:jj], p0=[3000], maxfev=100000)
    # E_std = np.sqrt(pcov[0][0])
    Enew.append(popt[0])

    #plt.plot(ind[:jj],Hertz(ind[:jj],E[-1]),'--',color=col)

    for j in range(len(properz)):
        f.write('{}\t{}\n'.format(properz[j]*1e9,properF[j]*1e9))
    f.close()
print('Terminated')
print(np.average(Enew))
#plt.show()