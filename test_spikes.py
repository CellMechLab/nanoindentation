import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import mvexperiment.experiment as experiment


exp = experiment.Chiaro(
    '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/PDMS/2020_12_3_PDMS_bilayers/calib/calib_1/Calib/')
exp.browse()
exp[0].open()
cv = exp[0][1]
z = cv.z
f = cv.f
k = 0.450  # from file


def linear(x, a, b):
    return a*x + b


popt, pcov = curve_fit(linear, z, f)
popt1, pocov1 = curve_fit(linear, z, f/k)
print(popt)
plt.plot(z, f, label='F-Z')
plt.plot(z, f/k, label='F/k - Z')
plt.plot(z, linear(z, *popt),
         label=' F = {0} * Z + {1}'.format(popt[0], popt[1]))
plt.plot(z, linear(z, *popt1),
         label=' F/k = {0} * Z + {1}'.format(popt1[0], popt1[1]))


plt.legend()
plt.show()
