# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nano_view.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1680, 1115)
        icon = QIcon()
        icon.addFile(u"../../../../.designer/backup/ico.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.Curve = QGroupBox(self.centralwidget)
        self.Curve.setObjectName(u"Curve")
        self.Curve.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Curve.sizePolicy().hasHeightForWidth())
        self.Curve.setSizePolicy(sizePolicy)
        self.horizontalLayout_6 = QHBoxLayout(self.Curve)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.Curve)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.label)

        self.curve_segment = QSpinBox(self.Curve)
        self.curve_segment.setObjectName(u"curve_segment")
        self.curve_segment.setMaximum(9)
        self.curve_segment.setValue(1)

        self.horizontalLayout_6.addWidget(self.curve_segment)

        self.crop = QPushButton(self.Curve)
        self.crop.setObjectName(u"crop")

        self.horizontalLayout_6.addWidget(self.crop)

        self.crop_left = QCheckBox(self.Curve)
        self.crop_left.setObjectName(u"crop_left")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.crop_left.sizePolicy().hasHeightForWidth())
        self.crop_left.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.crop_left)

        self.crop_right = QCheckBox(self.Curve)
        self.crop_right.setObjectName(u"crop_right")
        self.crop_right.setChecked(True)

        self.horizontalLayout_6.addWidget(self.crop_right)


        self.horizontalLayout_8.addWidget(self.Curve)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.view_all = QRadioButton(self.groupBox)
        self.view_all.setObjectName(u"view_all")
        self.view_all.setStyleSheet(u"color: red;")
        self.view_all.setChecked(True)

        self.horizontalLayout_4.addWidget(self.view_all)

        self.view_included = QRadioButton(self.groupBox)
        self.view_included.setObjectName(u"view_included")
        self.view_included.setStyleSheet(u"color: blue;")

        self.horizontalLayout_4.addWidget(self.view_included)

        self.view_active = QRadioButton(self.groupBox)
        self.view_active.setObjectName(u"view_active")

        self.horizontalLayout_4.addWidget(self.view_active)


        self.horizontalLayout_8.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMinimumSize)
        self.toggle_excluded = QRadioButton(self.groupBox_2)
        self.toggle_excluded.setObjectName(u"toggle_excluded")
        self.toggle_excluded.setStyleSheet(u"color: red;")
        self.toggle_excluded.setChecked(True)

        self.horizontalLayout_5.addWidget(self.toggle_excluded)

        self.toggle_included = QRadioButton(self.groupBox_2)
        self.toggle_included.setObjectName(u"toggle_included")
        self.toggle_included.setStyleSheet(u"color: blue;")

        self.horizontalLayout_5.addWidget(self.toggle_included)

        self.toggle_activated = QRadioButton(self.groupBox_2)
        self.toggle_activated.setObjectName(u"toggle_activated")

        self.horizontalLayout_5.addWidget(self.toggle_activated)


        self.horizontalLayout_8.addWidget(self.groupBox_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.save_dataHertz = QPushButton(self.groupBox_5)
        self.save_dataHertz.setObjectName(u"save_dataHertz")

        self.horizontalLayout_2.addWidget(self.save_dataHertz)

        self.save_avg_hertz = QPushButton(self.groupBox_5)
        self.save_avg_hertz.setObjectName(u"save_avg_hertz")

        self.horizontalLayout_2.addWidget(self.save_avg_hertz)

        self.save_dataES = QPushButton(self.groupBox_5)
        self.save_dataES.setObjectName(u"save_dataES")

        self.horizontalLayout_2.addWidget(self.save_dataES)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_8.addWidget(self.groupBox_5)


        self.verticalLayout_8.addLayout(self.horizontalLayout_8)

        self.splitter_4 = QSplitter(self.centralwidget)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.mainlist = QTreeWidget(self.splitter_4)
        self.mainlist.setObjectName(u"mainlist")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.mainlist.sizePolicy().hasHeightForWidth())
        self.mainlist.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        self.mainlist.setFont(font)
        self.mainlist.setFrameShape(QFrame.StyledPanel)
        self.mainlist.setFrameShadow(QFrame.Sunken)
        self.mainlist.setLineWidth(0)
        self.mainlist.setMidLineWidth(0)
        self.mainlist.setSortingEnabled(False)
        self.mainlist.setAnimated(False)
        self.splitter_4.addWidget(self.mainlist)
        self.splitter_3 = QSplitter(self.splitter_4)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter_3)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_7 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.g_fdistance = PlotWidget(self.layoutWidget)
        self.g_fdistance.setObjectName(u"g_fdistance")

        self.verticalLayout_7.addWidget(self.g_fdistance)

        self.g_single = PlotWidget(self.layoutWidget)
        self.g_single.setObjectName(u"g_single")

        self.verticalLayout_7.addWidget(self.g_single)

        self.splitter_3.addWidget(self.layoutWidget)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        sizePolicy2.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy2)
        self.splitter.setOrientation(Qt.Horizontal)
        self.analysis_group_box = QGroupBox(self.splitter)
        self.analysis_group_box.setObjectName(u"analysis_group_box")
        self.verticalLayout_5 = QVBoxLayout(self.analysis_group_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.analysis = QCheckBox(self.analysis_group_box)
        self.analysis.setObjectName(u"analysis")
        self.analysis.setEnabled(True)
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(11)
        font1.setBold(True)
        self.analysis.setFont(font1)
        self.analysis.setLayoutDirection(Qt.LeftToRight)
        self.analysis.setIconSize(QSize(15, 15))

        self.verticalLayout_5.addWidget(self.analysis)

        self.g_indentation = PlotWidget(self.analysis_group_box)
        self.g_indentation.setObjectName(u"g_indentation")
        self.g_indentation.setEnabled(True)
        font2 = QFont()
        font2.setBold(True)
        self.g_indentation.setFont(font2)
        self.g_indentation.setAcceptDrops(True)
        self.g_indentation.setInteractive(True)

        self.verticalLayout_5.addWidget(self.g_indentation)

        self.avg_hertz = PlotWidget(self.analysis_group_box)
        self.avg_hertz.setObjectName(u"avg_hertz")
        self.avg_hertz.setEnabled(True)
        self.avg_hertz.setInteractive(True)

        self.verticalLayout_5.addWidget(self.avg_hertz)

        self.g_scatter = PlotWidget(self.analysis_group_box)
        self.g_scatter.setObjectName(u"g_scatter")
        self.g_scatter.setEnabled(True)

        self.verticalLayout_5.addWidget(self.g_scatter)

        self.splitter.addWidget(self.analysis_group_box)
        self.es_group_box = QGroupBox(self.splitter)
        self.es_group_box.setObjectName(u"es_group_box")
        font3 = QFont()
        font3.setBold(False)
        self.es_group_box.setFont(font3)
        self.verticalLayout_10 = QVBoxLayout(self.es_group_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.es_analysis = QCheckBox(self.es_group_box)
        self.es_analysis.setObjectName(u"es_analysis")
        self.es_analysis.setEnabled(True)
        self.es_analysis.setFont(font1)
        self.es_analysis.setLayoutDirection(Qt.LeftToRight)
        self.es_analysis.setIconSize(QSize(15, 15))

        self.verticalLayout_10.addWidget(self.es_analysis)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.g_es = PlotWidget(self.es_group_box)
        self.g_es.setObjectName(u"g_es")

        self.verticalLayout_6.addWidget(self.g_es)

        self.g_decay = PlotWidget(self.es_group_box)
        self.g_decay.setObjectName(u"g_decay")
        self.g_decay.setEnabled(True)
        self.g_decay.setInteractive(True)

        self.verticalLayout_6.addWidget(self.g_decay)


        self.verticalLayout_10.addLayout(self.verticalLayout_6)

        self.splitter.addWidget(self.es_group_box)
        self.splitter_2.addWidget(self.splitter)
        self.groupBox_7 = QGroupBox(self.splitter_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName(u"label_14")
        font4 = QFont()
        font4.setFamily(u"Arial")
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setItalic(False)
        font4.setUnderline(False)
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_11.addWidget(self.label_14)

        self.g_histo = PlotWidget(self.groupBox_7)
        self.g_histo.setObjectName(u"g_histo")
        self.g_histo.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.g_histo.sizePolicy().hasHeightForWidth())
        self.g_histo.setSizePolicy(sizePolicy4)
        self.g_histo.setLineWidth(0)
        self.g_histo.setMidLineWidth(0)
        self.g_histo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.g_histo)

        self.splitter_2.addWidget(self.groupBox_7)
        self.splitter_3.addWidget(self.splitter_2)
        self.splitter_4.addWidget(self.splitter_3)

        self.verticalLayout_8.addWidget(self.splitter_4)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_12 = QGroupBox(self.centralwidget)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.open_o11new = QRadioButton(self.groupBox_12)
        self.open_o11new.setObjectName(u"open_o11new")
        self.open_o11new.setEnabled(False)
        self.open_o11new.setChecked(True)

        self.verticalLayout_3.addWidget(self.open_o11new)

        self.open_o11old = QRadioButton(self.groupBox_12)
        self.open_o11old.setObjectName(u"open_o11old")
        self.open_o11old.setEnabled(False)

        self.verticalLayout_3.addWidget(self.open_o11old)

        self.open_nanosurf = QRadioButton(self.groupBox_12)
        self.open_nanosurf.setObjectName(u"open_nanosurf")
        self.open_nanosurf.setEnabled(False)
        self.open_nanosurf.setChecked(False)

        self.verticalLayout_3.addWidget(self.open_nanosurf)

        self.open_easy_tsv = QRadioButton(self.groupBox_12)
        self.open_easy_tsv.setObjectName(u"open_easy_tsv")
        self.open_easy_tsv.setEnabled(False)

        self.verticalLayout_3.addWidget(self.open_easy_tsv)

        self.open_selectfolder = QPushButton(self.groupBox_12)
        self.open_selectfolder.setObjectName(u"open_selectfolder")
        self.open_selectfolder.setFont(font2)

        self.verticalLayout_3.addWidget(self.open_selectfolder)


        self.gridLayout_3.addWidget(self.groupBox_12, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.reset_exclude = QRadioButton(self.groupBox_4)
        self.reset_exclude.setObjectName(u"reset_exclude")
        self.reset_exclude.setChecked(True)

        self.verticalLayout_2.addWidget(self.reset_exclude)

        self.reset_activate = QRadioButton(self.groupBox_4)
        self.reset_activate.setObjectName(u"reset_activate")

        self.verticalLayout_2.addWidget(self.reset_activate)

        self.reset_all = QPushButton(self.groupBox_4)
        self.reset_all.setObjectName(u"reset_all")

        self.verticalLayout_2.addWidget(self.reset_all)


        self.gridLayout_3.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout = QGridLayout(self.groupBox_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.prominency = QGroupBox(self.groupBox_8)
        self.prominency.setObjectName(u"prominency")
        sizePolicy.setHeightForWidth(self.prominency.sizePolicy().hasHeightForWidth())
        self.prominency.setSizePolicy(sizePolicy)
        self.prominency.setCheckable(True)
        self.prominency.setChecked(False)
        self.formLayout = QFormLayout(self.prominency)
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(self.prominency)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.prominency_prominency = QSpinBox(self.prominency)
        self.prominency_prominency.setObjectName(u"prominency_prominency")
        self.prominency_prominency.setMinimum(1)
        self.prominency_prominency.setMaximum(999)
        self.prominency_prominency.setSingleStep(10)
        self.prominency_prominency.setValue(40)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.prominency_prominency)

        self.label_4 = QLabel(self.prominency)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.prominency_minfreq = QSpinBox(self.prominency)
        self.prominency_minfreq.setObjectName(u"prominency_minfreq")
        self.prominency_minfreq.setMinimum(3)
        self.prominency_minfreq.setMaximum(999)
        self.prominency_minfreq.setSingleStep(5)
        self.prominency_minfreq.setValue(25)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.prominency_minfreq)

        self.label_5 = QLabel(self.prominency)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.prominency_band = QSpinBox(self.prominency)
        self.prominency_band.setObjectName(u"prominency_band")
        self.prominency_band.setMinimum(1)
        self.prominency_band.setMaximum(999)
        self.prominency_band.setSingleStep(5)
        self.prominency_band.setValue(30)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.prominency_band)


        self.gridLayout.addWidget(self.prominency, 0, 0, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_26 = QLabel(self.groupBox_8)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setEnabled(True)
        font5 = QFont()
        font5.setFamily(u"Arial")
        font5.setPointSize(12)
        font5.setKerning(True)
        self.label_26.setFont(font5)
        self.label_26.setFrameShape(QFrame.NoFrame)
        self.label_26.setFrameShadow(QFrame.Plain)
        self.label_26.setLineWidth(1)
        self.label_26.setScaledContents(False)
        self.label_26.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.label_26)

        self.comboFsmooth = QComboBox(self.groupBox_8)
        self.comboFsmooth.setObjectName(u"comboFsmooth")
        self.comboFsmooth.setLayoutDirection(Qt.LeftToRight)
        self.comboFsmooth.setAutoFillBackground(False)
        self.comboFsmooth.setFrame(True)

        self.verticalLayout_4.addWidget(self.comboFsmooth)

        self.FSmooth_box = QGroupBox(self.groupBox_8)
        self.FSmooth_box.setObjectName(u"FSmooth_box")
        sizePolicy.setHeightForWidth(self.FSmooth_box.sizePolicy().hasHeightForWidth())
        self.FSmooth_box.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.FSmooth_box)


        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_8, 0, 2, 1, 1)

        self.groupBox_9 = QGroupBox(self.centralwidget)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout = QVBoxLayout(self.groupBox_9)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.quickView = QPushButton(self.groupBox_9)
        self.quickView.setObjectName(u"quickView")

        self.verticalLayout.addWidget(self.quickView)

        self.comboCP = QComboBox(self.groupBox_9)
        self.comboCP.setObjectName(u"comboCP")

        self.verticalLayout.addWidget(self.comboCP)

        self.CP_box = QGroupBox(self.groupBox_9)
        self.CP_box.setObjectName(u"CP_box")
        sizePolicy.setHeightForWidth(self.CP_box.sizePolicy().hasHeightForWidth())
        self.CP_box.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.CP_box)


        self.gridLayout_3.addWidget(self.groupBox_9, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(68, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setEnabled(True)
        self.formLayout_2 = QFormLayout(self.groupBox_6)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_8 = QLabel(self.groupBox_6)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.es_win = QSpinBox(self.groupBox_6)
        self.es_win.setObjectName(u"es_win")
        self.es_win.setMinimum(3)
        self.es_win.setMaximum(9999)
        self.es_win.setValue(21)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.es_win)

        self.label_21 = QLabel(self.groupBox_6)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_21)

        self.es_order = QSpinBox(self.groupBox_6)
        self.es_order.setObjectName(u"es_order")
        self.es_order.setMinimum(1)
        self.es_order.setMaximum(9)
        self.es_order.setValue(3)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.es_order)

        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_13)

        self.es_interpolate = QCheckBox(self.groupBox_6)
        self.es_interpolate.setObjectName(u"es_interpolate")
        self.es_interpolate.setChecked(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.es_interpolate)


        self.gridLayout_2.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.formLayout_3 = QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_9)

        self.stats_R = QLabel(self.groupBox_3)
        self.stats_R.setObjectName(u"stats_R")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.stats_R)

        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_17)

        self.stats_k = QLabel(self.groupBox_3)
        self.stats_k.setObjectName(u"stats_k")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.stats_k)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.stats_ne = QLabel(self.groupBox_3)
        self.stats_ne.setObjectName(u"stats_ne")
        self.stats_ne.setStyleSheet(u"color: red;")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.stats_ne)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_10)

        self.stats_ni = QLabel(self.groupBox_3)
        self.stats_ni.setObjectName(u"stats_ni")
        self.stats_ni.setStyleSheet(u"color: blue;")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.stats_ni)

        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.stats_na = QLabel(self.groupBox_3)
        self.stats_na.setObjectName(u"stats_na")
        self.stats_na.setStyleSheet(u"")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.stats_na)


        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.GroupFIT = QGroupBox(self.centralwidget)
        self.GroupFIT.setObjectName(u"GroupFIT")
        sizePolicy.setHeightForWidth(self.GroupFIT.sizePolicy().hasHeightForWidth())
        self.GroupFIT.setSizePolicy(sizePolicy)
        self.GroupFIT.setCheckable(False)
        self.verticalLayout_9 = QVBoxLayout(self.GroupFIT)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_16 = QLabel(self.GroupFIT)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_13.addWidget(self.label_16)

        self.fit_indentation = QSpinBox(self.GroupFIT)
        self.fit_indentation.setObjectName(u"fit_indentation")
        self.fit_indentation.setMinimum(10)
        self.fit_indentation.setMaximum(19999)
        self.fit_indentation.setValue(800)

        self.horizontalLayout_13.addWidget(self.fit_indentation)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_13)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_7 = QLabel(self.GroupFIT)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.label_19 = QLabel(self.GroupFIT)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout.addWidget(self.label_19)

        self.fit_center = QLabel(self.GroupFIT)
        self.fit_center.setObjectName(u"fit_center")
        self.fit_center.setStyleSheet(u"font-weight:bold;")
        self.fit_center.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.fit_center)

        self.label_23 = QLabel(self.GroupFIT)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_23)

        self.fit_std = QLabel(self.GroupFIT)
        self.fit_std.setObjectName(u"fit_std")
        self.fit_std.setStyleSheet(u"font-weight:bold;")
        self.fit_std.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.fit_std)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.GroupFIT)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_7.addWidget(self.label_6)

        self.label_18 = QLabel(self.GroupFIT)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_7.addWidget(self.label_18)

        self.data_average = QLabel(self.GroupFIT)
        self.data_average.setObjectName(u"data_average")
        self.data_average.setStyleSheet(u"font-weight:bold;")
        self.data_average.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.data_average)

        self.label_20 = QLabel(self.GroupFIT)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_20)

        self.data_std = QLabel(self.GroupFIT)
        self.data_std.setObjectName(u"data_std")
        self.data_std.setStyleSheet(u"font-weight:bold;")
        self.data_std.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.data_std)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_12 = QLabel(self.GroupFIT)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_14.addWidget(self.label_12)

        self.label_22 = QLabel(self.GroupFIT)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_14.addWidget(self.label_22)

        self.decay_e0 = QLabel(self.GroupFIT)
        self.decay_e0.setObjectName(u"decay_e0")
        self.decay_e0.setStyleSheet(u"font-weight:bold;")
        self.decay_e0.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.decay_e0)

        self.label_24 = QLabel(self.GroupFIT)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.label_24)

        self.decay_eb = QLabel(self.GroupFIT)
        self.decay_eb.setObjectName(u"decay_eb")
        self.decay_eb.setStyleSheet(u"font-weight:bold;")
        self.decay_eb.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.decay_eb)

        self.label_25 = QLabel(self.GroupFIT)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.label_25)

        self.decay_d0 = QLabel(self.GroupFIT)
        self.decay_d0.setObjectName(u"decay_d0")
        self.decay_d0.setStyleSheet(u"font-weight:bold;")
        self.decay_d0.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.decay_d0)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)


        self.gridLayout_2.addWidget(self.GroupFIT, 0, 2, 1, 1)

        self.slid_alpha = QSlider(self.centralwidget)
        self.slid_alpha.setObjectName(u"slid_alpha")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.slid_alpha.sizePolicy().hasHeightForWidth())
        self.slid_alpha.setSizePolicy(sizePolicy5)
        self.slid_alpha.setMaximum(255)
        self.slid_alpha.setSingleStep(1)
        self.slid_alpha.setValue(100)
        self.slid_alpha.setOrientation(Qt.Vertical)

        self.gridLayout_2.addWidget(self.slid_alpha, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 2, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Nano2021", None))
        self.Curve.setTitle(QCoreApplication.translate("MainWindow", u"Curve", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Segment", None))
        self.crop.setText(QCoreApplication.translate("MainWindow", u"crop 50nm", None))
        self.crop_left.setText(QCoreApplication.translate("MainWindow", u"L", None))
        self.crop_right.setText(QCoreApplication.translate("MainWindow", u"R", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.view_all.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.view_included.setText(QCoreApplication.translate("MainWindow", u"Included", None))
        self.view_active.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Toggle", None))
        self.toggle_excluded.setText(QCoreApplication.translate("MainWindow", u"Excluded", None))
        self.toggle_included.setText(QCoreApplication.translate("MainWindow", u"Included", None))
        self.toggle_activated.setText(QCoreApplication.translate("MainWindow", u"Activated", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Save", None))
        self.save_dataHertz.setText(QCoreApplication.translate("MainWindow", u"Hertz", None))
        self.save_avg_hertz.setText(QCoreApplication.translate("MainWindow", u"Avg F-Ind", None))
        self.save_dataES.setText(QCoreApplication.translate("MainWindow", u"ES", None))
        ___qtreewidgetitem = self.mainlist.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Files", None));
        self.analysis_group_box.setTitle("")
        self.analysis.setText(QCoreApplication.translate("MainWindow", u"Hertz Analysis", None))
        self.es_group_box.setTitle("")
        self.es_analysis.setText(QCoreApplication.translate("MainWindow", u"Elasticity Spectra Analysis ", None))
        self.groupBox_7.setTitle("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Combined Elasticity Statistics", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Open", None))
        self.open_o11new.setText(QCoreApplication.translate("MainWindow", u"Optics11 New", None))
        self.open_o11old.setText(QCoreApplication.translate("MainWindow", u"Optics11 Old", None))
        self.open_nanosurf.setText(QCoreApplication.translate("MainWindow", u"Nanosurf export", None))
        self.open_easy_tsv.setText(QCoreApplication.translate("MainWindow", u"Easy tsv", None))
        self.open_selectfolder.setText(QCoreApplication.translate("MainWindow", u"Load Experiment", None))
#if QT_CONFIG(shortcut)
        self.open_selectfolder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.reset_exclude.setText(QCoreApplication.translate("MainWindow", u"Exclude", None))
        self.reset_activate.setText(QCoreApplication.translate("MainWindow", u"Activate", None))
        self.reset_all.setText(QCoreApplication.translate("MainWindow", u"ALL", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Filtering ", None))
        self.prominency.setTitle(QCoreApplication.translate("MainWindow", u"Prominency ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Prominency", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Min Freq", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Band", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Others", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Contact Point ", None))
        self.quickView.setText(QCoreApplication.translate("MainWindow", u"Inspect", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Elasticity Spectra", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Window", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Order", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Interpolate", None))
        self.es_interpolate.setText("")
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Stats", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"R [nm]", None))
        self.stats_R.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"k [N/m]", None))
        self.stats_k.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>N<span style=\" vertical-align:sub;\">excluded</span></p></body></html>", None))
        self.stats_ne.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>N<span style=\" vertical-align:sub;\">included</span></p></body></html>", None))
        self.stats_ni.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>N<span style=\" vertical-align:sub;\">activated</span></p></body></html>", None))
        self.stats_na.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.GroupFIT.setTitle(QCoreApplication.translate("MainWindow", u"Results ", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Max Indentation [nm]", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">FIT</span></p></body></html>", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">Y</span> [kPa]: </p></body></html>", None))
        self.fit_center.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">ES</span> [kPa]: </p></body></html>", None))
        self.fit_std.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Stats</span></p></body></html>", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">y</span> [kPa]:</p></body></html>", None))
        self.data_average.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">ES</span> [kPa]:</p></body></html>", None))
        self.data_std.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Decay</span></p></body></html>", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">0</span> [kPa]:</p></body></html>", None))
        self.decay_e0.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>E<span style=\" vertical-align:sub;\">b</span> [Pa]:</p></body></html>", None))
        self.decay_eb.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>d<span style=\" vertical-align:sub;\">0</span> [nm]:</p></body></html>", None))
        self.decay_d0.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
    # retranslateUi

