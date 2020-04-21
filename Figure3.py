import plots

fnames=['data_figures/Fig3b_IndentFromRos10Noise.csv', 'data_figures/Fig3c_ElastoFromRos10Noise_AllData.csv', 'data_figures/Fig3c_ElastoFromRos10Noise_MedCurve+Fit.csv', 'data_figures/Fig3d_HistoFromRos10Noise.csv']
file2save='figures/Figure3'
figure_structure=[1,4]
figure_size=(16,4)
mode='single' #single--> linear fit + elasto data in histogram; bilayer--> 2-step exponetial fit

p=plots.plots()
p.LoadData(fnames)
p.InitiateFigure(figure_structure, figure_size)
p.ForceCurves(pos=1)
p.ElastoAll(mode, pos=2)
p.Histo(mode, pos=3)
p.SaveFigSvg(file2save)
p.SaveFigPng(file2save)
