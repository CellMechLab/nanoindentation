import numpy as np 
import time
import copy
import math
import scipy
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# optional packages
warned = False
try:
    import pychebfun
except:
    logging.info('Import Error\nCould not import pychebfun.\nInstall pychebfun (https://github.com/pychebfun/pychebfun/) to use chebfun derivatives.\n')
    warned = True
try:
    import pydmd.dmdc
except:
    logging.info('Import Error\nCould not import pydmd.\nInstall pydmd (florisvb fork: https://github.com/florisvb/PyDMD) to use dmd derivatives.\n')
    warned = True
try:
    import cvxpy
except:
    logging.info('Import Error\nCould not import cvxpy.\nInstall cvxpy (http://www.cvxpy.org/install/index.html) to use lineardiff.\nRecommended solver: MOSEK, free academic license available: https://www.mosek.com/products/academic-licenses/ \n')
    warned = True

if warned == True:
    logging.info('Import Error\nDespite these import errors, you can still use many of the methods without additional installations.\n')