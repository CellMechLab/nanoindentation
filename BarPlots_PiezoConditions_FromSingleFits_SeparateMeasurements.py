import csv
from matplotlib import pyplot as plt
import numpy as np

names=['WT', 'P1', 'KO', 'Plastin', 'Filamin', 'P1+10uMYoda', 'KO+10uMYoda']
data_0=['WT_1_20200316', 'WT_2_20200316','WT_3_20200316']
data_1=['P1_1_20200227', 'P1_2_20200316', 'P1_3_20200316', 'P1_4_20200316']
data_2=['KO_1_20200316', 'KO_2_20200316', 'KO_3_20200316']
data_3=['Plastin_1_20200305', 'Plastin_2_20200316', 'Plastin_3_20200316']
data_4=['Filamin_1_20200305', 'Filamin_2_20200316', 'Filamin_3_20200316']
data_5=['P1+Y10M_1_20200227', 'P1+Y10M_2_20200227', 'P1+Y10M_3_20200227']
data_6=['KO+Y10M_1_20200227', 'KO+Y10M_2_20200227', 'KO+Y10M_3_20200227']
names_meas=[data_0, data_1, data_2, data_3, data_4, data_5, data_6]

files_SingleFits=[]
files=[]
filesY=[]
for n in names:
    files_SingleFits.append('data_Piezo\ElastoHistoPiezo_' +n +'.csv')
    files.append('data_Piezo\\' +n +'_BilayerFit.tsv')
    filesY.append('data_Piezo\\' +n +'_Y.np.txt')
file_out=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_Piezo\PiezoConditions_FromSingleFits_SeparateMeasurements_BarPlots.csv"

files_meas=[]
filesY_meas=[]
for i, f in enumerate(files):
    file_meas=[]
    fileY_meas=[]
    y=filesY[i]
    for j, g in enumerate(names_meas[i]):
        file_meas.append(f[:-14]+g+f[-15:])
        fileY_meas.append(y[:-8]+g+y[-9:])
    files_meas.append(file_meas)
    filesY_meas.append(fileY_meas)

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
invalid0=[]
for file in files_SingleFits:
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            row=np.asarray(row)[1:]
            row=row.astype(float)
            if i==0:
                E0s = row
            if i==1:
                E0s_std = row
            if i==2:
                Ebs = row
            if i==3:
                Ebs_std = row
            if i==4:
                d0s = row
            if i==5:
                d0s_std = row
        E0 = np.average(E0s, weights=1 / E0s_std**2)
        Eb = np.average(Ebs, weights=1 / Ebs_std**2)
        d0 = np.average(d0s, weights=1 / d0s_std**2)
        E0_std=np.sqrt(np.average((E0s-E0)**2, weights=1/1 / E0s_std**2))
        Eb_std = np.sqrt(np.average((Ebs - Eb) ** 2, weights=1 / 1 / Ebs_std ** 2))
        d0_std = np.sqrt(np.average((d0s - d0) ** 2, weights=1 / 1 / d0s_std ** 2))
        #E0_std = np.std(E0s)
        #Eb_std = np.std(Ebs)
        #d0_std = np.std(d0s)
        E0_fit.append(E0)
        Eb_fit.append(Eb)
        d0_fit.append(d0)
        E0_fitstd.append(E0_std)
        Eb_fitstd.append(Eb_std)
        d0_fitstd.append(d0_std)

for file in filesY:
    Y=np.loadtxt(file, delimiter='\t')
    Ymean=np.mean(Y)
    Ystd=np.std(Y)
    Ys.append(Y)
    Ymeans.append(Ymean)
    Ymeanstd.append(Ystd)

