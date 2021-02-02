import numpy as np
import matplotlib.pyplot as plt

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

def hertz(x,R,E,nu=0.5):
    return 4*E/3/(1-nu**2)*np.sqrt(R)*x**1.5

xpost = np.linspace(0,indmax,indpoint)
Fpost = hertz(xpost,R,E)
zpost = xpost+Fpost/k

for i in range(N):
    f = open('./tmp/fake_{}_{}.tsv'.format(E,i),'w')
    f.write('#easy_tsv\n')
    f.write('#k: %.2f \n' % k)
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

    plt.plot(properz,properF)

    for j in range(len(properz)):
        f.write('{}\t{}\n'.format(properz[j]*1e9,properF[j]*1e9))
    f.close()
print('Terminated')
plt.show()