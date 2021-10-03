# Nanoindentation (NanoAnalysis) 

Nanoindentation experiments data analysis. 

## Introduction 
This user friendly graphical user interface (GUI) allows to bulk analyze nanoindentation force-distance curves of soft materials (for example hydrogels and cells) in order to get mechanical properties (Young\'s modulus) based on: 
1. The Hertz model;
2. The Oliver-Pharr model, to obtain a point-wise calculation of the Young\'s modulus, namely the elasticity spectra (ES). By fitting the ES with a bilayer model, cell's mechanical properties (cortex's modulus and thickness, cell's 'bulk' modulus) can be estimated. This method is described in our recent paper: https://doi.org/10.1186/s12951-020-00706-2.

Right now, the software only supports analysis of data obtained through a spherical indenter. 

## Important changes from previous release 
Data is now uploaded in a standard internal format (.json) after being screened in a newly designed  GUI (NanoPrepare: https://github.com/CellMechLab/NanoPrepare). The new GUI allows for cleaning of the dataset and exporting the cleaned dataset in .json, which is then uploaded in this GUI for analysis. Therefore, in order to use this GUI, NanoPrepare should be first downloaded. 

## Supported filetypes 
Internal format (.json). Conversion from manufacturers' format to .json is done in NanoPrepare. Right now, the following manufacturers' formats are supported: Optics 11 .txt files (both old and new versions are supported) and NanoSurf .txt files.

## Installation 
No installer is currently provided. In order use the GUI, a Python 3 environment with the following packages is required: PyQt5, NumPy, SciPy, PyQtGraph.

## Running the GUI
In order to access the GUI, run the nano file from the command line: 
```bash
python nano.py 
```
