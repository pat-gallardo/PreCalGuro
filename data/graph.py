# EXAMPLE PARABOLA 1 GRAPH

from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class parabolaGraph1Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(parabolaGraph1Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # num_x = int("How many x-axis? ")
        # num_y = int("How many y-axis? ")

        x = [0, 0]
        y = [0,-5]

        # x1 =[]
        # y1 =[]
        # for x in 
        x1 = [-10, -9, -8, -6, -3 ,0 , 3, 6, 8, 9, 10]
        y1 = [-10, -7, -5, -3, -1, 0, -1, -3, -5, -7, -10]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')

        self.plot(x1, y1, (0,0,0), QtCore.Qt.SolidLine)
        self.plot(x, y, (250,0,0), QtCore.Qt.DashLine)

    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 30)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = parabolaGraph1Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# # EXAMPLE PARABOLA 2 GRAPH
class parabolaGraph2Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(parabolaGraph2Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # num_x = int("How many x-axis? ")
        # num_y = int("How many y-axis? ")

        x = [-1, 1]
        y = [3, 3]

        x1 = [7, 5, 3,1, -1, 1, 3, 5, 7 ]
        y1 = [11, 10,9, 7, 3, -1, -3, -4, -5]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')

        self.plot(x1, y1, (0,0,0), QtCore.Qt.SolidLine)
        self.plot(x, y, (250,0,0), QtCore.Qt.DashLine)

    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 30)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = parabolaGraph2Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# # EXAMPLE ELLIPSE 1 GRAPH
class ellipseGraph1Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(ellipseGraph1Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # CENTER
        x = [-1]
        y = [2]
        # FOCI
        foci_x1 = [-1]
        foci_y1 = [6]
        foci_x2 = [-1]
        foci_y2 = [-2]
        # VERTICES
        vertix_x1 = [-1, -1]
        vertix_y1 = [7, -3]
        # MINOR AXIS Endpoints
        minAxis_x1 = [2, -4]
        minAxis_y1 = [2, 2]
        # Trace the whole ellipse
        x1 = [-1, -1.50, -2.50, -3.50, -4,
              -4, -4, -3.50, -2.50, -1.50,
              -1, -0.50, 0.50, 1.50, 2,
               2, 2, 1.50, 0.50, -0.50,      
               -1]
        y1 = [-3, -3, -2.50, -1, 1,
              2, 3, 5, 6.50, 7,
              7, 7, 6.50, 5, 3,
              2, 1, -1, -2.50, -3,
              -3]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')
        
        self.plot(vertix_x1, vertix_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(minAxis_x1, minAxis_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(x, y, (250,0,0), QtCore.Qt.DashLine)
        self.plotOuter(x1, y1, (0,0,0), QtCore.Qt.SolidLine)
        self.plot(foci_x1, foci_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(foci_x2, foci_y2, (250,0,0), QtCore.Qt.DashLine)
        
    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 8)
    def plotOuter(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 1)
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = ellipseGraph1Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# # EXAMPLE ELLIPSE 2 GRAPH
class ellipseGraph2Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(ellipseGraph2Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # CENTER
        x = [5]
        y = [3]
        # FOCI
        foci_x1 = [7.24]
        foci_y1 = [3]
        foci_x2 = [2.76]
        foci_y2 = [3]
        # VERTICES
        vertix_x1 = [8, 2]
        vertix_y1 = [3, 3]
        # MINOR AXIS Endpoints
        minAxis_x1 = [5,5]
        minAxis_y1 = [5,1]

        # Trace the whole ellipse
        x1 = [5, 4.50, 3.50, 2.50, 2, 
              2, 2, 2.50, 3.50, 4.50,
              5, 5.50, 6.50, 7.50, 8,
              8, 8, 7.50, 6.50, 5.50,
              5, ]
        y1 = [1, 1, 1.25, 1.75, 2.50, 
              3, 3.50, 4.25, 4.75, 5,
              5, 5, 4.75, 4.25, 3.50,
              3, 2.50, 1.75, 1.25, 1,
              1]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')

        self.plot(x, y, (250,0,0), QtCore.Qt.DashLine)
        self.plotOuter(x1, y1, (0,0,0), QtCore.Qt.SolidLine)
        self.plot(foci_x1, foci_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(foci_x2, foci_y2, (250,0,0), QtCore.Qt.DashLine)
        self.plot(vertix_x1, vertix_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(minAxis_x1, minAxis_y1, (250,0,0), QtCore.Qt.DashLine)
    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 10)
    def plotOuter(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 1)
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = ellipseGraph2Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# EXAMPLE HYPERBOLA 1A GRAPH
class hyperbolaGraph1Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(hyperbolaGraph1Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        foci_x2 = [7]
        foci_y2 = [-3]
        # VERTICES
        vertix_x1 = [-1, 5]
        vertix_y1 = [-3, -3]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')

        self.plot(foci_x2, foci_y2, (250,0,0), QtCore.Qt.DashLine)
        self.plot(vertix_x1, vertix_y1, (250,0,0), QtCore.Qt.DashLine)
    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 10)
    def plotOuter(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 1)
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = hyperbolaGraph1Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# EXAMPLE HYPERBOLA 2 GRAPH
class hyperbolaGraph2Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(hyperbolaGraph2Window, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # CENTER
        x = [2]
        y = [-3]
        # FOCI
        foci_x1 = [-3]
        foci_y1 = [-3]
        foci_x2 = [7]
        foci_y2 = [-3]
        # VERTICES
        vertix_x1 = [-1, 5]
        vertix_y1 = [-3, -3]

        # Trace the whole ellipse
        # Left side
        x1 = [-6,    -4,   -2,  -1,  -2 ,  -4,   -6]
        y1 = [-3.6, -3.5, -3.3, -3, -2.7, -2.5, -2.4]
        # Right side
        x2 = [ 10,    8,    6,   5,   6,    8,   10 ]
        y2 = [-3.6, -3.5, -3.3, -3, -2.7, -2.5, -2.4]

        # Add grid lines
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setBackground('w')

        self.plot(x, y, (250,0,0), QtCore.Qt.DashLine)
        self.plotOuter(x1, y1, (0,0,0), QtCore.Qt.SolidLine)
        self.plotOuter(x2, y2, (0,0,0), QtCore.Qt.SolidLine)
        self.plot(foci_x1, foci_y1, (250,0,0), QtCore.Qt.DashLine)
        self.plot(foci_x2, foci_y2, (250,0,0), QtCore.Qt.DashLine)
        self.plot(vertix_x1, vertix_y1, (250,0,0), QtCore.Qt.DashLine)
    def plot(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 10)
    def plotOuter(self, x, y, colorLine, styleLine):
        pen = pg.mkPen(color=colorLine, width = 3, symbolSize= 10,style= styleLine)
        self.graphWidget.plot(x, y, pen=pen, symbolSize= 1)
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = hyperbolaGraph2Window()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()