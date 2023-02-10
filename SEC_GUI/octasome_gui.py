import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import QFile, QTimer, pyqtSignal
from PyQt5 import QtTest
from mainwindow import Ui_MainWindow
import PyQt5.QtSerialPort
import math
import time

# PLUNGER_POSITION = 0
# MAXSPEED = 6000
# MINSPEED = 0
# OPERATING_SPEED = 400
# DISPENSE_VOLUME = 2
# PUMPSTATUS = 0b0

#class definition of main window
class MainWindow(QMainWindow):
    stateChanged = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.timer  = QTimer(self)
        self.ui.setupUi(self)
        self.show()
        # connect GUI signals to methods
        self.ui.connectButton.clicked.connect(self.serialConnect)                       # connect/disconnect from serial port
        self.ui.refreshButton.clicked.connect(self.serialRefresh)                       # refresh available ports in COM spinbox
        self.ui.syringeButton.clicked.connect(self.setSyringeSize)                      # updates GUI units and underlying maths
        self.ui.initializeButton.clicked.connect(self.initializePump)                   # initialize pump and valve select motors
        self.ui.fillButton.clicked.connect(self.fillPump)                               # fill the syringe barrel with fluid
        self.ui.emptyButton.clicked.connect(self.emptyPump)                             # empty the syringe barrel into storage reservoir
        self.ui.primeButton.clicked.connect(self.primeLines)                            # auto-prime fluid lines
        self.ui.emptyLinesButton.clicked.connect(self.emptyPumpLines)                   # cleans pump by flushing all lines [with water]
        self.ui.drawSpeedSpinBox.valueChanged.connect(self.updateDrawSlider)            # updates draw speed slider
        self.ui.drawSpeedSlider.valueChanged.connect(self.updateDrawSpeed)              # updates draw speed spinbox
        self.ui.dispenseSpeedSpinBox.valueChanged.connect(self.updateDispenseSlider)    # updates dispense speed slider
        self.ui.dispenseSpeedSlider.valueChanged.connect(self.updateDispenseSpeed)      # updates dispense speed spin box
        self.ui.dispenseSpinBox.valueChanged.connect(self.updateDispenseVolSlider)      # updates dispense volume slider
        self.ui.dispenseVolumeSlider.valueChanged.connect(self.updateDispenseVolume)    # updates dispense volume spin box
        self.ui.dispenseVolumeButton.clicked.connect(self.dispense)                     # dispenses specified volumes to specified columns
        self.ui.allCheckBox.stateChanged.connect(self.enableColumnSelect)               # toggles column checkbox states
        self.ui.stopButton.clicked.connect(self.stopPump)                               # sends halt command to pump


        # Set tooltips/statustips
        self.ui.fillButton.setToolTip("Fully draw syringe, from reservoir")
        self.ui.emptyButton.setToolTip("Dispense syringe barrel to reservoir")
        self.ui.primeButton.setToolTip(
                "1. Draw partly from reservoir.\n"
                "2. Dispense back to reservoir (remove any air).\n"
                "3. Draw fully from reservoir\n"
                "4. Dispense to each column line equally")
        self.ui.emptyLinesButton.setToolTip(
                "Draw from each column line, dispense to reservoir.")
        self.ui.dispenseVolumeButton.setToolTip(
                "Dispense specified volume from reservoir to column lines*\n"
                "* Either all columns, or specified columns")

        # default GUI state (everything greyed out except for comms until serial comms are connected):

        self.ui.setUpBox.setEnabled(False)
        self.ui.dispenseBox.setEnabled(False)
        self.ui.adjustmentBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)

        # column check boxes - if "all" is selected, then individual selection is greyed out
        self.ui.allCheckBox.setChecked(True)
        self.ui.column1CheckBox.setEnabled(False)
        self.ui.column1CheckBox.setEnabled(False)
        self.ui.column1CheckBox.setEnabled(False)
        self.ui.column1CheckBox.setEnabled(False)
        self.ui.column2CheckBox.setEnabled(False)
        self.ui.column3CheckBox.setEnabled(False)
        self.ui.column4CheckBox.setEnabled(False)
        self.ui.column5CheckBox.setEnabled(False)
        self.ui.column6CheckBox.setEnabled(False)
        self.ui.column7CheckBox.setEnabled(False)
        self.ui.column8CheckBox.setEnabled(False)

        # precision with which dispense volume can be set
        self.ui.dispenseSpinBox.setSingleStep(0.1)
        self.ui.dispenseVolumeSlider.setSingleStep(100)

        # maximum and minimum values for pump speeds
        self.ui.drawSpeedSpinBox.setMaximum(6000)
        self.ui.drawSpeedSpinBox.setMinimum(100)
        self.ui.drawSpeedSlider.setMinimum(1)
        self.ui.drawSpeedSlider.setMaximum(60)
        self.ui.dispenseSpeedSpinBox.setMaximum(6000)
        self.ui.dispenseSpeedSpinBox.setMinimum(100)
        self.ui.dispenseSpeedSlider.setMinimum(1)
        self.ui.dispenseSpeedSlider.setMaximum(60)

        # steps
        self.ui.drawSpeedSpinBox.setSingleStep(100)
        self.ui.drawSpeedSlider.setSingleStep(1)
        self.ui.dispenseSpeedSpinBox.setSingleStep(100)
        self.ui.dispenseSpeedSlider.setSingleStep(1)

        # initial, default speed
        self.ui.drawSpeedSpinBox.setValue(400)
        #self.ui.drawSpeedSlider.setValue(30)
        self.ui.dispenseSpeedSpinBox.setValue(400)
        #self.ui.dispenseSpeedSlider.setValue(30)

        # serial port
        self.serial = PyQt5.QtSerialPort.QSerialPort(self)

    def setBaud(self, baud=9600):
        '''
        Set the baud rate to the `baud` given.
        '''
        if baud == 9600:
            self.serial.setBaudRate(PyQt5.QtSerialPort.QSerialPort.Baud9600)
        if baud == 38400:
            self.serial.setBaudRate(PyQt5.QtSerialPort.QSerialPort.Baud38400)

    # attempts to connect to serial com port with assumed settings
    def serialConnect(self):
        # disable connect button before attempt
        self.ui.connectButton.setEnabled(False)
        portname = self.ui.comPortComboBox.currentText()
        # serial port settings
        self.serial.setPortName(portname)
        self.serial.setDataBits(PyQt5.QtSerialPort.QSerialPort.Data8)
        self.serial.setParity(PyQt5.QtSerialPort.QSerialPort.NoParity)
        self.serial.setStopBits(PyQt5.QtSerialPort.QSerialPort.OneStop)
        self.serial.setFlowControl(PyQt5.QtSerialPort.QSerialPort.NoFlowControl)
        # check if connection was successful.
        # Try baudrates 38400 and 9600
        opened = False
        self.setBaud(38400)
        opened = self.serial.open(PyQt5.QtCore.QIODevice.ReadWrite)
        baud = 38400
        # queryPump() on a failed open yields an int instead of a string
        if isinstance(self.queryPump(), int):
            self.serialDisconnect()
            self.setBaud(9600)
            self.stateChanged.emit("Open")
            opened = self.serial.open(PyQt5.QtCore.QIODevice.ReadWrite)
            baud = 9600

        # if connection is successful:
        if opened:
            self.serial.open(PyQt5.QtCore.QIODevice.ReadWrite)
            print("Connection Successful")
            print("Baud: {}".format(baud))
            self.serialInfo = PyQt5.QtSerialPort.QSerialPortInfo(portname)
            print(self.serialInfo.description())
            print(self.serialInfo.manufacturer())
            print(self.serialInfo.portName())
            print(self.serialInfo.productIdentifier())
            print(self.serialInfo.serialNumber())
            print(self.serialInfo.systemLocation())
            print(self.serialInfo.vendorIdentifier())
            # disable the combo-box when connected, change the connect button to a disconnect button
            self.ui.comPortComboBox.setEnabled(False)
            self.ui.refreshButton.setEnabled(False)
            self.ui.connectButton.setText("Disconnect")
            # since serial connection was successful, enable/disable portions of the GUI
            self.ui.setUpBox.setEnabled(True)
            self.ui.initializeButton.setEnabled(False)
            self.ui.fillButton.setEnabled(False)
            self.ui.emptyButton.setEnabled(False)
            # change the method that the the connect button is linked to (serialDisconnect)
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

