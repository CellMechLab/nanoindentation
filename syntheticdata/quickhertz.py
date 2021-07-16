import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

E = 6245
N = 40
R = 3400e-9
cp = 3.0e-6
indmax = 7e-6
cpoint = 1000
indpoint = 2000
Enoiselevel = 500
Fnoiselevel = 1e-10
Znoiselevel = 100e-9
k = 0.032
show = True

def hertz(x, R, E, nu=0.5):
    return 4*E/3/(1-nu**2)*np.sqrt(R)*x**1.5

def getCurve(E,indmax,indpoint,R,k):
    xpost = np.linspace(0, indmax, indpoint)
    Fpost = hertz(xpost, R, E)
    zpost = xpost+Fpost/k
    zero = np.zeros(1000)
    zres = np.linspace(0,max(zpost),indpoint)
    fres = np.interp(zres, zpost, Fpost)
    delta = zres[1]-zres[0]
    z = np.append( np.linspace(-1000*delta,-delta,1000) , zres )
    F = np.append(np.zeros(1000),fres)
    return z,F

def saveCurve(x,y,filename,R,k,E0):
    f = open(filename, 'w')
    f.write('#easy_tsv\n')
    f.write('#k: {} \n'.format(k))
    f.write('#R: {} \n'.format(R))
    f.write('#E: {} \n'.format(E0))
    f.write('#displacement [m] \t #force [N] \n')
    for xi,yi in zip(x,y):
        f.write('{}\t{}\n'.format(xi,yi))
    f.close()



#folder = '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Nanoindentation Github/nanoindentation/syntheticdata/tmp/'
folder ='./syntheticdata/tmp/'
for i in range(N):

    Enoise = Enoiselevel * np.random.normal() 
    E0 = E + Enoise

    name = 'fake_{}_{}.tsv'.format(E0, i)

    z,F = getCurve(E0,indmax,indpoint,R,k)
    # now randomize it
    noise = Fnoiselevel * np.random.normal(size=F.shape)
    F += noise

    znoise = Znoiselevel * np.random.normal(size=F.shape)
    z += znoise

    if show is True:
        plt.plot(z,F)
    saveCurve(z,F,folder+name,R,k,E0)

if show is True:
    plt.show()
print('Terminated')
