from datetime import datetime

class FileUtil:
  
    def saveRemindersToFile(self, ReminderTitle, Date ,StartTime, EndTime):
        reminder = ReminderTitle+ ';' + Date+';'+ StartTime+';' +  EndTime+ '\n' 
        with open('reminder.r','a') as reminderfile:
            reminderfile.write(reminder)
            reminderfile.close()
          
    def sortReminder(self):
        #TODO
       pass

    def deleteReminder(self,Index):
        with open("reminder.r", "r+") as f:
            lines = f.readlines()
            del lines[Index-1] 
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            
    def loadRemindersFromFile(self):
        noOfReminders = 0
        with open('reminder.r','r') as reminderfile:
            reminderfile.seek(0)
            first_char = reminderfile.read(1)
            if not first_char:
                print ("file is empty")
                return 0,0
            else:
                reminderfile.seek(0)
                r= reminderfile.readlines()
                for lines in r:
                    noOfReminders = noOfReminders + 1
                return r, noOfReminders
            reminderfile.close()
            