#disconnects from the serial port, re-configures GUI to allow re-connection to serial port
    def serialDisconnect(self):
    #close serial port
        self.serial.close()
        print("Disconnected")
    #re-enable combo-box, change disconnect button to connect button, connect correct method to connect button
        self.ui.comPortComboBox.setEnabled(True)
        self.ui.connectButton.setText("Connect")
        self.ui.refreshButton.setEnabled(True)
        self.ui.adjustmentBox.setEnabled(False)
        self.ui.dispenseBox.setEnabled(False)
        self.ui.setUpBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)
        self.ui.connectButton.clicked.disconnect()
        self.ui.connectButton.clicked.connect(self.serialConnect)

#refreshes contents of COM port dropdown menu
    def serialRefresh(self):
    #removes all items from combobox
        self.ui.comPortComboBox.clear()
    #adds available ports to combobox list
        for info in PyQt5.QtSerialPort.QSerialPortInfo.availablePorts():
            if "USB" in info.portName():
                self.ui.comPortComboBox.addItem(info.portName())


#sends a command through the serial port (appends the R to indicate execution), returns pump response
    def write(self, command):
        command = command + "R\r\n"
        print(command)
        self.serial.write(command.encode())
        #may not need this portion of the code
        self.serial.waitForBytesWritten(100)
        if(self.serial.waitForReadyRead(100)):
            response = self.receive()
            return response

