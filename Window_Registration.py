import os
import cv2
import sqlite3
import face_recognition
import sys
from datetime import datetime
from PyQt5 import QtGui, QtCore, QtWidgets
from face_recognition.face_recognition_cli import image_files_in_folder

class Registration(QtWidgets.QMainWindow):
    #Registration window for student registration
      
    def __init__(self):
        super(Registration, self).__init__()
        
        # Creating Window for Registration
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Registration")
        self.setWindowIcon(QtGui.QIcon('/home/hassi_ahk/Project/C-DAC_logo.png'))

        # Heading
        heading = QtWidgets.QLabel(self)
        heading.setAlignment(QtCore.Qt.AlignCenter)
        heading.setGeometry(QtCore.QRect(100, 30, 600, 60))
        heading.setStyleSheet("QLabel {background-color : blue; color :white;}")
        heading.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        heading.setText("REGISTRATION")

        # Default photo to display
        self.pic = QtWidgets.QLabel(self)
        self.pic.setGeometry(50, 120, 320, 320)
        self.pic.setPixmap(QtGui.QPixmap('/home/hassi_ahk/Project/default.png'))

        # Button for opening Webcam and take photo 
        click = QtWidgets.QPushButton(self)
        click.setText('CAPTURE')
        click.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        click.setGeometry(100, 420, 100, 30)
        click.clicked.connect(self.take_photo)

        # SET OF ENTRIES
        # Taking Student's Name
        label_name = QtWidgets.QLabel(self)
        label_name.setAlignment(QtCore.Qt.AlignCenter)
        label_name.setGeometry(QtCore.QRect(310, 150, 130, 30))
        label_name.setStyleSheet("QLabel {background-color : gray; color :black;}")
        label_name.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        label_name.setText('NAME')

        self.e1 = QtWidgets.QLineEdit(self)
        self.e1.setGeometry(450, 150, 300, 30)
        self.e1.setAlignment(QtCore.Qt.AlignCenter)

        self.e1.setFont(QtGui.QFont("Arial", 14))

        # Taking Student's Registration Number
        label_roll = QtWidgets.QLabel(self)
        label_roll.setAlignment(QtCore.Qt.AlignCenter)
        label_roll.setGeometry(QtCore.QRect(310, 250, 130, 30))
        label_roll.setStyleSheet("QLabel {background-color : gray; color :black;}")
        label_roll.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        label_roll.setText("ROLL NO")

        self.e2 = QtWidgets.QLineEdit(self)
        self.e2.setGeometry(450, 250, 300, 30)
        self.e2.setAlignment(QtCore.Qt.AlignCenter)
        self.e2.setFont(QtGui.QFont("Arial", 14))


        # Button for clearing fields 
        reset = QtWidgets.QPushButton(self)
        reset.setText("RESET")
        reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        reset.setGeometry(650, 450, 100, 30)
        reset.setStyleSheet("QPushButton {background-color : red ; color : white;}")
        self.entries = [self.e1, self.e2]
        reset.clicked.connect(self.erase)

        # Label for displaying message
        self.message = QtWidgets.QLabel(self)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setGeometry(QtCore.QRect(40, 500, 250, 30))
        self.message.setStyleSheet("QLabel {  color:red ; }")
        self.message.setFont(QtGui.QFont('Times', 13, QtGui.QFont.Bold))
        
        # Button for submission of data and storing in database 
        submit = QtWidgets.QPushButton(self)
        submit.setText("SUBMIT")
        submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        submit.setGeometry(520, 450, 100, 30)
        submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        submit.clicked.connect(self.store_in_database)
        
        # Button for closing the window
        back = QtWidgets.QPushButton(self)
        back.setText("BACK")
        back.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        back.setGeometry(390, 450, 100, 30)
        back.setStyleSheet("QPushButton { background-color : black ;color : white ; }")
        back.clicked.connect(self.create_main_window)
        
        self.year = datetime.now().date().year
        
    def erase(self):
    # Function for clearing fields and changing to default
        for entry in self.entries:
            entry.clear()
        self.pic.setPixmap(QtGui.QPixmap("/home/hassi_ahk/Project/default.png"))
        self.message.setText("")
    
    def take_photo(self):
    # Function for clicking, displaying and storing photo
        check_value = self.check()
        if (check_value == 1):
            self.message.setText("Invalid Name")
        elif (check_value == 2):
            self.message.setText("Roll - Out of Range")
        else:
            cap = cv2.VideoCapture(0)
            frame_number = 0
            path = '/home/hassi_ahk/Project/Reg_Images'

            if not os.path.exists(os.path.join(path, str(self.e2.text()))):
                os.makedirs(os.path.join(path, str(self.e2.text())))
            
            while True:
                ret, frame = cap.read()
                frame_number += 1
                rgb_frame = frame[:, :, ::-1]
                
                face_locations = face_recognition.face_locations(rgb_frame, model='cnn')
                
                for (top, right, bottom, left) in face_locations:
                    cv2.imwrite(os.path.join(os.path.join(path, str(self.e2.text())), str(self.e1.text()) + '_' + str(self.e2.text()) + '_' + str(frame_number) + '.jpg'), 
                                frame[top - 10 : bottom + 10, left - 6 : right + 6],
                                        [int(cv2.IMWRITE_JPEG_QUALITY), 1000000])
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.waitKey(200)
                    
                cv2.imshow('Image', frame)
                cv2.waitKey(1)
                
                if frame_number > 10:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.pic.setPixmap(QtGui.QPixmap(os.path.join(os.path.join(path, str(self.e2.text())), str(self.e1.text()) + '_' + str(self.e2.text()) + '_' + str(frame_number) + '.jpg')))

    def store_in_database(self):
    # Function for storing information in database
        check_value = self.check()
        print ('>>', check_value)
        if (check_value == 0):
            try:
                connection = sqlite3.connect('/home/hassi_ahk/Project/Attendance_System.db')
                cursor = connection.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS STUDENT (name TEXT NOT NULL, roll TEXT UNIQUE, year TEXT NOT NULL)')
                cursor.execute('INSERT INTO STUDENT (name, roll, year) VALUES(?, ?, ?)', (str(self.e1.text()), str(self.e2.text()), str(self.year)))
                connection.commit()
                cursor.close()
                connection.close()
                # Displaying message after successful submission 
                self.message.setText("Successfully Registered")
            except:
                self.message.setText("Already Registered")
        elif (check_value == 1):
            self.message.setText("Invalid Name")
        elif (check_value == 2):
            self.message.setText("Roll - Out of Range")
        elif (check_value == 4):
            self.message.setText("Click Capture again please.")
            

    def check(self):
    # Function to check validations
        path = '/home/hassi_ahk/Project/Reg_Images'
        name = str(self.e1.text())
        if (len(name) == 0):
            return 1
        
        for i in range(10):
            if (str(i) in name):
                return 1
        
        try:
            roll = int(self.e2.text())
            if (roll < 1 or roll > 100):
                return 2
        except:
            return 2
            
        try:
            for img_path in image_files_in_folder(os.path.join(path, str(self.e2.text()))):
                img = face_recognition.load_image_file(img_path)
                face_locations = face_recognition.face_locations(img, model='cnn')
                
                if face_locations != 1:
                    continue
                else:
                    break
                
            print (len(face_locations), 'face(s) detected')
            if (len(face_locations) != 1):
                return 4
        except:
            return 4
        
        return 0
    
    def create_main_window(self):
    # Function to close the registration window
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Registration()
    gui.show()
    sys.exit(app.exec_())