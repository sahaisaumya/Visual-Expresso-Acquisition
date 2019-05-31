import time
import serial
import struct
import matplotlib.pylab as pylab

ARRAY_SZ = 768
INWAITING_DT = 0.05
BUF_EMPTY_NUM = 3
BUF_EMPTY_DT = 0.01

class ArrayReader(serial.Serial):

    def __init__(self,**kwargs):
        super(ArrayReader,self).__init__(**kwargs)
        time.sleep(2.0)

    def emptyBuffer(self):
        """
        Empty the serial input buffer.
        """
        for i in range(0,BUF_EMPTY_NUM):
            self.flushInput()
            time.sleep(BUF_EMPTY_DT)

    def getFakeData(self):
        fakeData = 800*pylab.ones((ARRAY_SZ,))
        fakeData[:200] = 0.0*fakeData[:200]
        return fakeData

    def getLevel(self):
        self.emptyBuffer()
        self.write('y\n')
        time.sleep(0.1)
        line = self.readline()
        line = line.split()
        try:
            value = float(line[0]) 
        except:
            print line
            value = None
        return value 

    def getPixelData(self):
        self.emptyBuffer()
        self.write('x\n')
        # Wait until all data has arrived.
        while self.inWaiting() < ARRAY_SZ: # 2 bytes per data point
            time.sleep(INWAITING_DT)

        # Handles data from new firmware stream style
        data = []
        while len(data) < ARRAY_SZ and self.inWaiting() > 0:
            value = ord(self.read(1))
            data.append(value)

        if len(data) == ARRAY_SZ:
            return pylab.array(data)
        else:
            return None