#receives data from the serial port (while data is available in the input)
    def receive(self):
    #read byte by byte until no bytes available
        raw_data = b''
        raw_byte = self.serial.read(1)
        while raw_byte != b'':
            raw_data += raw_byte
            raw_byte = self.serial.read(1)
        raw_frame = bytearray(raw_data)
        frame_list = [byte for byte in raw_frame]
        print(frame_list)
        print(raw_data)
        return(frame_list)

#after syringe size is "set", change dispense box units to display appropriate scale (uL or mL)
    def setSyringeSize(self):
    #retreive volume from combobox
        size_numerical = self.getNumerical()
    #check if milliliters or microliters?
        if(size_numerical < 1): #microliters
            self.ui.dispenseSpinBox.setMaximum(size_numerical*1000)
            self.ui.dispenseSpinBox.setSingleStep(0.100)
            self.ui.dispenseSpinBox.setValue(size_numerical*1000)
            self.ui.dispenseUnits.setText("\u03bcL")
            self.ui.dispenseVolumeSlider.setMaximum(int(size_numerical*1000/0.1))
            self.ui.dispenseVolumeSlider.setSingleStep(1)
        else: #milliliters
            self.ui.dispenseSpinBox.setMaximum((size_numerical))
            self.ui.dispenseSpinBox.setSingleStep(0.100)
            self.ui.dispenseSpinBox.setValue(2)
            self.ui.dispenseVolumeSlider.setMaximum(int((size_numerical)/0.1))
            self.ui.dispenseVolumeSlider.setSingleStep(1)
            self.ui.dispenseUnits.setText("mL")
    #display pop-up confirmation that the syringe size has been set
        print("Syringe size set to " + self.ui.syringeComboBox.currentText())
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirmation")
        dlg.setText("Syringe size set to " + self.ui.syringeComboBox.currentText())
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()
    #once OK is pressed, enable the pump initialization button
        if button == QMessageBox.Ok:
            self.ui.initializeButton.setEnabled(True)
            print("OK!")

#returns numerical value of selected syringe size, since the values are strings in the combobox
    def getNumerical(self):
        size = self.ui.syringeComboBox.currentText()
        return{
            '25 mL':25,
            '50 \u03bcL':0.05,
            '100 \u03bcL':0.1,
            '250 \u03bcL':0.25,
            '500 \u03bcL':0.5,
            '1 mL':1,
            '5 mL':5,
            '10 mL':10,
            }[size]

