import sqlite3
import sys
from PyQt5 import QtWidgets


class Table(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.tableWidget = QtWidgets.QTableWidget()
        self.title = 'Attendance for all Students'
        self.left = 400
        self.top = 150
        self.width = 600
        self.height = 300
        self.init_ui()

    def init_ui(self):
        # Function for showing the widget
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_table_widget()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def create_table_widget(self):
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

        column = 0

        # Inserting the values into the table widget
        for row, roll in enumerate(distinct_rolls):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(roll)))

        for date in distinct_dates:
            attend = []
            column += 1
            for roll_number in distinct_rolls:
                cursor.execute("select attendance from attendance where roll = ? and date = ?", (roll_number, date))
                attend.append(cursor.fetchall()[0][0])

            for row, att in enumerate(attend):
                self.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(str(att)))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Table()
    sys.exit(app.exec_())
