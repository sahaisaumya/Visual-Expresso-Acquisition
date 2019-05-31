from PyQt4 import QtGui
from mcwidget_ui.mcwidget_ui import Ui_McWidget

class McWidget(QtGui.QWidget,Ui_McWidget):

    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        Ui_McWidget.setupUi(self,parent)
