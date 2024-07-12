import sys
import subprocess
import random
import time
import sqlite3
import os
import requests  # Bu kütüphaneyi import edin

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QStackedWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon
from realtime_widget import RealtimeWidget  # Bu widget için uygun import
from personel_bilgi import LogWidget  # Bu widget için uygun import

class DataLogger:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), 'SQL', 'terminal_data.db')
        self.conn = sqlite3.connect(db_path)
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

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images', 'morya.ico')))

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

        self.realtime_widget = RealtimeWidget()  # RealtimeWidget yerine kullanacağınız uygun widgeti ekleyin
        self.stacked_widget.addWidget(self.realtime_widget)

        self.log_widget = LogWidget()  # LogWidget yerine kullanacağınız uygun widgeti ekleyin
        self.stacked_widget.addWidget(self.log_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

        self.logger = DataLogger()  # Veritabanı ile logger oluştur

    def update_data(self):
        api_key = 'ZSDSMNPHJP1I435Z'  # Thingspeak API anahtarınızı buraya ekleyin
        channel_id = '2597068'  # Thingspeak kanal ID'nizi buraya ekleyin
        results = 1  # Alınacak son besleme sayısı

        url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results={results}'

        try:
            response = requests.get(url)
            data = response.json()

            if 'feeds' in data:
                latest_feed = data['feeds'][0]
                temperature = float(latest_feed.get('field1', '0.0'))
                humidity = float(latest_feed.get('field2', '0.0'))

                self.realtime_widget.update_data(temperature, humidity)  # RealtimeWidget'iniz için uygun metod adını ve parametreleri kullanın
                self.log_widget.update_data(temperature, humidity)  # LogWidget'iniz için uygun metod adını ve parametreleri kullanın

                self.logger.update_and_log_data(temperature, humidity)  # Veriyi logla

        except requests.exceptions.RequestException as e:
            print(f'Hata oluştu: {e}')

    def display(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_realtime.setChecked(index == 0)
        self.btn_logs.setChecked(index == 1)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # terminal.py dosyasını başlat
    terminal_path = os.path.join(os.path.dirname(__file__), 'terminal.py')
    subprocess.Popen(['python', terminal_path])

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
