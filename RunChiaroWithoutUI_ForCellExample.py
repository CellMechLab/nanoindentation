import chiaro_ForWithoutUI as chiaro
import matplotlib.pyplot as plt

data='Control\Control_1_20191217\\'

fname_OriginData_front=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\data\20200320_Elastography_FinalIndentData\\"
fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig4b_IndentCellExample.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig4c_ElastoCellExample_AllData.csv"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig4c_ElastoCellExample_MedCurve+Fit.csv"
fname_HistoData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig4d_HistoCellExample.csv"

open_mode = 2  # possible modes: 0: open_o11new, 1: open_o11old, 2: open_nanosurf
forward_segment = 0
Filter_params = [0.4, 30, 25]  # standart: prominency=0.4, band=30, minfreq=25
Crop_params=[100,100]
CP_mode = 1  # possible modes: 0: 'Chiaro', 1: 'eeff', 2: 'Nanosurf', 3: 'Nanosurf_Deriv'
CP_params = [100, 1.5, 10]  # window_length, threshold_CP, threshold_invalid
Elasto2_params = [30, 500, 2000, 301, 15000]  # grainstep, scaledistance, maxind, filwin
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [25, 500, 2000, 15000, 'yeserror']  # grainstep, scaledistance, maxind
fnamesCsv=[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData]
CsvSettings=[True, True, True, True, 'bilayer', 'yeserror'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer'
fname_OriginData= fname_OriginData_front + data

c=chiaro.curveWindow()
print('Step 0: Starting!')
c.b1SelectDir(fname=fname_OriginData, mode=open_mode, forward_segment=forward_segment)
print('Step 1: Curves openend!')
c.b2Filter(params=Filter_params)
print('Step 2: Curves filtered!')
c.b2_crop(params=Crop_params)
print('Step 3: Curves cropped!')
c.b2_contactPoint(mode=CP_mode, params=CP_params)
print('Step 4: Contact point found!')
c.b2_Alistography(params=Elasto2_params)
print('Step 5: Rising E(z) removed!')
c.b2tob3()
print('Step 6: Indentation calculated!')
c.b3_Alistography(params=Elasto3_params)#FromForceMed
print('Step 7: Elastic spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 8: Hertz calculated!')
c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
print('Step 9: Data saved to csv!')

#plt.plot(c.xmed, c.ymed)