E0s_meas=[]
Ebs_meas=[]
d0s_meas=[]
E0s_meas_std=[]
Ebs_meas_std=[]
d0s_meas_std=[]
Ys_meas_means = []
Ys_meas_std = []
E0sm_means=[]
Ebsm_means=[]
d0sm_means=[]
Ysm_means=[]
E0sm_std=[]
Ebsm_std=[]
d0sm_std=[]
Ysm_std=[]
scatterx_E0=[]
scatterx_Eb=[]
scatterx_d0=[]
scatterx_Y=[]
scattery_E0=[]
scattery_Eb=[]
scattery_d0=[]
scattery_Y=[]
scatterstd_E0=[]
scatterstd_Eb=[]
scatterstd_d0=[]
scatterstd_Y=[]
for i in range(len(files_meas)):
    E0_meas=[]
    Eb_meas=[]
    d0_meas=[]
    E0_meas_std=[]
    Eb_meas_std=[]
    d0_meas_std=[]
    invalid = []
    for file in files_meas[i]:
        with open(file) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for j, row in enumerate(reader):
                if j==0:
                    Eb = float(row[2])*1e9
                    E0= float(row[1])*1e9
                    d0 = float(row[3])
                if j==1:
                    Eb_std = float(row[2])*1e9
                    E0_std= float(row[1])*1e9
                    d0_std = float(row[3])
            if E0<200000 and Eb<35000 and d0<8000:
                E0_meas.append(E0)
                Eb_meas.append(Eb)
                d0_meas.append(d0)
                E0_meas_std.append(E0_std)
                Eb_meas_std.append(Eb_std)
                d0_meas_std.append(d0_std)
                scatterx_E0.append(i)
                scattery_E0.append(E0)
                scatterstd_E0.append(E0_std)
                scatterx_Eb.append(i)
                scattery_Eb.append(Eb)
                scatterstd_Eb.append(Eb_std)
                scatterx_d0.append(i)
                scattery_d0.append(d0)
                scatterstd_d0.append(d0_std)
                invalid.append(0)
            else:
                invalid.append(1)
    E0s_meas.append(E0_meas)
    Ebs_meas.append(Eb_meas)
    d0s_meas.append(d0_meas)
    E0s_meas_std.append(E0_meas_std)
    Ebs_meas_std.append(Eb_meas_std)
    d0s_meas_std.append(d0_meas_std)
    Y_meas_means=[]
    Y_meas_std=[]
    for j, file in enumerate(filesY_meas[i]):
        Y = np.loadtxt(file, delimiter='\t')
        Ymean = np.mean(Y)
        Ystd = np.std(Y)
        if invalid[j]==0:
            Y_meas_means.append(Ymean)
            Y_meas_std.append(Ystd)
            scatterx_Y.append(i)
            scattery_Y.append(Ymean)
            scatterstd_Y.append(Ystd)
    Ys_meas_means.append(Y_meas_means)
    Ys_meas_std.append(Y_meas_std)

    E0m_means=np.average(E0_meas, weights=1/np.asarray(E0_meas_std)**2)
    E0m_std=np.std(E0_meas)
    Ebm_means=np.average(Eb_meas, weights=1/np.asarray(Eb_meas_std)**2)
    Ebm_std=np.std(Eb_meas)
    d0m_means=np.average(d0_meas, weights=1/np.asarray(d0_meas_std)**2)
    d0m_std=np.std(d0_meas)
    Ym_means=np.average(Y_meas_means, weights=1/np.asarray(Y_meas_std)**2)
    Ym_std=np.std(Y_meas_means)
    E0sm_means.append(E0m_means)
    Ebsm_means.append(Ebm_means)
    d0sm_means.append(d0m_means)
    Ysm_means.append(Ym_means)
    E0sm_std.append(E0m_std)
    Ebsm_std.append(Ebm_std)
    d0sm_std.append(d0m_std)
    Ysm_std.append(Ym_std)

scatterx=[]
for i, d in enumerate(names_meas):
    scatterx_i=np.linspace(i-0.3, i+0.3, len(d))
    for j in range(len(d)):
        scatterx.append(scatterx_i[j])


# statistical significance, if n*stds don't overlap (other criterion?)
n_overlap=3
mags=[Ymeans, E0_fit, Eb_fit, d0_fit]
stds=[Ymeanstd, E0_fitstd, Eb_fitstd, d0_fitstd]
sig=[]
colors=[]
magsm=[Ysm_means, E0sm_means, Ebsm_means, d0sm_means]
stdsm=[Ysm_std, E0sm_std, Ebsm_std, d0sm_std]
sigm=[]
colorsm=[]
nonsig_color='blue'
sig_color='red'
for j in range(len(mags)):
    base=mags[j][0]
    base_up=base+stds[j][0]*n_overlap
    base_down=base-stds[j][0]*n_overlap
    sig_j=[0]
    colors_j=[nonsig_color]
    basem=magsm[j][0]
    basem_up=basem+stdsm[j][0]*n_overlap
    basem_down=basem-stdsm[j][0]*n_overlap
    sigm_j=[0]
    colorsm_j=[nonsig_color]
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
        sigm_i=0
        colorm_i=nonsig_color
        valm=magsm[j][i]
        valm_up=valm+stdsm[j][i]*n_overlap
        valm_down=valm-stdsm[j][i]*n_overlap
        if valm > basem and valm_down > basem_up:
            sigm_i=1
            colorm_i=sig_color
        if valm < basem and valm_up < basem_down:
            sigm_i=1
            colorm_i = sig_color
        sigm_j.append(sigm_i)
        colorsm_j.append(colorm_i)
    sig.append(sig_j)
    colors.append(colors_j)
    sigm.append(sigm_j)
    colorsm.append(colorsm_j)

