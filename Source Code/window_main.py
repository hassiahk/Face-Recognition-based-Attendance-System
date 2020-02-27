import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from .window_registration import Registration
from .window_attendance import Attendance


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self._registration_window = None
        self._attendance_window = None
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Automated Attendance System")
        self.setWindowIcon(QtGui.QIcon('/home/hassi_ahk/Project/C-DAC_logo.png'))

        # Heading
        heading = QtWidgets.QLabel(self)
        heading.setAlignment(QtCore.Qt.AlignCenter)
        heading.setGeometry(QtCore.QRect(100, 30, 600, 60))
        heading.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        heading.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        heading.setText("AUTOMATED ATTENDANCE SYSTEM")

        # Button for opening the Registration window
        registration_button = QtWidgets.QPushButton(self)
        registration_button.setText("REGISTRATION")
        registration_button.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        registration_button.setGeometry(450, 200, 200, 50)
        registration_button.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        registration_button.clicked.connect(self.create_registration_window)

        # Button for opening the Attendance window
        attendance_button = QtWidgets.QPushButton(self)
        attendance_button.setText("ATTENDANCE")
        attendance_button.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        attendance_button.setGeometry(450, 350, 200, 50)
        attendance_button.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        attendance_button.clicked.connect(self.create_attendance_window)

        # Label for displaying the Logo
        pic = QtWidgets.QLabel(self)
        pic.setGeometry(80, 150, 300, 350)
        pic.setPixmap(QtGui.QPixmap("/home/hassi_ahk/Project/C-DAC_logo.png"))

    def create_registration_window(self):
        # Function for creating an instance of Registration Window
        self._registration_window = Registration()
        self._registration_window.show()

    def create_attendance_window(self):
        # Function for creating an instance of Attendance Window
        self._attendance_window = Attendance()
        self._attendance_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
