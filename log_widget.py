from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["Zaman", "Nem (%)", "Sıcaklık (°C)"])
        self.log_table.horizontalHeader().setFont(QFont('Arial', 12))
        self.layout.addWidget(self.log_table)

    def update_data(self, temperature, humidity):
        # Log data
        row_position = self.log_table.rowCount()
        self.log_table.insertRow(row_position)
        self.log_table.setItem(row_position, 0, QTableWidgetItem("Current Time"))  # Replace with actual time value
        self.log_table.setItem(row_position, 1, QTableWidgetItem(f"{humidity:.2f}"))
        self.log_table.setItem(row_position, 2, QTableWidgetItem(f"{temperature:.2f}"))
