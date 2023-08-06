'''
Created on Aug 17, 2018

@author: reynolds
'''

import os, sys, struct
from wrtdk.parser.parser import parser
from wrtdk.parser.msg.wrtmsg import udp_wrapper
from wrtdk.io.sim.sim_simulator import sim_simulator

class mx3g(parser):
    ''' parser for the mfam mx3g message type'''

    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
        
        # initialize properites
        self.reset()
        
        # define constants
        self.COUNT_2_NT_VMAG = 1#1000 / 75
        self.NT_VMAG_2_COUNT = 1.0/self.COUNT_2_NT_VMAG
        self.COUNT_2_DEG_C = 1
        self.DEG_C_2_COUNT = 1.0/self.COUNT_2_DEG_C
        self.COUNT_2_NT = 50e-6
        self.NT_2_COUNT = 20000.0
        
    def reset(self):
        ''' resets the parser '''
        self._pps = self._minus1()
        self._synch = self._minus1()
        self._failed = self._minus1()
        self._count = self._minus1()
        self._status1 = self._minus1()
        self._status2 = self._minus1()
        self._mag1 = self._nan()
        self._stat1 = self._minus1()
        self._v1 = self._minus1()
        self._mag2 = self._nan()
        self._stat2 = self._minus1()
        self._v2 = self._minus1()
        self._bx = self._nan()
        self._by = self._nan()
        self._bz = self._nan()
        self._temperature = self._nan()
        self._a0 = self._minus1()
        self._a1 = self._minus1()
        self._a2 = self._minus1()
        self._checksum = self._minus1()
    
    def get(self,m1=0,m2=0,v1=0,v2=0,s1=0,s2=0,count=0,failed=0,synch=0,pps=0,a0=0,a1=0,a2=0,adc0=0,adc1=0,adc2=0,temp=0):
        int1 = (count & 0x03ff) | ((v2&0x0001) << 15) | ((v1&0x0001) << 14) | ((a2&0x0001) << 13) | ((a1&0x0001) << 12) | ((a0&0x0001) << 11)
        pps = ((pps & 0x0001) << 15) | ((synch & 0x0001) << 14) | (failed & 0x0001)
        return struct.pack('>HHihhihhhhi',
                           int1,
                           pps,
                           int(m1*self.NT_2_COUNT),
                           s1,
                           s2,
                           int(m2*self.NT_2_COUNT),
                           int(adc0*self.NT_VMAG_2_COUNT),
                           int(adc1*self.NT_VMAG_2_COUNT),
                           int(adc2*self.NT_VMAG_2_COUNT),
                           int(temp*self.DEG_C_2_COUNT),
                           0)
        #fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('>HHihhihhhhi',msg)
        #fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('<HHihhihhhhi',msg)
    
    def parse(self,msg):
        ''' parses the messages from the mx3g sensor platform '''
        self.reset()
        try:
            fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('>HHihhihhhhi',msg)
            self._v1 = (fid >> 14) & 0x0001
            self._v2 = (fid >> 15) & 0x0001
            self._a2 = (fid >> 13) & 0x0001
            self._a1 = (fid >> 12) & 0x0001
            self._a0 = (fid >> 11) & 0x0001
            self._count = fid & 0x03ff
            self._pps = stat >> 15
            self._synch = (stat >> 14) & 0x01
            self._failed = stat & 0x0001
            self._mag1  *= self.COUNT_2_NT
            self._status1 = stat1
            self._status2 = stat2
            self._mag2 *= self.COUNT_2_NT
            self._bx *= self.COUNT_2_NT_VMAG
            self._by *= self.COUNT_2_NT_VMAG
            self._bz *= self.COUNT_2_NT_VMAG
            self._temperature *= self.COUNT_2_DEG_C
            self._checksum = self._calculateChecksum(msg)
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))
            
    def getData(self):
        ''' returns the data from the message 
        0) mag 1 total field in nT
        1) mag 2 total field in nT
        2) bx in nT
        3) by in nT
        4) bz in nT
        5) temperature in F
        6) mag1 status
        7) mag2 status
        8) Reserved For Future Use (-1)
        9) count
        10) pps flag
        11) synched flag
        12) failed flag
        13) Mag 1 valid
        14) Mag 2 valid 
        15) A0
        16) A1
        17) A2
        '''
        return [self._mag1,self._mag2,
                self._bx,self._by,self._bz,
                self._temperature,
                self._status1,self._status2,
                -1,self._count,self._pps,
                self._synch,self._failed,
                self._v1,self._v2,
                self._a0,self._a1,self._a2]
    
    def debug(self):
        ''' debugs the message '''
        return 'id:%4d n:%4d m1:%10.3f s1:%2d s2:%2d m2:%10.3f' % (self._id,
                                                                   self._count,
                                                                   self._mag1,
                                                                   self._status1,
                                                                   self._status2,
                                                                   self._mag2)
    
