import chiaro_ForWithoutUI as chiaro
import matplotlib.pyplot as plt
import numpy as np

fname_OriginData=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\Lambda_AllDataRos.txt"
fname_IndentResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3b_IndentFromRos.txt"
fname_ElastoResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3d_ElastoFromRos.txt"
fname_LambdaResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation2\nanoindentation\data_figures\Fig3f_LambdaFromRos.txt"


# fname_OriginData=r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\data\20200320_Elastography_FinalIndentData\Control\Control_1_20191217"
# fname_ResultsData =r"C:\Users\Ines\Documents\PhD\Projects\Cortex-Massimo\AnalysisScriptMassimo\GitHub_Nanoindentation\nanoindentation\data_Elasto\Control"
# open_mode = 3  # possible modes: 0: open_o11new, 1: open_o11old, 2: open_nanosurf, 3: Ros digital data
# forward_segment = 0
# Filter_params = [0.4, 30, 25]  # standart: prominency=0.4, band=30, minfreq=25
# CP_mode = 1  # possible modes: 0: 'Chiaro', 1: 'eeff', 2: 'Nanosurf', 3: 'Nanosurf_Deriv'
# CP_params = [100, 1.5, 10]  # window_length, threshold_CP, threshold_invalid
# Elasto2_params = [30, 500, 2000, 301]  # grainstep, scaledistance, maxind, filwin
GenerateFake_params = [ 0, 4000,  20000, 2000, 300, 1] #noiselevel, maxlength, E1, E2, d0, mode: 0=50*same curve, 1=curves for different d
Yfit_params = [0, 1000]  # mode (0: maxIndentation, 1: maxForce), maxIndentValue
Elasto3_params = [30, 500, 2000]  # grainstep, scaledistance, maxind


c=chiaro.curveWindow()
print('Step 0: Starting!')
c.generateFake(fname=fname_OriginData, params=GenerateFake_params)
print('Step 5: Data loaded & Indentation calculated!')
c.b3Fit(params=Yfit_params)
print('Step 6: Hertz calculated!')
c.b3_Alistography(params=Elasto3_params)
print('Step 7: Elastic spectra calculated!')
#c.b3Export(fname=fname_ResultsData+"_Y.np.txt")
#c.b3Export2(fit=False, fname=fname_ResultsData+"_Bilayer.tsv")
#c.b3Export2(fit=True, fname=fname_ResultsData+"_BilayerFit.tsv")
#print('Step 8: All data saved !')


# ### save indent and elasto data
# label1=[]
# data1=[]
# label2=[]
# data2=[]
# for i, s in enumerate(c.b3['exp']):
#     label1.append('z_'+str(i))
#     label1.append('F_'+str(i))
#     data1.append(s.indentation)
#     data1.append(s.touch)
#     label2.append('z_'+str(i))
#     label2.append('E_'+str(i))
#     data2.append(s.ElastX)
#     data2.append(s.ElastY)
#     #plt.plot(s.indentation, s.touch)
#     #plt.plot(s.ElastX, s.ElastY)
# label1='\t'.join(label1)
# label2='\t'.join(label2)
#
# with open(fname_IndentResultsData, 'w') as f:
#     f.write(label1)
#     for i in range(len(data1[0])):
#         data_str='\n'
#         for j in range(len(data1)):
#             data_str += str(data1[j][i]) + '\t'
#         #data1 = '\t'.join(str(data1[:][i])) + '\n'
#         f.write(data_str)
#     f.close()
#
# with open(fname_ElastoResultsData, 'w') as f:
#     f.write('{}\n'.format(label2))
#     for i in range(len(data2[0])):
#         data_str='\n'
#         for j in range(len(data2)):
#             data_str += str(data2[j][i]) + '\t'
#         #data1 = '\t'.join(str(data1[:][i])) + '\n'
#         f.write(data_str)
#     f.close()


## calibrate lambda --> l=1.31 from fit2
d_real=np.asarray(range(200, 420, 20))

d01=np.asarray(c.d01)
lambda1=d_real/d01
std_d01=np.asarray(c.std_d01)
popt1, cov1 = np.polyfit(d_real, d01, 1, w=1/std_d01, cov=True)
lambda1_fit=1/popt1[0]
lambda1_std=np.sqrt(cov1[0][0])/popt1[0]**2
print(lambda1_fit, lambda1_std)

d02=np.asarray(c.d02)
lambda2=d_real/d02
std_d02=np.asarray(c.std_d02)
popt2, cov2 = np.polyfit(d_real, d02, 1, w=1/std_d02, cov=True)
lambda2_fit=1/popt2[0]
lambda2_std=np.sqrt(cov2[0][0])/popt2[0]**2
print(lambda2_fit, lambda2_std)

d03=np.asarray(c.d03)
lambda3=d_real/d03
std_d03=np.asarray(c.std_d03)
popt3, cov3 = np.polyfit(d_real, d03, 1, w=1/std_d03, cov=True)
lambda3_fit=1/popt3[0]
lambda3_std=np.sqrt(cov3[0][0])/popt3[0]**2
print(lambda3_fit, lambda3_std)

d04=np.asarray(c.d04)
lambda4=d_real/d04
std_d04=np.asarray(c.std_d04)
popt4, cov4 = np.polyfit(d_real, d04, 1, w=1/std_d04, cov=True)
lambda4_fit=1/popt4[0]
lambda4_std=np.sqrt(cov4[0][0])/popt4[0]**2
print(lambda4_fit, lambda4_std)

#plt.plot(d_real, c.d01)
plt.plot(d_real, c.d02)
#plt.plot(d_real, c.d03)
#plt.plot(d_real, c.d04)

def linear(x, a, b):
    y=a*x+b
    return y

#lin1=linear(d_real, popt1[0], popt1[1])
#lin2=linear(d_real, popt2[0], popt2[1])
#lin3=linear(d_real, popt3[0], popt3[1])
#lin4=linear(d_real, popt4[0], popt4[1])

# plt.plot(d_real, lin1)
# plt.plot(d_real, lin2)
# plt.plot(d_real, lin3)
# plt.plot(d_real, lin4)
#
# label=['d_real', 'd01', 'd02', 'd03']
# data=[d_real, d01, d02, d03]
# with open(fname_LambdaResultsData, 'w') as f:
#     f.write('{}\t{}\t{}\t{}\n'.format(label[0], label[1], label[2], label[3]))
#     for i in range(len(data[0])):
#         f.write('{}\t{}\t{}\t{}\n'.format(data[0][i], data[1][i], data[2][i], data[3][i]))
#     f.close()
