import csv
from matplotlib import pyplot as plt
import numpy as np

names=['Ctrl', 'Colch', 'Cytod', 'Jaspla']
files=['data_Elasto\Control_BilayerFit.tsv', 'data_Elasto\Colch_1000uM_BilayerFit.tsv', 'data_Elasto\CytoD_25uM_BilayerFit.tsv', 'data_Elasto\Jaspla_1uM_BilayerFit.tsv']
filesY=['data_Elasto\Control_Y.np.txt', 'data_Elasto\Colch_1000uM_Y.np.txt', 'data_Elasto\CytoD_25uM_Y.np.txt', 'data_Elasto\Jaspla_1uM_Y.np.txt']
file_out=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig5bcd_CellConditions_BarPlots.csv"

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
                Eb = float(row[2])*1e9
                E0= float(row[1])*1e9
                d0 = float(row[3])
            if i==1:
                Eb_std = float(row[2])*1e9
                E0_std= float(row[1])*1e9
                d0_std = float(row[3])
            # if i==2:
            #     E0= float(row[1])*1e9
            #     d0 = float(row[3])
            # if i==3:
            #     E0_std= float(row[1])*1e9
            #     d0_std = float(row[3])
            if i>8:
                 Ex.append(float(row[0])*1e9)
                 Ey.append(float(row[1])*1e9)
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
    Ymean=np.mean(Y)
    Ystd=np.std(Y)
    Ys.append(Y)
    Ymeans.append(Ymean)
    Ymeanstd.append(Ystd)

# statistical significance, if n*stds don't overlap (other criterion?)
n_overlap=2
mags=[Ymeans, E0_fit, Eb_fit, d0_fit]
stds=[Ymeanstd, E0_fitstd, Eb_fitstd, d0_fitstd]
sig=[]
colors=[]
nonsig_color='blue'
sig_color='red'
for j in range(len(mags)):
    base=mags[j][0]
    base_up=base+stds[j][0]*n_overlap
    base_down=base-stds[j][0]*n_overlap
    sig_j=[0]
    colors_j=[nonsig_color]
    for i in range(1, len(names)):
        sig_i=0
        color_i=nonsig_color
        val=mags[j][i]
        val_up=val+stds[j][i]*n_overlap
        val_down=val-stds[j][i]*n_overlap
        if val > base and val_down > base_up:
            sig_i=1
            color_i=sig_color
        if val < base and val_up < base_down:
            sig_i=1
            color_i = sig_color
        sig_j.append(sig_i)
        colors_j.append(color_i)
    sig.append(sig_j)
    colors.append(colors_j)

fig, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, figsize=(15,5))

ax0.bar([0,1,2,3], Ymeans, tick_label=names, yerr=Ymeanstd, color=colors[0])
ax0.set_title('Y')
ax1.bar([0,1,2,3], E0_fit, tick_label=names, yerr=E0_fitstd, color=colors[1])
ax1.set_title('E0')
ax2.bar([0,1,2,3], Eb_fit, tick_label=names, yerr=Eb_fitstd, color=colors[2])
ax2.set_title('Eb')
ax3.bar([0,1,2,3], d0_fit, tick_label=names, yerr=d0_fitstd, color=colors[3])
ax3.set_title('d0')

plt.tight_layout()
plt.show()

nice_names=['Control', 'Colchicine', 'Cytochalasin D', 'Jasplakinolide']

with open(file_out, mode='w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Condition','Value','Y (kPa)', 'E0 (kPa)', 'Eb (kPa)', 'd0 (nm)' ])
    for i, n in enumerate(names):
        label_mags = [nice_names[i], n + '_mean']
        label_stds = [nice_names[i], n + '_std']
        label_sigs = [nice_names[i], n + '_significance']
        # label_cols = [nice_names[i], n + '_color-significance']
        data_mags = label_mags
        data_stds = label_stds
        data_sigs = label_sigs
        # data_cols = label_cols
        for j in range(len(mags)):
            data_mags.append(mags[j][i])
            data_stds.append(stds[j][i])
            data_sigs.append(sig[j][i])
            # data_cols.append(colors[j][i])
        w.writerow(data_mags)
        w.writerow(data_stds)
        w.writerow(data_sigs)
        # w.writerow(data_cols)
