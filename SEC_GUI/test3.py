import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import QFile, QTimer
from mainwindow import Ui_MainWindow
import PyQt5.QtSerialPort
import math
import time

plunger_position = 0
maxspeed = 6000;
minspeed = 0;
operating_speed = 400;
dispense_volume = 2;

#class definition of main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    #connect GUI signals to methods
        self.ui.connectButton.clicked.connect(self.serialConnect)                       #connect/disconnect from serial port
        self.ui.refreshButton.clicked.connect(self.serialRefresh)                       #refresh available ports in COM spinbox
        self.ui.syringeButton.clicked.connect(self.setSyringeSize)                      #updates GUI units and underlying maths
        self.ui.initializeButton.clicked.connect(self.initializePump)                   #initialize pump and valve select motors
        self.ui.fillButton.clicked.connect(self.fillPump)                               #fill the syringe barrel with fluid
        self.ui.emptyButton.clicked.connect(self.emptyPumpLines)                                #empty the syringe barrel into storage reservoir
        self.ui.primeButton.clicked.connect(self.primeLines)                            #auto-prime fluid lines
        self.ui.cleanButton.clicked.connect(self.flushLines)                            #cleans pump by flushing all lines [with water]
        self.ui.drawSpeedSpinBox.valueChanged.connect(self.updateDrawSlider)            #updates draw speed slider
        self.ui.drawSpeedSlider.sliderMoved.connect(self.updateDrawSpeed)               #updates draw speed spinbox
        self.ui.dispenseSpeedSpinBox.valueChanged.connect(self.updateDispenseSlider)    #updates dispense speed slider
        self.ui.dispenseSpeedSlider.sliderMoved.connect(self.updateDispenseSpeed)       #updates dispense speed spin box
        self.ui.dispenseSpinBox.valueChanged.connect(self.updateDispenseVolSlider)      #updates dispense volume slider
        self.ui.dispenseVolumeSlider.sliderMoved.connect(self.updateDispenseVolume)     #updates dispense volume spin box
        self.ui.dispenseVolumeButton.clicked.connect(self.dispense)                           #dispenses specified volumes to specified columns                       
        self.ui.allCheckBox.stateChanged.connect(self.enableColumnSelect)               #toggles column checkbox states
        self.ui.stopButton.clicked.connect(self.stopPump)                               #sends halt command to pump
    
    #default GUI state (everything greyed out except for comms until serial comms are connected):

        self.ui.setUpBox.setEnabled(False)
        self.ui.dispenseBox.setEnabled(False)
        self.ui.adjustmentBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)
    
    #column check boxes - if "all" is selected, then individual selection is greyed out
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
    
    #precision with which dispense volume can be set
        self.ui.dispenseSpinBox.setSingleStep(0.1)
        self.ui.dispenseVolumeSlider.setTickInterval(100)      

    #maximum and minimum values for pump speeds    
        self.ui.drawSpeedSpinBox.setMaximum(maxspeed)
        self.ui.drawSpeedSpinBox.setMinimum(minspeed)
        self.ui.drawSpeedSlider.setMaximum(maxspeed)
        self.ui.drawSpeedSlider.setMinimum(minspeed)
        self.ui.dispenseSpeedSpinBox.setMaximum(maxspeed)
        self.ui.dispenseSpeedSpinBox.setMinimum(minspeed)
        self.ui.dispenseSpeedSlider.setMaximum(maxspeed)
        self.ui.dispenseSpeedSlider.setMinimum(minspeed)
    
    #steps
        self.ui.drawSpeedSpinBox.setSingleStep(100)
        self.ui.drawSpeedSlider.setTickInterval(100)
        self.ui.dispenseSpeedSpinBox.setSingleStep(100)
        self.ui.dispenseSpeedSlider.setTickInterval(100)
    
    #initial, default speed
        self.ui.drawSpeedSpinBox.setValue(operating_speed)
        self.ui.drawSpeedSlider.setValue(operating_speed)
        self.ui.dispenseSpeedSpinBox.setValue(operating_speed)
        self.ui.dispenseSpeedSlider.setValue(operating_speed)

    #serial port
        self.serial = PyQt5.QtSerialPort.QSerialPort(self)

