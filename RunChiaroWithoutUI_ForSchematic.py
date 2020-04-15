import chiaro_ForWithoutUI as chiaro
import csv

fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\FigAc_IndentFromRosNoNoise.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\FigAd_ElastoFromRosNoNoise.csv"

GenerateFake_params = [ 0, 4000,  20000, 2000, 300, 0] #noiselevel, maxlength, E1, E2, d0, mode: 0=50*same curve, 1=curves for different d
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [30, 500, 2000, 0.75]  # grainstep, scaledistance, maxind, cutoff

c=chiaro.curveWindow()
print('Step 0: Starting!')
c.generateFake(params=GenerateFake_params)
print('Step 1: Data loaded & Indentation calculated!')
c.b3_Alistography(params=Elasto3_params)
print('Step 2: Elastic spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 3: Hertz calculated!')

##save data to csv for figure graphs
s=c.b3['exp'][0]
data1a=['d'] + list(s.indentation)
data1b=['F'] + list(s.touch)
data2a=['d']+ list(s.ElastX)
data2b=['E'] + list(s.ElastY)
with open(fname_IndentResultsData, mode='w', newline='') as f:
    w=csv.writer(f)
    w.writerow(data1a)
    w.writerow(data1b)
with open(fname_ElastoAllData, mode='w', newline='') as f:
    w=csv.writer(f)
    w.writerow(data2a)
    w.writerow(data2b)
print('Step 8: Data saved to txt!')
