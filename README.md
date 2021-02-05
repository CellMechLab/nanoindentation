# Nanoindentation
Nanoindentation data  curve reader and analyser

## Introduction
This program offers a user friendly GUI and is intended to bulk analyse nanoindentation force-distance curves of soft materials and cells in 
order to get mechanical properties (Elastic or Young's Modulus) based on: 1. The simple Hertz model; 2. The Oliver-Pharr model, to obtain a pointwise calculation of the Young's Modulus, namely the elasticity spectra. For more information, please refer to this paper: 
https://doi.org/10.1186/s12951-020-00706-2. Right now, the software only supports analysis of data obtained through a spherical indenter

## Supported filetypes
At the moment the software is able to open Nanosurf exported files (TXT) and Optics11 Chiaro and Piuma TXT files (both old and nw versions are supported). Moreover, an 'Easy tsv' file format is also supported; this is an internal format to read synthetic data

## Installation
This program is an early version, so no installer is provided. It requires a Python 3 environment with the 
following packages:
* PyQt5, numpy, scipy
* pyqtgraph

## DOC
Run the nano file to access the UI
```bash
python nano.py
```