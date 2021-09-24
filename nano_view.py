# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nano_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1435, 921)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../.designer/backup/ico.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox_12 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.open_selectfolder = QtWidgets.QPushButton(self.groupBox_12)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.open_selectfolder.setFont(font)
        self.open_selectfolder.setObjectName("open_selectfolder")
        self.verticalLayout_3.addWidget(self.open_selectfolder)
        self.horizontalLayout_8.addWidget(self.groupBox_12)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.toggle_excluded = QtWidgets.QRadioButton(self.groupBox_2)
        self.toggle_excluded.setStyleSheet("color: red;")
        self.toggle_excluded.setChecked(True)
        self.toggle_excluded.setObjectName("toggle_excluded")
        self.horizontalLayout_5.addWidget(self.toggle_excluded)
        self.toggle_included = QtWidgets.QRadioButton(self.groupBox_2)
        self.toggle_included.setStyleSheet("color: blue;")
        self.toggle_included.setObjectName("toggle_included")
        self.horizontalLayout_5.addWidget(self.toggle_included)
        self.toggle_activated = QtWidgets.QRadioButton(self.groupBox_2)
        self.toggle_activated.setObjectName("toggle_activated")
        self.horizontalLayout_5.addWidget(self.toggle_activated)
        self.horizontalLayout_8.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.view_all = QtWidgets.QRadioButton(self.groupBox)
        self.view_all.setStyleSheet("color: red;")
        self.view_all.setChecked(True)
        self.view_all.setObjectName("view_all")
        self.horizontalLayout_4.addWidget(self.view_all)
        self.view_included = QtWidgets.QRadioButton(self.groupBox)
        self.view_included.setStyleSheet("color: blue;")
        self.view_included.setObjectName("view_included")
        self.horizontalLayout_4.addWidget(self.view_included)
        self.view_active = QtWidgets.QRadioButton(self.groupBox)
        self.view_active.setObjectName("view_active")
        self.horizontalLayout_4.addWidget(self.view_active)
        self.horizontalLayout_8.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reset_all = QtWidgets.QPushButton(self.groupBox_4)
        self.reset_all.setObjectName("reset_all")
        self.horizontalLayout.addWidget(self.reset_all)
        self.reset_activate = QtWidgets.QRadioButton(self.groupBox_4)
        self.reset_activate.setObjectName("reset_activate")
        self.horizontalLayout.addWidget(self.reset_activate)
        self.reset_exclude = QtWidgets.QRadioButton(self.groupBox_4)
        self.reset_exclude.setChecked(True)
        self.reset_exclude.setObjectName("reset_exclude")
        self.horizontalLayout.addWidget(self.reset_exclude)
        self.horizontalLayout_8.addWidget(self.groupBox_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.save_dataHertz = QtWidgets.QPushButton(self.groupBox_5)
        self.save_dataHertz.setObjectName("save_dataHertz")
        self.horizontalLayout_2.addWidget(self.save_dataHertz)
        self.save_avg_hertz = QtWidgets.QPushButton(self.groupBox_5)
        self.save_avg_hertz.setObjectName("save_avg_hertz")
        self.horizontalLayout_2.addWidget(self.save_avg_hertz)
        self.save_dataES = QtWidgets.QPushButton(self.groupBox_5)
        self.save_dataES.setObjectName("save_dataES")
        self.horizontalLayout_2.addWidget(self.save_dataES)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_8.addWidget(self.groupBox_5)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.mainlist = QtWidgets.QTreeWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainlist.sizePolicy().hasHeightForWidth())
        self.mainlist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mainlist.setFont(font)
        self.mainlist.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainlist.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainlist.setLineWidth(0)
        self.mainlist.setMidLineWidth(0)
        self.mainlist.setAnimated(False)
        self.mainlist.setObjectName("mainlist")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_3)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.g_fdistance = PlotWidget(self.layoutWidget)
        self.g_fdistance.setObjectName("g_fdistance")
        self.verticalLayout_7.addWidget(self.g_fdistance)
        self.g_single = PlotWidget(self.layoutWidget)
        self.g_single.setObjectName("g_single")
        self.verticalLayout_7.addWidget(self.g_single)
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_4)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.analysis_group_box = QtWidgets.QGroupBox(self.splitter)
        self.analysis_group_box.setAutoFillBackground(False)
        self.analysis_group_box.setStyleSheet("border-color: rgb(232, 232, 232);")
        self.analysis_group_box.setTitle("")
        self.analysis_group_box.setObjectName("analysis_group_box")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.analysis_group_box)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.analysis = QtWidgets.QCheckBox(self.analysis_group_box)
        self.analysis.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.analysis.setFont(font)
        self.analysis.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.analysis.setIconSize(QtCore.QSize(15, 15))
        self.analysis.setObjectName("analysis")
        self.verticalLayout_5.addWidget(self.analysis)
        self.g_indentation = PlotWidget(self.analysis_group_box)
        self.g_indentation.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.g_indentation.setFont(font)
        self.g_indentation.setAcceptDrops(True)
        self.g_indentation.setInteractive(True)
        self.g_indentation.setObjectName("g_indentation")
        self.verticalLayout_5.addWidget(self.g_indentation)
        self.avg_hertz = PlotWidget(self.analysis_group_box)
        self.avg_hertz.setEnabled(True)
        self.avg_hertz.setInteractive(True)
        self.avg_hertz.setObjectName("avg_hertz")
        self.verticalLayout_5.addWidget(self.avg_hertz)
        self.g_scatter = PlotWidget(self.analysis_group_box)
        self.g_scatter.setEnabled(True)
        self.g_scatter.setObjectName("g_scatter")
        self.verticalLayout_5.addWidget(self.g_scatter)
        self.es_group_box = QtWidgets.QGroupBox(self.splitter)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.es_group_box.setFont(font)
        self.es_group_box.setStyleSheet("border-color: rgb(232, 232, 232);")
        self.es_group_box.setTitle("")
        self.es_group_box.setObjectName("es_group_box")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.es_group_box)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.es_analysis = QtWidgets.QCheckBox(self.es_group_box)
        self.es_analysis.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.es_analysis.setFont(font)
        self.es_analysis.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.es_analysis.setIconSize(QtCore.QSize(15, 15))
        self.es_analysis.setObjectName("es_analysis")
        self.verticalLayout_10.addWidget(self.es_analysis)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.g_es = PlotWidget(self.es_group_box)
        self.g_es.setObjectName("g_es")
        self.verticalLayout_6.addWidget(self.g_es)
        self.g_decay = PlotWidget(self.es_group_box)
        self.g_decay.setEnabled(True)
        self.g_decay.setInteractive(True)
        self.g_decay.setObjectName("g_decay")
        self.verticalLayout_6.addWidget(self.g_decay)
        self.verticalLayout_10.addLayout(self.verticalLayout_6)
        self.verticalLayout_8.addWidget(self.splitter_4)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout.setObjectName("gridLayout")
        self.prominency = QtWidgets.QGroupBox(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prominency.sizePolicy().hasHeightForWidth())
        self.prominency.setSizePolicy(sizePolicy)
        self.prominency.setCheckable(True)
        self.prominency.setChecked(False)
        self.prominency.setObjectName("prominency")
        self.formLayout = QtWidgets.QFormLayout(self.prominency)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.prominency)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.prominency_prominency = QtWidgets.QSpinBox(self.prominency)
        self.prominency_prominency.setMinimum(1)
        self.prominency_prominency.setMaximum(999)
        self.prominency_prominency.setSingleStep(10)
        self.prominency_prominency.setProperty("value", 40)
        self.prominency_prominency.setObjectName("prominency_prominency")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.prominency_prominency)
        self.label_4 = QtWidgets.QLabel(self.prominency)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.prominency_minfreq = QtWidgets.QSpinBox(self.prominency)
        self.prominency_minfreq.setMinimum(3)
        self.prominency_minfreq.setMaximum(999)
        self.prominency_minfreq.setSingleStep(5)
        self.prominency_minfreq.setProperty("value", 25)
        self.prominency_minfreq.setObjectName("prominency_minfreq")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.prominency_minfreq)
        self.label_5 = QtWidgets.QLabel(self.prominency)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.prominency_band = QtWidgets.QSpinBox(self.prominency)
        self.prominency_band.setMinimum(1)
        self.prominency_band.setMaximum(999)
        self.prominency_band.setSingleStep(5)
        self.prominency_band.setProperty("value", 30)
        self.prominency_band.setObjectName("prominency_band")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.prominency_band)
        self.gridLayout.addWidget(self.prominency, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_26 = QtWidgets.QLabel(self.groupBox_8)
        self.label_26.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setKerning(True)
        self.label_26.setFont(font)
        self.label_26.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_26.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_26.setLineWidth(1)
        self.label_26.setScaledContents(False)
        self.label_26.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_4.addWidget(self.label_26)
        self.comboFsmooth = QtWidgets.QComboBox(self.groupBox_8)
        self.comboFsmooth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboFsmooth.setAutoFillBackground(False)
        self.comboFsmooth.setFrame(True)
        self.comboFsmooth.setObjectName("comboFsmooth")
        self.verticalLayout_4.addWidget(self.comboFsmooth)
        self.FSmooth_box = QtWidgets.QGroupBox(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FSmooth_box.sizePolicy().hasHeightForWidth())
        self.FSmooth_box.setSizePolicy(sizePolicy)
        self.FSmooth_box.setObjectName("FSmooth_box")
        self.verticalLayout_4.addWidget(self.FSmooth_box)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_8, 0, 2, 1, 1)
        self.groupBox_9 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.quickView = QtWidgets.QPushButton(self.groupBox_9)
        self.quickView.setObjectName("quickView")
        self.verticalLayout.addWidget(self.quickView)
        self.comboCP = QtWidgets.QComboBox(self.groupBox_9)
        self.comboCP.setObjectName("comboCP")
        self.verticalLayout.addWidget(self.comboCP)
        self.CP_box = QtWidgets.QGroupBox(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CP_box.sizePolicy().hasHeightForWidth())
        self.CP_box.setSizePolicy(sizePolicy)
        self.CP_box.setObjectName("CP_box")
        self.verticalLayout.addWidget(self.CP_box)
        self.gridLayout_3.addWidget(self.groupBox_9, 0, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setEnabled(True)
        self.groupBox_6.setObjectName("groupBox_6")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.es_win = QtWidgets.QSpinBox(self.groupBox_6)
        self.es_win.setMinimum(3)
        self.es_win.setMaximum(9999)
        self.es_win.setProperty("value", 21)
        self.es_win.setObjectName("es_win")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.es_win)
        self.label_21 = QtWidgets.QLabel(self.groupBox_6)
        self.label_21.setObjectName("label_21")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.es_order = QtWidgets.QSpinBox(self.groupBox_6)
        self.es_order.setMinimum(1)
        self.es_order.setMaximum(9)
        self.es_order.setProperty("value", 3)
        self.es_order.setObjectName("es_order")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.es_order)
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.es_interpolate = QtWidgets.QCheckBox(self.groupBox_6)
        self.es_interpolate.setText("")
        self.es_interpolate.setChecked(True)
        self.es_interpolate.setObjectName("es_interpolate")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.es_interpolate)
        self.gridLayout_2.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.stats_R = QtWidgets.QLabel(self.groupBox_3)
        self.stats_R.setObjectName("stats_R")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stats_R)
        self.label_17 = QtWidgets.QLabel(self.groupBox_3)
        self.label_17.setObjectName("label_17")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.stats_k = QtWidgets.QLabel(self.groupBox_3)
        self.stats_k.setObjectName("stats_k")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.stats_k)
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setObjectName("label_11")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.stats_ne = QtWidgets.QLabel(self.groupBox_3)
        self.stats_ne.setStyleSheet("color: red;")
        self.stats_ne.setObjectName("stats_ne")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.stats_ne)
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.stats_ni = QtWidgets.QLabel(self.groupBox_3)
        self.stats_ni.setStyleSheet("color: blue;")
        self.stats_ni.setObjectName("stats_ni")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.stats_ni)
        self.label_15 = QtWidgets.QLabel(self.groupBox_3)
        self.label_15.setObjectName("label_15")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.stats_na = QtWidgets.QLabel(self.groupBox_3)
        self.stats_na.setStyleSheet("")
        self.stats_na.setObjectName("stats_na")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.stats_na)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.GroupFIT = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroupFIT.sizePolicy().hasHeightForWidth())
        self.GroupFIT.setSizePolicy(sizePolicy)
        self.GroupFIT.setCheckable(False)
        self.GroupFIT.setObjectName("GroupFIT")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.GroupFIT)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_16 = QtWidgets.QLabel(self.GroupFIT)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_13.addWidget(self.label_16)
        self.fit_indentation = QtWidgets.QSpinBox(self.GroupFIT)
        self.fit_indentation.setMinimum(10)
        self.fit_indentation.setMaximum(19999)
        self.fit_indentation.setProperty("value", 800)
        self.fit_indentation.setObjectName("fit_indentation")
        self.horizontalLayout_13.addWidget(self.fit_indentation)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.GroupFIT)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.label_18 = QtWidgets.QLabel(self.GroupFIT)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_7.addWidget(self.label_18)
        self.data_average = QtWidgets.QLabel(self.GroupFIT)
        self.data_average.setStyleSheet("font-weight:bold;")
        self.data_average.setAlignment(QtCore.Qt.AlignCenter)
        self.data_average.setObjectName("data_average")
        self.horizontalLayout_7.addWidget(self.data_average)
        self.label_20 = QtWidgets.QLabel(self.GroupFIT)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_7.addWidget(self.label_20)
        self.data_std = QtWidgets.QLabel(self.GroupFIT)
        self.data_std.setStyleSheet("font-weight:bold;")
        self.data_std.setAlignment(QtCore.Qt.AlignCenter)
        self.data_std.setObjectName("data_std")
        self.horizontalLayout_7.addWidget(self.data_std)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_12 = QtWidgets.QLabel(self.GroupFIT)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_14.addWidget(self.label_12)
        self.label_22 = QtWidgets.QLabel(self.GroupFIT)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_14.addWidget(self.label_22)
        self.decay_e0 = QtWidgets.QLabel(self.GroupFIT)
        self.decay_e0.setStyleSheet("font-weight:bold;")
        self.decay_e0.setAlignment(QtCore.Qt.AlignCenter)
        self.decay_e0.setObjectName("decay_e0")
        self.horizontalLayout_14.addWidget(self.decay_e0)
        self.label_24 = QtWidgets.QLabel(self.GroupFIT)
        self.label_24.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_14.addWidget(self.label_24)
        self.decay_eb = QtWidgets.QLabel(self.GroupFIT)
        self.decay_eb.setStyleSheet("font-weight:bold;")
        self.decay_eb.setAlignment(QtCore.Qt.AlignCenter)
        self.decay_eb.setObjectName("decay_eb")
        self.horizontalLayout_14.addWidget(self.decay_eb)
        self.label_25 = QtWidgets.QLabel(self.GroupFIT)
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_14.addWidget(self.label_25)
        self.decay_d0 = QtWidgets.QLabel(self.GroupFIT)
        self.decay_d0.setStyleSheet("font-weight:bold;")
        self.decay_d0.setAlignment(QtCore.Qt.AlignCenter)
        self.decay_d0.setObjectName("decay_d0")
        self.horizontalLayout_14.addWidget(self.decay_d0)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.gridLayout_2.addWidget(self.GroupFIT, 0, 2, 1, 1)
        self.slid_alpha = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slid_alpha.sizePolicy().hasHeightForWidth())
        self.slid_alpha.setSizePolicy(sizePolicy)
        self.slid_alpha.setMaximum(255)
        self.slid_alpha.setSingleStep(1)
        self.slid_alpha.setProperty("value", 100)
        self.slid_alpha.setOrientation(QtCore.Qt.Vertical)
        self.slid_alpha.setObjectName("slid_alpha")
        self.gridLayout_2.addWidget(self.slid_alpha, 0, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 0, 1, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nano2021"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Open"))
        self.open_selectfolder.setText(_translate("MainWindow", "Load Experiment"))
        self.open_selectfolder.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Toggle"))
        self.toggle_excluded.setText(_translate("MainWindow", "Excluded"))
        self.toggle_included.setText(_translate("MainWindow", "Included"))
        self.toggle_activated.setText(_translate("MainWindow", "Activated"))
        self.groupBox.setTitle(_translate("MainWindow", "View"))
        self.view_all.setText(_translate("MainWindow", "All"))
        self.view_included.setText(_translate("MainWindow", "Included"))
        self.view_active.setText(_translate("MainWindow", "Active"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Reset"))
        self.reset_all.setText(_translate("MainWindow", "ALL"))
        self.reset_activate.setText(_translate("MainWindow", "Activate"))
        self.reset_exclude.setText(_translate("MainWindow", "Exclude"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Save"))
        self.save_dataHertz.setText(_translate("MainWindow", "Hertz"))
        self.save_avg_hertz.setText(_translate("MainWindow", "Avg F-Ind"))
        self.save_dataES.setText(_translate("MainWindow", "ES"))
        self.mainlist.setSortingEnabled(False)
        self.mainlist.headerItem().setText(0, _translate("MainWindow", "Files"))
        self.analysis.setText(_translate("MainWindow", "Hertz Analysis"))
        self.es_analysis.setText(_translate("MainWindow", "Elasticity Spectra Analysis "))
        self.groupBox_8.setTitle(_translate("MainWindow", "Filtering "))
        self.prominency.setTitle(_translate("MainWindow", "Prominency "))
        self.label_3.setText(_translate("MainWindow", "Prominency"))
        self.label_4.setText(_translate("MainWindow", "Min Freq"))
        self.label_5.setText(_translate("MainWindow", "Band"))
        self.label_26.setText(_translate("MainWindow", "Others"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Contact Point "))
        self.quickView.setText(_translate("MainWindow", "Inspect"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Elasticity Spectra"))
        self.label_8.setText(_translate("MainWindow", "Window"))
        self.label_21.setText(_translate("MainWindow", "Order"))
        self.label_13.setText(_translate("MainWindow", "Interpolate"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Stats"))
        self.label_9.setText(_translate("MainWindow", "R [nm]"))
        self.stats_R.setText(_translate("MainWindow", "0"))
        self.label_17.setText(_translate("MainWindow", "k [N/m]"))
        self.stats_k.setText(_translate("MainWindow", "0.00"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p>N<span style=\" vertical-align:sub;\">excluded</span></p></body></html>"))
        self.stats_ne.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p>N<span style=\" vertical-align:sub;\">included</span></p></body></html>"))
        self.stats_ni.setText(_translate("MainWindow", "0"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p>N<span style=\" vertical-align:sub;\">activated</span></p></body></html>"))
        self.stats_na.setText(_translate("MainWindow", "0"))
        self.GroupFIT.setTitle(_translate("MainWindow", "Results "))
        self.label_16.setText(_translate("MainWindow", "Max Indentation [nm]"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Stats</span></p></body></html>"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p>E<span style=\" vertical-align:sub;\">y  </span> <span>&#177;</span> <span>&sigma;</span> [kPa]:</p></body></html>"))
        self.data_average.setText(_translate("MainWindow", "0.00"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p>E<span style=\" vertical-align:sub;\">ES </span>± σ [kPa]:</p></body></html>"))
        self.data_std.setText(_translate("MainWindow", "0.00"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Decay</span></p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p>E<span style=\" vertical-align:sub;\">0</span> <span>&#177;</span> <span>&sigma;</span> [kPa]:</p></body></html>"))
        self.decay_e0.setText(_translate("MainWindow", "0.00"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p>E<span style=\" vertical-align:sub;\">b</span> <span>&#177;</span> <span>&sigma;</span> [Pa]:</p></body></html>"))
        self.decay_eb.setText(_translate("MainWindow", "0.00"))
        self.label_25.setText(_translate("MainWindow", "<html><head/><body><p>d<span style=\" vertical-align:sub;\">0</span> <span>&#177;</span> <span>&sigma;</span>[nm]:</p></body></html>"))
        self.decay_d0.setText(_translate("MainWindow", "0.00"))
from pyqtgraph import PlotWidget
