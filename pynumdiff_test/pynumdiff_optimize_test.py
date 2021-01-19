import numpy as np

# local imports
import pynumdiff
simulate = pynumdiff.utils.simulate
evaluate = pynumdiff.utils.evaluate

if __name__ == '__main__':

    noise_type = 'normal'
    noise_parameters = [0, 0.01]

    # time step and time series length
    dt = 0.1 # sampling time step
    simdt = 0.01 # simulation timestep
    timeseries_length =  50 # sec
    problem = 'pi_control'

    # simulate data
    x, x_truth, dxdt_truth, extras = r = pynumdiff.utils.simulate.__dict__[problem](timeseries_length, 
                                                                                noise_parameters=noise_parameters, 
                                                                                dt=dt, 
                                                                                simdt=0.01)

    cutoff_frequency = 0.1 # high frequency of signal in the data
    log_gamma = -1.6*np.log(cutoff_frequency) -0.71*np.log(dt) - 5.1
    tvgamma = np.exp(log_gamma)

    params, val = pynumdiff.optimize.smooth_finite_difference.meandiff(x, dt, params=None, 
                                                             tvgamma=tvgamma,
                                                             dxdt_truth=None)
    print('Optimal parameters: ', params)
    x_hat, dxdt_hat = pynumdiff.smooth_finite_difference.meandiff(x, dt, params)
    evaluate.plot(x, dt, x_hat, dxdt_hat, x_truth, dxdt_truth)