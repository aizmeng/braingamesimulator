#Developed By: vslcreations.com
#Team: hodor
#unitedbyhcl hackathon

import pyqtgraph as pg
import numpy as np
from PyQt4 import QtCore, QtGui
import mindwave,sys,time,ctypes

#DIRECTX Programming under ctypes for initiating virtual keys of system
SendInput = ctypes.windll.user32.SendInput
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
    
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#Direct X scancode definitions can be found here: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
DIK_ESCAPE=0x01
DIK_1=0x02
DIK_2               =0x03
DIK_3               =0x04
DIK_4               =0x05
DIK_5               =0x06
DIK_6               =0x07
DIK_7               =0x08
DIK_8               =0x09
DIK_9               =0x0A
DIK_0               =0x0B
DIK_MINUS           =0x0C    #/* - on main keyboard */
DIK_EQUALS          =0x0D
DIK_BACK            =0x0E    #/* backspace */
DIK_TAB             =0x0F
DIK_Q               =0x10
DIK_W               =0x11
DIK_E               =0x12
DIK_R               =0x13
DIK_T               =0x14
DIK_Y               =0x15
DIK_U               =0x16
DIK_I               =0x17
DIK_O               =0x18
DIK_P               =0x19
DIK_LBRACKET        =0x1A
DIK_RBRACKET        =0x1B
DIK_RETURN          =0x1C    #/* Enter on main keyboard */
DIK_LCONTROL        =0x1D
DIK_A               =0x1E
DIK_S               =0x1F
DIK_D               =0x20
DIK_F               =0x21
DIK_G               =0x22
DIK_H               =0x23
DIK_J               =0x24
DIK_K               =0x25
DIK_L               =0x26
DIK_SEMICOLON       =0x27
DIK_APOSTROPHE      =0x28
DIK_GRAVE           =0x29    #/* accent grave */
DIK_LSHIFT          =0x2A
DIK_BACKSLASH       =0x2B
DIK_Z               =0x2C
DIK_X               =0x2D
DIK_C               =0x2E
DIK_V               =0x2F
DIK_B               =0x30
DIK_N               =0x31
DIK_M               =0x32
DIK_COMMA           =0x33
DIK_PERIOD          =0x34    #/* . on main keyboard */
DIK_SLASH           =0x35    #/* / on main keyboard */
DIK_RSHIFT          =0x36
DIK_MULTIPLY        =0x37    #/* * on numeric keypad */
DIK_LMENU           =0x38    #/* left Alt */
DIK_SPACE           =0x39
DIK_CAPITAL         =0x3A
DIK_F1              =0x3B
DIK_F2              =0x3C
DIK_F3              =0x3D
DIK_F4              =0x3E
DIK_F5              =0x3F
DIK_F6              =0x40
DIK_F7              =0x41
DIK_F8              =0x42
DIK_F9              =0x43
DIK_F10             =0x44
DIK_NUMLOCK         =0x45
DIK_SCROLL          =0x46    #/* Scroll Lock */
DIK_NUMPAD7         =0x47
DIK_NUMPAD8         =0x48
DIK_NUMPAD9         =0x49
DIK_SUBTRACT        =0x4A    #/* - on numeric keypad */
DIK_NUMPAD4         =0x4B
DIK_NUMPAD5         =0x4C
DIK_NUMPAD6         =0x4D
DIK_ADD             =0x4E    #/* + on numeric keypad */
DIK_NUMPAD1         =0x4F
DIK_NUMPAD2         =0x50
DIK_NUMPAD3         =0x51
DIK_NUMPAD0         =0x52
DIK_DECIMAL         =0x53    #/* . on numeric keypad */
DIK_F11             =0x57
DIK_F12             =0x58
RUN_W=0x2A
RUN_S=0x2A
RUN_A=0x2A
RUN_D=0x2A

# Functions for pressing and releaseing the keys
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