#initializes pump
    def initializePump(self):
    #first, query pump
        busy = self.queryPump()
    #if pump is busy, then display a pop up indicating that pump is busy
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        #self.write("/1Z15,9,1v400V400A6000v800V800A0")
        #self.write("/1Z")
        self.write("/1w1,0I1W0")
        plunger_position = 0
    #after initialization, enable the rest of the GUI
        self.ui.fillButton.setEnabled(True)
        self.ui.emptyButton.setEnabled(True)
        self.enableAllBoxes()

#enables all subwindows of the GUI
    def enableAllBoxes(self):
            self.ui.setUpBox.setEnabled(True)
            self.ui.adjustmentBox.setEnabled(True)
            self.ui.dispenseBox.setEnabled(True)
            self.ui.emergencyStopBox.setEnabled(True)

#sends query command.. 0 = pump busy executing another command
    def queryPump(self):
        response = self.write("/1Q")
        try:
            status_bit = bin(response[3] >> 5 &0b1)
        except:
            status_bit = 0b0
        pumpstatus = status_bit
        return status_bit

#fills pump by changing to first valve, moving to position 6000 (400 steps per second)
    def fillPump(self):
        #display pop up if pump is busy..
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        #build command string
        speed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V" + str(speed) + "A6000"
        self.write(command_string)
        plunger_position = 6000

#empties pump by changing to first valve, moving to position 0 (1000 steps per second)
    def emptyPump(self):
        #display pop up if pump is busy..
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        #build command string
        speed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V" + str(speed) + "A0"
        print(command_string)
        self.write(command_string)
        plunger_position = 0

#primes lines by dispensing a fixed volume through each channel
    def primeLines(self):
    #check if pump is busy
        #display pop up if pump is busy..
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        drawspeed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        dispensespeed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V" + str(drawspeed) + "A800" + "V" + str(dispensespeed) + "A0V" + str(drawspeed) + "A6000"
    #build command string
        command_string += "V" + str(dispensespeed)
        for column in range(8):
            command_string += "I" + str(column+2) + "D" + str(750)
        command_string += "I1V" + str(drawspeed)# + "A6000"
        plunger_position = 6000
        print(command_string)
        self.write(command_string)

#empties lines
    def emptyLines(self):
    #empty pump
        #self.emptyPump()
    #do not build and send command until pump is no longer busy
        #self._waitReady(1,10,1)
    #build command to draw from each line
        speed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V" + str(speed)
        for column in range(8):
            command_string += "I" + str(column+2) + "P" + str(750)
        print(command_string)
    #do not send another command until pump is no longer busy
        #self._waitReady()
    #empty pump
        #self.emptyPump()
        self.write(command_string)

#empties pumps and lines
    def emptyPumpLines(self):
    #check if pump is busy
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
    #empty pump and lines
        drawspeed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        dispensespeed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V"+ str(dispensespeed)+ "A0" +"V" + str(drawspeed)
        for column in range(8):
            command_string += "I" + str(column+2) + "P" + str(750)
        command_string += "I1V" + str(dispensespeed) + "A0"
        plunger_position = 0
        print(command_string)
        self.write(command_string)
        # self.emptyPump()
        # #do not build and send command until pump is no longer busy
        # self._waitReady(1, 10, 1)
        # self.emptyLines()
        # self._waitReady(1, 10, 1)
        # self.emptyPump()

#clean lines by dispensing a fixed volume through each channel
    def cleanLines(self):
    #check if pump is busy
        #display pop up if pump is busy..
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        drawspeed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        dispensespeed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        command_string = "/1I1V" + str(drawspeed) + "A6000"
    #build command string
        command_string += "V" + str(dispensespeed)
        for column in range(8):
            command_string += "I" + str(column+2) + "D" + str(750)
        command_string += "I1V" + str(drawspeed)# + "A6000"
        plunger_position = 6000
        print(command_string)
        self.write(command_string)

#flushes lines a couple of times...
    def flushLines(self):
    #check if pump is busy
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        self.cleanLines()

