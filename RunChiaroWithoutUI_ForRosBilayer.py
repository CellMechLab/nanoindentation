import chiaro_ForWithoutUI as chiaro

fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3b_IndentFromRos10Noise.csv"
fname_ElastoAllData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3c_ElastoFromRos10Noise_AllData.csv"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3c_ElastoFromRos10Noise_MedCurve+Fit.csv"
fname_HistoData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3d_HistoFromRos10Noise.csv"

GenerateFake_params = [10, 4000,  20000, 2000, 300, 0] #noiselevel, maxlength, E1, E2, d0, mode: 0=50*same curve, 1=curves for different d
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [25, 500, 2000, 0.75]  # grainstep, scaledistance, maxind, cutoff
fnamesCsv=[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData]
CsvSettings=[True, True, True, True, 'bilayer'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer'


c=chiaro.curveWindow()
print('Step 0: Starting!')
c.generateFake(params=GenerateFake_params)
print('Step 1: Data loaded & Indentation calculated!')
c.b3_Alistography(params=Elasto3_params)
print('Step 2: Elasticity spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 3: Hertz calculated!')
c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
print('Step 4: Data saved to csv!')