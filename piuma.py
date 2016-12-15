from PyQt4 import QtCore, QtGui

import sys,os
import pyqtgraph as pg
import piuma_view as view
import piuma_engine as engine

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
SILENT = False

def manageLog():
    print("Unexpected error")
    for r in sys.exc_info():
        print('-- {0}'.format(r))
    QtGui.QApplication.restoreOverrideCursor()


htmlpre = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:"Ubuntu"; font-size:11pt; font-weight:400; font-style:normal;">\n<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8pt;">'
htmlpost = '</span></p></body></html>'


class curveWindow ( QtGui.QMainWindow ):
    def __init__ ( self, parent = None ):
        QtGui.QMainWindow.__init__( self, parent )
        self.setWindowTitle( 'Piuma Matrix Viewer' )
        self.ui = view.Ui_facewindow()
        self.ccurve=[-1,-1]
        self.singlecurve = False
        self.ui.setupUi( self )
        self.setConnections()

    def onlyOne(self):
        self.singlecurve = True
        self.ui.bLoadScan.setEnabled(False)
        self.ui.bSetLevel.setEnabled(False)
        self.ui.bEMap.setEnabled(False)
        self.guessScan()

    def guessScan(self):
        msg = 'Select one file belonging to the scan'
        if self.singlecurve is True:
            msg = 'Select the file you want to open'
        filename = QtGui.QFileDialog.getOpenFileName(self, msg, './')
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            self.scan = engine.pscan(filename)
            self.ui.labCalib.setText(str(self.scan.calib))
            self.ui.labDate.setText(self.scan.date)
            self.ui.labFilename.setText(self.scan.dir)
            self.ui.labK.setText(str(self.scan.k))
            self.ui.labName.setText(str(self.scan.basename))
            self.ui.labRadius.setText(str(self.scan.tipradius))
            self.ui.wSegment.setMaximum(len(self.scan.protocol)-1)
            self.ui.wSegment.setValue(1)
            pvalue = 0
            ptime = 0
            col = ['r','b']
            for i in range(7):
                if i<len(self.scan.protocol):
                    ps = self.scan.protocol[i]
                    self.ui.tabProtocol.item(i,0).setText(str(ps.aim))
                    self.ui.tabProtocol.item(i,1).setText(str(ps.duration))
                    self.ui.grafo.plot([ptime,ptime+ps.duration],[pvalue,ps.aim],pen = col[i%2],symbol='o')
                    ptime = ptime+ps.duration
                    pvalue = ps.aim
                else:
                    for j in range(2):
                        self.ui.tabProtocol.item(i,j).setText('--')
            if self.singlecurve is True:
                self.scan.add(filename,load=True)
                self.scan.curves[0].createSegments(self.scan.protocol)
                self.ccurve = [0,0]
                self.ui.labScan.setText('n.a.')
                self.ui.labXi.setText('n.a.')
                self.ui.labYi.setText('n.a.')
                self.ui.labDx.setText('n.a.')
                self.ui.labDy.setText('n.a.')
            else:
                self.scan.guessDir()
                self.ui.labScan.setText(str(self.scan.snumber))
                self.ui.labXi.setText(str(self.scan.xi))
                self.ui.labYi.setText(str(self.scan.yi))
                self.ui.labDx.setText('{0}'.format(round(self.scan.dx*100)/100.0))
                self.ui.labDy.setText('{0}'.format(round(self.scan.dy*100)/100.0))

        except:
            if SILENT is True:
                manageLog()
            else:
                raise
        QtGui.QApplication.restoreOverrideCursor()

    def guessName(self,x,y,i,full=False):
            nm = self.scan.basename + ' S-{0} X-{1} Y-{2} I-{3}.txt'.format(self.scan.snumber,x,y,i)
            if full:
                return os.path.join(self.scan.dir,nm)
            else:
                return nm

    def addDir(self,dirname=None):
        if dirname == None:
            dirname = QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory', './')
            if not os.path.isdir(dirname):
                return
        QtCore.QCoreApplication.processEvents()
        pmax = len(os.listdir(dirname))

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            progress = QtGui.QProgressDialog("Opening files...", "Cancel opening", 0, pmax);
            i=0
            for fnamealone in os.listdir(dirname):
                #if i % 100 == 0:
                QtCore.QCoreApplication.processEvents()
                fname = os.path.join(str(dirname), fnamealone)
                self.exp.addFiles([str(fname)])
                progress.setValue(i)
                i=i+1
                if (progress.wasCanceled()):
                    break
            progress.setValue(pmax)
        except:
            if SILENT is True:
                manageLog()
            else:
                QtGui.QApplication.restoreOverrideCursor()
                raise
        QtGui.QApplication.restoreOverrideCursor()
        self.fileList()

    def selectCurve(self):
        self.ccurve = [self.sender().numi,self.sender().numj]
        self.refreshCurve()

    def refreshCurve(self):
        if self.ccurve == [-1,-1]:
            return
        self.ui.graCurva.clear()
        if self.singlecurve is True:
            cv = self.scan.curves[0]
        else:
            cv = self.scan.matrix[self.ccurve[0]][self.ccurve[1]]
        i = 0
        ws = self.ui.wSegment.value()
        col = [0.3,0.7]
        order = self.ui.cbViewMode.currentIndex()
        winderiv = self.ui.winSlider.value()

        if self.ui.tabMode.tabText(self.ui.tabMode.currentIndex())=='Hertz':
            val = self.ui.contactThresh.value()
            if order == 2:
                self.ui.graCurva.plot([cv.segments[ws].z[0],cv.segments[ws].z[-1]],[val,val],pen='r')
            elif order == 0:
                (xc,yc) = cv.segments[ws].getPoint(val,dir='Y',order=2,win=winderiv)
                self.ui.graCurva.plot([xc,xc],[yc,yc],pen='r',symbol='o')
                fitlimit = self.ui.vFitLimit.value()
                if self.ui.radIndentation.isChecked():
                    (xm,ym) = cv.segments[ws].getPoint(xc+fitlimit,dir='X')
                else:
                    (xm,ym) = cv.segments[ws].getPoint(fitlimit,dir='Y')
                self.ui.graCurva.plot([xm,xm],[ym,ym],pen='g',symbol='o')

                try:
                    E = cv.segments[ws].getE(xc,xm)
                    jmin,jmax = cv.segments[ws].getJ(xc,xm)

                    #print(E)
                    self.ui.labEcurrent.setText('E: {0} Pa'.format(E))
                    xx = cv.segments[ws].z[jmin:jmax]
                    self.ui.graCurva.plot(xx,cv.segments[ws].hertz(abs(xx-xc),E)+cv.segments[ws].f[jmin],pen='g')
                except:
                    pass
        elif self.ui.tabMode.tabText(self.ui.tabMode.currentIndex())=='Test':
            if self.ui.togFlat.isChecked():
                x = cv.segments[ws].z
                y = cv.segments[ws].f
                import numpy as np
                x,y = np.sort(np.array([x,y]),axis=1)
                self.ui.graCurva.plot(x,y,pen='b')

        elif self.ui.tabMode.tabText(self.ui.tabMode.currentIndex())=='Force':
            if order==0:
                yc = self.ui.fLevel.value()
                self.ui.graCurva.plot([cv.segments[ws].z[0],cv.segments[ws].z[-1]],[yc,yc],pen='r',symbol='o')

        for s in cv.segments:
            if i == ws:
                c = 'r'
            else:
                c = col[i%2]
            i+=1

            if order == 0:
                self.ui.graCurva.plot(s.z,s.f,pen=c)
            else:
                self.ui.graCurva.plot(s.z,s.getDerivative(order,win=winderiv),pen=c)

    def loadAll(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        twas = self.ui.bLoad.text()
        self.ui.bLoad.setText('Loading ...')
        QtGui.QApplication.processEvents()
        self.pixels=[]
        col = ['red','green','yellow']
        fmaxall = -2000000000
        fminall = 200000000
        try:
            for i in range(self.scan.xi):
                riga = []
                for j in range(self.scan.yi):
                    if self.scan.matrix[i][j] is not None:
                        self.scan.matrix[i][j].load()
                        self.scan.matrix[i][j].createSegments(self.scan.protocol)
                        mam = max( [ max(s.f) for s in self.scan.matrix[i][j].segments ] )
                        mim = min( [ min(s.f) for s in self.scan.matrix[i][j].segments ] )
                        if mam >= fmaxall:
                            fmaxall = mam
                        if mim <= fminall:
                            fminall = mim
                        l = QtGui.QPushButton()
                        l.width = 10
                        l.height = 10
                        l.numi = i
                        l.numj = j
                        l.setFlat(True)
                        l.clicked.connect(self.selectCurve)
                        l.setStyleSheet('background-color:{0}; border: none;'.format(col[(i*10+j)%3]))
                        #l.setSizePolicy(QtGui.QSizePolicy( QtGui.QSizePolicy.Expanding ,QtGui.QSizePolicy.Expanding))
                        self.ui.cubo.addWidget(l,i,j)
                        riga.append(l)
                self.pixels.append(riga)
            self.ui.fLevel.setMaximum(fmaxall)
            self.ui.fLevel.setMinimum(fminall)
        except:
            if SILENT is True:
                manageLog()
            else:
                QtGui.QApplication.restoreOverrideCursor()
                self.ui.bLoad.setText(twas)
                raise
        self.ui.bLoad.setText(twas)
        QtGui.QApplication.restoreOverrideCursor()

    def colora(self):
        colors = []
        for i in range(self.scan.xi):
            for j in range(self.scan.yi):
                if self.scan.matrix[i][j] is not None:
                    if self.scan.matrix[i][j].color is not None:
                        colors.append(self.scan.matrix[i][j].color)
        fmin = min(colors)
        fmax = max(colors)
        for i in range(self.scan.xi):
            for j in range(self.scan.yi):
                if self.scan.matrix[i][j] is not None:
                    if self.scan.matrix[i][j].color is None:
                        self.pixels[i][j].setStyleSheet('background-color: red; border: none;')
                    else:
                        colore = int(255 * (self.scan.matrix[i][j].color-fmin)/(fmax-fmin))
                        self.pixels[i][j].setStyleSheet('background-color: rgb({0},{0},{0}); border: none;'.format(colore))

    def colorYoung(self):
        ws = self.ui.wSegment.value()
        winderiv = self.ui.winSlider.value()
        fitlimit = self.ui.vFitLimit.value()
        val = self.ui.contactThresh.value()
        for i in range(self.scan.xi):
            riga = []
            for j in range(self.scan.yi):
                if self.scan.matrix[i][j] is not None:
                    (xc,yc) = self.scan.matrix[i][j].segments[ws].getPoint(val,dir='Y',order=2,win=winderiv)
                    if self.ui.radIndentation.isChecked():
                        (xm,ym) = self.scan.matrix[i][j].segments[ws].getPoint(xc+fitlimit,dir='X')
                    else:
                        (xm,ym) = self.scan.matrix[i][j].segments[ws].getPoint(fitlimit,dir='Y')
                    try:
                        z = self.scan.matrix[i][j].segments[ws].getE(xc,xm)
                        self.scan.matrix[i][j].color = z
                    except:
                        z=0
                        self.scan.matrix[i][j].color = None
        self.colora()

    def colorForce(self):
        ws = self.ui.wSegment.value()
        flevel = float(self.ui.fLevel.value())
        for i in range(self.scan.xi):
            for j in range(self.scan.yi):
                if self.scan.matrix[i][j] is not None:
                    z = self.scan.matrix[i][j].segments[ws].getZ(flevel)
                    self.scan.matrix[i][j].color = z
        self.colora()

    def saveMap(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,'Save map file to disk',self.scan.dir,'*.xyz')
        if filename is not None:
            f = open(filename,'w')
            f.write('# Channel: Value (max)\n# Lateral units: m\n# Value units: m\n')
            for cv in self.scan.curves:
                if cv.color is not None:
                    f.write('{0}\t{1}\t{2}\n'.format(cv.xi,cv.yi,cv.color))
            f.close()


    def setConnections(self):
        self.ui.bLoadScan.clicked.connect(self.guessScan)
        self.ui.bSingleCurve.clicked.connect(self.onlyOne)
        self.ui.bLoad.clicked.connect(self.loadAll)
        self.ui.bSetLevel.clicked.connect(self.colorForce)
        self.ui.wSegment.valueChanged.connect(self.refreshCurve)
        self.ui.winSlider.valueChanged.connect(self.refreshCurve)
        self.ui.cbViewMode.currentIndexChanged.connect(self.refreshCurve)
        self.ui.contactThresh.valueChanged.connect(self.refreshCurve)
        self.ui.vFitLimit.valueChanged.connect(self.refreshCurve)
        self.ui.radIndentation.clicked.connect(self.refreshCurve)
        self.ui.radForce.clicked.connect(self.refreshCurve)
        self.ui.bEMap.clicked.connect(self.colorYoung)
        self.ui.fLevel.valueChanged.connect(self.refreshCurve)
        self.ui.tabWidget.currentChanged.connect(self.refreshCurve)
        self.ui.tabMode.currentChanged.connect(self.refreshCurve)
        self.ui.bSaveMap.clicked.connect(self.saveMap)
        #QtCore.QObject.connect(self.ui.bLoadScan, QtCore.SIGNAL("clicked()"), self.addFile)
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName( 'Piuma Matrix Viewer' )
    destefano = curveWindow()
    destefano.show()
    QtCore.QObject.connect( app, QtCore.SIGNAL( 'lastWindowClosed()' ), app, QtCore.SLOT( 'quit()' ) )
    sys.exit(app.exec_())
