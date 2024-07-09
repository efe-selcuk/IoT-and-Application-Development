import sys
import socket
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QTabWidget, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QStackedWidget, QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap
import pyqtgraph as pg

class DataReceiver(QThread):
    data_received = pyqtSignal(dict)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('localhost', 10000))
        
        while True:
            data, _ = sock.recvfrom(4096)
            data = json.loads(data.decode())
            self.data_received.emit(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ESP8266 AWS IoT Data Visualization")
        self.setGeometry(100, 100, 1200, 800)

        # Set window icon
        self.setWindowIcon(QIcon('C:/Users/HP/OneDrive/Masaüstü/IoT and Application Development/morya.ico'))

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
        self.btn_realtime.setStyleSheet("background-color: #333; color: white; padding: 10px;")
        self.btn_realtime.clicked.connect(lambda: self.display(0))
        self.top_menu.addWidget(self.btn_realtime)
        
        self.btn_logs = QPushButton("Geçmiş Veriler")
        self.btn_logs.setCheckable(True)
        self.btn_logs.setFont(QFont('Arial', 14))
        self.btn_logs.setStyleSheet("background-color: #333; color: white; padding: 10px;")
        self.btn_logs.clicked.connect(lambda: self.display(1))
        self.top_menu.addWidget(self.btn_logs)

        self.main_layout.addLayout(self.top_menu)

        # Stacked widget for content
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Real-time data widget
        self.realtime_widget = QWidget()
        self.init_realtime_widget()
        self.stacked_widget.addWidget(self.realtime_widget)

        # Log data widget
        self.log_widget = QWidget()
        self.init_log_widget()
        self.stacked_widget.addWidget(self.log_widget)

        # Data for plotting and logging
        self.time_data = {}
        self.temp_data = {}
        self.hum_data = {}

        for fridge_id in range(1, 101):  # 100 fridges
            self.time_data[fridge_id] = []
            self.temp_data[fridge_id] = []
            self.hum_data[fridge_id] = []

        # Start data receiver thread
        self.data_receiver = DataReceiver()
        self.data_receiver.data_received.connect(self.update_data)
        self.data_receiver.start()

    def init_realtime_widget(self):
        self.realtime_layout = QVBoxLayout(self.realtime_widget)

        # Title label
        self.title_label = QLabel("ESP8266 AWS IoT Data Visualization")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setStyleSheet("color: white;")
        self.realtime_layout.addWidget(self.title_label)

        # Indicators layout
        self.indicators_layout = QHBoxLayout()

        # Humidity indicator
        self.humidity_frame = QFrame()
        self.humidity_frame.setFrameShape(QFrame.StyledPanel)
        self.humidity_frame.setStyleSheet("background-color: #333; border: 2px solid #555;")
        self.humidity_layout = QVBoxLayout(self.humidity_frame)
        self.humidity_label = QLabel("Nem: -- %")
        self.humidity_label.setFont(QFont('Arial', 20))
        self.humidity_label.setStyleSheet("color: white;")
        self.humidity_indicator = QLabel()
        self.humidity_layout.addWidget(self.humidity_label, alignment=Qt.AlignCenter)
        self.humidity_layout.addWidget(self.humidity_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.humidity_frame)
        
        # Temperature indicator
        self.temperature_frame = QFrame()
        self.temperature_frame.setFrameShape(QFrame.StyledPanel)
        self.temperature_frame.setStyleSheet("background-color: #333; border: 2px solid #555;")
        self.temperature_layout = QVBoxLayout(self.temperature_frame)
        self.temperature_label = QLabel("Sıcaklık: -- °C")
        self.temperature_label.setFont(QFont('Arial', 20))
        self.temperature_label.setStyleSheet("color: white;")
        self.temperature_indicator = QLabel()
        self.temperature_layout.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        self.temperature_layout.addWidget(self.temperature_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.temperature_frame)
        
        self.realtime_layout.addLayout(self.indicators_layout)

        # Plot widget for real-time data
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#121212')  # Dark background
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Customize axis labels
        styles = {'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'}
        self.plot_widget.getAxis('left').setLabel('Değer', **styles)
        self.plot_widget.getAxis('bottom').setLabel('Zaman', **styles)

        self.plot_widget.addLegend(offset=(50, 50), brush=(50, 50, 50, 150))  # Legend settings
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Grid settings
        
        # Enable only horizontal scrolling
        self.plot_widget.setMouseEnabled(x=True, y=False)

        self.realtime_layout.addWidget(self.plot_widget)

    def init_log_widget(self):
        self.log_layout = QVBoxLayout(self.log_widget)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels(["Depo ID", "Zaman", "Nem (%)", "Sıcaklık (°C)"])
        self.log_table.horizontalHeader().setStyleSheet("background-color: #333; color: white; font-size: 14pt;")
        self.log_layout.addWidget(self.log_table)

    def update_data(self, data):
        fridge_id = data['id']
        humidity = data['humidity']
        temperature = data['temperature']

        # Update indicators
        if len(self.hum_data[fridge_id]) > 0 and humidity > self.hum_data[fridge_id][-1]:
            self.humidity_indicator.setPixmap(QPixmap("arrow_up.png"))
        else:
            self.humidity_indicator.setPixmap(QPixmap("arrow_down.png"))

        if len(self.temp_data[fridge_id]) > 0 and temperature > self.temp_data[fridge_id][-1]:
            self.temperature_indicator.setPixmap(QPixmap("arrow_up.png"))
        else:
            self.temperature_indicator.setPixmap(QPixmap("arrow_down.png"))

        # Update labels
        self.humidity_label.setText(f"Nem: {humidity:.2f}%")
        self.temperature_label.setText(f"Sıcaklık: {temperature:.2f}°C")

        # Append data for plotting and logging
        current_time = len(self.time_data[fridge_id])
        self.time_data[fridge_id].append(current_time)
        self.temp_data[fridge_id].append(temperature)
        self.hum_data[fridge_id].append(humidity)

        # Update plots
        self.plot_widget.plot(self.time_data[fridge_id], self.temp_data[fridge_id], pen='r', name=f"Fridge {fridge_id} Temp")
        self.plot_widget.plot(self.time_data[fridge_id], self.hum_data[fridge_id], pen='b', name=f"Fridge {fridge_id} Hum")

        # Update logs
        row_position = self.log_table.rowCount()
        self.log_table.insertRow(row_position)
        self.log_table.setItem(row_position, 0, QTableWidgetItem(str(fridge_id)))
        self.log_table.setItem(row_position, 1, QTableWidgetItem(str(current_time)))
        self.log_table.setItem(row_position, 2, QTableWidgetItem(str(humidity)))
        self.log_table.setItem(row_position, 3, QTableWidgetItem(str(temperature)))

    def display(self, index):
        self.stacked_widget.setCurrentIndex(index)
        self.btn_realtime.setChecked(index == 0)
        self.btn_logs.setChecked(index == 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
