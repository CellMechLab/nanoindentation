# -*- coding: utf-8 -*-

import pickle

f = open('20191203-PEGSH3.5.pickle','rb')
data = pickle.load(f)
f.close()

x = data[0].z
y = data[0].ffil

xbasic = x[:800]
ybasic = y[:800]

import numpy as np
import matplotlib.pyplot as plt

def takeout(f,j,w=0,a=1):
    if j<w+a-1:
        return f
    df = np.fft.rfft(f)
    x = np.arange(0,len(f),1)
    
    xx = np.concatenate(  ( x[j-w-a:j-w],x[j+w+1:j+w+1+a]  ) )
    yy = np.concatenate(  ( df[j-w-a:j-w],df[j+w+1:j+w+1+a]  ) )
    
    rm,rq = np.polyfit(xx, yy.real, 1)
    im,iq = np.polyfit(xx, yy.imag, 1)
    
    df.real[j-w:j+w+1] = rm*x[j-w:j+w+1]+rq
    df.imag[j-w:j+w+1] = im*x[j-w:j+w+1]+iq
    
    fnew = np.fft.irfft(df, len(f))
    return fnew

from scipy.signal import savgol_filter

def smooth(f,win,order):
    if win%2 == 0:
        win +=1
    return savgol_filter(f,win,order)


def ora(y,win=40,order=3):
    plt.plot(y,label='pre')
    ynew = takeout(y,win,order)
    plt.plot(y-ynew,label='post')
    plt.legend()
    
def yn(y,win=33):
    df = np.fft.rfft(y)
    df.real[win:-win] = savgol_filter(df.real,win,3)[win:-win]
    df.imag[win:-win] = savgol_filter(df.imag,win,3)[win:-win]
    return np.fft.irfft(df,len(y))        