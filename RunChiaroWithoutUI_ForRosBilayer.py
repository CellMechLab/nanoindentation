import chiaro_ForWithoutUI as chiaro
import csv
import matplotlib.pyplot as plt
import numpy as np

#fname_OriginData=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\Lambda_AllDataRos.txt"
fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3b_IndentFromRos10Noise.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3d_ElastoFromRos10Noise_AllData.csv"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3d_ElastoFromRos10Noise_MedCurve+Fit.csv"


# fname_OriginData=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\data\20200320_Elastography_FinalIndentData\Control\Control_1_20191217"
# fname_ResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation\nanoindentation\data_Elasto\Control"
# open_mode = 3  # possible modes: 0: open_o11new, 1: open_o11old, 2: open_nanosurf, 3: Ros digital data
# forward_segment = 0
# Filter_params = [0.4, 30, 25]  # standart: prominency=0.4, band=30, minfreq=25
# CP_mode = 1  # possible modes: 0: 'Chiaro', 1: 'eeff', 2: 'Nanosurf', 3: 'Nanosurf_Deriv'
# CP_params = [100, 1.5, 10]  # window_length, threshold_CP, threshold_invalid
# Elasto2_params = [30, 500, 2000, 301]  # grainstep, scaledistance, maxind, filwin
GenerateFake_params = [10, 4000,  20000, 2000, 300, 0] #noiselevel, maxlength, E1, E2, d0, mode: 0=50*same curve, 1=curves for different d
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [30, 500, 2000, 0.75]  # grainstep, scaledistance, maxind, cutoff


c=chiaro.curveWindow()
print('Step 0: Starting!')
c.generateFake(params=GenerateFake_params)
print('Step 5: Data loaded & Indentation calculated!')
c.b3Fit(params=Yfit_params)
print('Step 6: Hertz calculated!')
c.b3_Alistography(params=Elasto3_params)
print('Step 7: Elastic spectra calculated!')
#c.b3Export(fname=fname_ResultsData+"_Y.np.txt")
#c.b3Export2(fit=False, fname=fname_ResultsData+"_Bilayer.tsv")
#c.b3Export2(fit=True, fname=fname_ResultsData+"_BilayerFit.tsv")
#print('Step 8: All data saved !')


##save data to csv for figure graphs
data1a=[]
data1b=[]
data2a=[]
data2b=[]
for i, s in enumerate(c.b3['exp']):
    label_1a=['z_'+str(i)]
    label_1b=['F_'+str(i)]
    data_1a=label_1a + list(s.indentation)
    data_1b=label_1b + list(s.touch)
    label_2a=['z_'+str(i)]
    label_2b=['E_'+str(i)]
    data_2a=label_2a + list(s.ElastX)
    data_2b=label_2b + list(s.ElastY)
    data1a.append(data_1a)
    data1b.append(data_1b)
    data2a.append(data_2a)
    data2b.append(data_2b)
data3a=['xmed'] + list(c.xmed)
data3b=['ymed'] + list(c.ymed)
data3c=['yerr'] + list(c.yerr)
data3d=['y+err'] + list(c.ymed + c.yerr)
data3e=['y-err'] + list(c.ymed - c.yerr)
data3f=['fit1x'] + list(c.xmed)
data3g=['fit1y'] + list(c.fit1)
data3h=['fit1x'] + list(c.xmed[:c.i_cutoff])
data3i=['fit2y'] + list(c.fit2[:c.i_cutoff])

with open(fname_IndentResultsData, mode='w', newline='') as f:
    w=csv.writer(f)
    for i in range(len(data1a)):
        w.writerow(data1a[i])
        w.writerow(data1b[i])

with open(fname_ElastoAllData, mode='w', newline='') as f:
    w=csv.writer(f)
    for i in range(len(data2a)):
        w.writerow(data2a[i])
        w.writerow(data2b[i])

with open(fname_ElastoResultsData, mode='w', newline='') as f:
    w=csv.writer(f)
    w.writerow(data3a)
    w.writerow(data3b)
    w.writerow(data3c)
    w.writerow(data3d)
    w.writerow(data3e)
    w.writerow(data3f)
    w.writerow(data3g)
    w.writerow(data3h)
    w.writerow(data3i)

print('Step 8: Data saved to txt!')