#attempts to connect to serial com port with assumed settings (i.e. 38400baud, 8N1)
#NOTE: baud rate was manually changed to 38400
    def serialConnect(self):
    #disable connect button before attempt
        self.ui.connectButton.setEnabled(False)
        portname = self.ui.comPortComboBox.currentText()
    #serial port settings
        self.serial.setPortName(portname)
        self.serial.setBaudRate(PyQt5.QtSerialPort.QSerialPort.Baud38400)
        self.serial.setDataBits(PyQt5.QtSerialPort.QSerialPort.Data8)
        self.serial.setParity(PyQt5.QtSerialPort.QSerialPort.NoParity)
        self.serial.setStopBits(PyQt5.QtSerialPort.QSerialPort.OneStop)
        self.serial.setFlowControl(PyQt5.QtSerialPort.QSerialPort.NoFlowControl)
    #check if connection was successful
        if(self.serial.open(PyQt5.QtCore.QIODevice.ReadWrite)):
        #if connection is successful:
            print("Connection Successful")
            self.serialInfo = PyQt5.QtSerialPort.QSerialPortInfo(portname)
        #TODO: use this information to check that the GUI is connected to the correct device
            print(self.serialInfo.description())
            print(self.serialInfo.manufacturer())
            print(self.serialInfo.portName())
            print(self.serialInfo.productIdentifier())
            print(self.serialInfo.serialNumber())
            print(self.serialInfo.systemLocation())
            print(self.serialInfo.vendorIdentifier())
        #disable the combo-box when connected, change the connect button to a disconnect button
            self.ui.comPortComboBox.setEnabled(False)
            self.ui.refreshButton.setEnabled(False)
            self.ui.connectButton.setText("Disconnect")
        #since serial connection was successful, enable/disable portions of the GUI
            self.ui.setUpBox.setEnabled(True)
            self.ui.initializeButton.setEnabled(False)
            self.ui.fillButton.setEnabled(False)
            self.ui.emptyButton.setEnabled(False)
        #change the method that the the connect button is linked to (serialDisconnect)
            self.ui.connectButton.clicked.disconnect()
            self.ui.connectButton.clicked.connect(self.serialDisconnect)
        else:
        #if connection is unsuccessful:
            print("Connection Failed")
        #display a pop-up indicating unsuccessful connection
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Connection Failed")
            dlg.setText("Failed to connect :(")
            dlg.setIcon(QMessageBox.Critical)
            button = dlg.exec()
        #close dialog when the OK button is pressed
            if button == QMessageBox.Ok:
                print("OK!")
    #re-enable the connect (now disconnect) button
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
        if(size_numerical < 1):
            self.ui.dispenseSpinBox.setMaximum((size_numerical*1000)/2)
            self.ui.dispenseSpinBox.setSingleStep(1)
            self.ui.dispenseSpinBox.setValue(0)
            self.ui.dispenseUnits.setText("\u03bcL")
            self.ui.dispenseVolumeSlider.setMaximum(1000*(size_numerical*1000)/2)
            self.ui.dispenseVolumeSlider.setTickInterval(1000)
        else:
            self.ui.dispenseSpinBox.setMaximum((size_numerical)/2)
            self.ui.dispenseSpinBox.setSingleStep(0.1)
            self.ui.dispenseSpinBox.setValue(0)
            self.ui.dispenseVolumeSlider.setMaximum(1000*(size_numerical)/2)
            self.ui.dispenseVolumeSlider.setTickInterval(0.1*1000)
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
        self.write("/1Z15,9,1v400V400A6000v800V800A0")
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
        return status_bit

#fills pump by changing to first valve, moving to position 6000 (400 steps per second)
    def fillPump(self):
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
        self.write("/1I1v400V400A6000")
        plunger_position = 6000

#empties pump by changing to first valve, moving to position 0 (1000 steps per second)
    def emptyPump(self):
        self.write("/1I1v1000V1000A0v400V400")
        plunger_position = 0

#primes lines by dispensing a fixed volume through each channel
    def primeLines(self):
        fillPump()
    #do not build and send command until pump is no longer busy
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump()
    #build command string
        command_string = "/1"
        for column in range(8):
            command_string = command_string + "I" + str(column+2) + "M1"  + "D" + str(750)
        print(command_string)
        self.write(command_string)