class mfamfile(mx3g):
    ''' parses the mfam messages from a file '''
    
    def __init__(self):
        ''' Constructor '''
        super().__init__()# inherit superclass
    
    def parse(self, msg):
        ''' little endian parser '''
        
        try:
            fid,stat,self._mag1,stat1,stat2,self._mag2,self._bx,self._by,self._bz,self._temperature,_ = struct.unpack('<HHihhihhhhi',msg)
            self._id = (0b11111000 & (fid)) >> 3
            self._count = (fid >> 8) & 0xff + ((fid & 0b00000111) << 8)
            self._pps = ((stat & 0xff) & 0b10000000) >> 7
            self._synch = ((stat & 0xff) & 0b01000000) >> 6
            self._failed = ((stat >> 8) & 0b00000001)
            self._mag1 *= self.COUNT_2_NT
            self._status1 = stat1#(stat1 & 0b11100000) >> 5
            self._status2 = stat2#(stat2 & 0b11100000) >> 5
            self._mag2 *= self.COUNT_2_NT
            self._bx *= self.COUNT_2_NT_VMAG
            self._by *= self.COUNT_2_NT_VMAG
            self._bz *= self.COUNT_2_NT_VMAG
            self._temperature *= self.COUNT_2_DEG_C
            self._checksum = self._calculateChecksum(msg)
        except Exception as e:
            self._error = True
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d. MSG:%s'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno,msg))

def test_mfamfile():
    print('testing mfamfile ...')
    tf = mfamfile()
    filename = r'C:\Users\reynolds\Documents\1704_madunit\data\20180830_mfam\MFAM24'
    with open(filename,'rb') as f:
        n = 4
        spcr = 4
        off = 16
        mlen = 28
        msg = f.read(off+n*mlen+spcr*n)
        
        for i in range(n):
            start = off+(i)*mlen + spcr*i
            end = off+(i+1)*mlen + spcr*i
            m = msg[start:end]
            tf.parse(m)
            if not tf.hasErrored():
                print('%4d:%4d %s %3d %s' % 
                      (start,
                       end,
                       tf.debug(),
                       len(msg[start:end]),
                       str(msg[start:end])))
            else:
                print('%4d:%4d %s' % (start,end,str(msg[start:end])) )
                
def test_m3xg():
    m = mx3g()
    f = r'C:\Users\reynolds\Documents\1704_madunit\data\20190327_mfam-test\madunit_mfam_test_1.dat'
    print(os.path.exists(f))
    msg = get_msg(f,20)
    for mm in msg:
        print('len: %d msg:%s' % (len(mm),mm))
        m.parse(mm)
        print(m.getData())
    
def get_msg(filename,n=1):
    reader = sim_simulator()
    reader.read(filename,'$MFAM1')
    payload = []
    wrapper = udp_wrapper()
    while len(payload) < n:
        msg,dt = reader.getNext()
        wrapper.parse(msg[0:wrapper.LENGTH])
        if not wrapper.hasErrored():
            payload.append(msg[wrapper.getMsgStart():wrapper.getMsgEnd()])
    
    return payload
                
if __name__ == '__main__':
    test_mfamfile()
    print()
    test_m3xg()