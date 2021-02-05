#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:46:35 2020

@author: giuseppeciccone
"""
import mvexperiment.experiment as experiment
from matplotlib import pyplot as plt
import numpy as np
import pynumdiff
from derivative import dxdt
from scipy import signal
from scipy.integrate import cumtrapz


if __name__ == '__main__':  # IMPORTANT FOR PARALLEL PROCESSES

    RealData = True

    if RealData is True:  # realdata
        exp = experiment.Chiaro(
            '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/hydrogels data/10 wv pc PEGFN/matrix_scan08 sample 1/')
        exp.browse()
        exp[0].open()
        cv = exp[0][1]
        x = cv.z
        x = x[:len(x)]
        y = cv.f
        y = y[:len(y)]
        dx = np.average(x[1:] - x[:-1])

    else:  # fakedata
        exp = experiment.Easytsv(
            '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/Synthetic_Hertz_Data/Fake_Data1/')
        exp.browse()
        exp[0].open()
        cv = exp[0]
        y = cv.data['force']
        x = cv.data['z']
        dx = np.average(x[1:] - x[:-1])
        print(dx)

    # PSD
    # We should select 'frequency where power begings to decrease and noise starts to increase'
    freqs, psd = signal.welch(y)
    # Frequency selection
    cutoff_frequency = 0.0039
    # then, optimization parameter given by:
    log_gamma = -1.6*np.log(cutoff_frequency) - 0.71*np.log(dx) - 5.1
    tvgamma = np.exp(log_gamma)
    print(tvgamma)

    ################
    ## PYNUMDIFF ###
    ################

    names = ['iterated fd', 'smooth mean fd',
             'smooth butter fd',  # 'smooth spline fd'
             'lm savgol']
    derivates = []

    # FINITE DIFFERENCES

    # finite difference first order -> too noisy
    # finite difference second order -> too noisy
    # iternative finite difference first order
    params, val = pynumdiff.optimize.finite_difference.first_order(y, dx, params=None,
                                                                   options={
                                                                       'iterate': True},
                                                                   tvgamma=tvgamma,
                                                                   dxdt_truth=None)

    # SMOOTH FINITE DIFFERENCES

    # median smoothing -> too noisy
    # mean smoothing
    params1, val1 = pynumdiff.optimize.smooth_finite_difference.meandiff(y, dx, params=None,
                                                                         options={
                                                                             'iterate': True},
                                                                         tvgamma=tvgamma,
                                                                         dxdt_truth=None)

    # Gaussian smoothing -> similar to mean smoothing
    # Friedrichs smoothing -> similar to mean smoothing
    # Butterworth smoothing
    params2, val2 = pynumdiff.optimize.smooth_finite_difference.butterdiff(y, dx, params=None,
                                                                           options={
                                                                               'iterate': True},
                                                                           tvgamma=tvgamma,
                                                                           dxdt_truth=None)

    # Spline smoothing -> very very slow
    # params3, val3 = pynumdiff.optimize.smooth_finite_difference.splinediff(y, dx, params=None,
    #                                                                        options={
    #                                                                            'iterate': True},
    #                                                                        tvgamma=tvgamma,
    #                                                                        dxdt_truth=None)

    # TVR MODELS: computationally expensive, so not worh to try

    # LINEAR MODELS

    # Sav-gol filter
    params4, val4 = pynumdiff.optimize.linear_model.savgoldiff(
        y, dx, params=None, tvgamma=tvgamma, dxdt_truth=None, options={'smooth': True})

    # KALAM SMOOTHING

    print(params)
    print(params1)
    print(params2)
    # print(params3)
    print(params4)

    x_hat, dxdt_hat = pynumdiff.finite_difference.first_order(
        y, dx, params, options={'iterate': True})
    derivates.append(dxdt_hat)

    x_hat1, dxdt_hat1 = pynumdiff.smooth_finite_difference.meandiff(
        y, dx, params1, options={'iterate': True})
    derivates.append(dxdt_hat1)

    x_hat2, dxdt_hat2 = pynumdiff.smooth_finite_difference.butterdiff(
        y, dx, params2, options={'iterate': True})
    derivates.append(dxdt_hat2)

    # x_hat3, dxdt_hat3 = pynumdiff.smooth_finite_difference.splinediff(
    #     y, dx, params3, options={'iterate': True})
    # derivates.append(dxdt_hat3)

    x_hat4, dxdt_hat4 = pynumdiff.linear_model.savgoldiff(
        y, dx, params4, options={'smooth': True})
    derivates.append(dxdt_hat4)

    fig = plt.figure(figsize=(3, 3))
    plt.loglog(freqs, psd)
    plt.title('PSD: power spectral density', fontsize=10, y=1.05)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power')
    plt.vlines(cutoff_frequency, 0, 8e6, color='red', lw=3)
    fig.tight_layout()

    fig = plt.figure(figsize=(10, 5))
    orig = []
    # integrating derivatives
    for i in range(len(derivates)):
        orig.append(cumtrapz(derivates[i], dx=dx, initial=0))

    plt.subplot(121)
    for i in range(len(derivates)):
        # indexing from 1 avoids bit undershoot that badly re-scales plot
        plt.plot(x[0:], derivates[i][0:], '-',
                 lw=2,  label=names[i], alpha=0.5)
    plt.legend()

    plt.subplot(122)
    plt.plot(x, y, 'k', label='original data', ms=0.1, alpha=0.8)
    for i in range(len(derivates)):
        plt.plot(x, orig[i], label=names[i], ms=0.1, alpha=0.8)

    plt.legend()
    plt.show()