#GUI Controls: Designed by QT Designer & Converted using pyuic
#Contains all GUI Components & event triggers
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    #DEF GLOBAL VARIABLES
    connectstats = "Disconnected"
    attention = 0
    meditation = 0
    eyeblink = 0
    threshol = 40
    port = 'COM3'       #CHANGE PORT VALUE FROM Device Manager>>COM Devices
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(350, 400)
        MainWindow.setMinimumSize(QtCore.QSize(350, 400))
        MainWindow.setMaximumSize(QtCore.QSize(350, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("favicon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 294, 331))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setStyleSheet(_fromUtf8("background-color: rgb(230, 0, 0);\n"
"font: 11pt \"MS Shell Dlg 2\";"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_2.addWidget(self.pushButton_2, 9, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 0, 2, 1, 1)
        self.pushButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(85, 170, 0);\n"
"font: 12pt \"MS Shell Dlg 2\";"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 9, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBox, 5, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_2.addWidget(self.lineEdit, 4, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.gridLayoutWidget)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 7, 0, 1, 3)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 2, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 6, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuEile = QtGui.QMenu(self.menubar)
        self.menuEile.setObjectName(_fromUtf8("menuEile"))

        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionWiFi = QtGui.QAction(MainWindow)
        self.actionWiFi.setObjectName(_fromUtf8("actionWiFi"))
        self.actionEthernet = QtGui.QAction(MainWindow)
        self.actionEthernet.setObjectName(_fromUtf8("actionEthernet"))
        self.actionInfo = QtGui.QAction(MainWindow)
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.actionDeveloper = QtGui.QAction(MainWindow)
        self.actionDeveloper.setObjectName(_fromUtf8("actionDeveloper"))
        self.menuEile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionInfo)
        self.menuAbout.addAction(self.actionDeveloper)
        self.menubar.addAction(self.menuEile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Game Simulator", None))
        self.pushButton_2.setText(_translate("MainWindow", "QUIT", None))
        self.label_2.setText(_translate("MainWindow", "Connection Status:", None))
        self.label_5.setText(_translate("MainWindow", self.connectstats, None))
        self.label_12.setText(_translate("MainWindow", "Enter COM PORT", None))
        self.lineEdit_2.setText(_translate("MainWindow", self.port, None))
        self.pushButton.setText(_translate("MainWindow", "CONNECT", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "Asphalt8", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "GTA Sanandreas", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "NFS MMW", None))
        self.lineEdit.setText(_translate("MainWindow", str(self.threshol), None))
        self.label_6.setText(_translate("MainWindow", "Enter Threshold", None))
        self.label_3.setText(_translate("MainWindow", "Attention", None))
        self.label_8.setText(_translate("MainWindow", str(self.attention), None))
        self.label_7.setText(_translate("MainWindow", "Eye Blink", None))
        self.label_10.setText(_translate("MainWindow", str(self.eyeblink), None))
        self.label_9.setText(_translate("MainWindow", str(self.meditation), None))
        self.label.setText(_translate("MainWindow", "Select Your Game:", None))
        self.label_4.setText(_translate("MainWindow", "Meditation", None))
        self.label_11.setText(_translate("MainWindow", "Focus here to test key presses...", None))
        self.menuEile.setTitle(_translate("MainWindow", "File", None))
        self.menuAbout.setTitle(_translate("MainWindow", "About", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionInfo.setText(_translate("MainWindow", "Info", None))
        self.actionDeveloper.setText(_translate("MainWindow", "Developer", None))

        #Linking Menus
        self.actionExit.setStatusTip('Exit')
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.triggered.connect(self.close)
        self.actionInfo.setStatusTip('About Help')
        self.actionInfo.triggered.connect(self.help)
        self.actionDeveloper.setStatusTip('About Developer')
        self.actionDeveloper.triggered.connect(self.devinfo)

        #Linking Buttons
        self.pushButton.clicked.connect(lambda:self.connection())
        self.pushButton_2.clicked.connect(lambda:self.close())
        
    #DEF FUNCTIONS
    def close(self):
        sys.exit()
    def help(self):
        print "HELP"
        self.msg = QtGui.QMessageBox()
        self.msg.setIcon(QtGui.QMessageBox.Information)
        self.msg.setWindowTitle("Help")
        self.msg.setWindowIcon(QtGui.QIcon('favicon.jpg'))
        self.msg.setText("1.Check your network connections properly.\n2.Click Connect button to create selected connection.\n3.Open any of your game and start playing.\n4.Click Disconnect button to disconnect.\n\nTechnical Queries: email@vslcreations.in")
        self.msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.msg.exec_()
    def devinfo(self):
        print "DEVELOPER INFO"
        self.msg = QtGui.QMessageBox()
        self.msg.setIcon(QtGui.QMessageBox.Information)
        self.msg.setWindowTitle("About Developer")
        self.msg.setWindowIcon(QtGui.QIcon('favicon.jpg'))
        self.msg.setText("Vishal Aditya\nSoftware Developer\nwww.vslcreations.com")
        self.msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        self.msg.exec_()

    def connection(self):
        self.connectstats = 'Connected'
        self.port = str(self.lineEdit_2.text()) #GET PORT 
        self.threshol = int(self.lineEdit.text())#GET THRESHOLD
        #DEVICE CONNECTION
        #THINK GEAR DERIVER MUST BE INSTALLED
        headset = mindwave.Headset(self.port, 'CC0E')
        time.sleep(2)        
        headset.connect()
        print "Connecting..."
        self.statusbar.showMessage("Device Connecting...")
        while headset.status != 'connected':
            time.sleep(0.5)
            if headset.status == 'standby':
                headset.connect()
                print "Retrying connect..."
                self.statusbar.showMessage("Device Connecting...")
        print "Connected."
        self.statusbar.showMessage("Device Connected")
        self.label_5.setText(_translate("MainWindow", self.connectstats, None))
        
        #BLINK FROM RAW VALUE
        intiVal = 0.00    
        while True:
            self.attention = headset.attention
            self.meditation = headset.meditation
            initVal = headset.raw_value
            time.sleep(0.1)
            blink = abs(headset.raw_value - initVal)
            
            #Initiating send keys: Main Game Simulator Logics
            #Currently using attention values only
            if(self.attention > self.threshol):    #UP w
                print "w KEY"
                self.statusbar.showMessage("<w> KEY Pressed")
                PressKey(0x11)
            if(self.attention < self.threshol):    #UP w
                ReleaseKey(0x11)
            if(blink > 400):  #DOWN s
                print "s KEY"
                self.statusbar.showMessage("<s> KEY Pressed")
                PressKey(0x1F)
                self.eyeblink = 1
            if(blink < 400):  #DOWN s
                ReleaseKey(0x1F)
                self.eyeblink = 0
            if(self.attention > self.threshol+20):#space
                print "SPACE KEY"
                self.statusbar.showMessage("<space> KEY Pressed")
                PressKey(0x39)
            if(self.attention < self.threshol+20):#space
                ReleaseKey(0x39)
            
            #UI SETTEXT FOR LABELS
            self.label_8.setText(_translate("MainWindow", str(self.attention), None))
            self.label_10.setText(_translate("MainWindow", str(self.eyeblink), None))
            self.label_9.setText(_translate("MainWindow", str(self.meditation), None))
            #Update UI in realtime
            QtGui.QApplication.processEvents()
                
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

