import chiaro_ForWithoutUI as chiaro
import matplotlib.pyplot as plt

#data=r'gels\\01-20191113-02-screened.pickle'
#data='01-20191113-02-screened.pickle'
#data='20191203-PEGSH3.5.pickle'
data='gel.pickle'

fname_OriginData_front=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\\"
fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2b_IndentGel_AllData.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2c_ElastoGel_AllData.csv"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2c_ElastoGel_MedCurve+Fit.csv"
fname_HistoData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2d_HistoGel.csv"
fname_AvHertzData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2b_IndentGel_MedCurve+Fit.csv"


Yfit_params = [0, 500, 'yeserror']  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [10, 500, 500, 15000, 'yeserror']  # grainstep, scaledistance, maxind, threshold_oscialltions, error_in_med_curve yes/no
fnamesCsv=[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData, None, fname_AvHertzData]
CsvSettings=[True, True, True, True, False, True, 'single', 'yeserror'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer', error_in_med_curve yes/no
fname_OriginData= fname_OriginData_front + data

c=chiaro.curveWindow()
print('Step 0: Starting!')
c.load_pickle(fname_OriginData)
print('Step 1: Curves openend!')
c.b3_Alistography(params=Elasto3_params)
print('Step 2: Elasticity spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 3: Hertz calculated!')
c.b3_HertzFitOfAverage(params=Yfit_params)
print('Step 8: Average Hertz calculated!')
c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
print('Step 4: Data saved to csv!')