#updates draw speed slider when spinbox is changed
    def updateDrawSlider(self):
        tick = int(int(self.ui.drawSpeedSpinBox.value())/100)
        self.ui.drawSpeedSlider.setValue(tick)
        operating_speed = tick

#updates draw speed spinbox when slider is changed
    def updateDrawSpeed(self):
        val = self.ui.drawSpeedSlider.value()
        val = val*100
        self.ui.drawSpeedSpinBox.setValue(val)
        operating_speed = val

#updates dispense speed slider when spinbox is changed
    def updateDispenseSlider(self):
        tick = int(int(self.ui.dispenseSpeedSpinBox.value())/100)
        self.ui.dispenseSpeedSlider.setValue(tick)
        operating_speed = tick

#updates dispense speed spinbox when slider is changed
    def updateDispenseSpeed(self):
        val = self.ui.dispenseSpeedSlider.value()
        val = val*100
        self.ui.dispenseSpeedSpinBox.setValue(val)
        operating_speed = val

#updates dispense volume slider when spinbox is changed
    def updateDispenseVolSlider(self):
        tick = int(self.ui.dispenseSpinBox.value()/0.1)
        self.ui.dispenseVolumeSlider.setValue(tick)
        dispense_volume = tick

#updates dispense volume spinbox when slider is changed
    def updateDispenseVolume(self):
        val = self.ui.dispenseVolumeSlider.value()*0.1
        self.ui.dispenseSpinBox.setValue(val)
        dispense_volume = val

    #translates dispense volume value from spin box into number of steps (based off of syringe size)
    #NOTE: assumes 6000 steps = full plunge
    def dispenseVolumeSteps(self):
        #calls getNumerical method to translate the selected volume into a numerical value
        full_volume = self.getNumerical()
        #if the chosen syringe volume is uL scale, treat dispense volume value as uL
        if self.getNumerical() < 1:
            target_volume = self.ui.dispenseSpinBox.value()/1000
        else:
            target_volume = self.ui.dispenseSpinBox.value()
        #milli-liters per step = volume of syringe/total number of steps possible
        mL_per_step = full_volume/6000
        #calculate steps needed
        steps = int(target_volume/mL_per_step)
        print("steps per dispense: " + str(steps))
        return steps

#toggles column checkbox enable states based off of "all" checkbox
    def enableColumnSelect(self):
        if(self.ui.allCheckBox.checkState()):
            self.ui.column1CheckBox.setEnabled(False)
            self.ui.column2CheckBox.setEnabled(False)
            self.ui.column3CheckBox.setEnabled(False)
            self.ui.column4CheckBox.setEnabled(False)
            self.ui.column5CheckBox.setEnabled(False)
            self.ui.column6CheckBox.setEnabled(False)
            self.ui.column7CheckBox.setEnabled(False)
            self.ui.column8CheckBox.setEnabled(False)
        else:
            self.ui.column1CheckBox.setEnabled(True)
            self.ui.column2CheckBox.setEnabled(True)
            self.ui.column3CheckBox.setEnabled(True)
            self.ui.column4CheckBox.setEnabled(True)
            self.ui.column5CheckBox.setEnabled(True)
            self.ui.column6CheckBox.setEnabled(True)
            self.ui.column7CheckBox.setEnabled(True)
            self.ui.column8CheckBox.setEnabled(True)

