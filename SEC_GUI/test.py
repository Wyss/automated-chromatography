import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtCore import QFile, QTimer
from mainwindow import Ui_MainWindow
import PyQt5.QtSerialPort
import math
import time


plunger_position = 0
start = time.time()
#status_bit = 0
#class definition of main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        # timer = QTimer(self)           
        # timer.start(1000)
    #connect GUI signals to methods
        self.ui.connectButton.clicked.connect(self.serialConnect)
        self.ui.initializeButton.clicked.connect(self.initializePump)
        self.ui.syringeButton.clicked.connect(self.setSyringeSize)
        #self.ui.primeButton.clicked.connect(self.primeLines)
        self.ui.fillButton.clicked.connect(self.fillPump)
        self.ui.emptyButton.clicked.connect(self.emptyPump)
        #self.ui.dispenseVolumeButton.clicked.connect(self.setDispense)
        #self.ui.dispenseVolumeButton.clicked.connect(self.queryPump)
        self.ui.dispenseButton.clicked.connect(self.dispense)
        self.ui.stopButton.clicked.connect(self.stopPump)
        self.ui.allCheckBox.stateChanged.connect(self.enableColumnSelect)
    #default GUI state (everything greyed out except for comms until serial comms are connected):
        self.ui.dispenseBox.setEnabled(False)
        self.ui.setUpBox.setEnabled(False)
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
        self.ui.dispenseSpinBox.setValue(0)
    #serial port
        #self.serial = PyQt5.QtSerialPort.QSerialPort(self, readyRead = self.receive)
        self.serial = PyQt5.QtSerialPort.QSerialPort(self)
    #define methods
    #this method is for testing.. 
    def printStop(self):
        print("Button Clicked")
    
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
    
    #enables all subwindows of the GUI
    def enableAllBoxes(self):
            self.ui.dispenseBox.setEnabled(True)
            self.ui.setUpBox.setEnabled(True)
            self.ui.emergencyStopBox.setEnabled(True)
    
    #attempts to connect to serial com port with assumed settings (i.e. 38400baud, 8N1)
    #NOTE: baud rate was manually changed to 38400
    def serialConnect(self):
        #disable connect button before attempt
        self.ui.connectButton.setEnabled(False)
        portname = self.ui.comPortComboBox.currentText()
        #serial port settings
        self.serial.setPortName(portname)
        #self.serial.setBaudRate(PyQt5.QtSerialPort.QSerialPort.Baud9600)
        self.serial.setBaudRate(PyQt5.QtSerialPort.QSerialPort.Baud38400)
        self.serial.setDataBits(PyQt5.QtSerialPort.QSerialPort.Data8)
        self.serial.setParity(PyQt5.QtSerialPort.QSerialPort.NoParity)
        self.serial.setStopBits(PyQt5.QtSerialPort.QSerialPort.OneStop)
        self.serial.setFlowControl(PyQt5.QtSerialPort.QSerialPort.NoFlowControl)

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
            self.ui.connectButton.setText("Disconnect")
            #since serial connection was successful, enable/disable portions of the GUI
            self.ui.setUpBox.setEnabled(True)
            self.ui.initializeButton.setEnabled(False)
            #self.ui.primeButton.setEnabled(False)
            #self.ui.primeVolumeSpinBox.setEnabled(False)
            #self.ui.primeUnits.setEnabled(False)
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

    #read data from the serial port (while data is available in the input)
    def receive(self):
        #read until EOL (\n)
        #while self.serial.canReadLine():
            #text = self.serial.readLine().data()
            # print(text)
            # return text

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

    #send a command through the serial port (appends the R to indicate execution)
    #TODO: edit this method such that the status of the pump is queried, confirmed available before sending another command
    def write(self, command):
        command = command + "R\r\n"
        print(command)
        self.serial.write(command.encode())
        #may not need this portion of the code
        self.serial.waitForBytesWritten(100)
        if(self.serial.waitForReadyRead(100)):
            response = self.receive()    
            return response
    #disconnects from the serial port, re-configures GUI to allow re-connection to serial port
    def serialDisconnect(self):
        #close serial port
        self.serial.close()
        print("Disconnected")
        #re-enable combo-box, change disconnect button to connect button, connect correct method to connect button
        #TODO: re-fresh com port listing in the combo box everytime the disconnect is called
        self.ui.comPortComboBox.setEnabled(True)
        self.ui.connectButton.setText("Connect")
        self.ui.dispenseBox.setEnabled(False)
        self.ui.setUpBox.setEnabled(False)
        self.ui.emergencyStopBox.setEnabled(False)
        self.ui.connectButton.clicked.disconnect()
        self.ui.connectButton.clicked.connect(self.serialConnect)

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
        #use time.time() to create a non-blocking approach to checking how much time has elapsed (do not use sleep)
        #query pump -- if busy, keep querying until not busy
        # busy = self.queryPump()
        # while(busy == bin(0)):        
        #     start = time.time()
        #     print("Disabling buttons..")
        #     #delay for a certain amount of time
        #     self.ui.dispenseButton.setEnabled(False)
        #     self.ui.dispenseBox.setEnabled(False)
        #     self.ui.dispenseButton.repaint()
        #     self.ui.dispenseBox.repaint()      
            
        #     while(True):      
        #         print(time.time() - start)
        #         if((time.time() - start) > 5):
        #             break
        #     busy = self.queryPump()
        # print("Re-enabling buttons..")
        # self.ui.dispenseButton.setEnabled(True)
        # self.ui.dispenseBox.setEnabled(True)
    #TODO: disable dispense and prime buttons while the pump is running

    #interrupts the pump and stops operation
    def stopPump(self):
        print("STOP PUMP!!!!")
        self.serial.write("/1TR\r\n".encode())

    #initializes pump and sets speed to fastest configuration 
    def initializePump(self):
        #self.serial.write("/1Zv1000V6000c900S0R\r\n".encode())
        #self.serial.write("/1Zv1000V6000c900S0R\r\n".encode())
        #self.serial.write("/1Z15,9,1v400V400A6000A0R\r\n".encode())
        #self.write("/1Z15,9,1v400V400A6000A0")
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
        self.write("/1Z15,9,1v400V400A6000v800V800A0")
        #self.write("/1Z10,9,1,v400V400")
        plunger_position = 0
        #after initialization, enable the rest of the GUI
        # self.ui.primeButton.setEnabled(True)
        # self.ui.primeVolumeSpinBox.setEnabled(True)
        # self.ui.primeUnits.setEnabled(True)
        self.ui.fillButton.setEnabled(True)
        self.ui.emptyButton.setEnabled(True)
        self.enableAllBoxes()

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
        #self.serial.write("/1I1v400V400A6000R\r\n".encode())
        self.write("/1I1v400V400A6000")
        plunger_position = 6000

    #empties pump by changing to first valve, moving to position 0 (1000 steps per second)
    def emptyPump(self):
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
        #self.serial.write("/1I1v1000V1000A0R\r\n".encode())
        self.write("/1I1v1000V1000A0v400V400")
        plunger_position = 0

    #sends query command.. stuck in this function until ready
    def queryPump(self):
        response = self.write("/1Q")
        try:
            status_bit = bin(response[3] >> 5 &0b1)
        except:
            status_bit = 0b0
        print(status_bit)
        return status_bit
    #returns numerical value of selected syringe size
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
#         switch size:
#             case "25 mL":
#                 size_numerical = 25
#             case "50 \u03bcL":
#                 size_numerical = 0.05
#             case "100 \u03bcL":
#                 size_numerical = 0.1
#             case "250 \u03bcL":
#                 size_numerical = 0.25
#             case "500 \u03bcL":
#                 size_numerical = 0.5
#             case "1 mL":
#                 size_numerical = 1
#             case "5 mL":
#                 size_numerical = 5
#             case "10 mL":
#                 size_numerical = 10
#         return(size_numerical)
    
    #after syringe size is "set", change dispense box units to display appropriate scale (uL or mL)
    def setSyringeSize(self):
        size_numerical = self.getNumerical()
        if(size_numerical < 1):
            self.ui.dispenseSpinBox.setMaximum((size_numerical*1000)/2)
            self.ui.dispenseSpinBox.setSingleStep(1)
            self.ui.dispenseSpinBox.setValue(0)
            self.ui.dispenseUnits.setText("\u03bcL")
        else:
            self.ui.dispenseSpinBox.setMaximum((size_numerical)/2)
            self.ui.dispenseSpinBox.setSingleStep(0.1)
            self.ui.dispenseSpinBox.setValue(0)
            self.ui.dispenseUnits.setText("mL")
        #pop-up confirmation that the syringe size has been set        
        print("Syringe size set to " + self.ui.syringeComboBox.currentText())
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirmation")
        dlg.setText("Syringe size set to " + self.ui.syringeComboBox.currentText())
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()
        if button == QMessageBox.Ok:
            self.ui.initializeButton.setEnabled(True)
            print("OK!")
    
    #method for priming lines.. should be the same as dispense, but with larger volumes in mind...
    #it's a little counter-intuitive, because it also uses the column check boxes to determin which lines to prime
    #TODO: command string grows to long at points.. split up command strong by column and query pump before sending additional commands
    # def primeLines(self):
    #     #calculate steps needed to prime amount of volume, given syringe volume
    #     syringe_size = self.getNumerical()      #represents the chosen syringe volume, in mL
    #     prime_volume = self.ui.primeVolumeSpinBox.value()
    #     #fill the syringe
    #     command_string = "/1I1A6000"
    #     position = 6000

    #     if(self.ui.allCheckBox.checkState()):
    #         #prime ALL lines
    #         for column in range(8):
    #             #print(column)
    #             print(sys.getsizeof(command_string))
    #             steps_needed = int(6000*(prime_volume/syringe_size))    #represents the total steps needed to dispense prime volume
    #             #print(steps_needed)
    #             while(steps_needed > 0):
    #                 #refill syringe if more liquid is needed
    #                 if(steps_needed >= position):
    #                     command_string = command_string + "M1" + "I" + str(column + 2) + "M1" + "D" + str(position)
    #                     steps_needed = steps_needed - position
    #                     position = 0
    #                 else:
    #                     command_string = command_string + "M1" + "I" + str(column + 2) + "M1" + "D" + str(steps_needed)
    #                     position = position - steps_needed
    #                     steps_needed = 0
    #                 if(position == 0):
    #                     command_string = command_string + "I1A6000"     #fill syringe
    #                     position = 6000
    #         #print(sys.getsizeof(command_string))
    #             #print(command_string)
    #             while(self.queryPump() == 0):
    #                 self.serial.waitForReadyRead(10000)

    #             self.write(command_string)
    #             command_string = "/1"
    #     else:
    #         #prime only the selected lines
    #         print("hi")
    #         valves = self.getColumnCheckBoxes()
    #         index = 1
    #         #will build command string based on the column boxes that are checked
    #         for states in valves:
    #             index = index + 1
    #             print(states)

    #             #TODO: add if statement here that checks sizeof command_string and sends it via serial once it has reached a certain threshold (avoid overflow)
    #             if(states == True):
    #                 steps_needed = int(6000*(prime_volume/syringe_size))    #represents the total steps needed to dispense prime volume
    #                 print(steps_needed)
    #                 while(steps_needed > 0):
    #                     #refill syringe if more liquid is needed
    #                     if(steps_needed >= position):
    #                         command_string = command_string + "M1" + "I" + str(index) + "M1" + "D" + str(position)
    #                         steps_needed = steps_needed - position
    #                         position = 0
    #                     else:
    #                         command_string = command_string + "M1" + "I" + str(index) + "M1" + "D" + str(steps_needed)
    #                         position = position - steps_needed
    #                         steps_needed = 0
    #                     if(position == 0):
    #                         command_string = command_string + "I1A6000"     #fill syringe
    #                         position = 6000
    #         print(command_string)
    #         self.write(command_string)
    
    #pop-up confirmation that the dispense volume has been set
    #doesn't actually do anything.. perhaps gray out dispense button until the set dispense volume has been pressed (i.e. disable the spin box everytime a change is detected)
    def setDispense(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirmation")
        dvolume = self.ui.dispenseSpinBox.value()
        formatted_num = '{0:.4f}'.format(dvolume)
        dlg.setText("Dispense Volume Set to " + str(formatted_num) + "mL")
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec()
        if button == QMessageBox.Ok:
            self.ui.initializeButton.setEnabled(True)
            print("OK!")

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
