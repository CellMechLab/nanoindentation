import chiaro_ForWithoutUI as chiaro

data=['Control', 'Colch_1000uM', 'CytoD_10uM', 'CytoD_25uM', 'Jaspla_1uM']
data_0=['Control_1_20191217', 'Control_2_20191217','Control_3_20191217', 'Control_4_20191217', 'Control_5_20191204']
data_1=['Colch1000uM_2_20191217', 'Colch1000uM_3_20191217', 'Colch1000uM_4_20191204'] #'Colch1000uM_1_20191217', 'Colch1000uM_5_20191203'
data_2=['CytoD10uM_1_20191213', 'CytoD10uM_2_20191217', 'CytoD10uM_3_20191217', 'CytoD10uM_4_20191217']
data_3=['CytoD25uM_1_20200127', 'CytoD25uM_2_20200127', 'CytoD25uM_3_20200127']
data_4=['Jaspla1uM_1_20191217', 'Jaspla1uM_2_20191217', 'Jaspla1uM_3_20191217']
data_meas=[data_0, data_1, data_2, data_3, data_4]

fname_OriginData_front=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\data\20200320_Elastography_FinalIndentData\\"
fname_ResultsData_front =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_Elasto"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig5a_ElastoCells_MedCurve+Fit_"

open_mode = 2  # possible modes: 0: open_o11new, 1: open_o11old, 2: open_nanosurf
forward_segment = 0
Filter_params = [0.4, 30, 25]  # standart: prominency=0.4, band=30, minfreq=25
Crop_params=[100,100]
CP_mode = 1  # possible modes: 0: 'Chiaro', 1: 'eeff', 2: 'Nanosurf', 3: 'Nanosurf_Deriv'
CP_params = [100, 1.5, 10]  # window_length, threshold_CP, threshold_invalid
Elasto2_params = [25, 500, 2000, 301, 15000]  # grainstep, scaledistance, maxind, filwin, threshold_oscillations
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [30, 500, 2000, 15000, 'yeserror']  # grainstep, scaledistance, maxind, threshold_oscialltions, error_in_med_curve yes/no
CsvSettings=[False, False, True, False, False, 'bilayer', 'yeserror'] #0: save force curves, 1: save all elasto data, 2: save elasto med + fit, 3: save histo data + gauss, 4: 'single' or 'bilayer', error_in_med_curve yes/no

for i, data_i in enumerate(data):
    print('<<<<<<<< Treating data set', data_i, '! >>>>>>>>')
    for data_meas_j in data_meas[i]:
        print('<<<<<<<< Treating subset', data_meas_j, '! >>>>>>>>')
        fname_OriginData= fname_OriginData_front + data_i + "\\" + data_meas_j
        fname_ResultsData = fname_ResultsData_front + "\\" +  data_i +"_"+ data_meas_j
        fnamesCsv = [None, None, fname_ElastoResultsData+data_i+'_'+data_meas_j+'.csv', None]

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
        # c.pars2=c.pars1
        # c.covs2=c.covs1
        c.b3Export(fname=fname_ResultsData+"_Y.np.txt")
        #c.b3Export2(fit=False, fname=fname_ResultsData+"_Bilayer.tsv")
        c.b3Export2(fit=True, fname=fname_ResultsData+"_BilayerFit.tsv")
        print('Step 9: All data saved for', data_i, '!')
        #c.b3ExportToCsvForPlots(fnamesCsv, CsvSettings)
        #print('Step 10: Data saved to csv!')