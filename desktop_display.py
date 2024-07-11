import sys
import subprocess
import random
import time
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QStackedWidget, QTableWidgetItem, QLineEdit, QLabel, QTableWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon
from realtime_widget import RealtimeWidget
from personel_bilgi import LogWidget

class DataLogger:
    def __init__(self):
        self.conn = sqlite3.connect(r'C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\terminal_data.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT NOT NULL,
                            temperature REAL NOT NULL,
                            humidity REAL NOT NULL
                          )''')
        self.conn.commit()

    def update_and_log_data(self, temperature, humidity):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO sensor_data (timestamp, temperature, humidity) VALUES (?, ?, ?)',
                       (timestamp, temperature, humidity))
        self.conn.commit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ESP8266 AWS IoT Data Visualization")
        self.setGeometry(100, 100, 1200, 800)

        self.setWindowIcon(QIcon(r"C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\images\morya.ico"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #121212; color: white;")

        self.top_menu = QHBoxLayout()
        self.top_menu.setSpacing(20)
        self.top_menu.setAlignment(Qt.AlignTop)

        self.btn_realtime = QPushButton("Anlık Veriler")
        self.btn_realtime.setCheckable(True)
        self.btn_realtime.setChecked(True)
        self.btn_realtime.setFont(QFont('Arial', 14))
        self.btn_realtime.setStyleSheet("background-color: #555; color: white; padding: 10px; border: none;")
        self.btn_realtime.clicked.connect(lambda: self.display(0))
        self.top_menu.addWidget(self.btn_realtime)

        self.btn_logs = QPushButton("Personel Bilgi Sistemi")
        self.btn_logs.setCheckable(True)
        self.btn_logs.setFont(QFont('Arial', 14))
        self.btn_logs.setStyleSheet("background-color: #555; color: white; padding: 10px; border: none;")
        self.btn_logs.clicked.connect(lambda: self.display(1))
        self.top_menu.addWidget(self.btn_logs)

        self.main_layout.addLayout(self.top_menu)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.realtime_widget = RealtimeWidget()
        self.stacked_widget.addWidget(self.realtime_widget)

        self.log_widget = LogWidget()
        self.stacked_widget.addWidget(self.log_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        self.logger = DataLogger()  # Veritabanı ile logger oluştur

    def update_data(self):
        humidity = random.uniform(30.0, 70.0)  # Simulated humidity value
        temperature = random.uniform(-10.0, 20.0)  # Simulated temperature value

        self.realtime_widget.update_data(temperature, humidity)
        self.log_widget.update_data(temperature, humidity)

        self.logger.update_and_log_data(temperature, humidity)  # Veriyi logla

    def display(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_realtime.setChecked(index == 0)
        self.btn_logs.setChecked(index == 1)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # terminal.py dosyasını başlat
    subprocess.Popen(['python', r'C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\terminal.py'])

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
