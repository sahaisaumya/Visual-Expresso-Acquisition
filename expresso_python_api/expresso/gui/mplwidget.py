from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Rectangle

class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure(facecolor='w', edgecolor='w')
        self.ax = self.fig.add_subplot(111)
        rect1 = Rectangle((600,0), 168, 3.5, color=(.8,.8,.8))
        self.ax.add_patch(rect1)
        self.ax.maxNLocator = MaxNLocator
        FigureCanvas.__init__(self,self.fig)
        FigureCanvas.setSizePolicy(
                self, 
                QtGui.QSizePolicy.Expanding, 
                QtGui.QSizePolicy.Expanding
                )
        FigureCanvas.updateGeometry(self)

class MplWidget(QtGui.QWidget):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

