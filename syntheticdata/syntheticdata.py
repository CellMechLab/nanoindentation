#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:29:21 2020

@author: giuseppeciccone
"""

# This script generates fake F-z data following a specific contact mechanics model (model) in order to test nanoindentation software
# Only the forward segment is generated
# Particularly, it generates a number of .tsv files (num_files) having z as first column and F as second column.
# The files should be read in the graphical user interface using the Easy tsv format.
# the F array has random gaussian noise (add_noise) added to it. Both noise baseline and scale can be controlled.

import matplotlib.pyplot as plt
import numpy as np
import csv
import os


class FakeData:
    # PARAMETERS SPECIFIC TO EACH MODEL: populate under specific model class (e.g. FakeHertzData -> E, v)
    parameters = {}
    # 2 nm spacing of data

    def __init__(self,  K=0.0186, R=3500.5, ind0=np.linspace(-5000.0, -1.0, 2500), indc=np.linspace(0, 10000.0, 5000)):
        self.K = K  # nN/nm (cantilever spring constant )
        self.R = R  # nm (probe radious)
        self.ind0 = ind0  # nm (indentation no contact)
        self.indc = indc  # nm (indentation contact)
        self.ind = np.concatenate((ind0, indc))  # total indentation
        self.params = {}  # specific contact mechanics parameters

        def model(self):  # returns z, F arrays for specific model (eg Herz, Oliver Pharr)
            pass

        # adds noise to force data and returns noisy F data and corresponding z
        def add_noise(self, noise_mean, noise_std):
            pass

        def gen_data_files(self, num_files):  # generates and saves data files
            pass


class FakeDataHertz(FakeData):  # fake Hertzian data
    # Hertz parameters: E (nN/nm**2) and Poisson's Ratio (v)

    def model(self):
        self.params = {'E': (5 * 1000 * 10**9 / (10 ** 9)**2), 'v':  0.5}
        F = 4/3 * (self.params['E'] / (1-self.params['v']**2)
                   ) * np.sqrt(self.R) * self.ind**(1.5)  # Hertz nN
        # replaces Nans from negative indentations (ind0) with zeros
        F = np.nan_to_num(F, nan=0.0)
        dcantilver = F/self.K
        z = self.ind + dcantilver
        z = z + 5000.0  # shifts along x axis to have +ve values
        return z, F  # returns arrays

    def add_noise(self, noise_baseline=0, noise_scale=3):  # change noise_scale here
        z, F = self.model()
        noise = np.random.normal(noise_baseline, noise_scale, F.shape)
        F_noise = F + noise
        return z, F_noise, noise_scale  # returns arrays

    def gen_data_file(self, numfile=50):  # easy tsv, change numfile here
        for nfiles in range(numfile):
            z, F_noise, noise_scale = self.add_noise()
            folder_path = '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/Synthetic_Hertz_Data/Fake_Data%d' % noise_scale  # Change Directory Here
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = "CurveHertz_%d.tsv" % nfiles
            with open(os.path.join(folder_path, filename), 'w') as f:
                f.write('#easy_tsv\n')
                f.write('#k: %.2f \n' % self.K)
                f.write('#R: %.2f \n' % self.R)
                f.write('#displacement [nm] \t #force [nN] \n')
                tsv_writer = csv.writer(f, delimiter='\t')
                tsv_writer.writerows(zip(z, F_noise))


# Saving #numfile files with specific #noise_scale
FakeDataHertz().gen_data_file()
# savefilesbilayer = FakeDataBilayer().gen_data_file()

# Plotting
# fakedata1 = FakeDataHertz().add_noise(0,1)
# fakedataBilayer1 = FakeDataBilayer().add_noise(0,10)
# plt.plot(fakedataBilayer1[0], fakedataBilayer1[1], 'ok')
# plt.plot(fakedata1[0],fakedata1[1], 'or', ms = 5, alpha= 0.5)
# plt.xlabel('Distance [nm]')
# plt.ylabel('Force [nN]')
# plt.show()
