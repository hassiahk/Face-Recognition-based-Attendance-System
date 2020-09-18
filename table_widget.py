import sqlite3
import sys
from PyQt5 import QtWidgets


class Table(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tableWidget = QtWidgets.QTableWidget()
        self.title = 'Attendance for all Students'
        self.left = 400
        self.top = 150
        self.width = 600
        self.height = 300
        self.initUI()

    def initUI(self):
        # Function for showing the widget
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def create_table(self):
        # Function for creating table a table widget
        connection = sqlite3.connect("/home/hassi_ahk/Project/Attendance_System.db")

        cursor = connection.cursor()
        cursor.execute("select distinct(date) from attendance")
        temp1 = cursor.fetchall()

        cursor.execute("select distinct(roll) from attendance")
        temp2 = cursor.fetchall()

        distinct_dates = []
        distinct_rolls = []

        for i in temp1:
            distinct_dates.append(i[0])
        distinct_dates.sort(key=lambda x: x)

        for j in temp2:
            distinct_rolls.append(j[0])
        distinct_rolls.sort(key=lambda x: x)

        header_labels = ['Roll No']
        header_labels.extend(distinct_dates)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(header_labels))

        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        count = 0

        # Inserting the values into the table widget
        for row_number, roll in enumerate(distinct_rolls):
            self.tableWidget.insertRow(row_number)
            self.tableWidget.setItem(row_number, count, QtWidgets.QTableWidgetItem(str(roll)))

        for i in distinct_dates:
            attend = []
            count += 1
            for j in distinct_rolls:
                cursor.execute("select attendance from attendance where roll = ? and date = ?", (j, i))
                attend.append(cursor.fetchall()[0][0])

            for row_number, att in enumerate(attend):
                self.tableWidget.setItem(row_number, count, QtWidgets.QTableWidgetItem(str(att)))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Table()
    sys.exit(app.exec_())
