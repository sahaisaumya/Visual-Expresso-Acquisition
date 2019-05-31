from __future__ import print_function
import serial,sys
import time
import numpy
#from expresso.libs.serial_device import SerialDevice

ARRAY_SZ = 768
NUM_CHANNELS = 5
MAX_ERROR_CNT = 10

# Serial Command Ids
CMD_SET_MODE = 0
CMD_GET_MODE = 1
CMD_GET_CHANNEL = 2
CMD_GET_LEVEL = 3
CMD_GET_LEVELS = 4
CMD_GET_PIXEL_DATA = 5
CMD_GET_WORKING_BUFFER = 6
CMD_GET_DEVICE_ID = 7
CMD_SET_DEVICE_ID = 9
CMD_UNSET_NORM_CONST = 10
CMD_SET_NORM_CONST_FROM_BUFFER = 11
CMD_SET_NORM_CONST_FROM_FLASH = 12
CMD_SET_CHANNEL = 13
CMD_SAVE_NORM_CONST_TO_FLASH=14
CMD_GET_BOUND_DATA = 15
CMD_SET_DEVICE_ID = 16

# Operating modes
MODE_STOPPED = 0
MODE_SINGLE_CHANNEL = 1
MODE_MULTI_CHANNEL = 2
MODE_DEBUG = 3

ALLOWED_MODES = (
        MODE_STOPPED, 
        MODE_SINGLE_CHANNEL, 
        MODE_MULTI_CHANNEL,
        MODE_DEBUG,
        )
ALLOWED_CHANNELS = range(0,NUM_CHANNELS)

SUCCESS_CHR = '0' 
EXPRESSO_DEV_ID = 'XP'

