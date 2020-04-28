import plots

fnames=['data_figures/Fig2b_IndentGel_AllData.csv', 'data_figures/Fig2b_IndentGel_MedCurve+Fit.csv', 'data_figures/Fig2c_ElastoGel_AllData.csv', 'data_figures/Fig2c_ElastoGel_MedCurve+Fit.csv', 'data_figures/Fig2d_HistoGel.csv', None]
file2save='figures/Figure2'
figure_structure=[1,4]
figure_size=(16,4)
mode='single' #single--> linear fit + elasto data in histogram; bilayer--> 2-step exponetial fit

p=plots.plots()
p.LoadData(fnames)
p.InitiateFigure(figure_structure, figure_size)
p.ForceCurvesWithAverage(pos=1, ax_lim=[500])
p.ElastoAll(mode, pos=2)
p.Histo(mode, pos=3)
p.SaveFigSvg(file2save)
p.SaveFigPng(file2save)
