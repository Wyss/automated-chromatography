import sys
import math
import time
import signal
import argparse
import atexit
import ast
from PyQt5 import QtTest, QtSerialPort
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog, QMessageBox,
                             QPushButton, qApp, QFrame, QWidget)
from PyQt5.QtCore import QFile, QTimer, QIODevice, pyqtSignal, Qt
from mainwindow import Ui_MainWindow

# to import consolewindow from parent dir
sys.path.append("..")
from consolewindow import Ui_ConsoleWindow

# PLUNGER_POSITION = 0
# MAXSPEED = 6000
# MINSPEED = 0
# OPERATING_SPEED = 400
# DISPENSE_VOLUME = 2
# PUMPSTATUS = 0b0
STEPS_PER_STROKE = 48000            # Microstep mode
ONE_SECOND_STROKE_SPEED = 48000     # Microstep mode
PUMP_IDS = [1, 2]                   # Pump identifier set on hardware
DUAL_ID = "A"                       # Pump IDs 1 & 2 addressed together

# class definition of main window
class MainWindow(QMainWindow):
    stateChanged = pyqtSignal(str)

    def __init__(self, debug=False, busy_debug=False, file_name=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.timer  = QTimer(self)
        self.ui.setupUi(self)
        self.show()
        self.CmdStr = CommandStringBuilder()
        self.console_window = None
        self.ui_console = None

        # close window with X
        self.closeEvent = self.quitExit

        # set constants/configs
        self.debug = debug
        self.busy_debug = busy_debug
        self.file_name = file_name
        if self.file_name:
            self.file = open(self.file_name, "w")
            print("File opened: {}".format(self.file.name))
            # self.openFile(self.write)

        # BUTTONS
        # connect/disconnect from serial port:
        self.ui.connectButton.clicked.connect(self.serialConnect)
        # refresh available ports in COM spinbox:
        self.ui.refreshButton.clicked.connect(self.serialRefresh)
        # update GUI units and underlying maths:
        self.ui.syringeButton.clicked.connect(self.setSyringeSize)
        # initialize pump and valve select motors:
        self.ui.initializeButton.clicked.connect(self.initializePump)
        # fill the syringe barrel with fluid:
        self.ui.fillButton.clicked.connect(self.fillPump)
        # empty the syringe barrel into storage reservoir:
        self.ui.emptyButton.clicked.connect(self.emptyPump)
        # auto-prime fluid lines:
        self.ui.primeButton.clicked.connect(self.primeLines)
        # Remove all fluid from lines back to reservoir:
        self.ui.emptyLinesButton.clicked.connect(self.emptyPumpLines)
        # dispense specified volumes to specified columns:
        self.ui.dispenseVolumeButton.clicked.connect(self.dispense)
        # toggle column checkbox states:
        self.ui.allCheckBox.stateChanged.connect(self.enableColumnSelect)
        # send halt command to pump:
        self.ui.stopButton.clicked.connect(self.stopPump)
        # FILE MENU
        # quit application
        self.ui.actionQuit.triggered.connect(self.quitExit)
        # open console
        self.ui.actionConsole.triggered.connect(self.openConsole)
        # ACTION MENU
        # reconnect & init:
        self.ui.actionReconnectInit.triggered.connect(self.reconnectAndInit)
        # send halt command to pump:
        self.ui.actionEmergStop.triggered.connect(self.stopPump)

        # Set tooltips
        self.setConnectTooltip()
        # for all pushbuttons, set statustip to its tooltip
        for button in self.ui.centralwidget.findChildren(QPushButton):
            button.setStatusTip(button.toolTip())

        # default GUI state (everything greyed out except for comms until
        # serial comms are connected):

        self.ui.setUpBox.setEnabled(False)
        self.ui.dispenseBox.setEnabled(False)
        self.ui.adjustmentBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)

        # default syringe size
        self.ui.syringeComboBox.setCurrentText("5 mL")

        # QLabel formatting
        col_labels = [
            self.ui.col1_label,
            self.ui.col2_label,
            self.ui.col3_label,
            self.ui.col4_label,
            self.ui.col5_label,
            self.ui.col6_label
            ]
        for col_label in col_labels:
            col_label.setAlignment(Qt.AlignHCenter)

        vFrames = [
            self.ui.col1vFrame,
            self.ui.col2vFrame,
            self.ui.col3vFrame,
            self.ui.col4vFrame,
            self.ui.col5vFrame,
            self.ui.col6vFrame
            ]
        for vFrame in vFrames:
            vFrame.setFrameShape(QFrame.Box)

        # column check boxes - if "all" is selected, then individual selection
        # is greyed out
        self.ui.allCheckBox.setChecked(True)
        checkboxes = [
            self.ui.col1CheckBox,
            self.ui.col2CheckBox,
            self.ui.col3CheckBox,
            self.ui.col4CheckBox,
            self.ui.col5CheckBox,
            self.ui.col6CheckBox
        ]
        for box in checkboxes:
            box.setEnabled(False)

        # set dispense volume precision (set in mainwindow.*)
        # self.ui.dispenseSpinBox.setSingleStep(0.1)

        # maximum and minimum values for pump speeds
        max_speed = self.speedStepToMLPerSec(ONE_SECOND_STROKE_SPEED/4)
        self.ui.drawSpeedSpinBox.setMaximum(max_speed)
        self.ui.drawSpeedSpinBox.setMinimum(0.1)
        self.ui.dispenseSpeedSpinBox.setMaximum(max_speed)
        self.ui.dispenseSpeedSpinBox.setMinimum(0.1)

        # steps
        # self.ui.drawSpeedSpinBox.setSingleStep(100)
        # self.ui.dispenseSpeedSpinBox.setSingleStep(100)

        # initial, default speed
        self.ui.drawSpeedSpinBox.setValue(1)
        self.ui.dispenseSpeedSpinBox.setValue(1)

        # serial port
        self.serial = QtSerialPort.QSerialPort(self)
        self.serialRefresh()

        # Run when app exist
        atexit.register(self.exitCommands)

    def setConnectTooltip(self):
        """Set the Connect button tooltip for when it's in "connect" mode
        """
        tip = "Connect to the COM port selected in the dropdown"
        self.ui.connectButton.setToolTip(tip)
        self.ui.connectButton.setStatusTip(tip)

    def setBaud(self, baud=9600):
        """Set the baud rate to the `baud` given."""
        if baud == 9600:
            self.serial.setBaudRate(QtSerialPort.QSerialPort.Baud9600)
        if baud == 38400:
            self.serial.setBaudRate(QtSerialPort.QSerialPort.Baud38400)

    def reconnectAndInit(self):
        if self.serial.isOpen():
            self.serialDisconnect()
        self.serialConnect()
        self.setSyringeSize()
        self.initializePump()

    def serialConnect(self):
        """attempts to connect to serial com port with assumed settings"""
        # disable connect button before attempt
        self.ui.connectButton.setEnabled(False)
        portname = self.ui.comPortComboBox.currentText()
        # serial port settings
        if self.debug:
            opened = True
        else:
            self.serial.setPortName(portname)
            self.serial.setDataBits(QtSerialPort.QSerialPort.Data8)
            self.serial.setParity(QtSerialPort.QSerialPort.NoParity)
            self.serial.setStopBits(QtSerialPort.QSerialPort.OneStop)
            self.serial.setFlowControl(QtSerialPort.QSerialPort.NoFlowControl)
            # check if connection was successful.
            # Try baudrates 38400 and 9600
            opened = False
            self.setBaud(38400)
            opened = self.serial.open(QIODevice.ReadWrite)
            baud = 38400
            # queryPump() on a failed open yields an int instead of a string
            query_pump = self.queryPump()
            if isinstance(query_pump[0], int) or isinstance(query_pump[1], int):
                self.serialDisconnect()
                self.setBaud(9600)
                self.stateChanged.emit("Open")
                opened = self.serial.open(QIODevice.ReadWrite)
                baud = 9600

        # if connection is successful:
        if opened:
            if self.debug:
                self.dbprint("pump connected")
            else:
                self.serial.open(QIODevice.ReadWrite)
                print("Connection Successful")
                print("Baud: {}".format(baud))
                self.serialInfo = QtSerialPort.QSerialPortInfo(portname)
                print(self.serialInfo.description())
                print(self.serialInfo.manufacturer())
                print(self.serialInfo.portName())
                print(self.serialInfo.productIdentifier())
                print(self.serialInfo.serialNumber())
                print(self.serialInfo.systemLocation())
                print(self.serialInfo.vendorIdentifier())
            # disable the combo-box when connected, change the connect button
            # to a disconnect button
            self.ui.comPortComboBox.setEnabled(False)
            self.ui.refreshButton.setEnabled(False)
            self.ui.connectButton.setText("Disconnect")
            self.ui.connectButton.setToolTip(
                "Close the serial connection to the pump")
            self.ui.connectButton.setStatusTip(self.ui.connectButton.toolTip())
            # since serial connection was successful, enable/disable portions
            # of the GUI
            self.ui.setUpBox.setEnabled(True)
            self.ui.initializeButton.setEnabled(False)
            self.ui.fillButton.setEnabled(False)
            self.ui.emptyButton.setEnabled(False)
            # change the method that the the connect button is linked to
            # (serialDisconnect)
            self.ui.connectButton.clicked.disconnect()
            self.ui.connectButton.clicked.connect(self.serialDisconnect)
        # if connection is unsuccessful:
        else:
            print("Connection Failed")
            # display a pop-up indicating unsuccessful connection
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Connection Failed")
            dlg.setText("Failed to connect :(")
            dlg.setIcon(QMessageBox.Critical)
            button = dlg.exec()
            # close dialog when the OK button is pressed
            if button == QMessageBox.Ok:
                print("OK!")
        # re-enable the connect (now disconnect) button
        self.ui.connectButton.setEnabled(True)

    def serialDisconnect(self):
        """disconnects from the serial port, re-configures GUI to allow
        re-connection to serial port
        """
        if self.debug:
            self.dbprint("disconnected")
        else:
            # close serial port
            self.serial.close()
            print("Disconnected")
        # re-enable combo-box, change disconnect button to connect button,
        # connect correct method to connect button
        self.ui.comPortComboBox.setEnabled(True)
        self.ui.connectButton.setText("Connect")
        self.ui.refreshButton.setEnabled(True)
        self.ui.adjustmentBox.setEnabled(False)
        self.ui.dispenseBox.setEnabled(False)
        self.ui.setUpBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)
        self.ui.syringeButton.setEnabled(True)
        self.ui.syringeButton.setText("Set Syringe Size")
        self.ui.syringeComboBox.setEnabled(True)
        self.setConnectTooltip()
        self.ui.connectButton.clicked.disconnect()
        self.ui.connectButton.clicked.connect(self.serialConnect)

    def serialRefresh(self):
        """refreshes contents of COM port dropdown menu"""
        # removes all items from combobox
        self.ui.comPortComboBox.clear()
        # adds available ports to combobox list
        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            if "USB" or "COM" in info.portName():
                self.ui.comPortComboBox.addItem(info.portName())
        if self.ui.comPortComboBox.count() == 0:
            self.ui.comPortComboBox.addItem("<no COM found>")

    def write(self, cmd_dict):
        """sends a command through the serial port (appends the R to indicate
        execution), returns pump response
        """
        if type(cmd_dict) is not dict:
            self.dbprint("CMD IS NOT DICT!!!!")
            return
        cmd = ""
        for i in cmd_dict:
            cmd_dict[i] += self.CmdStr.execute()
            cmd += cmd_dict[i]
        print(cmd_dict)
        print(cmd.encode())
        if self.file_name:
            self.file.write("> {}".format(cmd))
        if self.debug:
            self.dbprint("command sent")
        else:
            self.serial.write(cmd.encode())
            # may not need this portion of the code
            time.sleep(0.02)
            self.serial.waitForBytesWritten(100)
            if self.serial.waitForReadyRead(100):
                response = self.receive()
                return response

    def receive(self):
        """receives data from the serial port (while data is available in the
        input)
        """
        # read byte by byte until no bytes available
        raw_data = b''
        raw_byte = self.serial.read(1)
        while raw_byte != b'':
            raw_data += raw_byte
            raw_byte = self.serial.read(1)
        raw_frame = bytearray(raw_data)
        frame_list = [byte for byte in raw_frame]
        str_data = str(raw_data)[2:-1]
        print(raw_data)
        if self.file_name:
            self.file.write("< {}\n\n".format(str_data))
        return frame_list

    def setSyringeSize(self):
        """after syringe size is "set", change dispense box units to display
        appropriate scale (uL or mL)
        """
        # retreive volume from combobox
        syringe_size_ml = self.getSyringeSize_ml()
        # check if milliliters or microliters?
        if(syringe_size_ml < 1): # microliters
            units = "\u03bcL"
            self.ui.dispenseSpinBox.setMaximum(syringe_size_ml*1000)
            self.ui.dispenseSpinBox.setSingleStep(0.100)
            self.ui.dispenseSpinBox.setValue(syringe_size_ml*1000)
            self.ui.volRangeLabel.setText(
                    "(0-{}{})".format(syringe_size_ml*1000, units))
        else: # milliliters
            units = "mL"
            self.ui.dispenseSpinBox.setMaximum((10))
            # self.ui.dispenseSpinBox.setSingleStep(0.100)
            self.ui.dispenseSpinBox.setValue(2.5)
            self.ui.volRangeLabel.setText(
                    "(0-{}{})".format(syringe_size_ml, units))
        self.ui.dispenseUnits.setText(units)
        # display pop-up confirmation that the syringe size has been set
        size = self.ui.syringeComboBox.currentText()
        print("Syringe size set to " + size)

        self.ui.syringeButton.setText("Syringe is {}".format(size))
        self.ui.syringeButton.setEnabled(False)
        self.ui.syringeComboBox.setEnabled(False)
        self.ui.initializeButton.setEnabled(True)

    def getSyringeSize_ml(self):
        """returns numerical value of selected syringe size in ml, since the
        values are strings in the combobox
        """
        size = self.ui.syringeComboBox.currentText()
        syringe_options = {
            '25 mL': 25,
            '10 mL': 10,
            '5 mL': 5,
            '1 mL': 1,
            '500 \u03bcL': 0.5,
            '250 \u03bcL': 0.25,
            '100 \u03bcL': 0.1,
            '50 \u03bcL': 0.05
            }
        return syringe_options[size]

    def initializePump(self):
        """initializes pump"""
        cmd_dict = {}
        if self.debug:
            self.dbprint("pump initialized")
        # check if pump is busy
        if self.checkBusy(busy_debug=False):
            return
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = self.CmdStr.initPump(pump_id)
        # after initialization, enable the rest of the GUI
        self.write(cmd_dict)
        self.ui.fillButton.setEnabled(True)
        self.ui.emptyButton.setEnabled(True)
        self.enableAllBoxes()

    def enableAllBoxes(self):
        """enables all subwindows of the GUI"""
        self.ui.setUpBox.setEnabled(True)
        self.ui.adjustmentBox.setEnabled(True)
        self.ui.dispenseBox.setEnabled(True)
        self.ui.emergencyStopBox.setEnabled(True)

    def queryPump(self):
        """sends query command.. 0 = pump busy executing another command"""
        pump_status = []
        for pump_id in PUMP_IDS:
            response = self.write(self.CmdStr.queryPump(pump_id))
            time.sleep(0.02)
            try:
                status_bit = bin(response[3] >> 5 &0b1)
            except:
                status_bit = 0b0
            pump_status.append(status_bit)
        return pump_status

    def fillPump(self):
        """fills pump by opening all valves, moving to position
        STEPS_PER_STROKE
        """
        cmd_dict = {}
        # check if pump is busy
        if self.checkBusy():
            return
        # build command string
        speed_ml = self.ui.drawSpeedSpinBox.value()  # get speed from GUI
        speed_count = self.speedMLToStepPerSec(speed_ml)
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = (
                    self.CmdStr.pumpID(pump_id) +
                    self.CmdStr.setValvesIn() +
                    self.CmdStr.setTopSpeed(speed_count) +
                    self.CmdStr.fullPickup()
            )
        self.write(cmd_dict)

    def emptyPump(self):
        """empties pump back into input source, moving to position 0
        """
        cmd_dict = {}
        # check if pump is busy
        if self.checkBusy():
            return
        # build command string
        speed_ml = self.ui.dispenseSpeedSpinBox.value()    # get speed from GUI
        speed_count = self.speedMLToStepPerSec(speed_ml)
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = (
                    self.CmdStr.pumpID(pump_id) +
                    self.CmdStr.setValvesIn() +
                    self.CmdStr.setTopSpeed(speed_count) +
                    self.CmdStr.fullDispense()
            )
        self.write(cmd_dict)

    def primeLines(self):
        """primes lines by dispensing a fixed volume through each channel"""
        # check if pump is busy
        cmd_dict = {}
        if self.checkBusy():
            return
        draw_speed_ml = self.ui.drawSpeedSpinBox.value()    # get speed from GUI
        dispense_speed_ml = self.ui.dispenseSpeedSpinBox.value()    # get speed from GUI
        draw_speed_count = self.speedMLToStepPerSec(draw_speed_ml)
        dispense_speed_count = self.speedMLToStepPerSec(dispense_speed_ml)
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = (
                    self.CmdStr.pumpID(pump_id) +
                    self.CmdStr.setValvesIn() +
                    self.CmdStr.setTopSpeed(draw_speed_count) +
                    self.CmdStr.relativePickup(int(STEPS_PER_STROKE*0.75)) +
                    self.CmdStr.setTopSpeed(dispense_speed_count) +
                    self.CmdStr.fullDispense() +
                    self.CmdStr.setTopSpeed(draw_speed_count) +
                    self.CmdStr.fullPickup() +
                    self.CmdStr.setValvesOut() +
                    self.CmdStr.setTopSpeed(dispense_speed_count) +
                    self.CmdStr.fullDispense() +
                    self.CmdStr.setValvesIn()
            )
        self.write(cmd_dict)

    def emptyPumpLines(self):
        """Pickup from all lines, dispense back to source reservoir"""
        cmd_dict = {}
        # check if pump is busy
        if self.checkBusy():
            return
        # empty pump and lines
        draw_speed_ml = self.ui.drawSpeedSpinBox.value()    # get speed from GUI
        dispense_speed_ml = self.ui.dispenseSpeedSpinBox.value()    # get speed from GUI
        draw_speed_count = self.speedMLToStepPerSec(draw_speed_ml)
        dispense_speed_count = self.speedMLToStepPerSec(dispense_speed_ml)
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = (
                    self.CmdStr.pumpID(pump_id) +
                    self.CmdStr.setValvesIn() +
                    self.CmdStr.setTopSpeed(dispense_speed_count) +
                    self.CmdStr.fullDispense() +
                    self.CmdStr.setValvesOut() +
                    self.CmdStr.setTopSpeed(draw_speed_count) +
                    self.CmdStr.fullPickup() +
                    self.CmdStr.setValvesIn() +
                    self.CmdStr.setTopSpeed(dispense_speed_count) +
                    self.CmdStr.fullDispense()
            )
        self.write(cmd_dict)

    def enableColumnSelect(self):
        """toggles column checkbox enable states based off of "all" checkbox"""
        if(self.ui.allCheckBox.checkState()):
            self.ui.col1CheckBox.setEnabled(False)
            self.ui.col2CheckBox.setEnabled(False)
            self.ui.col3CheckBox.setEnabled(False)
            self.ui.col4CheckBox.setEnabled(False)
            self.ui.col5CheckBox.setEnabled(False)
            self.ui.col6CheckBox.setEnabled(False)
        else:
            self.ui.col1CheckBox.setEnabled(True)
            self.ui.col2CheckBox.setEnabled(True)
            self.ui.col3CheckBox.setEnabled(True)
            self.ui.col4CheckBox.setEnabled(True)
            self.ui.col5CheckBox.setEnabled(True)
            self.ui.col6CheckBox.setEnabled(True)

    def dispense(self):
        """dispenses to the columns (all or selected columns [wellplate columns])"""
        cmd_dict = {}
        # TODO: make sure this deals with all reasonable cases.. may want to query pump status before commands are written
        # check if pump is busy
        if self.checkBusy():
            return
        draw_speed_ml = self.ui.drawSpeedSpinBox.value()    # get speed from GUI
        dispense_speed_ml = self.ui.dispenseSpeedSpinBox.value()    # get speed from GUI
        draw_speed_count = self.speedMLToStepPerSec(draw_speed_ml)
        dispense_speed_count = self.speedMLToStepPerSec(dispense_speed_ml)
        # if the "all" check box is selected, dispense to all columns
        all_columns = False
        if self.ui.allCheckBox.checkState():
            print("all columns")
            columns = [True] * 6
        # else just the selected columns
        else:
            columns = self.getColumnCheckBoxes()    # [True, False, True, ...]
        # need to add 2 False columns to match pump channels
        columns.extend([False] * 2)
        num_cols = columns.count(True)
        if num_cols == 6:
            all_columns = True

        # get the number of steps needed based on value of dispense volume
        syringe_size_ml = self.getSyringeSize_ml()
        if syringe_size_ml < 1:
            ml_per_column = self.ui.dispenseSpinBox.value()/1000
        else:
            ml_per_column = self.ui.dispenseSpinBox.value()
        ml_to_dispense = ml_per_column * 2  # syringes divided to 2 cols, so vol/syringe = 2*col_vol
        total_steps = self.volumeToSteps(ml_to_dispense)
        num_of_strokes = total_steps / STEPS_PER_STROKE
        total_ml = ml_per_column * num_cols

        # builds command string.
        self.dbprint(
            "\n\tDISPENSE:\n"
            "\t\t# of columns: {num_cols}\n"
            "\t\tall columns?  {all_columns}\n"
            "\t\tml/column:    {ml_per_column}\n"
            "\t\ttotal ml:     {total_ml}\n"
            "\t\ttotal steps:  {total_steps}\n"
            "\t\t# of strokes: {num_of_strokes}"
            "".format(num_cols=num_cols, all_columns=all_columns,
                      ml_per_column=ml_per_column, total_ml=total_ml,
                      total_steps=total_steps, num_of_strokes=num_of_strokes
                      ).expandtabs(4))

        steps_remaining = total_steps
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = self.CmdStr.pumpID(pump_id)
        # do the dispense in a loop
        for stroke in range(math.ceil(num_of_strokes)):
            # if more than 1 stroke req'd, full stroke
            if num_of_strokes > 1:
                steps = STEPS_PER_STROKE
            # if less than 1 stroke req'd, just do that many steps
            else:
                steps = int(num_of_strokes * STEPS_PER_STROKE)
            # draw from reservoir and prepare dispense speed
            for pump_id in DUAL_ID:
                print("columns (sent to setValves): {}".format(columns))
                cmd_dict[pump_id] += (
                        self.CmdStr.setValvesIn() +
                        self.CmdStr.setTopSpeed(draw_speed_count) +
                        self.CmdStr.absolutePosition(steps) +
                        self.CmdStr.setValves(columns) +
                        self.CmdStr.setTopSpeed(dispense_speed_count) +
                        self.CmdStr.fullDispense()
                )
            self.dbprint(cmd_dict)
            num_of_strokes -= 1
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] += self.CmdStr.setValvesIn()
        self.write(cmd_dict)

        # # separate the valves for the two pumps
        # columns_split = [columns[0:6], columns[6:12]]
        # for i, pump_id in enumerate(range(1,3)):
        #     valve_list = columns_split[i]
        #     cmd_str = self.CmdStr.pumpID(pump_id)
        #     # do the dispense in a loop
        #     for stroke in range(math.ceil(num_of_strokes)):
        #         # if more than 1 stroke req'd, full stroke
        #         if num_of_strokes > 1:
        #             steps = STEPS_PER_STROKE
        #         # if less than 1 stroke req'd, just do that many steps
        #         else:
        #             steps = int(num_of_strokes * STEPS_PER_STROKE)
        #         # draw from reservoir and prepare dispense speed
        #         cmd_str = (cmd_str +
        #                    self.CmdStr.setValvesIn() +
        #                    self.CmdStr.setTopSpeed(draw_speed_count) +
        #                    self.CmdStr.absolutePosition(steps) +
        #                    self.CmdStr.setValves(valve_list) +
        #                    self.CmdStr.setTopSpeed(dispense_speed_count) +
        #                    self.CmdStr.fullDispense())
        #         self.dbprint(cmd_str)
        #         num_of_strokes -= 1
        #     cmd_str += self.CmdStr.setValvesIn()
        #     cmd_list.append(cmd_str)
        # self.write(cmd_dict)

    def getColumnCheckBoxes(self):
        """method to check which column boxes are selected; for use by the
        dispense/prime methods
        """
        # boolean array, true = box selected
        result = [self.ui.col1CheckBox.isChecked(),
                  self.ui.col2CheckBox.isChecked(),
                  self.ui.col3CheckBox.isChecked(),
                  self.ui.col4CheckBox.isChecked(),
                  self.ui.col5CheckBox.isChecked(),
                  self.ui.col6CheckBox.isChecked()]
        return result

    def stopPump(self):
        """interrupts the pump and stops operation"""
        cmd_dict = {}
        cmd = ""
        print("STOP PUMP!!!!")
        for pump_id in DUAL_ID:
            cmd_dict[pump_id] = self.CmdStr.terminate(pump_id)
            if self.debug:
                self.dbprint("pump {} stopped".format(pump_id))
        for i in cmd_dict:
            cmd += cmd_dict[i]
        print(cmd_dict)
        print(cmd.encode())
        if self.debug:
            if self.file_name:
                self.file.write("> {}".format(cmd))
        else:
            self.serial.write(cmd.encode())
            time.sleep(0.02)

    def quitExit(self, event):
        qApp.quit()

    def volumeToSteps(self, volume_ml):
        """Convert given volume in ml to a number of steps
        """
        syringe_vol = self.getSyringeSize_ml()
        # steps = vol*(max_steps/max_vol)
        steps = volume_ml * (STEPS_PER_STROKE/syringe_vol)
        return int(steps)

    def speedStepToMLPerSec(self, step_per_sec):
        """Convert given volume in steps/second to mL/second"""
        syringe_vol = self.getSyringeSize_ml()
        ml_per_step = ONE_SECOND_STROKE_SPEED / syringe_vol

        ml_per_sec = step_per_sec / ml_per_step
        return ml_per_sec

    def speedMLToStepPerSec(self, ml_per_sec):
        """Convert given volume in steps/second to mL/second"""
        syringe_vol = self.getSyringeSize_ml()
        ml_per_step = ONE_SECOND_STROKE_SPEED / syringe_vol

        step_per_sec = ml_per_sec * ml_per_step
        return int(step_per_sec)

    def checkBusy(self, attempts=3, timeout=.1, busy_debug=None):
        """Test if pump is busy. Retries `attempts` times, waiting `timeout`
        seconds between attempts. If it is busy after that, display a warning
        popup and stop attempting.
        """
        if busy_debug is None:
            busy_debug = self.busy_debug
        if self.debug and not busy_debug:
            self.dbprint("not busy")
            return False
        # Try (attempts) times and wait (timeout) sec between
        for attempt in range(attempts):
            print("Attempt # {}".format(attempt))
            # check for debugging busy flag or try for real
            if busy_debug:
                self.dbprint("busy")
                busy = bin(0)
            else:
                busy = self.queryPump()
            # return if not busy or sleep if busy
            if busy[0] != bin(0) or busy[1] != bin(0):
                return False
            else:
                time.sleep(timeout)
        # if it reaches here, it IS busy, display popup
        print("Pump is busy!!!!!")
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning")
        dlg.setText("Pump is busy")
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()
        if button == QMessageBox.Ok:
            print("OK!")
            return True

    # def closeEvent(self, event):
    def exitCommands(self):
        """Things to run at application exit"""
        print("exiting cleanly...")
        if self.file_name:
            self.file.close()
            print("File {} closed".format(self.file_name))
        if self.serial.isOpen():
            print("closing serial port...")
            self.serial.close()
            print("serial port closed.")

    def dbprint(self, msg=""):
        """helper function, 'debug print.' Appends "DEBUG MODE: " before message
        and only displays if app running in debug mode
        """
        if self.debug:
            print("DEBUG MODE: {}".format(msg))
        return

    def openConsole(self):
        """Open the console window to send manual commands
        """
        self.ui_console = None
        if self.console_window is None:
            self.console_window = QMainWindow()
            self.ui_console = Ui_ConsoleWindow()
            self.ui_console.setupUi(self.console_window)
            # connect signals
            self.ui_console.actionClose.triggered.connect(self.closeConsole)
            self.ui_console.sendButton.clicked.connect(self.sendConsoleCmd)
            self.ui_console.cmdLineEdit.returnPressed.connect(self.sendConsoleCmd)
            # override closeEvent because X-ing out breaks it for next time
            self.console_window.closeEvent = self.closeConsole
        self.console_window.show()

    def closeConsole(self, event):
        """Close the console window
        """
        self.console_window.close()
        self.console_window = None

    def sendConsoleCmd(self):
        """Send the command entered in the lineEdit
        """
        raw_cmd = self.ui_console.cmdLineEdit.text()
        cmd = ast.literal_eval(F'"{raw_cmd}"')
        self.ui_console.consoleTextEdit.append(raw_cmd)
        print(cmd.encode())

        self.serial.write(cmd.encode())
        # may not need this portion of the code
        time.sleep(0.02)
        self.serial.waitForBytesWritten(100)
        if self.serial.waitForReadyRead(100):
            response = self.receive()
            self.ui_console.consoleTextEdit.append(str(response))
            return response


