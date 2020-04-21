import plots

fnames=['data_figures/Fig5a_ElastoCells_MedCurve+Fit_Control.csv', 'data_figures/Fig5a_ElastoCells_MedCurve+Fit_Colch_1000uM.csv', 'data_figures/Fig5a_ElastoCells_MedCurve+Fit_CytoD_25uM.csv', 'data_figures/Fig5a_ElastoCells_MedCurve+Fit_Jaspla_1uM.csv']
file_bar='data_figures/Fig5bcd_CellConditions_BarPlots.csv'
file_bar_single='data_figures/Fig5bcd_CellConditions_SeparateMeasurements_BarPlots_SingleValues.csv'
file2save='figures/Figure5'
figure_structure=[1,5]
figure_size=(20,4)
mode='bilayer' #single--> linear fit + elasto data in histogram; bilayer--> 2-step exponetial fit

p=plots.plots()
p.LoadData_Conditions(fnames)
p.LoadData_BarPlots(file_bar)
p.LoadData_BarPlots_SingleValues(file_bar_single)
p.InitiateFigure(figure_structure, figure_size)
p.ElastoMed_Conditions(mode, pos=0)
p.BarPlots_WithSingleMeasurements(pos=1)
p.SaveFigSvg(file2save)
p.SaveFigPng(file2save)
