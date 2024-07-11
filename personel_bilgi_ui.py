from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel, QDateEdit, QTimeEdit, QWidget, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate, QTime

class LogWidgetUI(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Title label
        self.title_label = QLabel("Personel Bilgi Sistemi")
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Input layout
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Adı Soyadı")
        self.input_layout.addWidget(self.name_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(self.get_current_date())
        self.input_layout.addWidget(self.date_input)

        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm:ss")
        self.time_input.setTime(self.get_current_time())
        self.input_layout.addWidget(self.time_input)

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Durum")
        self.input_layout.addWidget(self.status_input)

        self.terminal_input = QComboBox()
        self.populate_terminals()
        self.input_layout.addWidget(self.terminal_input)

        self.add_button = QPushButton("Ekle")
        self.input_layout.addWidget(self.add_button)

        self.layout.addLayout(self.input_layout)

        # Log table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(7)  # ID sütunu eklenmiş durumda
        self.log_table.setHorizontalHeaderLabels(["ID", "Adı Soyadı", "Müdahale Tarihi", "Müdahale Saati", "Durum", "Zaman", "Terminal"])
        self.log_table.horizontalHeader().setFont(QFont('Arial', 12))
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.log_table)

    def get_current_date(self):
        return QDate.currentDate()

    def get_current_time(self):
        return QTime.currentTime()

    def populate_terminals(self):
        # Örnek olarak 30 terminal ekliyoruz
        for i in range(1, 31):
            self.terminal_input.addItem(f"Terminal {i}")