class ExpressoSerial(serial.Serial):

    def __init__(self, port):
        self.isExpressoDevice = False
        super(ExpressoSerial,self).__init__(port, baudrate=3000000, timeout=1)
        time.sleep(2.0)
        self.emptyBuffer()
        cmd = self.makeCommand(CMD_GET_DEVICE_ID)
        self.write(cmd)
        # The get id command should return a message 0 0x5850YYZZ which is a hex
        # encoded string for the S/N of the device. 5850 = XP, and YYZZ is the 
        # number of the device, e.g., 3031 = 01.
        line = self.readline()
        # Check that we have a successful response from the device
        if line.startswith(SUCCESS_CHR):
            line = line.split()[1]
            # Now check that this is in fact an Expresso device
            if  (len(line)>=2): 
                self.devId = line.decode("hex")
                if (self.devId[0:2]==EXPRESSO_DEV_ID):
                    self.isExpressoDevice = True
        # At this time, it would be strange to have a case where a customer 
        # has a Leaflab Maple plugged in, and it isn't an Expresso.  Thus,
        # this will notify the user, but will not halt the application.
        if not self.isExpressoDevice:
            raise RuntimeWarning, 'Device '+port+' is not an Expresso.'
            return

    def getMode(self):
        """
        Returns the operating mode of the device
        """
        cmd = self.makeCommand(CMD_GET_MODE)
        self.write(cmd)
        line = self.readline()
        if line.startswith(SUCCESS_CHR):
            line = line.rsplit()
            mode = int(line[1])
            return mode
        else:
            raise IOError, 'unable to get mode'

    def getChannel(self):
        """
        Returns the single channel mode channel setting from the device.
        """
        cmd = self.makeCommand(CMD_GET_CHANNEL)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to get channel'
        line = line.rsplit()
        chan = int(line[1])
        return chan

    def setMode(self, *args):
        """
        Sets the operating mode of the device.  For single channel mode can also set the 
        current channel setting. 
        """
        if len(args) ==  1:
            mode = int(args[0])
            self.checkMode(mode)
            cmd = self.makeCommand(CMD_SET_MODE, mode)
        else:
            mode = int(args[0])
            self.checkMode(mode)
            chan = int(args[1])
            self.checkChannel(chan)
            cmd = self.makeCommand(CMD_SET_MODE, mode, chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to set mode' 

    def setModeStopped(self):
        """
        Sets the operating mode of the device to stopped.
        """
        self.setMode(MODE_STOPPED)

    def setModeSingleChannel(self,chan=None):
        """
        Sets the operating mode of the device to single channel.
        """
        if chan == None:
            self.setMode(MODE_SINGLE_CHANNEL)
        else:
            self.setMode(MODE_SINGLE_CHANNEL, chan)

    def setModeMultiChannel(self):
        """
        Sets the mode of the device to multi channel
        """
        self.setMode(MODE_MULTI_CHANNEL)

    def setChannel(self,chan):
        """
        Sets the device's single channel mode channel setting. 
        """
        chan = int(chan)
        self.checkChannel(chan)
        cmd = self.makeCommand(CMD_SET_CHANNEL,chan)
        self.write(cmd)
        line=self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to set channel' 

    def getBoundData(self):
        """
        """
        cmd = self.makeCommand(CMD_GET_BOUND_DATA)
        self.write(cmd)

        line=self.readline()
        #if not line.startswith(SUCCESS_CHR):
            #raise IOError, 'unable to read bound data'
        line = line.split()
        level = float(line[1])
        a = int(line[2])
        b = int(line[3])

        data = []
        errorCnt = 0
        while len(data) < ARRAY_SZ:
            byte = self.read(1)
            try:
                data.append(ord(byte))
            except TypeError, e:
                errorCnt += 1
            if errorCnt >= MAX_ERROR_CNT:
                raise IOError, 'error reading pixel values'
        return level,a,b,numpy.array(data)
        
    def getPixelData(self):
        """
        Returns the fluid level and the array of pixel values from the device.

        Note, might want to break this into to functions  - a request and a
        receive. As timing is a little uneven - i.e.g sometimes we query the
        micro when it is in the middle of a big computation and it takes bit
        for it to respond.
        """
        cmd = self.makeCommand(CMD_GET_PIXEL_DATA)
        self.write(cmd)

        line=self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to read pixel data'
        line = line.split()
        level = float(line[1])

        data = []
        errorCnt = 0
        while len(data) < ARRAY_SZ:
            byte = self.read(1)
            try:
                data.append(ord(byte))
            except TypeError, e:
                errorCnt += 1
            if errorCnt >= MAX_ERROR_CNT:
                raise IOError, 'error reading pixel values'
        return level, numpy.array(data)

    def getWorkingBuffer(self):
        """
        Returns the data in the working buffer.
        """
        cmd = self.makeCommand(CMD_GET_WORKING_BUFFER)
        self.write(cmd)

        line=self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to read pixel data'
        line = line.split()
        level = float(line[1])

        data = []
        errorCnt = 0
        while len(data) < ARRAY_SZ:
            byte = self.read(1)
            try:
                data.append(ord(byte))
            except TypeError, e:
                errorCnt += 1
            if errorCnt >= MAX_ERROR_CNT:
                raise IOError, 'error reading pixel values'
        return level, numpy.array(data)

    def getLevel(self,chan=None):
        """
        Get the level for the specified channel. If chan=None then the level
        for the currently selected channel (in single channel mode)  is returned.  
        Otherwise the level for the channel specified by chan is returned. 
        """
        if chan is None:
            chan = self.getChannel()
        else:
            chan = int(chan)
            self.checkChannel(chan)
        cmd = self.makeCommand(CMD_GET_LEVEL,chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to get level'
        line = line.rsplit()
        level = float(line[1])
        return level
    
    def getLevels(self):
        """
        Get levels for all channels. 
        """
        self.getLevels_Cmd()
        levels = self.getLevels_Rsp()
        return levels

    def getLevels_Cmd(self):
        cmd = self.makeCommand(CMD_GET_LEVELS)
        self.write(cmd)

    def getLevels_Rsp(self):
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to get levels'
        line = line.rsplit()
        levels = [float(x) for x in line[1:]]
        return levels

    def unSetNormConst(self,chan):
        """
        Unsets the pixel normalization constants for the given channel
        """
        chan = int(chan)
        self.checkChannel(chan)
        cmd = self.makeCommand(CMD_UNSET_NORM_CONST,chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to unset normalization constants'
        return

    def setNormConstFromBuffer(self,chan):
        """
        Sets the pixel normalization constants for the given channel.
        """
        chan = int(chan)
        self.checkChannel(chan)
        cmd = self.makeCommand(CMD_SET_NORM_CONST_FROM_BUFFER,chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to set normalization constants from buffer'
        return

    def setNormConstFromFlash(self,chan):
        """
        Sets the pixel normalization constants for the given channel from 
        flash memory.
        """
        chan = int(chan)
        self.checkChannel(chan)
        cmd = self.makeCommand(CMD_SET_NORM_CONST_FROM_FLASH,chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to set normalization constants from flash'
        return

    def saveNormConstToFlash(self,chan):
        """
        Saves the current normalization constants to flash memory.
        """
        chan = int(chan)
        self.checkChannel(chan)
        cmd = self.makeCommand(CMD_SAVE_NORM_CONST_TO_FLASH,chan)
        self.write(cmd)
        line = self.readline()
        if not line.startswith(SUCCESS_CHR):
            raise IOError, 'unable to save normalization constants to flash'
        return

    def emptyBuffer(self):
        """
        Empty the serial input buffer.
        """
        while self.inWaiting() > 0:
            self.read()

    def makeCommand(self,*args):
        """
        Packs arguments into a command string suitable for sending to the 
        device.
        """
        args = map(str,args)
        cmd = ','.join(args)
        cmd =  '[{0}]'.format(cmd)
        return cmd

    def checkMode(self,mode): 
        if not mode in ALLOWED_MODES: 
            raise ValueError, ' mode, {0}, not allowed'.format(mode)

    def checkChannel(self,chan): 
        if not chan in ALLOWED_CHANNELS: 
            raise ValueError, 'chan, {0}, not allowed'.format(chan)

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    dev = ExpressoSerial('/dev/ttyACM0')

    if 0:
        mode = dev.getMode()
        print('mode', mode)
    if 0:
        chan = dev.getChannel()
        print('channel', chan)
    if 0:
        mode = dev.getMode()
        print('original mode:', mode)

        print('setting single channel mode')
        dev.setMode(MODE_SINGLE_CHANNEL)
        mode = dev.getMode()
        chan = dev.getChannel()
        print('mode = ', mode)
        print('chan =', chan)

        print('setting single channel mode + channel = 1')
        dev.setMode(MODE_SINGLE_CHANNEL, 1)
        mode = dev.getMode()
        chan = dev.getChannel()
        print('mode = ', mode)
        print('chan =', chan)

        print('setting single channel mode + channel = 0')
        dev.setMode(MODE_SINGLE_CHANNEL, 0)
        mode = dev.getMode()
        chan = dev.getChannel()
        print('mode = ', mode)
        print('chan =', chan)

        print('setting multi channel mode')
        dev.setMode(MODE_MULTI_CHANNEL)
        mode = dev.getMode()
        print('mode = ', mode)

        print('returning to mode stopped')
        dev.setMode(MODE_STOPPED)
        mode = dev.getMode()
        print('mode = ', mode)

    if 0:
        for i in range(NUM_CHANNELS) + [0]:
            print('setting channel to {0}'.format(i))
            dev.setChannel(i)
            chan = dev.getChannel()
            print('chan = {0}'.format(chan))

    if 0:
        dev.setMode(MODE_SINGLE_CHANNEL)
        mode = dev.getMode()
        print('mode = ', mode)

        level, data = dev.getPixelData()
        print(level)
        print(data.shape)

        dev.setMode(MODE_STOPPED)
        mode = dev.getMode()
        print('mode = ', mode)

    if 0:

        dev.setMode(MODE_SINGLE_CHANNEL,0)
        mode = dev.getMode()
        chan = dev.getChannel()
        print('mode = ', mode)
        print('chan =', chan)

        level = dev.getLevel()
        print('level = ', level)

        dev.setMode(MODE_STOPPED)
        mode = dev.getMode()
        print('mode = ', mode)

    if 0:
        dev.setMode(MODE_MULTI_CHANNEL)
        mode = dev.getMode()
        print('mode = ', mode)

        levels = dev.getLevels()
        print('levels', levels)
        
        dev.setMode(MODE_STOPPED)
        mode = dev.getMode()
        print('mode = ', mode)

    if 1:
        for i in range(0,NUM_CHANNELS):
            print('unsetting norm const for chan {0}'.format(i))
            dev.unSetNormConst(i)

    if 1:
        for i in range(0,NUM_CHANNELS):
            print('setting norm const from buffer for chan {0}'.format(i))
            dev.setNormConstFromBuffer(i)

    if 0:
        for i in range(0,NUM_CHANNELS):
            print('setting norm const from flash for chan {0}'.format(i))
            dev.setNormConstFromFlash(i)

    if 1:
        for i in range(0,NUM_CHANNELS):
            print('saving norm const to flash for chan {0}'.format(i))
            dev.saveNormConstToFlash(i)
            time.sleep(0.5)
