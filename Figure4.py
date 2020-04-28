import plots

fnames=['data_figures/Fig4b_IndentCellExample_AllData.csv', 'data_figures/Fig4b_IndentCellExample_MedCurve+Fit.csv', 'data_figures/Fig4c_ElastoCellExample_AllData.csv', 'data_figures/Fig4c_ElastoCellExample_MedCurve+Fit.csv', 'data_figures/Fig4d_HistoCellExample.csv', None]
file2save='figures/Figure4'
figure_structure=[1,4]
figure_size=(16,4)
mode='single' #single--> linear fit + elasto data in histogram; bilayer--> 2-step exponetial fit

p=plots.plots()
p.LoadData(fnames)
p.InitiateFigure(figure_structure, figure_size)
p.ForceCurvesWithAverage(pos=1, ax_lim=[1000, 0, 4])
p.ElastoAll(mode, pos=2, ax_lim=[2000, -10000, 20000])
p.Histo(mode, pos=3)
p.SaveFigSvg(file2save)
p.SaveFigPng(file2save)