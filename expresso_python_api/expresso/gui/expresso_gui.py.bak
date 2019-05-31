import sys
import functools
import pylab
import time
import array_reader
from PyQt4 import QtCore
from PyQt4 import QtGui
from optical_sensor_gui_ui import Ui_MainWindow 
#from array_reader import *

MM2NL = 5.0e3/54.8
PIXEL2MM = 63.5e-3
CAPILLARY_VOLUME = PIXEL2MM*MM2NL*array_reader.ARRAY_SZ

DFLT_PORT = '/dev/ttyACM0'

TIMER_SINGLE_INTERVAL_MS =  25
TIMER_MULTI_INTERVAL_MS =  5

SINGLE_CHANNEL_TAB = 0
MULTI_CHANNEL_TAB = 1

STOPPED = 0
RUNNING = 1


class OpticalSensorMainWindow(QtGui.QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(OpticalSensorMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.setupTimer()
        self.initialize()

    def setupTimer(self):
        """
        Setup timer object
        """
        self.timerSingleChannel = QtCore.QTimer()
        self.timerSingleChannel.setInterval(TIMER_SINGLE_INTERVAL_MS)
        self.timerSingleChannel.timeout.connect(self.timerSingleChannel_Callback)

        self.timerMultiChannel = QtCore.QTimer()
        self.timerMultiChannel.setInterval(TIMER_MULTI_INTERVAL_MS)
        self.timerMultiChannel.timeout.connect(self.timerMultiChannel_Callback)

    def connectActions(self):
        self.connectLineEdit.editingFinished.connect(self.connectLineEditBlur_Callback)
        self.connectPushButton.pressed.connect(self.connectPressed_Callback)
        self.connectPushButton.clicked.connect(self.connectClicked_Callback)
        for i in range(array_reader.NUM_CHANNELS):
            rb = getattr(self,'channelRadioButton_{0}'.format(i+1))
            rb.clicked.connect(self.modeSingleChannel_Callback)
        self.singleChannelStart.clicked.connect(self.singleChannelStart_Callback)
        self.multiChannelStart.clicked.connect(self.multiChannelStart_Callback)
        #self.multiChannelStart.pressed.connect(self.modeMultiChannel_Callback)
        #self.multiChannelStart.clicked.connect(self.timerMultiChannel_Callback)
        self.tabWidget.currentChanged.connect(self.tabChanged_Callback)

        self.logMultiChannel.clicked.connect(self.logMultiChannel_Callback)

    def timerMultiChannel_Callback(self):
        if self.timerMultiChannel.isActive():
            pixelLevelList = self.dev.getLevels()
            if pixelLevelList is not None:
                for i, pixelLevel in enumerate(pixelLevelList):
                    pb = getattr(self,'multiChannelProgressBar_{0}'.format(i+1))
                    fluidLevel = pixelLevel*PIXEL2MM*MM2NL
                    if fluidLevel >= 0:
                        pb.setFormat(r'%v nl')
                        pb.show()
                        pb.setValue(fluidLevel)
                    else:
                        pb.setFormat(r'no data')
                        pb.setValue(0)
            else:
                for i in range(array_reader.NUM_CHANNELS):
                    pb.setFormat(r'no data')
                    pb.setValue(0)

    def multiChannelStart_Callback(self):
        if (self.multiChannelState==STOPPED):
            self.timerMultiChannel.start()
            rsp = self.dev.setMode(array_reader.MODE_MULTI_CHANNEL)
            self.multiChannelStart.setText('Stop')
            self.multiChannelState = RUNNING 
            self.logMultiChannel.setEnabled(True)
            return

        if (self.multiChannelState==RUNNING):
            self.timerMultiChannel.stop()
            self.logMultiChannel.setDisabled(True)
            self.multiChannelStart.setText('Start')
            self.multiChannelState = STOPPED
            for i in range(array_reader.NUM_CHANNELS):
                pb = getattr(self,'multiChannelProgressBar_{0}'.format(i+1))
                pb.setFormat(r'no data')
                pb.setValue(0)

    def timerSingleChannel_Callback(self):
        t0 = time.time()

        if not (self.timerSingleChannel.isActive()):
            self.timerSingleChannel.start()
            self.singleChannelStart.setText('Stop')

        pixelLevel, data = self.dev.getPixelData()
        fluidLevel = pixelLevel*MM2NL*PIXEL2MM
        
        # Enable boxes, update progress bar
        self.singleChannelPixelBox.setEnabled(True)
        self.singleChannelLevelBox.setEnabled(True)

        # Plot pixel data
        self.pixelPlot.set_visible(True)
        self.pixelPlot.set_data(self.pixelPosArray,data)

        # Plot level data
        if pixelLevel >= 0:
            pixelLevel = int(pixelLevel)
            fluidLevel = int(fluidLevel)
            self.levelPlot.set_xdata([pixelLevel])
            self.levelPlot.set_ydata([data[pixelLevel]])
            self.levelPlot.set_visible(True)
            self.singleChannelProgressBar.setFormat(r'%v nl')
            self.singleChannelProgressBar.show()
            self.singleChannelProgressBar.setValue(fluidLevel)
        else:
            self.levelPlot.set_visible(False)
            self.singleChannelProgressBar.setFormat(r'no data')
            self.singleChannelProgressBar.setValue(0)

        self.mpl.canvas.show()
        self.mpl.canvas.fig.canvas.draw()

        t1 = time.time()
        dt = t1-t0
        #print dt

    def singleChannelStart_Callback(self):
        if (self.timerSingleChannel.isActive()):
            self.timerSingleChannel.stop()
            self.singleChannelPixelBox.setDisabled(True)
            self.singleChannelLevelBox.setDisabled(True)
            self.singleChannelStart.setText('Start')
            self.multiChannelStart.setEnabled(True)
            self.singleChannelProgressBar.setFormat(r'no data')
            self.singleChannelProgressBar.setValue(0)
            self.mpl.canvas.hide()
        else:
            self.timerSingleChannel.start()
            self.singleChannelPixelBox.setEnabled(True)
            self.singleChannelLevelBox.setEnabled(True)
            self.singleChannelStart.setText('Stop')
            self.multiChannelStart.setEnabled(False)
            
    def modeSingleChannel_Callback(self):
        for i in range(array_reader.NUM_CHANNELS):
            rb = getattr(self,'channelRadioButton_{0}'.format(i+1))
            if rb.isChecked():
                break
        rsp = self.dev.setMode(array_reader.MODE_SINGLE_CHANNEL,i)
        self.singleChannelStart.setEnabled(True)

    def logMultiChannel_Callback(self):
        pass
    
    def connectLineEditBlur_Callback(self):
        self.port = str(self.connectLineEdit.text())

    def initialize(self):

        self.dev = None
        self.port = DFLT_PORT
        self.isConnected = False
        self.connectLineEdit.setText(self.port)
        self.setWidgetEnableOnDisconnect()
        self.multiChannelState = STOPPED

        # Set progressbar ranges
        self.singleChannelProgressBar.setRange(0,CAPILLARY_VOLUME)
        for i in range(1,6):
            progressBar = getattr(self,'multiChannelProgressBar_{0}'.format(i))
            progressBar.setRange(0,CAPILLARY_VOLUME)

    def connectPressed_Callback(self):
        if self.dev == None:
            self.connectPushButton.setText('Disconnect')
            self.connectLineEdit.setEnabled(False)

    def connectClicked_Callback(self):
        if self.dev == None:
            self.dev = array_reader.ArrayReader(
                    port=self.port,
                    baudrate=3000000,
                    timeout=1
                    )
            self.isConnected = True
            self.setWidgetEnableOnConnect()
        else:
            self.connectPushButton.setText('Connect')
            self.dev.close()
            self.dev = None
            self.isConnected = False
            self.setWidgetEnableOnDisconnect()

    def tabChanged_Callback(self):
        if self.isConnected:
            self.setWidgetEnableOnConnect()
        else:
            self.setWidgetEnableOnDisconnect()

    def setWidgetEnableOnConnect(self):
        if (self.tabWidget.currentIndex()==SINGLE_CHANNEL_TAB):
            self.connectLineEdit.setEnabled(False)
            for i in range(array_reader.NUM_CHANNELS):
                rb = getattr(self,'channelRadioButton_{0}'.format(i+1))
                rb.setEnabled(True)
            
            # Initialize plot
            self.pixelPlot, = self.mpl.canvas.ax.plot([],[],linewidth=2)
            self.levelPlot, = self.mpl.canvas.ax.plot([0],[0],'or')
            self.pixelPlot.set_visible(False)
            self.levelPlot.set_visible(False)

            # Sensor data
            self.pixelPosArray = pylab.arange(0,array_reader.ARRAY_SZ)

            self.mpl.canvas.ax.set_autoscale_on(False)
            #self.mpl.canvas.ax.set_visible(False)
            self.mpl.canvas.ax.set_position([.175,.175,.75,.75])
            self.mpl.canvas.ax.grid('on')
            self.mpl.canvas.ax.set_xlim(0,array_reader.ARRAY_SZ)
            self.mpl.canvas.ax.set_ylim(0,500)
            self.mpl.canvas.ax.set_xlabel('percentage (%)')
            self.mpl.canvas.ax.set_ylabel('intensity (V)')
            self.mpl.canvas.ax.set_xticks(range(0,array_reader.ARRAY_SZ,array_reader.ARRAY_SZ/4)+[array_reader.ARRAY_SZ])
            self.mpl.canvas.ax.set_xticklabels([0,25,50,75,100])
            #self.mpl.canvas.ax.xaxis.set_major_locator(self.mpl.canvas.ax.maxNLocator(4))
            self.mpl.canvas.hide()
            #self.mpl.canvas.ax.set_title('Stopped')

        if (self.tabWidget.currentIndex()==MULTI_CHANNEL_TAB):
            self.multiChannelLevelBox.setEnabled(True)
            self.multiChannelStart.setEnabled(True)
            self.logMultiChannel.setDisabled(True)
            for i in range(array_reader.NUM_CHANNELS):
                pb = getattr(self,'multiChannelProgressBar_{0}'.format(i+1))
                pb.setFormat(r'no data')
                pb.setValue(0)

    def setWidgetEnableOnDisconnect(self):
        self.connectLineEdit.setEnabled(True)
        if (self.tabWidget.currentIndex()==SINGLE_CHANNEL_TAB):
            for i in range(array_reader.NUM_CHANNELS):
                rb = getattr(self,'channelRadioButton_{0}'.format(i+1))
                if rb.isChecked():
                    rb.setChecked(False)
                rb.setDisabled(True)
            self.singleChannelPixelBox.setDisabled(True)
            self.singleChannelLevelBox.setDisabled(True)
            self.singleChannelStart.setDisabled(True)
            self.singleChannelProgressBar.setFormat(r'no data')
            self.mpl.canvas.hide()
            if self.timerSingleChannel.isActive():
                self.timerSingleChannel.stop()
            if self.timerMultiChannel.isActive():
                self.timerMultiChannel.stop()
                
        if (self.tabWidget.currentIndex()==MULTI_CHANNEL_TAB):
            self.logMultiChannel.setDisabled(True)
            self.multiChannelStart.setDisabled(True)
            self.multiChannelLevelBox.setDisabled(True)
            for i in range(array_reader.NUM_CHANNELS):
                pb = getattr(self,'multiChannelProgressBar_{0}'.format(i+1))
                pb.setFormat(r'no data')
                pb.setValue(0)
            if self.timerSingleChannel.isActive():
                self.timerSingleChannel.stop()
            if self.timerMultiChannel.isActive():
                self.timerMultiChannel.stop()

    def main(self):
        self.show()


def opticalSensorMain():
    app = QtGui.QApplication(sys.argv)
    mainWindow = OpticalSensorMainWindow()
    mainWindow.main()
    app.exec_()

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    opticalSensorMain()
