import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QStackedWidget, QSizePolicy, QFrame, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import pyqtgraph as pg
import random
from realtime_widget import RealtimeWidget
from log_widget import LogWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ESP8266 AWS IoT Data Visualization")
        self.setGeometry(100, 100, 1200, 800)

        # Set window icon
        self.setWindowIcon(QIcon(r"C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\images\morya.ico"))

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #121212; color: white;")  # Black theme

        # Top menu
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

        self.btn_logs = QPushButton("Geçmiş Veriler")
        self.btn_logs.setCheckable(True)
        self.btn_logs.setFont(QFont('Arial', 14))
        self.btn_logs.setStyleSheet("background-color: #555; color: white; padding: 10px; border: none;")
        self.btn_logs.clicked.connect(lambda: self.display(1))
        self.top_menu.addWidget(self.btn_logs)

        self.main_layout.addLayout(self.top_menu)

        # Stacked widget for content
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Real-time data widget
        self.realtime_widget = RealtimeWidget()
        self.stacked_widget.addWidget(self.realtime_widget)

        # Log data widget
        self.log_widget = LogWidget()
        self.stacked_widget.addWidget(self.log_widget)

        # Timer for updating data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update data every second

    def update_data(self):
        # Simulate receiving data
        humidity = random.uniform(30.0, 70.0)  # Simulated humidity value
        temperature = random.uniform(-10.0, 20.0)  # Simulated temperature value

        # Update widgets
        self.realtime_widget.update_data(temperature, humidity)
        self.log_widget.update_data(temperature, humidity)

    def display(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_realtime.setChecked(index == 0)
        self.btn_logs.setChecked(index == 1)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
