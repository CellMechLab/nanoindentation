# nanoindentation
Nanoindentation curve reader and analyzer

## Introduction
This program is intended to bulk analyze nanoindentation force-distance curve in 
order to get mechanical properties based on the Hertz model, in terms of Young's
modulus. 

## Supported filetypes
At the moment the software is able to open Nanosurf exported files (TXT) and
Optics11 Chiaro and Piuma TXT files (both old and nw versions are supported)

## Installation
This program is in a very early alpha, so no installer is provided. It requires a Python 3 environment with the 
following packages:
* PyQt5, numpy, scipy
* pyqtgraph