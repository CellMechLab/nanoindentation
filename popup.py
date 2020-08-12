from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import numpy as np

class uiPanel(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setFixedSize(1000,1000)

        layout = QtWidgets.QGridLayout()
        layout.setSpacing(15)
        widget = pg.PlotWidget()
        self.p1 = widget.plotItem
        self.p2 = pg.ViewBox()
        self.p1.setLabels(left='FD curve')
        self.p1.showAxis('right')
        self.p1.scene().addItem(self.p2)
        self.p1.getAxis('right').linkToView(self.p2)
        self.p2.setXLink(self.p1)
        self.p1.getAxis('right').setLabel('Weight', color='#0000ff')
        self.p1.showGrid(True,True)
        self.x1=None
        self.y1=None

        self.updateViews()
        self.p1.vb.sigResized.connect(self.updateViews)
        layout.addWidget(widget, 1,0,10,2)

        self.manual_slider = QSlider(Qt.Horizontal)
        self.manual_slider.setMinimum(-15000)
        self.manual_slider.setMaximum(15000)
        self.manual_slider.setValue(0)
        self.manual_slider.setTickPosition(QSlider.TicksAbove)
        self.manual_slider.setTickInterval(100)
        layout.addWidget(self.manual_slider, 11, 0, 1, 2)
        self.CPnew=None
        self.CP_man=None
        self.yCP=None
        self.manual_slider.sliderReleased.connect(self.setCP_manual)
        self.ManCP = False

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.forward_accept =QtWidgets.QPushButton("Set CP + >>")
        self.backward_accept = QtWidgets.QPushButton("<< + Set CP")
        self.forward_reject =QtWidgets.QPushButton("Keep old CP + >>")
        self.backward_reject = QtWidgets.QPushButton("<< + Keep old CP")
        self.forward_exclude = QtWidgets.QPushButton("Exclude Curve + >>")
        self.backward_exclude = QtWidgets.QPushButton("<< + Exclude Curve")
        self.button_box.accepted.connect(self.accept)
        self.button_box.accepted.connect(self.ManCPSet)
        self.button_box.rejected.connect(self.reject)
        self.forward_accept.clicked.connect(self.ManCPSet)
        self.backward_accept.clicked.connect(self.ManCPSet)
        self.forward_accept.clicked.connect(self.accept)
        self.backward_accept.clicked.connect(self.accept)
        self.forward_reject.clicked.connect(self.reject)
        self.backward_reject.clicked.connect(self.reject)
        self.forward_exclude.clicked.connect(self.exclude)
        self.backward_exclude.clicked.connect(self.exclude)
        self.forward_exclude.clicked.connect(self.reject)
        self.backward_exclude.clicked.connect(self.reject)
        self.excluded=None
        self.next=None
        self.forward_accept.clicked.connect(self.select_next)
        self.backward_accept.clicked.connect(self.select_before)
        self.forward_exclude.clicked.connect(self.select_next)
        self.backward_exclude.clicked.connect(self.select_before)
        self.forward_reject.clicked.connect(self.select_next)
        self.backward_reject.clicked.connect(self.select_before)
        layout.addWidget(self.button_box, 15, 0, 1, 2)
        layout.addWidget(self.forward_accept, 12, 1)
        layout.addWidget(self.forward_reject, 13, 1)
        layout.addWidget(self.backward_accept, 12, 0)
        layout.addWidget(self.backward_reject, 13, 0)
        layout.addWidget(self.forward_exclude, 14, 1)
        layout.addWidget(self.backward_exclude, 14, 0)
        self.setLayout(layout)
        self.setWindowTitle("Contact Point Inspection")

    def exclude(self):
        self.excluded=True

    def select_next(self):
        self.next=1

    def select_before(self):
        self.next=-1

    def ManCPSet(self):
        if self.CP_man is not None:
            self.ManCP=True

        ## Handle view resizing
    def updateViews(self):
        self.p2.setGeometry(self.p1.vb.sceneBoundingRect())
        self.p2.linkedViewChanged(self.p1.vb, self.p2.XAxis)

    def setPlots(self,x1,y1,x2=None,y2=None,x0=None,y0=None):
        self.x1=x1
        self.y1=y1
        self.plot1=self.p1.plot(x1,y1,pen='b')
        if x0 is not None:
            self.p1.plot([x0],[y0],pen='b',symbol='o')
        if x2 is not None:
            self.p2.addItem(pg.PlotCurveItem(x2, y2, pen='r'))


    def setCP_manual(self):
        if self.CPnew is None:
            self.CPnew = self.p1.plot([0], [0], pen='r', symbol='o')
        self.CPnew.clear()
        self.CP_man = self.manual_slider.value()
        if self.CP_man < self.x1[0]:
            self.CP_man = self.x1[0]
        if self.CP_man > self.x1[-1]:
            self.CP_man = self.x1[-1]
        iCP = np.argmin(abs(self.x1 - self.CP_man))
        self.yCP = self.y1[iCP]
        self.CPnew = self.p1.plot([self.CP_man], [self.yCP], pen='r', symbol='o')