#dispenses to the columns (all or individually selected)
#TODO: make sure this deals with all reasonable cases.. may want to query pump status before commands are written
    def dispense(self):
        plunger_position = 0
        busy = self.queryPump()
        if(busy == bin(0)):
            print("Pump is busy!!!!!")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Pump is busy")
            dlg.setIcon(QMessageBox.Information)
            button = dlg.exec()
            if button == QMessageBox.Ok:
                print("OK!")
                return
        drawspeed = int(self.ui.drawSpeedSpinBox.value())    #get speed from GUI
        dispensespeed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        #get the number of steps needed based on value of dispense volume
        increment = self.dispenseVolumeSteps()
        #if the "all" check box is selected, dispense to all valves
        if(self.ui.allCheckBox.checkState()):
            print("all columns")
            #builds command string.. may update this..
            command_string = "/1V" + str(drawspeed) + "I1A6000V" + str(dispensespeed)
            for column in range(8):
                if(plunger_position - increment < 0):
                    command_string += "V" + str(drawspeed) + "I1A6000V" + str(dispensespeed)
                    plunger_position = 6000
                    command_string += "I" + str(column+2) + "D" + str(increment)
                    plunger_position = plunger_position - increment
                else:
                    command_string += "I" + str(column+2) + "D" + str(increment)
                    plunger_position = plunger_position - increment
                print(plunger_position)
                print(command_string)
            command_string += "I1A0"
            plunger_position = 0
            print(command_string)
            self.write(command_string)
        #if "all" check box is not selected, dispense based off of the checkboxes that are
        else:
            valves = self.getColumnCheckBoxes()
            index = 1
            command_string = "/1"
            #will build command string based on the column boxes that are checked
            for states in valves:
                index = index + 1
                print(states)
                if(states == True):
                    if(plunger_position - increment < 0):
                        command_string += "V" + str(drawspeed) + "I1A6000V" + str(dispensespeed)
                        plunger_position = 6000
                        command_string += "I" + str(index) + "D" + str(increment)
                        plunger_position = plunger_position - increment
                    else:
                        command_string += "I" + str(index) + "D" + str(increment)
                        plunger_position = plunger_position - increment
                    print(plunger_position)
                    print(command_string)
            command_string += "I1A0"
            plunger_position = 0
            print(command_string)
            self.write(command_string)

#method to check which column boxes are selected; for use by the dispense/prime methods
    def getColumnCheckBoxes(self):
        #boolean array, true = box selected
        result = [self.ui.column1CheckBox.isChecked(),
            self.ui.column2CheckBox.isChecked(),
            self.ui.column3CheckBox.isChecked(),
            self.ui.column4CheckBox.isChecked(),
            self.ui.column5CheckBox.isChecked(),
            self.ui.column6CheckBox.isChecked(),
            self.ui.column7CheckBox.isChecked(),
            self.ui.column8CheckBox.isChecked()]
        return result

#interrupts the pump and stops operation
    def stopPump(self):
        print("STOP PUMP!!!!")
        self.serial.write("/1TR\r\n".encode())

    def getSteps(self, target_volume):
        #assume no microstepping for now..
        total_stepcount = 6000
        syringeVolume = getNumerical() #gets the numerical value for syringe size based off of combobox
        steps = int((target_volume/syringeVolume)*total_stepcount)
        return steps

    def dispenseVolumeToValve(self, volume, valve):
        steps = getSteps(self, target_volume)           #function to translate volume into steps
        speed = int(self.ui.dispenseSpeedSpinBox.value())    #get speed from GUI
        target_column = valve + 1                              #9 channels, 1 is connected to resevoir, 2-9 route to columns

        if(plunger_position == 0):
            fillPump()
        #build the right command based off of volume, speed, and desired valve
        self._waitReady(self, 0.3, 10, 20)

        command_string = "/1" + "v10L4" + "V" + str(speed) + "c10" + "I" + str(target_column) + "D" + str(steps)

    def _waitReady(self, polling_interval=1, timeout=10, delay=None):
        print("waiting..\n")
        if delay:
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.queryPump)
            self.timer.start(delay*1000)
        else:
            self.queryPump()

        start = time.time()
        while (start-time.time()) < (timeout):
            print(pumpstatus)
            ready = self.queryPump()
            if not ready:
                self.timer.setSingleShot(True)
                self.timer.timeout.connect(self.queryPump)
                self.timer.start(1000)
            else:
                return

#MAIN
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #instance of MainWindow class
    window = MainWindow()

    #list all available com ports in comboBox on window
    for info in PyQt5.QtSerialPort.QSerialPortInfo.availablePorts():
        if "USB" in info.portName():
            window.ui.comPortComboBox.addItem(info.portName())

    #window.show()
    sys.exit(app.exec())
