import cv2
import os
import sqlite3
import face_recognition
import shutil
import sys
from face_recognition.face_recognition_cli import image_files_in_folder
from datetime import datetime

from Widget_Table import Table
from PyQt5 import QtGui, QtCore, QtWidgets



X = []
y = []

class Attendance(QtWidgets.QMainWindow):
    # Attendance Window
    def __init__(self):
        super(Attendance, self).__init__()
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('/home/hassi_ahk/Project/C-DAC_logo.png'))

        # Heading
        heading = QtWidgets.QLabel(self)
        heading.setAlignment(QtCore.Qt.AlignCenter)
        heading.setGeometry(QtCore.QRect(200,20,400,50))
        heading.setStyleSheet("QLabel {background-color : blue; color :white;}")
        heading.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold))
        heading.setText("ATTENDANCE")

        # Button for marking the attendance for the day
        mark_attendance = QtWidgets.QPushButton(self)
        mark_attendance.setText("MARK ATTENDANCE")
        mark_attendance.setStyleSheet("QPushButton { background-color : gray;color : black ; }")
        mark_attendance.setFont(QtGui.QFont('Times', 16, QtGui.QFont.Bold))
        mark_attendance.setGeometry(250, 300, 300, 50)
        mark_attendance.clicked.connect(self.mark)

        # Button for checking the attendance
        check_attendance = QtWidgets.QPushButton(self)
        check_attendance.setText("CHECK ATTENDANCE")
        check_attendance.setStyleSheet("QPushButton { background-color : gray;color : black ; }")
        check_attendance.setFont(QtGui.QFont('Times', 16, QtGui.QFont.Bold))
        check_attendance.setGeometry(250, 150, 300, 50)
        check_attendance.clicked.connect(self.create_check_attendance)
        
        # Button for closing the attendance window
        back = QtWidgets.QPushButton(self)
        back.setText("BACK")
        back.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        back.setGeometry(150, 450, 100, 30)
        back.setStyleSheet("QPushButton { background-color : black ;color : white ; }")
        back.clicked.connect(self.create_main_window)
        
    def create_check_attendance(self):
    # Function for creating an instance of the table widget
        self._check_attendance = Table()
        self._check_attendance.show()
    
    def mark(self):
        self.get_frames() # to get frames from the recorded video
        self.extract_faces() # to read all faces from the frames
        self.match() # match extracted faces to those in database and update the database

    def get_frames(self):
        path = '/home/hassi_ahk/Project/Temp'
        count = 0
        
        print("Getting frames\n")
        
        try:
            if os.path.exists(path):
                os.removedirs(path)
        except OSError:
            shutil.rmtree(path)
        if not os.path.exists(path):
            os.makedirs(path)
        
        cap = cv2.VideoCapture('/home/hassi_ahk/Project/Videos/VID_20190130_134928.mp4') # video file path
        while True:
            ret, frame = cap.read()
            cap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
            
            if ret :
                cv2.imwrite(path + "/frame {}.jpg" .format(count), frame)     # save frame as JPEG file
                count += 1
            else:
                break
        print("Getting frames, Done!\n")
        
    def extract_faces(self):
        faces_dir = '/home/hassi_ahk/Project/Reg_Images'
        
        print("Extracting faces\n")
        
        for labels in os.listdir(faces_dir):  
            if not os.path.isdir(os.path.join(faces_dir, labels)):
                continue
                
            for img_path in image_files_in_folder(os.path.join(faces_dir, labels)):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image, model='hog')
                
                if len(face_bounding_boxes) != 1:
                    continue
                else:
                    # Appending the face encodings in to a List
                    X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    y.append(labels)
                    
        print("Extracted faces\n")
        
    def match(self):
        path = '/home/hassi_ahk/Project/Temp'
        face_names = []
        present = {}
        
        print("Matching the extracted faces with known faces")
        
        for img_path in image_files_in_folder(path):
            image = face_recognition.load_image_file(img_path)
            face_locations = face_recognition.face_locations(image, model='hog')
            face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(X, face_encoding, tolerance=0.60)
                
                name = None
                
                if True in matches:
                    match_index = matches.index(True)
                    name = y[match_index]
                else:
                    continue
        
                face_names.append(name)
        
        for i in face_names:
            present[i] = 'Present'
        
        connection = sqlite3.connect('/home/hassi_ahk/Project/Attendance_System.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * from STUDENT")
        
        roll_nos = []
        attendance = []
        
        for each_row in cursor.fetchall():
            roll_nos.append(each_row[1])
            
        for i in roll_nos:
            if i in present:
                attendance.append('P')
            else:
                attendance.append('A')
        
        day = datetime.now().date().day
        month = datetime.now().date().month
        year = datetime.now().date().year
        
        date = str(day) + '-' + str(month) + '-' + str(year)
        
        cursor.execute("CREATE TABLE IF NOT EXISTS attendance (roll TEXT NOT NULL, attendance TEXT NOT NULL, date TEXT NOT NULL)")
        for roll, attend in zip(roll_nos, attendance):
            cursor.execute("INSERT INTO attendance (roll, attendance, date) VALUES (?, ?, ?)", (roll, attend, date))
            connection.commit()
        
        cursor.close()
        connection.close()
        
        print("Updated the database")
        
    def create_main_window(self):
    # Function for closing the attendance window
        self.close()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Attendance()
    gui.show()
    sys.exit(app.exec_())
