import csv
from matplotlib import pyplot as plt
import numpy as np

names=['Ctrl', 'Colch', 'Cytod', 'Jaspla']
files=['data_b3\CtrlAll_BilayerFit.tsv', 'data_b3\ColchAll_BilayerFit.tsv', 'data_b3\CytodAll_BilayerFit.tsv', 'data_b3\JasplaAll_BilayerFit.tsv']
filesY=['data_b3\CtrlAll_Y.np.txt', 'data_b3\ColchAll_Y.np.txt', 'data_b3\CytodAll_Y.np.txt', 'data_b3\JasplaAll_Y.np.txt']

E0_fit = []
Eb_fit = []
d0_fit = []
E0_fitstd = []
Eb_fitstd = []
d0_fitstd = []
Exs=[]
Eys=[]
Ys=[]
Ymeans=[]
Ymeanstd=[]

for file in files:
    #file='data_b3' + str(\) + name + 'All_BilayerFit.tsv'
    with open(file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        Ex=[]
        Ey=[]

        for i, row in enumerate(reader):
            if i==0:
                E0= float(row[1])
                Eb = float(row[2])
                d0 = float(row[3])
            if i==1:
                E0_std= float(row[1])
                Eb_std = float(row[2])
                d0_std = float(row[3])
            if i>2:
                Ex.append(float(row[0]))
                Ey.append(float(row[1]))
        E0_fit.append(E0)
        Eb_fit.append(Eb)
        d0_fit.append(d0)
        E0_fitstd.append(E0_std)
        Eb_fitstd.append(Eb_std)
        d0_fitstd.append(d0_std)
        Exs.append(Ex)
        Eys.append(Ey)

for file in filesY:
    #file='data_b3' + str(\) + name + 'All_BilayerFit.tsv'
    Y=np.loadtxt(file, delimiter='\t')
    print(len(Y))
    Ymean=np.mean(Y)
    Ystd=np.std(Y)
    Ys.append(Y)
    Ymeans.append(Ymean)
    Ymeanstd.append(Ystd)


#fig = plt.figure(figsize=(10,20))
fig, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, figsize=(15,5))

ax0.bar([0,1,2,3], Ymeans, tick_label=names, yerr=Ymeanstd)
ax0.set_title('Y')
ax1.bar([0,1,2,3], E0_fit, tick_label=names, yerr=E0_fitstd)
ax1.set_title('E0')
ax2.bar([0,1,2,3], Eb_fit, tick_label=names, yerr=E0_fitstd)
ax2.set_title('Eb')
ax3.bar([0,1,2,3], d0_fit, tick_label=names, yerr=E0_fitstd)
ax3.set_title('d0')

plt.tight_layout()
plt.show()