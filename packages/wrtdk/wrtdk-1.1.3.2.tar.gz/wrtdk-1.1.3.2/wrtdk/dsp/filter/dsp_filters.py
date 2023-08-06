'''
Created on Jan 22, 2019

@author: reynolds
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt, butter, filtfilt

class dsp_filter(object):
    ''' a super class for filtering data '''

    def __init__(self,ftype):
        ''' Sets the filter type '''
        self._type = ftype
        
    def filter(self,x):
        ''' filters the data '''
        return x
    
    def __str__(self):
        ''' returns the name of the filter '''
        return type(self).__name__
        
class no_filter(dsp_filter):
    ''' Performs no filtering to the data  '''
    
    def __init__(self):
        ''' sets the filter type to none '''
        super().__init__('NoFiilter')
        
    def filter(self,x):
        ''' returns the input without filtering it '''
        return x
    
class cutoff_filter(dsp_filter):
    ''' Performs an absolute cutoff filter by limiting bounds '''
    
    def __init__(self,cutoff):
        ''' sets the type to cutoff and sets the cutoff values '''
        super().__init__('CutoffFilter')
        self.setCutoff(cutoff)
        
    def setCutoff(self,cutoff):
        ''' sets the cutoff values '''
        self._cutoff = cutoff
        
    def filter(self,x):
        ''' returns the number if its inbetween the cutoff 
        values otherwise it returns an NaN '''
        y = x.copy()
        
        # cutoff filter the data
        for i,xx in np.ndenumerate(y): y[i] = max(min(xx,self._cutoff[1]),self._cutoff[0])
        
        return y
        
class median_fitler(dsp_filter):
    ''' Performs a median filter '''
    
    def __init__(self,window=15):
        ''' sets the filter type and window size '''
        super().__init__('MedianFilter')
        self.setWindow(window)
        
    def setWindow(self,window=15):
        ''' sets the window size '''
        self._win = window
    
    def filter(self,x):
        ''' run a median filter over the data '''
        return medfilt(x,self._win)

class butter_filter(dsp_filter):
    
    def __init__(self,lowcut,highcut,fs,order=4, *args, **kwargs):
        super().__init__('butterworth_filter')
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        
        if 'bandpass' in kwargs.keys() or 'bandstop' in kwargs.keys():
            cutoff = [low,high]
        else: cutoff = [low]
        
        self.b,self.a = butter(order,cutoff,*args,**kwargs)
        
    def filter(self,x):
        return filtfilt(self.b,self.a,x)

if __name__.startswith('__main__'):
    t = np.arange(100)
    x = 100.0*np.random.rand(len(t))+52e3
    
    nfilt = no_filter()
    x1 = nfilt.filter(x)
    
    mfilt = median_fitler(15)
    x2 = mfilt.filter(x)
    
    cfilt = cutoff_filter([52050,52080])
    x3 = cfilt.filter(x-np.mean(x))
    
    t1 = np.arange(0,.4,0.01)
    y1 = 10*np.cos(2*np.pi*50*t1)
    y2 = 8 * np.cos(2*np.pi*4*t1)
    y3 = y1 + y2
    
    bfilt = butter_filter(40,50,100,8,btype='lowpass',analog=False)
    x4 = bfilt.filter(y3)
    
    #plt.plot(t,x,t,x1,t,x2,t,x3)#,t1,y1)
    #plt.legend(['original','none','median','cutoff'])
    #plt.show()
    
    plt.plot(t1,y3,t1,x4)
    plt.show()
    