class CommandStringBuilder(object):
    """Generates strings for pump commands"""
    def __init__(self):
        pass

    def pumpID(self, id):
        """Set the target pump to receive subsequent commands"""
        return "/{}".format(id)

    def initPump(self, id):
        """Initialize the pump"""
        return "{}W".format(self.pumpID(id))

    def terminate(self, id):
        """Terminate the pump's actions. Includes Run cmd and EOL chars
        /1TR\\r\\n"""
        return "{}TR\r\n".format(self.pumpID(id))

    def queryPump(self, id):
        """Query the pump"""
        return "{}Q".format(self.pumpID(id))

    def setTopSpeed(self, speed):
        """Set the pump's top speed for subsequent movements"""
        return "V{}".format(speed)

    def setStartSpeed(self, speed):
        """Set the pump's starting speed for subsequent movements"""
        return "v{}".format(speed)

    def setAcceleration(self, slope):
        """Set the speed slope for subsequent movements"""
        return "L{}".format(slope)

    def setValvesIn(self):
        """Set all valves to Input position"""
        return "I"

    def setValvesOut(self):
        """Set all valves to Output position"""
        return "O"

    def setValves(self, valve_list=[False] * 8):
        """Set valves individually"""
        if len(valve_list) < 8:
            ext_by = 8 - len(valve_list)
            valve_list.extend([False] * ext_by)
        print("valve_list = {}".format(valve_list))

        # final 2 valves should always be False, so
        # False count = 8 & True count = 6
        if valve_list.count(False) == 8:
            return self.setValvesIn()
        elif valve_list.count(True) == 6:
            return self.setValvesOut()
        else:
            cmd_str = "B"
            for v in valve_list:
                cmd_str += str(int(v))
            print("SetValves str: {}".format(cmd_str))
            return cmd_str

    def fullPickup(self):
        """Move the plunger to the absolute position given"""
        return self.absolutePosition(STEPS_PER_STROKE)

    def fullDispense(self):
        """Move the plunger to the absolute position given"""
        return self.absolutePosition(0)

    def absolutePosition(self, position):
        """Move the plunger to the absolute position given"""
        return "A{}".format(position)

    def relativePickup(self, steps):
        """Move the plunger down (pickup) by the number of given steps"""
        return "P{}".format(steps)

    def relativeDispense(self, steps):
        """Move the plunger up (dispense) by the number of given steps"""
        return "D{}".format(steps)

    def execute(self, end_line=True):
        """Executes the command string"""
        cmd_str = "R"
        if end_line:
            cmd_str += "\r\n"
        return cmd_str

