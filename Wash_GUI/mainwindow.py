# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Wash_GUI\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 817)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Wash_GUI\\../../../Desktop/unnamed.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.commsBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commsBox.sizePolicy().hasHeightForWidth())
        self.commsBox.setSizePolicy(sizePolicy)
        self.commsBox.setMinimumSize(QtCore.QSize(0, 65))
        self.commsBox.setMaximumSize(QtCore.QSize(16777215, 65))
        self.commsBox.setObjectName("commsBox")
        self.layoutWidget = QtWidgets.QWidget(self.commsBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 31, 441, 32))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comPortComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comPortComboBox.setObjectName("comPortComboBox")
        self.comPortComboBox.addItem("")
        self.horizontalLayout.addWidget(self.comPortComboBox)
        self.connectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.refreshButton = QtWidgets.QPushButton(self.layoutWidget)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.gridLayout_2.addWidget(self.commsBox, 0, 0, 1, 1)
        self.setUpBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setUpBox.sizePolicy().hasHeightForWidth())
        self.setUpBox.setSizePolicy(sizePolicy)
        self.setUpBox.setMinimumSize(QtCore.QSize(0, 65))
        self.setUpBox.setMaximumSize(QtCore.QSize(16777215, 65))
        self.setUpBox.setObjectName("setUpBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.setUpBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(12, 31, 441, 32))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.syringeComboBox = QtWidgets.QComboBox(self.layoutWidget1)
        self.syringeComboBox.setObjectName("syringeComboBox")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.syringeComboBox)
        self.syringeButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.syringeButton.setObjectName("syringeButton")
        self.horizontalLayout_2.addWidget(self.syringeButton)
        self.initializeButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.initializeButton.setObjectName("initializeButton")
        self.horizontalLayout_2.addWidget(self.initializeButton)
        self.gridLayout_2.addWidget(self.setUpBox, 1, 0, 1, 1)
        self.adjustmentBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adjustmentBox.sizePolicy().hasHeightForWidth())
        self.adjustmentBox.setSizePolicy(sizePolicy)
        self.adjustmentBox.setMinimumSize(QtCore.QSize(0, 195))
        self.adjustmentBox.setMaximumSize(QtCore.QSize(16777215, 195))
        self.adjustmentBox.setObjectName("adjustmentBox")
        self.layoutWidget2 = QtWidgets.QWidget(self.adjustmentBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 90, 441, 101))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.speedGroupBox = QtWidgets.QGroupBox(self.layoutWidget2)
        self.speedGroupBox.setObjectName("speedGroupBox")
        self.layoutWidget3 = QtWidgets.QWidget(self.speedGroupBox)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 35, 201, 61))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.drawSpeedSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.drawSpeedSpinBox.setFont(font)
        self.drawSpeedSpinBox.setDecimals(1)
        self.drawSpeedSpinBox.setSingleStep(0.1)
        self.drawSpeedSpinBox.setObjectName("drawSpeedSpinBox")
        self.horizontalLayout_6.addWidget(self.drawSpeedSpinBox)
        self.drawSpeedUnits = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.drawSpeedUnits.setFont(font)
        self.drawSpeedUnits.setObjectName("drawSpeedUnits")
        self.horizontalLayout_6.addWidget(self.drawSpeedUnits)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addWidget(self.speedGroupBox)
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget2)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 33, 201, 61))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.dispenseSpeedSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget4)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.dispenseSpeedSpinBox.setFont(font)
        self.dispenseSpeedSpinBox.setDecimals(1)
        self.dispenseSpeedSpinBox.setSingleStep(0.1)
        self.dispenseSpeedSpinBox.setObjectName("dispenseSpeedSpinBox")
        self.horizontalLayout_7.addWidget(self.dispenseSpeedSpinBox)
        self.dispenseSpeedUnits = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.dispenseSpeedUnits.setFont(font)
        self.dispenseSpeedUnits.setObjectName("dispenseSpeedUnits")
        self.horizontalLayout_7.addWidget(self.dispenseSpeedUnits)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5.addWidget(self.groupBox)
        self.layoutWidget5 = QtWidgets.QWidget(self.adjustmentBox)
        self.layoutWidget5.setGeometry(QtCore.QRect(10, 30, 441, 58))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.fillButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.fillButton.setObjectName("fillButton")
        self.verticalLayout_7.addWidget(self.fillButton)
        self.primeButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.primeButton.setObjectName("primeButton")
        self.verticalLayout_7.addWidget(self.primeButton)
        self.horizontalLayout_8.addLayout(self.verticalLayout_7)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.emptyButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.emptyButton.setObjectName("emptyButton")
        self.verticalLayout.addWidget(self.emptyButton)
        self.emptyLinesButton = QtWidgets.QPushButton(self.layoutWidget5)
        self.emptyLinesButton.setObjectName("emptyLinesButton")
        self.verticalLayout.addWidget(self.emptyLinesButton)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        self.gridLayout_2.addWidget(self.adjustmentBox, 2, 0, 1, 1)
        self.dispenseBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dispenseBox.setObjectName("dispenseBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dispenseBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.dispenseVolumeBox = QtWidgets.QGroupBox(self.dispenseBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dispenseVolumeBox.sizePolicy().hasHeightForWidth())
        self.dispenseVolumeBox.setSizePolicy(sizePolicy)
        self.dispenseVolumeBox.setMinimumSize(QtCore.QSize(0, 77))
        self.dispenseVolumeBox.setObjectName("dispenseVolumeBox")
        self.layoutWidget6 = QtWidgets.QWidget(self.dispenseVolumeBox)
        self.layoutWidget6.setGeometry(QtCore.QRect(11, 31, 421, 37))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.dispenseSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.dispenseSpinBox.setFont(font)
        self.dispenseSpinBox.setDecimals(1)
        self.dispenseSpinBox.setMinimum(0.1)
        self.dispenseSpinBox.setSingleStep(0.5)
        self.dispenseSpinBox.setObjectName("dispenseSpinBox")
        self.horizontalLayout_4.addWidget(self.dispenseSpinBox)
        self.dispenseUnits = QtWidgets.QLabel(self.layoutWidget6)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.dispenseUnits.setFont(font)
        self.dispenseUnits.setObjectName("dispenseUnits")
        self.horizontalLayout_4.addWidget(self.dispenseUnits)
        self.volRangeLabel = QtWidgets.QLabel(self.layoutWidget6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volRangeLabel.sizePolicy().hasHeightForWidth())
        self.volRangeLabel.setSizePolicy(sizePolicy)
        self.volRangeLabel.setObjectName("volRangeLabel")
        self.horizontalLayout_4.addWidget(self.volRangeLabel)
        self.gridLayout_3.addWidget(self.dispenseVolumeBox, 0, 0, 1, 1)
        self.columnSelectBox = QtWidgets.QGroupBox(self.dispenseBox)
        font = QtGui.QFont()
        font.setBold(False)
        self.columnSelectBox.setFont(font)
        self.columnSelectBox.setObjectName("columnSelectBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.columnSelectBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.allCheckBox = QtWidgets.QCheckBox(self.columnSelectBox)
        self.allCheckBox.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.allCheckBox.setFont(font)
        self.allCheckBox.setStyleSheet("")
        self.allCheckBox.setText("")
        self.allCheckBox.setObjectName("allCheckBox")
        self.gridLayout.addWidget(self.allCheckBox, 0, 5, 1, 1)
        self.col6_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col6_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col6_label.setObjectName("col6_label")
        self.gridLayout.addWidget(self.col6_label, 1, 8, 1, 1)
        self.col6vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col6vFrame.setObjectName("col6vFrame")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.col6vFrame)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.col6CheckBox = QtWidgets.QCheckBox(self.col6vFrame)
        self.col6CheckBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col6CheckBox.setFont(font)
        self.col6CheckBox.setStyleSheet("")
        self.col6CheckBox.setText("")
        self.col6CheckBox.setChecked(True)
        self.col6CheckBox.setObjectName("col6CheckBox")
        self.verticalLayout_13.addWidget(self.col6CheckBox)
        self.gridLayout.addWidget(self.col6vFrame, 2, 8, 1, 1)
        self.col3_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col3_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col3_label.setObjectName("col3_label")
        self.gridLayout.addWidget(self.col3_label, 1, 5, 1, 1)
        self.col4_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col4_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col4_label.setObjectName("col4_label")
        self.gridLayout.addWidget(self.col4_label, 1, 6, 1, 1)
        self.col1_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col1_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col1_label.setObjectName("col1_label")
        self.gridLayout.addWidget(self.col1_label, 1, 3, 1, 1)
        self.col2vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col2vFrame.setObjectName("col2vFrame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.col2vFrame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.col2CheckBox = QtWidgets.QCheckBox(self.col2vFrame)
        self.col2CheckBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col2CheckBox.setFont(font)
        self.col2CheckBox.setStyleSheet("")
        self.col2CheckBox.setText("")
        self.col2CheckBox.setChecked(True)
        self.col2CheckBox.setObjectName("col2CheckBox")
        self.verticalLayout_9.addWidget(self.col2CheckBox)
        self.gridLayout.addWidget(self.col2vFrame, 2, 4, 1, 1)
        self.col4vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col4vFrame.setObjectName("col4vFrame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.col4vFrame)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.col4CheckBox = QtWidgets.QCheckBox(self.col4vFrame)
        self.col4CheckBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col4CheckBox.setFont(font)
        self.col4CheckBox.setStyleSheet("")
        self.col4CheckBox.setText("")
        self.col4CheckBox.setChecked(True)
        self.col4CheckBox.setObjectName("col4CheckBox")
        self.verticalLayout_11.addWidget(self.col4CheckBox)
        self.gridLayout.addWidget(self.col4vFrame, 2, 6, 1, 1)
        self.col2_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col2_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col2_label.setObjectName("col2_label")
        self.gridLayout.addWidget(self.col2_label, 1, 4, 1, 1)
        self.label = QtWidgets.QLabel(self.columnSelectBox)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.col1vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col1vFrame.setObjectName("col1vFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.col1vFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.col1CheckBox = QtWidgets.QCheckBox(self.col1vFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col1CheckBox.setFont(font)
        self.col1CheckBox.setStyleSheet("")
        self.col1CheckBox.setText("")
        self.col1CheckBox.setChecked(True)
        self.col1CheckBox.setObjectName("col1CheckBox")
        self.verticalLayout_2.addWidget(self.col1CheckBox)
        self.gridLayout.addWidget(self.col1vFrame, 2, 3, 1, 1)
        self.ABvFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.ABvFrame.setObjectName("ABvFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ABvFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.ABvFrame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.ABvFrame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.ABvFrame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.ABvFrame)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.gridLayout.addWidget(self.ABvFrame, 2, 2, 1, 1)
        self.col5vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col5vFrame.setObjectName("col5vFrame")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.col5vFrame)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.col5CheckBox = QtWidgets.QCheckBox(self.col5vFrame)
        self.col5CheckBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col5CheckBox.setFont(font)
        self.col5CheckBox.setStyleSheet("")
        self.col5CheckBox.setText("")
        self.col5CheckBox.setChecked(True)
        self.col5CheckBox.setObjectName("col5CheckBox")
        self.verticalLayout_12.addWidget(self.col5CheckBox)
        self.gridLayout.addWidget(self.col5vFrame, 2, 7, 1, 1)
        self.col3vFrame = QtWidgets.QFrame(self.columnSelectBox)
        self.col3vFrame.setObjectName("col3vFrame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.col3vFrame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.col3CheckBox = QtWidgets.QCheckBox(self.col3vFrame)
        self.col3CheckBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.col3CheckBox.setFont(font)
        self.col3CheckBox.setStyleSheet("")
        self.col3CheckBox.setText("")
        self.col3CheckBox.setChecked(True)
        self.col3CheckBox.setObjectName("col3CheckBox")
        self.verticalLayout_10.addWidget(self.col3CheckBox)
        self.gridLayout.addWidget(self.col3vFrame, 2, 5, 1, 1)
        self.col5_label = QtWidgets.QLabel(self.columnSelectBox)
        self.col5_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.col5_label.setObjectName("col5_label")
        self.gridLayout.addWidget(self.col5_label, 1, 7, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.dispenseVolumeButton = QtWidgets.QPushButton(self.columnSelectBox)
        self.dispenseVolumeButton.setObjectName("dispenseVolumeButton")
        self.verticalLayout_4.addWidget(self.dispenseVolumeButton)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.columnSelectBox, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.dispenseBox, 3, 0, 1, 1)
        self.emergencyStopBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emergencyStopBox.sizePolicy().hasHeightForWidth())
        self.emergencyStopBox.setSizePolicy(sizePolicy)
        self.emergencyStopBox.setMinimumSize(QtCore.QSize(0, 60))
        self.emergencyStopBox.setMaximumSize(QtCore.QSize(16777215, 60))
        self.emergencyStopBox.setObjectName("emergencyStopBox")
        self.stopButton = QtWidgets.QPushButton(self.emergencyStopBox)
        self.stopButton.setGeometry(QtCore.QRect(10, 30, 441, 21))
        self.stopButton.setObjectName("stopButton")
        self.gridLayout_2.addWidget(self.emergencyStopBox, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionConsole = QtWidgets.QAction(MainWindow)
        self.actionConsole.setObjectName("actionConsole")
        self.actionEmergStop = QtWidgets.QAction(MainWindow)
        self.actionEmergStop.setObjectName("actionEmergStop")
        self.actionEmergStop1 = QtWidgets.QAction(MainWindow)
        self.actionEmergStop1.setObjectName("actionEmergStop1")
        self.actionReconnectInit = QtWidgets.QAction(MainWindow)
        self.actionReconnectInit.setObjectName("actionReconnectInit")
        self.menuFile.addAction(self.actionEmergStop)
        self.menuFile.addAction(self.actionConsole)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuActions.addAction(self.actionEmergStop)
        self.menuActions.addAction(self.actionReconnectInit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.comPortComboBox, self.connectButton)
        MainWindow.setTabOrder(self.connectButton, self.refreshButton)
        MainWindow.setTabOrder(self.refreshButton, self.syringeComboBox)
        MainWindow.setTabOrder(self.syringeComboBox, self.syringeButton)
        MainWindow.setTabOrder(self.syringeButton, self.initializeButton)
        MainWindow.setTabOrder(self.initializeButton, self.fillButton)
        MainWindow.setTabOrder(self.fillButton, self.emptyButton)
        MainWindow.setTabOrder(self.emptyButton, self.primeButton)
        MainWindow.setTabOrder(self.primeButton, self.emptyLinesButton)
        MainWindow.setTabOrder(self.emptyLinesButton, self.drawSpeedSpinBox)
        MainWindow.setTabOrder(self.drawSpeedSpinBox, self.dispenseSpeedSpinBox)
        MainWindow.setTabOrder(self.dispenseSpeedSpinBox, self.dispenseSpinBox)
        MainWindow.setTabOrder(self.dispenseSpinBox, self.allCheckBox)
        MainWindow.setTabOrder(self.allCheckBox, self.col1CheckBox)
        MainWindow.setTabOrder(self.col1CheckBox, self.col2CheckBox)
        MainWindow.setTabOrder(self.col2CheckBox, self.col3CheckBox)
        MainWindow.setTabOrder(self.col3CheckBox, self.col4CheckBox)
        MainWindow.setTabOrder(self.col4CheckBox, self.col5CheckBox)
        MainWindow.setTabOrder(self.col5CheckBox, self.col6CheckBox)
        MainWindow.setTabOrder(self.col6CheckBox, self.dispenseVolumeButton)
        MainWindow.setTabOrder(self.dispenseVolumeButton, self.stopButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SEC"))
        self.commsBox.setTitle(_translate("MainWindow", "Communications"))
        self.comPortComboBox.setItemText(0, _translate("MainWindow", "<COM Port>"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.refreshButton.setToolTip(_translate("MainWindow", "Refresh the list of COM ports"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.setUpBox.setTitle(_translate("MainWindow", "Set Up"))
        self.syringeComboBox.setItemText(0, _translate("MainWindow", "25 mL"))
        self.syringeComboBox.setItemText(1, _translate("MainWindow", "10 mL"))
        self.syringeComboBox.setItemText(2, _translate("MainWindow", "5 mL"))
        self.syringeComboBox.setItemText(3, _translate("MainWindow", "1 mL"))
        self.syringeComboBox.setItemText(4, _translate("MainWindow", "500 μL"))
        self.syringeComboBox.setItemText(5, _translate("MainWindow", "250 μL"))
        self.syringeComboBox.setItemText(6, _translate("MainWindow", "100 μL"))
        self.syringeComboBox.setItemText(7, _translate("MainWindow", "50 μL"))
        self.syringeButton.setToolTip(_translate("MainWindow", "Set the syringe barrel size (ensure this matches the physical barrel size)"))
        self.syringeButton.setText(_translate("MainWindow", "Set Syringe Size"))
        self.initializeButton.setToolTip(_translate("MainWindow", "Initialize pump before sending commands"))
        self.initializeButton.setText(_translate("MainWindow", "Initialize Pump"))
        self.adjustmentBox.setTitle(_translate("MainWindow", "Adjustments"))
        self.speedGroupBox.setTitle(_translate("MainWindow", "Draw Speed"))
        self.drawSpeedUnits.setText(_translate("MainWindow", "mL/s"))
        self.groupBox.setTitle(_translate("MainWindow", "Dispense Speed"))
        self.dispenseSpeedUnits.setText(_translate("MainWindow", "mL/s"))
        self.fillButton.setToolTip(_translate("MainWindow", "Fully draw syringe, from reservoir"))
        self.fillButton.setText(_translate("MainWindow", "Fill Syringe Barrel"))
        self.primeButton.setToolTip(_translate("MainWindow", "1. Draw partly from reservoir.\n"
"2. Dispense back to reservoir (remove any air).\n"
"3. Draw fully from reservoir.\n"
"4. Dispense to each column line equally."))
        self.primeButton.setText(_translate("MainWindow", "Prime/Clean Lines"))
        self.emptyButton.setToolTip(_translate("MainWindow", "Dispense syringe barrel to reservoir"))
        self.emptyButton.setText(_translate("MainWindow", "Empty Syringe Barrel"))
        self.emptyLinesButton.setToolTip(_translate("MainWindow", "Draw from each column line, dispense to reservoir."))
        self.emptyLinesButton.setText(_translate("MainWindow", "Empty Lines"))
        self.dispenseBox.setTitle(_translate("MainWindow", "Dispense"))
        self.dispenseVolumeBox.setTitle(_translate("MainWindow", "Dispense Volume"))
        self.dispenseUnits.setText(_translate("MainWindow", "mL"))
        self.columnSelectBox.setTitle(_translate("MainWindow", "Column Selection"))
        self.col6_label.setText(_translate("MainWindow", "6"))
        self.col6CheckBox.setStatusTip(_translate("MainWindow", "A6B6"))
        self.col3_label.setText(_translate("MainWindow", "3"))
        self.col4_label.setText(_translate("MainWindow", "4"))
        self.col1_label.setText(_translate("MainWindow", "1"))
        self.col2CheckBox.setStatusTip(_translate("MainWindow", "A2B2"))
        self.col4CheckBox.setStatusTip(_translate("MainWindow", "A4B4"))
        self.col2_label.setText(_translate("MainWindow", "2"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">All</p></body></html>"))
        self.col1CheckBox.setStatusTip(_translate("MainWindow", "A1B1"))
        self.label_3.setText(_translate("MainWindow", "A"))
        self.label_2.setText(_translate("MainWindow", "B"))
        self.label_4.setText(_translate("MainWindow", "C"))
        self.label_5.setText(_translate("MainWindow", "D"))
        self.col5CheckBox.setStatusTip(_translate("MainWindow", "A5B5"))
        self.col3CheckBox.setStatusTip(_translate("MainWindow", "A3B3"))
        self.col5_label.setText(_translate("MainWindow", "5"))
        self.dispenseVolumeButton.setToolTip(_translate("MainWindow", "Dispense specified volume from reservoir to column lines*\n"
"* Either all columns, or specified columns"))
        self.dispenseVolumeButton.setText(_translate("MainWindow", "Dispense to Columns"))
        self.emergencyStopBox.setTitle(_translate("MainWindow", "Emergency Stop"))
        self.stopButton.setToolTip(_translate("MainWindow", "Interrupt pump and stop all actions."))
        self.stopButton.setText(_translate("MainWindow", "STOP PUMP"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuActions.setTitle(_translate("MainWindow", "Action"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setStatusTip(_translate("MainWindow", "Quit the application"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionConsole.setText(_translate("MainWindow", "Console"))
        self.actionConsole.setStatusTip(_translate("MainWindow", "Open a console for manual serial commands. Connection must be open."))
        self.actionConsole.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionEmergStop.setText(_translate("MainWindow", "Emergency Stop"))
        self.actionEmergStop.setStatusTip(_translate("MainWindow", "Force stop the pump."))
        self.actionEmergStop.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionEmergStop1.setText(_translate("MainWindow", "Emergency Stop"))
        self.actionEmergStop1.setStatusTip(_translate("MainWindow", "Force stop the pump."))
        self.actionEmergStop1.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionReconnectInit.setText(_translate("MainWindow", "Reconnect and Initialize"))
        self.actionReconnectInit.setStatusTip(_translate("MainWindow", "Disconnect, set syringe size, and initialize pump."))
        self.actionReconnectInit.setShortcut(_translate("MainWindow", "Ctrl+R"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
