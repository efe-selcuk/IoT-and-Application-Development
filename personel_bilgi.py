import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel, QDateEdit, QTimeEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.db_conn = sqlite3.connect(r'C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\SQL\personel_bilgi.db')
        self.create_table()  # Veritabanında tablo oluştur

        self.init_ui()

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS personel_bilgileri (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ad_soyad TEXT NOT NULL,
                            mudahale_tarihi TEXT NOT NULL,
                            mudahale_saati TEXT NOT NULL,
                            durum TEXT NOT NULL,
                            timestamp TEXT NOT NULL
                          )''')
        self.db_conn.commit()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLineEdit, QDateEdit, QTimeEdit {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 16px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: 1px solid #555555;
                padding: 10px;
                font-size: 16px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
            QTableWidget {
                background-color: #3d3d3d;
                border: 1px solid #555555;
                color: #ffffff;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4d4d4d;
                border: 1px solid #555555;
                padding: 5px;
                font-size: 14px;
                color: #ffffff;
            }
        """)

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
        self.date_input.setDate(QDateTime.currentDateTime().date())
        self.input_layout.addWidget(self.date_input)

        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm:ss")
        self.time_input.setTime(QDateTime.currentDateTime().time())
        self.input_layout.addWidget(self.time_input)

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Durum")
        self.input_layout.addWidget(self.status_input)

        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_entry)
        self.input_layout.addWidget(self.add_button)

        self.layout.addLayout(self.input_layout)

        # Log table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(5)
        self.log_table.setHorizontalHeaderLabels(["ID", "Adı Soyadı", "Müdahale Tarihi", "Müdahale Saati", "Durum", "Zaman"])
        self.log_table.horizontalHeader().setFont(QFont('Arial', 12))
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.log_table)

        # Load existing entries from database
        self.load_entries()

    def add_entry(self):
        name = self.name_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm:ss")
        status = self.status_input.text()
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        cursor = self.db_conn.cursor()
        cursor.execute('''INSERT INTO personel_bilgileri (ad_soyad, mudahale_tarihi, mudahale_saati, durum, timestamp)
                          VALUES (?, ?, ?, ?, ?)''', (name, date, time, status, timestamp))
        self.db_conn.commit()

        self.load_entries()  # Reload entries after adding new one

        # Clear the input fields
        self.name_input.clear()
        self.status_input.clear()

    def load_entries(self):
        self.log_table.clearContents()
        self.log_table.setRowCount(0)

        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM personel_bilgileri''')
        entries = cursor.fetchall()

        for row_num, row_data in enumerate(entries):
            self.log_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.log_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def update_data(self, temperature, humidity):
        pass  # No data update needed for this widget
