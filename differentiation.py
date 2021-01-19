# -*- coding: utf-8 -*-

import mvexperiment.experiment as experiment
from scipy.integrate import cumtrapz
from derivative import dxdt
import numpy as np
from matplotlib import pyplot as plt

exp = experiment.Chiaro("../../Piuma/Oana/2019-10-17/5LMVPM/matrix_scan01/")
exp.browse()
exp[0].open()  
cv = exp[0][1]

x=cv.z
y=cv.f
dx = np.average( x[1:]-x[:-1] )

names = ['finite_difference','savitzky_golay','spectral','spline','trend_filtered']
names = ['finite_difference','savitzky_golay','spline','trend_filtered']

derivates = []
# 1. Finite differences with central differencing using 3 points.
result1 = dxdt(y, x, kind="finite_difference", k=2)
derivates.append(result1)
# 2. Savitzky-Golay using cubic polynomials to fit in a centered window of length 1
result2 = dxdt(y, x, kind="savitzky_golay", left=3*dx, right=3*dx, order=3)
derivates.append(result2)
# 3. Spectral derivative
#result3 = dxdt(y, x, kind="spectral")
#derivates.append(result3)
# 4. Spline derivative with smoothing set to 0.01
result4 = dxdt(y, x, kind="spline", s=1e-2)
derivates.append(result4)
# 5. Total variational derivative with regularization set to 0.01
result5 = dxdt(y, x, kind="trend_filtered", order=0, alpha=0.001)
derivates.append(result5)


orig=[]
for i in range(len(derivates)):
    orig.append(cumtrapz(derivates[i], dx=dx, initial=0) )
    
plt.subplot(121)
for i in range(len(derivates)):
    plt.plot(x,derivates[i],label=names[i],alpha=0.75)
plt.legend()

plt.subplot(122)
N=200
plt.plot(x,y-y[N],'ko',label='src')
for i in range(len(derivates)):
    plt.plot(x,orig[i]-orig[i][N],'--',label=names[i])
plt.legend()

plt.show()
