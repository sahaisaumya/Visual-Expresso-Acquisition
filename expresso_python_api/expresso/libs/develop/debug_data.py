import sys,re
import matplotlib
import pylab
import numpy as np

with open('debug_data.txt') as f:
    data = f.readlines()

deriv_data = []
time = []
level = []
deriv_data_line = []
level_plot = []
cnt = 0
level_comp = 0
for datum in data:
    line = datum.split(' ')
    if re.search('2012',line[0]):
        if (len(deriv_data_line) > 0) and (level[-1]!=level_comp):
            level_comp = level[-1]
            y = np.array(deriv_data_line)
            pylab.subplot(211)
            pylab.plot(deriv_data_line)
            deriv_data_line = []
            level_plot.append(level_comp)
            cnt+=1
        time.append(' '.join(line[0:1]))
        level.append(line[2])
        line = (' '.join(line[3:]).replace('[','')).strip()
        deriv_data_line = line.split()
    else:
        line = (' '.join(line[1:]).replace(']','')).strip()
        deriv_data_line.extend(line.split())
    if cnt > 5:
        break

pylab.subplot(212)
pylab.plot(level_plot,'ro')
pylab.show()
