#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:29:21 2020

@author: giuseppeciccone
"""

#This script generates fake F-z data following a specific contact mechanics model (model) in order to test nanoindentation software 
#Only the forward segment is generated 
#Particularly, it generates a number of .tsv files (num_files) having z as first column and F as second column. 
#The files should be read in the graphical user interface using the Easy tsv format. 
#the F array has random gaussian noise (add_noise) added to it. Both noise baseline and scale can be controlled.

import matplotlib.pyplot as plt 
import numpy as np 
import csv
import os 
                                    
class FakeData:
    ##PARAMETERS SPECIFIC TO EACH MODEL: populate under specific model class (e.g. FakeHertzData -> E, v)
   parameters = {} 
   #2 nm spacing of data 
   def __init__(self,  K=5, R=3500.5, ind0 = np.linspace(-5000.0, -1.0, 2500), indc=np.linspace(0, 10000.0, 5000)): 
    self.K = K #nN/nm (cantilever spring constant )
    self.R = R #nm (probe radious)
    self.ind0 = ind0 #nm (indentation no contact)
    self.indc = indc #nm (indentation contact)
    self.ind = np.concatenate((ind0, indc)) #total indentation  
    
    def model(self): #returns z, F arrays for specific model (eg Herz, Oliver Pharr)
        pass 
    
    def add_noise(self, noise_mean, noise_std): #adds noise to force data and returns noisy F data and corresponding z
        pass
    
    def gen_data_files(self, num_files): #generates and saves data files
        pass 
    
class FakeDataHertz(FakeData): #fake Hertzian data                              
    parameters = {'E' : (5 * 1000* 10**9 / ( 10 ** 9 )**2) , 'v':  0.5} #Hertz parameters: E (nN/nm**2) and Poisson's Ratio (v)
    def model(self): 
        F = 4/3 * (self.parameters['E']/ (1-self.parameters['v']**2) ) * np.sqrt(self.R) * self.ind**(1.5)  #Hertz nN
        F = np.nan_to_num(F, nan = 0.0) #replaces Nans from negative indentations (ind0) with zeros
        dcantilver = F/self.K       
        z = self.ind + dcantilver 
        z = z + 5000.0 #shifts along x axis to have +ve values
        return z, F  #returns arrays  

    def add_noise(self, noise_baseline=0, noise_scale=0): #change noise_scale here
        z, F = self.model()
        noise =  np.random.normal(noise_baseline, noise_scale, F.shape)
        F_noise =  F + noise    
        return z, F_noise, noise_scale #returns arrays
    
    def gen_data_file(self, numfile=5): #easy tsv, change numfile here
        for nfiles in range(numfile): 
            z, F_noise, noise_scale = self.add_noise()
            folder_path = 'C:/Users/2181259c/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/Synthetic_Hertz_Data/Fake_Data%d'%noise_scale #Change Directory Here 
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = "CurveHertz_%d.tsv"%nfiles 
            with open(os.path.join(folder_path, filename), 'w') as f:
                f.write('#easy_tsv\n')
                f.write('#k: %.2f \n'%self.K)
                f.write('#R: %.2f \n'%self.R)
                f.write('#displacement [nm] \t #force [nN] \n')
                tsv_writer = csv.writer(f, delimiter='\t' )
                tsv_writer.writerows(zip(z, F_noise))

#has to be rivisited
class FakeDataBilayer(FakeData): #Doss et al., Soft Matter, 2019
    parameters = {'E1' : (10 * 1000* 10**9 / ( 10 ** 9 )**2) , 'E2' : (5 * 1000* 10**9 / ( 10 ** 9 )**2), 'h': 10000.0} #v1 = v2 = 0.5 assumed 
    def model(self):
        a0 = np.sqrt(self.R * self.ind)
        ratio = a0 /  self.parameters['h'] 
        hertz = 16 * (self.parameters['E1'] * np.sqrt(self.R) * self.ind**(1.5)) / 9
        coeff1 = 0.85 * ratio + 3.36 * ratio**2 
        coeff2 = 0.72 - 0.34 * ratio + 0.51  * ratio **2
        F = hertz * ((coeff1+1) / (coeff1 * (self.parameters['E1']/self.parameters['E2'])**coeff2 +1 ))
        F = np.nan_to_num(F, nan = 0.0) #replaces Nans from negative indentations (ind0) with zeros
        dcantilver = F/self.K       
        z = self.ind + dcantilver 
        return z, F
    
    def add_noise(self, noise_baseline=0, noise_scale=10): #change noise_scale here
        z, F = self.model()
        noise =  np.random.normal(noise_baseline, noise_scale, F.shape)
        F_noise =  F + noise    
        return z, F_noise, noise_scale #returns arrays
    
    def gen_data_file(self, numfile=5): #easy tsv, change numfile here
        for nfiles in range(numfile): 
            z, F_noise, noise_scale = self.add_noise()
            folder_path = '/Users/giuseppeciccone/OneDrive - University of Glasgow/PhD/Nanoindentation/Data/Synthetic_Hertz_Data_Bilayer/Fake_Data%d'%noise_scale
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = "CurveBilayer_%d.tsv"%nfiles 
            with open(os.path.join(folder_path, filename), 'w') as f:
                f.write('#easy_tsv\n')
                f.write('#k: %.2f \n'%self.K)
                f.write('#R: %.2f \n'%self.R)
                f.write('#displacement [nm] \t #force [nN] \n')
                tsv_writer = csv.writer(f, delimiter='\t' )
                tsv_writer.writerows(zip(z, F_noise))

#Saving #numfile files with specific #noise_scale
savefileshertz = FakeDataHertz().gen_data_file()
#savefilesbilayer = FakeDataBilayer().gen_data_file()

#Plotting
fakedata1 = FakeDataHertz().add_noise(0,1)
fakedataBilayer1 = FakeDataBilayer().add_noise(0,10)
'''plt.plot(fakedataBilayer1[0], fakedataBilayer1[1], 'ok')
plt.plot(fakedata1[0],fakedata1[1], 'or', ms = 5, alpha= 0.5)
plt.xlabel('Distance [nm]')
plt.ylabel('Force [nN]')
plt.show()'''