def _sigint_handler(*args):
    """Handle ctrl+c sigint cleanly"""
    print("\n"
          "Quitting from ctrl+c")
    qApp.quit()

# MAIN
if __name__ == "__main__":
    # cmdline argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug",
            help="Don't attempt pump communication, enable buttons as if "
                 "connected.",
            action="store_true")
    parser.add_argument("-b", "--busy-debug",
            help="Pretend the pump is always busy for debugging. Only works "
                 "in conjunction with [-d --debug] arg.",
            action="store_true")
    parser.add_argument("-w", "--write", metavar="FILENAME",
            help="Write the serial commands to FILENAME. Appends '.log' to "
                 "name.",
            action="store")
    args = parser.parse_args()

    # argparse: -b needs -d
    if args.busy_debug and not args.debug:
        print("-b (--busy-debug) arg only works with -d (--debug) arg. "
              "Activating -d (--debug).")
        args.debug=True
    # argparse: -w saves filename filename
    if args.write:
        file_name = "{}.log".format(args.write)
    else:
        file_name = None

    # handle sigint (ctrl+c) with sigint_handler function
    signal.signal(signal.SIGINT, _sigint_handler)

    app = QApplication(sys.argv)

    # allows interpreter handle ctrl+C every 250 ms
    sigint_timer = QTimer()
    sigint_timer.start(250)
    sigint_timer.timeout.connect(lambda: None)

    # instance of MainWindow class
    window = MainWindow(args.debug, args.busy_debug, file_name)

    # window.show()
    sys.exit(app.exec())
