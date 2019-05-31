from __future__ import print_function
import time
import scipy
import numpy as np
import matplotlib
matplotlib.use('GtkAgg')
import pylab
pylab.ion()
from array_reader import ArrayReader
import sys 
reader = ArrayReader(port='/dev/ttyACM0')

testSingleChannel = True
testMultiChannel = False
CHNL_1 = 0
CHNL_2 = 1
CHNL_3 = 2
CHNL_4 = 3
CHNL_5 = 4
pylab.ion()

i = 0
config = { 
        'modeDebug' : True,
        'modeSingleChannel' : False,
        'modeMultiChannel'  : False,
        'channel'           : 2,
        } 
level_lst = np.array([])
level_delta = 20
window_size = 10

while 1:
    # Single-channel mode
    if config['modeDebug']:
        channel = config['channel']
        if i==0:
            rsp = reader.setMode(3,channel)
        t0 = time.time()
        #level, pixelData = reader.getPixelData()
        level,a,b,pixelData = reader.getBoundData()
        print('upper, lower, level = ', a,b,level)
        level, derivData = reader.getWorkingBuffer()
        #line = [time.strftime('%Y-%m-%d %H:%M:%S'),str(format(level,'06.02f')), \
                #str(a),str(pixelData[a]),str(b),str(pixelData[b]),'\n']
        line = [time.strftime('%Y-%m-%d %H:%M:%S'),str(format(level,'06.02f')), \
                str(derivData),'\n']
        line = ' '.join(line)
        # Running average of level
        level_lst = np.append(level_lst,level)
        if (len(level_lst) > window_size):
            level_lst = np.delete(level_lst,0)
        level_avg = np.mean(level_lst)
        if (abs(level-level_avg)>level_delta):
            level_lst[-1] = level_avg
            with open('debug/debug_data.txt','a') as f:
                f.write(line)
                f.flush()

        t1 = time.time()
        dt = t1-t0
        #print(dt)
        #print(i,level)
        #if (level < 0):
            #sys.exit()

        if 1:    
            if i==0:
                pylab.figure(1)
                pylab.grid('on')
                h_deriv, = pylab.plot(derivData,linewidth=2)
                h_level, = pylab.plot([0],[0],'ro')
                h_level.set_visible(False)
                pylab.xlim(0,768)
                pylab.xlabel('pixel')
                pylab.ylabel('intensity')
                pylab.xlim(0,768)
                pylab.ylim(50,200)
            else:
                h_deriv.set_ydata(derivData)
                if level >= 0:
                    level = int(level)
                    h_level.set_xdata([level])
                    h_level.set_ydata([derivData[level]])
                    h_level.set_visible(True)
                else:
                    h_level.set_visible(False)
        if 0:
            if i==0:
                pylab.figure(1)
                pylab.subplot(211)
                h_line, = pylab.plot(pixelData,linewidth=2)
                pylab.grid('on')
                h_level, = pylab.plot([0],[0],'ro')
                h_a, = pylab.plot([0],[0],'yo')
                h_b, = pylab.plot([0],[0],'go')
                h_level.set_visible(False)
                pylab.grid('on')
                #pylab.ylim(100,150)
                pylab.xlim(0,768)
                pylab.xlabel('pixel')
                pylab.ylabel('intensity')
                #pylab.subplot(212)
                #h_edge, = pylab.plot(edge_data,linewidth=2)
                pylab.subplot(212)
                h_deriv, = pylab.plot(derivData,linewidth=2)
                h_aa, = pylab.plot([0],[0],'yo')
                h_bb, = pylab.plot([0],[0],'go')
                pylab.ylim(0,256)
                pylab.xlim(0,768)
                pylab.ylim(100,175)
            else:
                h_line.set_ydata(pixelData)
                h_deriv.set_ydata(derivData)
                #h_edge.set_ydata(edge_data)
                if level >= 0:
                    level = int(level)
                    h_level.set_xdata([level])
                    h_a.set_xdata([a])
                    h_b.set_xdata([b])
                    h_level.set_ydata([pixelData[level]])
                    h_a.set_ydata([pixelData[a]])
                    h_b.set_ydata([pixelData[b]])
                    h_level.set_visible(True)
                    h_aa.set_xdata([a])
                    h_bb.set_xdata([b])
                    h_aa.set_ydata([derivData[a]])
                    h_bb.set_ydata([derivData[b]])
                else:
                    h_level.set_visible(False)
        pylab.draw()

    # Multi-channel mode
    if config['modeMultiChannel']:
        if i==0:
            rsp = reader.setMode(2)
        levels = reader.getLevels()
        print(i, ": ", levels)

    i += 1
