'''
Created on Jan 28, 2019

@author: reynolds
'''

import sys, os, struct, math
from wrtdk.parser.parser import parser

class lord3dm_cv5(parser):
    ''' A class for parsing the messages from the Lord Microstraim 3DM-CV5 '''

    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
        
        # initialize properties
        self.reset()
        
    def reset(self):
        ''' resets the parsed values '''
        self._y = self._nan()
        self._p = self._nan()
        self._r = self._nan()
        self._pos = 0
        self._plen = 0
        self._flen = 0
        self._fdsc = 0
        
    def get(self,roll=0,pitch=0,yaw=0):
        return struct.pack('>BBBBBBfff',
                           117,101,128,18,14,12,
                           math.radians(roll),math.radians(pitch),math.radians(yaw))
        
    def parse(self,msg):
        ''' parses rll, pitch and yaw from the 3DM-CV5 message '''
        self.reset()
        
        try:
            if msg[0] != 117: raise ValueError('Incorrect sync1 byte.')
            if msg[1] != 101: raise ValueError('Incorrect sync2 byte.')
            if msg[2] != 128: raise ValueError('Incorrect desc set byte.')
            self._plen = msg[3]
            self._pos = 4
            
            while self._pos < self._plen:
                self._flen = msg[self._pos]
                self._fdsc = msg[self._pos+1]
                
                if self._fdsc == 12:# euler angles
                    self._r,self._p,self._y = struct.unpack('>fff',
                             msg[self._pos+2:self._pos+self._flen])
                
                self._pos += self._flen
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
            
    def getData(self):
        ''' returns the data to match the BNO055 imu 
        0) roll in degrees
        1) pitch in degrees
        2) yaw in degrees
        4) temperature in celcius
        5) system calibration value
        6) accelerometer calibration value
        7) gyro calibration value
        8) mag calibration value'''
        return [math.degrees(self._r),math.degrees(self._p),math.degrees(self._y),
                self._nan(),0,0,0,0]
        
    def get_euler(self):
        return [math.degrees(self._r),
                math.degrees(self._p),
                math.degrees(self._y)]