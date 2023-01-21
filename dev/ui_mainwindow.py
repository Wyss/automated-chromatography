# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(270, 600)
        MainWindow.setMinimumSize(QSize(270, 600))
        MainWindow.setMaximumSize(QSize(270, 600))
        icon = QIcon()
        icon.addFile(u"../../../Desktop/unnamed.jpg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.commsBox = QGroupBox(self.centralwidget)
        self.commsBox.setObjectName(u"commsBox")
        self.commsBox.setGeometry(QRect(10, 10, 251, 61))
        self.layoutWidget = QWidget(self.commsBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 231, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.comPortComboBox = QComboBox(self.layoutWidget)
        self.comPortComboBox.addItem("")
        self.comPortComboBox.setObjectName(u"comPortComboBox")

        self.horizontalLayout.addWidget(self.comPortComboBox)

        self.connectButton = QPushButton(self.layoutWidget)
        self.connectButton.setObjectName(u"connectButton")

        self.horizontalLayout.addWidget(self.connectButton)

        self.setUpBox = QGroupBox(self.centralwidget)
        self.setUpBox.setObjectName(u"setUpBox")
        self.setUpBox.setGeometry(QRect(10, 70, 251, 161))
        self.layoutWidget1 = QWidget(self.setUpBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 20, 231, 131))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.syringeComboBox = QComboBox(self.layoutWidget1)
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.addItem("")
        self.syringeComboBox.setObjectName(u"syringeComboBox")

        self.horizontalLayout_2.addWidget(self.syringeComboBox)

        self.syringeButton = QPushButton(self.layoutWidget1)
        self.syringeButton.setObjectName(u"syringeButton")

        self.horizontalLayout_2.addWidget(self.syringeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.initializeButton = QPushButton(self.layoutWidget1)
        self.initializeButton.setObjectName(u"initializeButton")

        self.verticalLayout.addWidget(self.initializeButton)

        self.fillButton = QPushButton(self.layoutWidget1)
        self.fillButton.setObjectName(u"fillButton")

        self.verticalLayout.addWidget(self.fillButton)

        self.emptyButton = QPushButton(self.layoutWidget1)
        self.emptyButton.setObjectName(u"emptyButton")

        self.verticalLayout.addWidget(self.emptyButton)

        self.emergencyStopBox = QGroupBox(self.centralwidget)
        self.emergencyStopBox.setObjectName(u"emergencyStopBox")
        self.emergencyStopBox.setGeometry(QRect(10, 480, 251, 61))
        self.stopButton = QPushButton(self.emergencyStopBox)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(20, 20, 211, 31))
        self.dispenseBox = QGroupBox(self.centralwidget)
        self.dispenseBox.setObjectName(u"dispenseBox")
        self.dispenseBox.setGeometry(QRect(10, 240, 251, 241))
        self.columnSelectBox = QGroupBox(self.dispenseBox)
        self.columnSelectBox.setObjectName(u"columnSelectBox")
        self.columnSelectBox.setGeometry(QRect(10, 70, 231, 161))
        self.layoutWidget2 = QWidget(self.columnSelectBox)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 211, 134))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.allCheckBox = QCheckBox(self.layoutWidget2)
        self.allCheckBox.setObjectName(u"allCheckBox")

        self.horizontalLayout_5.addWidget(self.allCheckBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.column1CheckBox = QCheckBox(self.layoutWidget2)
        self.column1CheckBox.setObjectName(u"column1CheckBox")

        self.verticalLayout_2.addWidget(self.column1CheckBox)

        self.column2CheckBox = QCheckBox(self.layoutWidget2)
        self.column2CheckBox.setObjectName(u"column2CheckBox")

        self.verticalLayout_2.addWidget(self.column2CheckBox)

        self.column3CheckBox = QCheckBox(self.layoutWidget2)
        self.column3CheckBox.setObjectName(u"column3CheckBox")

        self.verticalLayout_2.addWidget(self.column3CheckBox)

        self.column4CheckBox = QCheckBox(self.layoutWidget2)
        self.column4CheckBox.setObjectName(u"column4CheckBox")

        self.verticalLayout_2.addWidget(self.column4CheckBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.column5CheckBox = QCheckBox(self.layoutWidget2)
        self.column5CheckBox.setObjectName(u"column5CheckBox")

        self.verticalLayout_3.addWidget(self.column5CheckBox)

        self.column6CheckBox = QCheckBox(self.layoutWidget2)
        self.column6CheckBox.setObjectName(u"column6CheckBox")

        self.verticalLayout_3.addWidget(self.column6CheckBox)

        self.column7CheckBox = QCheckBox(self.layoutWidget2)
        self.column7CheckBox.setObjectName(u"column7CheckBox")

        self.verticalLayout_3.addWidget(self.column7CheckBox)

        self.column8CheckBox = QCheckBox(self.layoutWidget2)
        self.column8CheckBox.setObjectName(u"column8CheckBox")

        self.verticalLayout_3.addWidget(self.column8CheckBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.dispenseButton = QPushButton(self.layoutWidget2)
        self.dispenseButton.setObjectName(u"dispenseButton")

        self.verticalLayout_4.addWidget(self.dispenseButton)

        self.dispenseVolumeBox = QGroupBox(self.dispenseBox)
        self.dispenseVolumeBox.setObjectName(u"dispenseVolumeBox")
        self.dispenseVolumeBox.setGeometry(QRect(10, 20, 231, 51))
        self.layoutWidget3 = QWidget(self.dispenseVolumeBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 20, 211, 26))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.dispenseSpinBox = QDoubleSpinBox(self.layoutWidget3)
        self.dispenseSpinBox.setObjectName(u"dispenseSpinBox")
        self.dispenseSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.dispenseSpinBox.setDecimals(4)
        self.dispenseSpinBox.setMaximum(1000.000000000000000)
        self.dispenseSpinBox.setValue(2.000000000000000)

        self.horizontalLayout_4.addWidget(self.dispenseSpinBox)

        self.dispenseUnits = QLabel(self.layoutWidget3)
        self.dispenseUnits.setObjectName(u"dispenseUnits")

        self.horizontalLayout_4.addWidget(self.dispenseUnits)

        self.dispenseVolumeButton = QPushButton(self.layoutWidget3)
        self.dispenseVolumeButton.setObjectName(u"dispenseVolumeButton")

        self.horizontalLayout_4.addWidget(self.dispenseVolumeButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 270, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SEC", None))
        self.commsBox.setTitle(QCoreApplication.translate("MainWindow", u"Communications", None))
        self.comPortComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"<COM Port>", None))

        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.setUpBox.setTitle(QCoreApplication.translate("MainWindow", u"Set Up", None))
        self.syringeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"25 mL", None))
        self.syringeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"50 \u03bcL", None))
        self.syringeComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"100 \u03bcL", None))
        self.syringeComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"250 \u03bcL", None))
        self.syringeComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"500 \u03bcL", None))
        self.syringeComboBox.setItemText(5, QCoreApplication.translate("MainWindow", u"1 mL", None))
        self.syringeComboBox.setItemText(6, QCoreApplication.translate("MainWindow", u"5 mL", None))
        self.syringeComboBox.setItemText(7, QCoreApplication.translate("MainWindow", u"10 mL", None))

        self.syringeButton.setText(QCoreApplication.translate("MainWindow", u"Set Syringe Size", None))
        self.initializeButton.setText(QCoreApplication.translate("MainWindow", u"Initialize Pump", None))
        self.fillButton.setText(QCoreApplication.translate("MainWindow", u"Fill Pump", None))
        self.emptyButton.setText(QCoreApplication.translate("MainWindow", u"Empty Pump", None))
        self.emergencyStopBox.setTitle(QCoreApplication.translate("MainWindow", u"Emergency Stop", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP PUMP", None))
        self.dispenseBox.setTitle(QCoreApplication.translate("MainWindow", u"Dispense", None))
        self.columnSelectBox.setTitle(QCoreApplication.translate("MainWindow", u"Column Selection", None))
        self.allCheckBox.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.column1CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 1", None))
        self.column2CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 2", None))
        self.column3CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 3", None))
        self.column4CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 4", None))
        self.column5CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 5", None))
        self.column6CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 6", None))
        self.column7CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 7", None))
        self.column8CheckBox.setText(QCoreApplication.translate("MainWindow", u"Column 8", None))
        self.dispenseButton.setText(QCoreApplication.translate("MainWindow", u"Dispense to Columns", None))
        self.dispenseVolumeBox.setTitle(QCoreApplication.translate("MainWindow", u"Dispense Volume", None))
        self.dispenseUnits.setText(QCoreApplication.translate("MainWindow", u"mL", None))
        self.dispenseVolumeButton.setText(QCoreApplication.translate("MainWindow", u"Set Volume", None))
    # retranslateUi