x=range(len(names))
fig, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, figsize=(15,6))
ax0.bar(x, Ymeans, tick_label=names, yerr=Ymeanstd, color=colors[0])
ax0.plot(scatterx_Y, scattery_Y, 'o', color='black')
#ax0.errorbar(scatterx, scattery_Y, yerr=scatterstd_Y, fmt='o', color='black')
ax0.set_title('Y')
ax1.bar(x, E0_fit, tick_label=names, yerr=E0_fitstd, color=colors[1])
ax1.plot(scatterx_E0, scattery_E0, 'o', color='black')
#ax1.errorbar(scatterx, scattery_E0, yerr=scatterstd_E0, fmt='o', color='black')
ax1.set_title('E0')
ax2.bar(x, Eb_fit, tick_label=names, yerr=Eb_fitstd, color=colors[2])
ax2.plot(scatterx_Eb, scattery_Eb, 'o', color='black')
#ax2.errorbar(scatterx, scattery_Eb, yerr=scatterstd_Eb, fmt='o', color='black')
ax2.set_title('Eb')
ax3.bar(x, d0_fit, tick_label=names, yerr=d0_fitstd, color=colors[3])
ax3.plot(scatterx_d0, scattery_d0, 'o', color='black')
#ax3.errorbar(scatterx, scattery_d0, yerr=scatterstd_d0, fmt='o', color='black')
ax3.set_title('d0')
#
# fig1, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, figsize=(15,6))
# ax0.bar(x, Ymeans, tick_label=names, yerr=Ymeanstd, color=colors[0])
# #ax0.plot(scatterx_Y, scattery_Y, 'o', color='black')
# ax0.errorbar(scatterx, scattery_Y, yerr=scatterstd_Y, fmt='o', color='black')
# ax0.set_title('Y')
# ax1.bar(x, E0_fit, tick_label=names, yerr=E0_fitstd, color=colors[1])
# #ax1.plot(scatterx_E0, scattery_E0, 'o', color='black')
# ax1.errorbar(scatterx, scattery_E0, yerr=scatterstd_E0, fmt='o', color='black')
# ax1.set_title('E0')
# ax2.bar(x, Eb_fit, tick_label=names, yerr=Eb_fitstd, color=colors[2])
# #ax2.plot(scatterx_Eb, scattery_Eb, 'o', color='black')
# ax2.errorbar(scatterx, scattery_Eb, yerr=scatterstd_Eb, fmt='o', color='black')
# ax2.set_title('Eb')
# ax3.bar(x, d0_fit, tick_label=names, yerr=d0_fitstd, color=colors[3])
# #ax3.plot(scatterx_d0, scattery_d0, 'o', color='black')
# ax3.errorbar(scatterx, scattery_d0, yerr=scatterstd_d0, fmt='o', color='black')
# ax3.set_title('d0')
#
# fig2, (ax0, ax1, ax2, ax3) = plt.subplots(1,4, figsize=(15,6))
# ax0.bar(x, Ysm_means, tick_label=names, yerr=Ysm_std, color=colorsm[0])
# ax0.plot(scatterx_Y, scattery_Y, 'o', color='black')
# #ax0.errorbar(scatterx, scattery_Y, yerr=scatterstd_Y, fmt='o', color='black')
# ax0.set_title('Y')
# ax1.bar(x, E0sm_means, tick_label=names, yerr=E0sm_std, color=colorsm[1])
# ax1.plot(scatterx_E0, scattery_E0, 'o', color='black')
# #ax1.errorbar(scatterx, scattery_E0, yerr=scatterstd_E0, fmt='o', color='black')
# ax1.set_title('E0')
# ax2.bar(x, Ebsm_means, tick_label=names, yerr=Ebsm_std, color=colorsm[2])
# ax2.plot(scatterx_Eb, scattery_Eb, 'o', color='black')
# #ax2.errorbar(scatterx, scattery_Eb, yerr=scatterstd_Eb, fmt='o', color='black')
# ax2.set_title('Eb')
# ax3.bar(x, d0sm_means, tick_label=names, yerr=d0sm_std, color=colorsm[3])
# ax3.plot(scatterx_d0, scattery_d0, 'o', color='black')
# #ax3.errorbar(scatterx, scattery_d0, yerr=scatterstd_d0, fmt='o', color='black')
# ax3.set_title('d0')

plt.tight_layout()
plt.show()

nice_names=names

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

scatter_names=['Y', 'E0', 'Eb', 'd0']
scatterx=[scatterx_Y, scatterx_E0, scatterx_Eb, scatterx_d0]
scattery=[scattery_Y, scattery_E0, scattery_Eb, scattery_d0]
scatterstd=[scatterstd_Y, scatterstd_E0, scatterstd_Eb, scatterstd_d0]
row0=['position_value'] + list(range(len(nice_names)))
row1=['position_name'] + list(nice_names)
with open(file_out[:-4]+'_SingleValues.csv', mode='w', newline='') as f:
    w = csv.writer(f)
    w.writerow(row0)
    w.writerow(row1)
    for i, n in enumerate(scatter_names):
        datax = [n + '_position']
        datay = [n + '_value']
        datastd = [n + '_std']
        for j in range(len(scatterx[i])):
            datax.append(scatterx[i][j])
            datay.append(scattery[i][j])
            datastd.append(scatterstd[i][j])
        w.writerow(datax)
        w.writerow(datay)
        w.writerow(datastd)