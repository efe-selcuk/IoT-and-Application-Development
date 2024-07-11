import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidgetItem, QLineEdit, QPushButton, QLabel, QDateEdit, QTimeEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime

from personel_bilgi_ui import LogWidgetUI

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()

        db_path = os.path.join(os.path.dirname(__file__), 'SQL', 'personel_bilgi.db')
        self.db_conn = sqlite3.connect(db_path)
        self.create_table()  # Veritabanında tablo oluştur

        self.ui = LogWidgetUI()  # Tasarımı yükleyen UI nesnesi
        self.ui.add_button.clicked.connect(self.add_entry)  # Bağlantıları ayarla

        self.init_ui()

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS personel_bilgileri (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ad_soyad TEXT NOT NULL,
                            mudahale_tarihi TEXT NOT NULL,
                            mudahale_saati TEXT NOT NULL,
                            durum TEXT NOT NULL,
                            timestamp TEXT NOT NULL,
                            terminal TEXT NOT NULL
                          )''')
        self.db_conn.commit()

    def init_ui(self):
        self.setWindowTitle("Personel Bilgi Sistemi")
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
        self.layout.addWidget(self.ui)  # UI nesnesini ana layout'a ekle

        # Load existing entries from database
        self.load_entries()

    def add_entry(self):
        name = self.ui.name_input.text()
        date = self.ui.date_input.date().toString("yyyy-MM-dd")
        time = self.ui.time_input.time().toString("HH:mm:ss")
        status = self.ui.status_input.text()
        terminal = self.ui.terminal_input.currentText()
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        cursor = self.db_conn.cursor()
        cursor.execute('''INSERT INTO personel_bilgileri (ad_soyad, mudahale_tarihi, mudahale_saati, durum, timestamp, terminal)
                          VALUES (?, ?, ?, ?, ?, ?)''', (name, date, time, status, timestamp, terminal))
        self.db_conn.commit()

        self.load_entries()  # Yeni giriş ekledikten sonra kayıtları yeniden yükle

        # Giriş alanlarını temizle
        self.ui.name_input.clear()
        self.ui.status_input.clear()

    def load_entries(self):
        self.ui.log_table.clearContents()
        self.ui.log_table.setRowCount(0)

        cursor = self.db_conn.cursor()
        cursor.execute('''SELECT * FROM personel_bilgileri''')
        entries = cursor.fetchall()

        for row_num, row_data in enumerate(entries):
            self.ui.log_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.ui.log_table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def update_data(self, temperature, humidity):
        # Implement your update logic here
        pass  # Placeholder, replace with actual logic

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = LogWidget()
    widget.show()
    sys.exit(app.exec_())
