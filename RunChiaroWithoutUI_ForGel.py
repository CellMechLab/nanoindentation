import chiaro_ForWithoutUI as chiaro

data='20191203-PEGSH3.5.pickle'

fname_OriginData_front=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\\"
fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2b_IndentGel.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2c_ElastoGel_AllData.csv"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2c_ElastoGel_MedCurve+Fit.csv"
fname_HistoData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig2d_HistoGel.csv"

Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [25, 500, 2000, 0.75]  # grainstep, scaledistance, maxind
fnamesCsv=[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData]
CsvSettings=[True, True, True, True, 'single']#'single'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer'
fname_OriginData= fname_OriginData_front + data

c=chiaro.curveWindow()
print('Step 0: Starting!')
c.load_pickle(fname_OriginData)
print('Step 1: Curves openend!')
c.b3_Alistography(params=Elasto3_params)
print('Step 2: Elasticity spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 3: Hertz calculated!')
c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
print('Step 4: Data saved to csv!')