#empties lines 
    def emptyLines(self):
    #empty pump 
        emptyPump()
    #do not build and send command until pump is no longer busy
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump()
    #build command to draw from each line
        command_string = "/1"
        for column in range(8):
            command_string = command_string + "I" + str(column+2) + "M1"  + "U" + str(857)
        print(command_string)
    #do not send another command until pump is no longer busy   
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump()
    #empty pump
        emptyPump()
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
        emptyPump()
        #do not build and send command until pump is no longer busy
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump() 
        emptyLines()

#clean lines by dispensing a fixed volume through each channel
    def cleanLines(self):
    #check if pump is busy    
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump() 
        emptyPump()
    #do not build and send command until pump is no longer busy
        busy = self.queryPump()
        while(busy == bin(0)):
            busy = self.queryPump() 
    #build string   
        command_string = "/1"
        for column in range(8):
            command_string = command_string + "I" + str(column+2) + "M1"  + "D" + str(750)
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
        for i in range(4):
            cleanLines()

#updates draw speed slider when spinbox is changed
    def updateDrawSlider(self):
        tick = int(self.ui.drawSpeedSpinBox.value())
        self.ui.drawSpeedSlider.setValue(tick)
        operating_speed = tick

#updates draw speed spinbox when slider is changed
    def updateDrawSpeed(self):
        val = self.ui.drawSpeedSlider.value()
        self.ui.drawSpeedSpinBox.setValue(val)
        operating_speed = val

#updates dispense speed slider when spinbox is changed
    def updateDispenseSlider(self):
        tick = int(self.ui.dispenseSpeedSpinBox.value())
        self.ui.dispenseSpeedSlider.setValue(tick)
        operating_speed = tick

#updates dispense speed spinbox when slider is changed
    def updateDispenseSpeed(self):
        val = self.ui.dispenseSpeedSlider.value()
        self.ui.dispenseSpeedSpinBox.setValue(val)
        operating_speed = val

#updates dispense volume slider when spinbox is changed
    def updateDispenseVolSlider(self):
        tick = int(self.ui.dispenseSpinBox.value())*1000
        self.ui.dispenseVolumeSlider.setValue(tick)
        dispense_volume = tick

#updates dispense volume spinbox when slider is changed
    def updateDispenseVolume(self):
        val = self.ui.dispenseVolumeSlider.value()/1000
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
    def dispense(self, plunger_position):
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
        #get the number of steps needed based on value of dispense volume
        increment = self.dispenseVolumeSteps()
        #if the "all" check box is selected, dispense to all valves
        if(self.ui.allCheckBox.checkState()):
            print("all columns")
            #builds command string.. may update this..
            command_string = "/1"
            for column in range(8):
                if(plunger_position - increment < 0):
                    command_string = command_string + "v300V300I1A6000M1v1000V1000"
                    plunger_position = 6000
                    command_string = command_string + "I" + str(column+2) + "M1"  + "D" + str(increment)
                    plunger_position = plunger_position - increment
                else:
                    command_string = command_string + "I" + str(column+2) + "M1"  + "D" + str(increment)
                    plunger_position = plunger_position - increment
                print(plunger_position)
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
                        command_string = command_string + "I1A6000M1"
                        plunger_position = 6000
                        command_string = command_string + "I" + str(index) +"M1" + "D" + str(increment)
                        plunger_position = plunger_position - increment
                    else:
                        command_string = command_string + "I" + str(index) +"M1" + "D" + str(increment)
                        plunger_position = plunger_position - increment
                    
                    print(plunger_position)
                    print(command_string)
                    #self.serial.write(command.encode())               
            self.write(command_string)
    #TODO: disable dispense and prime buttons while the pump is running

#interrupts the pump and stops operation
    def stopPump(self):
        print("STOP PUMP!!!!")
        self.serial.write("/1TR\r\n".encode())

#MAIN
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #instance of MainWindow class
    window = MainWindow()

    #list all available com ports in comboBox on window
    for info in PyQt5.QtSerialPort.QSerialPortInfo.availablePorts():
            window.ui.comPortComboBox.addItem(info.portName())
    
    #window.show()
    sys.exit(app.exec())