from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QScrollArea, QGroupBox, QWidget, QFormLayout, \
    QLabel, QLineEdit, QHBoxLayout, QBoxLayout, QSizePolicy,QStackedWidget ,QVBoxLayout,QGridLayout,QCheckBox,QMessageBox
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from FileUtils import FileUtil
import re
import sys

class AddReminderWindow(QWidget):
    
    Update = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.title ='Add Reminder'
        self.left = 500
        self.top = 200
        self.width_ = 600
        self.height = 600
        self.NoBoderStyleSheet = ("border :0px;\n")
        self.setStyleSheet("background-color: black;\n" "padding:0px;\n" "spacing:0px;\n")
        self.InitWindow()
        layout = self.InitUI()
        gridLayout = QVBoxLayout()        
        gridLayout.addStretch()
        gridLayout.setSpacing(0)
        gridLayout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.isMouseButtonDown = True
            self.oldPos = event.globalPos()


    def mouseReleaseEvent(self, event):
        self.isMouseButtonDown = False

    def mouseMoveEvent(self, event):
        if self.isMouseButtonDown == True:
            delta =  (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        
    def AppendReminder(self):
        if self.Title.text()  == '' or self.Date.text()== '' or self.StartTime.text()== '' or self.EndTime.text()=='':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Missing Fields')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        if not re.search("..-..-....",self.Date.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Enter Data in the format DD-MM-YYYY')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        if not re.search("..:..",self.StartTime.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Enter time in the format HH:MM')
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        if not re.search("..:..",self.EndTime.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Enter time in the format HH:MM')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        
        FileUtil.saveRemindersToFile(self,self.Title.text(),self.Date.text(),self.StartTime.text(),self.EndTime.text())
        self.Title.clear()
        self.Date.clear()
        self.StartTime.clear()
        self.EndTime.clear()
        self.Update.emit()
        self.close()

    
    def InitTopBar(self):
        TopBar = QHBoxLayout()
        TopBar.setContentsMargins(0,0,0,0)
        Back = QPushButton('')
        Back.setMinimumHeight(45)
        Back.setMinimumWidth(45)
        Back.setStyleSheet("QPushButton{background-color: black;\n color: black;\n border: 1px solid black;\n border-radius:25px;\n padding:10px;\n image: url(Back.png);\n}"
                            "QPushButton::hover{background-color : #31034a;}\n")
        Back.clicked.connect(lambda: self.close())
        TopBar.addWidget(Back)
        TopBar.addStretch()
        tempBox = QGroupBox()
        tempBox.setContentsMargins(0,0,0,0)
        tempBox.setMaximumHeight(45)
        tempBox.setMaximumWidth(45)
        tempBox.setStyleSheet("background-color: black;\n" "padding:0px;\n"+self.NoBoderStyleSheet)
        tempBox.setLayout(TopBar)
        return tempBox
    
    def InitUI(self):
        Layout = QVBoxLayout()
        Layout.setContentsMargins(10,10,10,10)
        Layout.setSpacing(5)
        TopBar = self.InitTopBar()
        
        self.Title = QLineEdit()
        self.Title.setFont(QFont('Open Sans',15))
        self.Title.setStyleSheet("background-color: grey;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:15px;\n\n}")
        self.Title.setMinimumHeight(50)        
        self.Title.setMinimumWidth(400)
        self.Title.setPlaceholderText('Enter Title')
        Layout.addWidget(self.Title)

        self.Date = QLineEdit()
        self.Date.setFont(QFont('Open Sans',15))
        self.Date.setStyleSheet("background-color: grey;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:15px;\n\n}")
        self.Date.setMinimumHeight(50)
        self.Date.setMinimumWidth(400)
        self.Date.setPlaceholderText('Enter Date')
        Layout.addWidget(self.Date)
        
        self.StartTime = QLineEdit()
        self.StartTime.setFont(QFont('Open Sans',15))
        self.StartTime.setStyleSheet("background-color: grey;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:15px;\n\n}")
        self.StartTime.setMinimumHeight(50)
        self.StartTime.setMinimumWidth(400)
        self.StartTime.setPlaceholderText('Enter Start Time')
        Layout.addWidget(self.StartTime)
        
        self.EndTime = QLineEdit()
        self.EndTime.setFont(QFont('Open Sans',15))
        self.EndTime.setStyleSheet("background-color: grey;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:15px;\n\n}")
        self.EndTime.setMinimumHeight(50)
        self.EndTime.setMinimumWidth(400)
        self.EndTime.setPlaceholderText('Enter End Time')
        Layout.addWidget(self.EndTime)
        

        addReminder = QPushButton('Add')
        addReminder.setStyleSheet("QPushButton{background-color: #52057b;\n color: White;\n border: 1px solid #52057b;\n border-radius:25px;\n padding:10px;\n }"
                            "QPushButton::hover{background-color : #31034a;}\n")
        addReminder.setMinimumHeight(50)
        addReminder.setMinimumWidth(400)
        addReminder.clicked.connect(self.AppendReminder)
        Layout.addWidget(addReminder)
        tempBox = QGroupBox()
        
        
        tempBox.setStyleSheet("background-color: Black;\n" "padding:0px;\n"+self.NoBoderStyleSheet)
        tempBox.setLayout(Layout)
        
        templayout = QVBoxLayout()
        templayout.setContentsMargins(0, 0, 0, 10)
        templayout.setSpacing(0)
        templayout.addWidget(TopBar)
        templayout.addWidget(tempBox)
        return templayout
    
    def printTest(self):
        print('test')
        
    def InitWindow(self):
        self.setWindowTitle(self.title)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setWindowFlags(flags)



    

