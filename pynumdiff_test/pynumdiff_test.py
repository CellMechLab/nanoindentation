#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:46:35 2020

@author: giuseppeciccone
"""
#import mvexperiment.experiment as experiment
import numpy as np
from scipy.integrate import cumtrapz
from scipy import signal
import pynumdiff
#Importing some experimental PDMS data 
#RealData = False #False: uses fake data, True: uses real data
if __name__ == '__main__':  #IMPORTANT FOR PARALLEL PROCESSES
    #if RealData is True: #realdata
    #    exp = experiment.Chiaro('/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/PDMS/2020_12_7_PDMS_bilayers_stiffprobe/10_1_homogeneous/10_1_homogeneous/matrix_scan01/')
    #    exp.browse()
    #    exp[0].open()
    #    cv = exp[0][1]
    #    x = cv.z
    #    y = cv.f
    #    dx = np.average( x[1:] - x[:-1] )
        
    #else: #fakedata
    #    exp = experiment.Easytsv('./Fake_Data1/')
    #    exp.browse()
    #    exp[0].open()
    #    cv = exp[0]
    #    y = cv.data['force']
    #    x = cv.data['z']
    #    dx = np.average( x[1:] - x[:-1] )
    
    
    x = np.loadtxt('x.txt')
    y = np.loadtxt('y.txt')
    dx = np.average( x[1:] - x[:-1] )
    
    #power spectral density of data
    #We should select 'frequency where power begings to decrease and noise starts to increase'
    #
    freqs, psd = signal.welch(y)
    #Frequency selection 
    cutoff_frequency =  0.009 #IMPORTANT PARAMETER FOR SMOOTH DERIVATIVE 
    #then, optimization parameter given by: 
    log_gamma = -1.6*np.log(cutoff_frequency) -0.71*np.log(dx) - 5.1
    tvgamma = np.exp(log_gamma)
    print(tvgamma)
    
    
    ###########################################
    ## PYNUMDIFF VS DERIVATIVE LIBRARY TESTS###
    ###########################################
    
    names = [ 'iterative finite diff', 'smooth finite diff (mean)', 'smooth finite diff (mean) opt']
    derivates = []
    # 1. Finite differences with central differencing using 3 points. - TOO NOISY 
    #result1 = dxdt(y, x, kind="finite_difference", k=2)
    #derivates.append(result1)
    # 2. Savitzky-Golay using cubic polynomials to fit in a centered window of length 1 - TOO NOISY 
    #result2 = dxdt(y, x, kind="savitzky_golay", left=3*dx, right=3*dx, order=3)
    #derivates.append(result2)
    # 3. Spectral derivative - TOO NOISY 
    #result3 = dxdt(y, x, kind="spectral")
    #derivates.append(result3)
    # 4. Spline derivative with smoothing set to 0.01 - TOO NOISY 
    #result4 = dxdt(y, x, kind="spline", s=1e-2)
    #derivates.append(result4)
    # 5. Total variational derivative with regularization set to 0.01 - UNSTABLE AT THE END
    #result5 = dxdt(y, x, kind="trend_filtered", order=0, alpha=0.01) 
    #derivates.append(result5)
    
    #Observations: derivative library is MUCH slower and gives very noisy results. 
    #for this, we will use the pynumdiff library, which is much faster at computing 
    #numerical derivatives of noisy data and offers an optimization procedure to find optimal 
    #parameters for given numerical derivative method. 
    
    #1.finite difference
    x_hat, dxdt_hat = pynumdiff.finite_difference.first_order(y, dx, params = [500], options={'iterate': True})
    derivates.append(dxdt_hat)
    params = [20, 4]
    #3. smooth finite difference - meandiff
    x_hat1, dxdt_hat1 = pynumdiff.smooth_finite_difference.meandiff(y, dx, params, options={'iterate': True})
    derivates.append(dxdt_hat1)
    
    #3. smooth finite difference - meandiff (finds optimised paramterers and uses them to compute deriv)
    params, val = pynumdiff.optimize.finite_difference.first_order(y, dx, params=None, 
                                                                          options={'iterate': True},
                                                                          tvgamma=tvgamma,
                                                                          dxdt_truth=None)
    
    print(params)
  
    x_hat2, dxdt_hat2 = pynumdiff.finite_difference.first_order(y, dx, params)
    derivates.append(dxdt_hat2)
    
    
    from matplotlib import pyplot as plt
    
    fig = plt.figure(figsize=(3, 3))
    plt.loglog(freqs, psd)
    plt.title('PSD: power spectral density', fontsize= 10, y = 1.05 )
    plt.xlabel('Frequency [Hz]')
    plt.vlines(cutoff_frequency, 0, 8e6, color = 'red', lw = 3)
    fig.tight_layout()
    
    fig = plt.figure(figsize=(10,5))
    orig=[]
    #integrating derivatives
    for i in range(len(derivates)):
        orig.append(cumtrapz(derivates[i], dx=dx, initial=0) )
        
    plt.subplot(121)
    for i in range(len(derivates)):
        plt.plot(x[1:],derivates[i][1:],label=names[i],alpha=1) #indexing from 1 avoids bit undershoot that badly re-scales plot
    plt.legend()
    
    plt.subplot(122)
    plt.plot(x,y,'k', label='src', ms =1, alpha = 0.5)
    for i in range(len(derivates)):
        plt.plot(x,orig[i],'-',label=names[i], alpha = 0.5)
    
    plt.legend()
    plt.show()