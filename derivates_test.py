import mvexperiment.experiment as experiment
from scipy.integrate import cumtrapz
from scipy import signal
from derivative import dxdt
import numpy as np
from matplotlib import pyplot as plt

RealData = True

if RealData is True:  # realdata
    exp = experiment.Chiaro(
        '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/PDMS/2020_12_3_PDMS_bilayers/ind1/40_1_homogeneous/matrix_scan02')
    exp.browse()
    exp[0].open()
    cv = exp[0][1]
    x = cv.z
    x = x[:len(x)-1000]
    y = cv.f
    y = y[:len(y)-1000]
    dx = np.average(x[1:] - x[:-1])

else:  # fakedata
    exp = experiment.Easytsv(
        '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/Synthetic_Hertz_Data/Fake_Data5/')
    exp.browse()
    exp[0].open()
    cv = exp[0]
    y = cv.data['force']
    y = y[:len(y)-100]
    x = cv.data['z']
    x = x[:len(x)-100]
    dx = np.average(x[1:] - x[:-1])
    print(dx)


names = ['1', '2', '3', '4']
derivates = []

# 1. Finite differences with central differencing using 3 points.
#result1 = dxdt(y, x, kind="finite_difference", k=1)
# derivates.append(result1)
# 2. Savitzky-Golay using cubic polynomials to fit in a centered window of length 1
#result2 = dxdt(y, x, kind="savitzky_golay", left=.5, right=.5, order=3)
# derivates.append(result2)
# 3. Spectral derivative
# result3 = dxdt(y, x, kind="spectral")
# derivates.append(result3)
# # 4. Spline derivative with smoothing set to 0.01
# result4 = dxdt(y, x, kind="spline", s=1e-2)
# derivates.append(result4)
# # 5. Total variational derivative with regularization set to 0.01
# result5 = dxdt(y, x, kind="trend_filtered", order=0, alpha=1e-2)
# derivates.append(result5)

fig = plt.figure(figsize=(10, 5))
orig = []
# integrating derivatives
for i in range(len(derivates)):
    orig.append(cumtrapz(derivates[i], dx=dx, initial=0))

plt.subplot(121)
for i in range(len(derivates)):
    # indexing from 20 avoids bit undershoot that badly re-scales plot
    plt.plot(x[0:], derivates[i][0:], '-',
             lw=2,  label=names[i], alpha=0.5)
plt.legend()

plt.subplot(122)
plt.plot(x, y, 'k', label='original data', ms=0.1, alpha=0.8)
for i in range(len(derivates)):
    plt.plot(x, orig[i], label=names[i], ms=0.1, alpha=0.8)

plt.legend()
plt.show()
