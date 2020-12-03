from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QScrollArea, QGroupBox, QWidget, QFormLayout, \
    QLabel, QLineEdit, QHBoxLayout, QBoxLayout, QSizePolicy,QStackedWidget ,QVBoxLayout,QGridLayout,QCheckBox,QMessageBox
from PyQt5 import QtCore,Qt
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound
from AddReminder import AddReminderWindow
from FileUtils import FileUtil
import threading
import time as Time
from datetime import datetime
import sys
import sip

    
class Window(QWidget):
    reminderevent = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.w = None
        self.title ='Reminder'
        self.left = 500
        self.top = 200
        self.width_ = 600
        self.height = 800
        self.setStyleSheet("background-color: black;\n" "padding:0px;\n" "spacing:0px;\n")

        self.InitWindow()
        self.NoBoderStyleSheet = ("border :0px;\n")
        layout = self.LoadLayout()
        addReminder = QPushButton('Add')
        addReminder.setStyleSheet("QPushButton{background-color: #52057b;\n color: White;\n border: 1px solid #52057b;\n border-radius:25px;\n padding:10px;\nspacing :10px; }"
                            "QPushButton::hover{background-color : #31034a;}\n")
        addReminder.setMinimumHeight(50)
        addReminder.setFont(QFont('Open Sans',15))
        addReminder.clicked.connect(self.showAddReminderWindow)
        layout.addWidget(addReminder)
        self.setLayout(layout)
        self.reminderevent.connect(self.showAlertWindow)
        t = threading.Thread(target = self.showAlert)
        t.deamon =True
        t.start()
        
    def mousePressEvent(self, event):
        if event.button() == 1:
            self.isMouseButtonDown = True
            self.oldPos = event.globalPos()


    def mouseReleaseEvent(self, event):
            self.isMouseButtonDown = False

    def mouseMoveEvent(self, event):
        if self.isMouseButtonDown == True:
             delta =  (event.globalPos() - self.oldPos)
            #print(delta)
             self.move(self.x() + delta.x(), self.y() + delta.y())
             self.oldPos = event.globalPos()

    def showAlertWindow(self,amsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Pending Task")
        msg.setInformativeText(amsg)
        msg.setWindowTitle("Task Alert")
        msg.exec_()

    def showAlert(self):
        file = FileUtil()
        today = datetime.today()
        time = datetime.now()
        systime = time.strftime("%H:%M")
        print(systime)
        sysdate =today.strftime("%d-%m-%Y")
        reminders ,count= FileUtil.loadRemindersFromFile(file)
        for reminder in reminders:
            r = reminder.split(';')        
            if r[1] == sysdate:
                if r[2] == systime:
                    self.reminderevent.emit(r[0])
                    
        Time.sleep(60)
        
    def showAddReminderWindow(self, checked):
        if self.w is None:
            self.w = AddReminderWindow()
            
        #self.w.setWindowModality(Qt.WindowModal)
        self.w.show()        
        self.w.Update.connect(self.UpdateReminders)
        #self.UpdateReminders()
        
    def Close(self):
        self.close()
        self.w.close()
        
    def DoneWithReminder(self,button):
        index = self.reminderContainer.indexOf(button.parent())
        print(index)
        file = FileUtil()
        FileUtil.deleteReminder(self,index)
        button.parent().deleteLater()
        
    def upperFrame(self):
        frame = QHBoxLayout()
        frame.setContentsMargins(20,0, 0, 0)
        Title = QLabel(self.title)
        Title.setFont(QFont('Open Sans',15))
        Title.setStyleSheet('color:white;\n')
        frame.addWidget(Title)
        frame.setSpacing(0)
        Close = QPushButton('')
        Close.setMinimumHeight(45)
        Close.setMinimumWidth(45)
        Close.setStyleSheet("QPushButton{background-color: black;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:10px;\n image: url(X.png);\n}"
                            "QPushButton::hover{background-color : #31034a;}\n")
        Close.clicked.connect(lambda: self.close())
        
        Minimize = QPushButton('')
        Minimize.setStyleSheet("QPushButton{background-color: black;\n color: White;\n border: 1px solid black;\n border-radius:25px;\n padding:10px;\n image: url(Min.png);\n}"
                            "QPushButton::hover{background-color : #31034a;}\n")
        Minimize.clicked.connect(lambda: self.showMinimized())
        
        Minimize.setMinimumHeight(45)
        Minimize.setMinimumWidth(45)
        frame.addStretch()
        frame.addWidget(Minimize)
        frame.addWidget(Close)
        tempBox = QGroupBox()
        tempBox.setMaximumHeight(45)
        tempBox.setStyleSheet("background-color: black;\n" "padding:0px;\n"+self.NoBoderStyleSheet)
        tempBox.setLayout(frame)
        return tempBox
    
    def LoadLayout(self):
        ScrollBoxStyleSheet = ("""
        QScrollBar:vertical {              
        border: 0px solid #999999;
        background:white;
        width:5px;    
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background-color: gray ;
        min-height: 0px;
        border-radius:2px;
    }
    QScrollBar::add-line:vertical {
        background-color: white;
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        background-color:white;
        height: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    } 
    QScrollArea
       {
        border :0px;
       }""")
        root = QStackedWidget(self)
        reminders ,count= FileUtil.loadRemindersFromFile(self)

        self.reminderContainer = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(ScrollBoxStyleSheet)
        reminderGroupBox = QGroupBox()        
        self.reminderContainer.addStretch()
        reminderGroupBox.setLayout(self.reminderContainer)
        scroll.setWidget(reminderGroupBox)
        if(count != 0):
            for reminder in  reminders:
                self.reminderContainer.addWidget(self.reminderUI(reminder))
        root.setStyleSheet("padding:0px;\n" + self.NoBoderStyleSheet)
        #root.addWidget(reminderGroupBox)        
        #rootBox = QGroupBox()
        #rootBox.setLayout(scroll)
        root.addWidget(scroll)        
        templayout = QGridLayout()
        templayout.setContentsMargins(0, 0, 0, 10)
        templayout.setSpacing(0)
        templayout.addWidget(self.upperFrame())
        templayout.addWidget(root)
        
        return templayout
    
    def UpdateReminders(self):
        while self.reminderContainer.count():
            child = self.reminderContainer.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.reminderContainer.addStretch()
        reminders ,count= FileUtil.loadRemindersFromFile(self)
        for reminder in  reminders:
            self.reminderContainer.addWidget(self.reminderUI(reminder))
    
    def reminderUI(self, reminder):
        reminderList = reminder.split(';',4)
        reminderTitle = QLabel(reminderList[0])
        reminderDate = QLabel(reminderList[1])
        reminderStartTime = QLabel(reminderList[2])
        reminderEndTime = QLabel(reminderList[3])

        reminderTitle.setFont(QFont('Open Sans',15)) 
        reminderDate.setFont(QFont('Open Sans',15)) 
        reminderStartTime.setFont(QFont('Open Sans',15))
        reminderEndTime.setFont(QFont('Open Sans',15))
        
        reminderBox = QVBoxLayout()
        reminderBox.addWidget(reminderTitle)
        reminderBox.addWidget(reminderDate)
        reminderBox.addWidget(reminderStartTime)
        reminderBox.addWidget(reminderEndTime)
        reminderBox2 = QHBoxLayout()
        doneButton = QPushButton('Done')
        doneButton.setStyleSheet(
            "background-color: White;\n" "border: 1px solid white;\n" "border-radius:25px;\n" "padding:10px;\n""color: Black;\n" )
        doneButton.setMinimumHeight(50)
        doneButton.setMaximumWidth(100)
        doneButton.clicked.connect(lambda: self.DoneWithReminder(doneButton))
        temp = QGroupBox()
        temp.setStyleSheet(self.NoBoderStyleSheet)
        temp.setLayout(reminderBox)
        reminderBox2.addWidget(temp)
        reminderBox2.addWidget(doneButton)
        temp2 = QGroupBox()
        temp2.setMaximumHeight(150)
        temp2.setStyleSheet('border-radius:25px;\n'"background-color: #a40eda;\n""border: 1px solid #a40eda;\n""color: White;\n")
        temp2.setLayout(reminderBox2)
        return temp2        
        

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width_, self.height)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
