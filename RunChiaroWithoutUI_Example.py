import chiaro_ForWithoutUI as chiaro
import matplotlib.pyplot as plt

data='filepath' #for Chiaro files or Nanosurf files converted to txt

###where to save the results as csv files
fname_IndentResultsData =r"C:\...\Indent_AllData.csv"
fname_ElastoAllData =r"C:\...\Elasto_AllData.csv"
fname_ElastoResultsData =r"C:\...\Elasto_MedCurve+Fit.csv"
fname_HistoData =r"C:\...\Histo.csv"
fname_ElastoHistoData =r"C:\...\ElastoHisto.csv"
fname_AvHertzData =r"C:\...\Indent_MedCurve+Fit.csv"
fname_ResultsData =r"C:\...\Results"

###parameters to open files
open_mode = 2  # 0 for chiaro, 2 for nanosruf; possible modes: 0: open_o11new, 1: open_o11old, 2: open_nanosurf
forward_segment = 0
###parameters to prepare focre-distance curves
Filter_params = [0.4, 30, 25]  # standart: prominency=0.4, band=30, minfreq=25
Crop_params=[100,100] #how many points to crop from front and back of curve to remove filtering artefacts
###parameters to find contact point and remove invalid curves (no contact, rising elasticity spectrum)
CP_mode = 1  # possible modes: 0: 'Chiaro', 1: 'eeff', 2: 'Nanosurf', 3: 'Nanosurf_Deriv'
CP_params = [500, 0.5, 10]  # window_length, threshold_CP, threshold_invalid
Elasto2_params = [30, 500, 2000, 301, 15000]  # grainstep, scaledistance, maxind, filwin
###parameters to fit Hertz model and elastic spectra
Yfit_params = [0, 1000, 'yeserror']  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [25, 500, 2000, 15000, 'yeserror']  # grainstep, scaledistance, maxind
###parameters to save results as csv files
fnamesCsv=[fname_IndentResultsData, fname_ElastoAllData, fname_ElastoResultsData, fname_HistoData, fname_ElastoHistoData, fname_AvHertzData]
CsvSettings=[True, True, True, True, True, True, 'bilayer', 'yeserror'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer'
fname_OriginData= data



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
c.b3_Alistography(params=Elasto3_params)
print('Step 7: Elasticity spectra calculated!')
c.b3Fit(params=Yfit_params)
print('Step 8: Hertz calculated!')
c.b3_HertzFitOfAverage(params=Yfit_params)
print('Step 8: Average Hertz calculated!')
c.b3Export(fname=fname_ResultsData+"_Y.np.txt")
c.b3Export2(fit=True, fname=fname_ResultsData+"_BilayerFit.tsv")
print('Step 9: All data saved to txt and tsv!')
c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
print('Step 10: Data saved to csv!')
