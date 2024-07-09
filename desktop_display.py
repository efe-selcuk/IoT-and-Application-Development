import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QTabWidget, QTableWidget, QTableWidgetItem,
                             QHBoxLayout, QStackedWidget, QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
import pyqtgraph as pg

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
        self.realtime_widget = QWidget()
        self.init_realtime_widget()
        self.stacked_widget.addWidget(self.realtime_widget)

        # Log data widget
        self.log_widget = QWidget()
        self.init_log_widget()
        self.stacked_widget.addWidget(self.log_widget)

        # Data for plotting and logging
        self.time_data = []
        self.temp_data = []
        self.hum_data = []

        # Timer for updating data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update data every second

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
        self.humidity_frame.setStyleSheet("background-color: #555; border: 2px solid #777; border-radius: 10px;")
        self.humidity_layout = QVBoxLayout(self.humidity_frame)
        self.humidity_label = QLabel("Nem: -- %")
        self.humidity_label.setFont(QFont('Arial', 20))
        self.humidity_label.setStyleSheet("color: white; margin: 5px;")
        self.humidity_indicator = QLabel()
        self.humidity_layout.addWidget(self.humidity_label, alignment=Qt.AlignCenter)
        self.humidity_layout.addWidget(self.humidity_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.humidity_frame)
        
        # Temperature indicator
        self.temperature_frame = QFrame()
        self.temperature_frame.setFrameShape(QFrame.StyledPanel)
        self.temperature_frame.setStyleSheet("background-color: #555; border: 2px solid #777; border-radius: 10px;")
        self.temperature_layout = QVBoxLayout(self.temperature_frame)
        self.temperature_label = QLabel("Sıcaklık: -- °C")
        self.temperature_label.setFont(QFont('Arial', 20))
        self.temperature_label.setStyleSheet("color: white; margin: 5px;")
        self.temperature_indicator = QLabel()
        self.temperature_layout.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        self.temperature_layout.addWidget(self.temperature_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.temperature_frame)
        
        self.realtime_layout.addLayout(self.indicators_layout)

        # Plot widgets for real-time data
        self.plot_widget_temp = pg.PlotWidget()
        self.plot_widget_temp.setBackground('#121212')  # Dark background
        self.plot_widget_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_widget_temp.getAxis('left').setLabel('Sıcaklık (°C)', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_temp.getAxis('bottom').setLabel('Zaman', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_temp.addLegend(offset=(50, 50), brush=(50, 50, 50, 150))  # Legend settings
        self.plot_widget_temp.showGrid(x=True, y=True, alpha=0.3)  # Grid settings
        self.plot_widget_temp.setMouseEnabled(x=True, y=False)
        self.realtime_layout.addWidget(self.plot_widget_temp)

        self.plot_widget_hum = pg.PlotWidget()
        self.plot_widget_hum.setBackground('#121212')  # Dark background
        self.plot_widget_hum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_widget_hum.getAxis('left').setLabel('Nem (%)', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_hum.getAxis('bottom').setLabel('Zaman', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_hum.addLegend(offset=(50, 50), brush=(50, 50, 50, 150))  # Legend settings
        self.plot_widget_hum.showGrid(x=True, y=True, alpha=0.3)  # Grid settings
        self.plot_widget_hum.setMouseEnabled(x=True, y=False)
        self.realtime_layout.addWidget(self.plot_widget_hum)

    def init_log_widget(self):
        self.log_layout = QVBoxLayout(self.log_widget)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["Zaman", "Nem (%)", "Sıcaklık (°C)"])
        self.log_table.horizontalHeader().setStyleSheet("background-color: #555; color: white; font-size: 14pt;")
        self.log_layout.addWidget(self.log_table)

    def update_data(self):
        # Simulate receiving data
        humidity = random.uniform(30.0, 70.0)  # Simulated humidity value
        temperature = random.uniform(20.0, 30.0)  # Simulated temperature value

        # Update indicators
        if len(self.hum_data) > 0 and humidity > self.hum_data[-1]:
            self.humidity_indicator.setPixmap(QPixmap("arrow_up.png"))
        else:
            self.humidity_indicator.setPixmap(QPixmap("arrow_down.png"))

        if len(self.temp_data) > 0 and temperature > self.temp_data[-1]:
            self.temperature_indicator.setPixmap(QPixmap("arrow_up.png"))
        else:
            self.temperature_indicator.setPixmap(QPixmap("arrow_down.png"))

        # Update labels
        self.humidity_label.setText(f"Nem: {humidity:.2f}%")
        self.temperature_label.setText(f"Sıcaklık: {temperature:.2f}°C")

        # Append data for plotting and logging
        current_time = len(self.time_data) + 1
        self.time_data.append(current_time)
        self.temp_data.append(temperature)
        self.hum_data.append(humidity)

        # Update plot for temperature
        self.plot_widget_temp.clear()
        temp_pen = pg.mkPen(color=('#FF5733'), width=2, style=Qt.SolidLine, antialias=True)  # Red, slightly transparent, smooth line
        self.plot_widget_temp.plot(self.time_data, self.temp_data, pen=temp_pen, name='Sıcaklık')

        # Update plot for humidity
        self.plot_widget_hum.clear()
        hum_pen = pg.mkPen(color=('#33A7FF'), width=2, style=Qt.SolidLine, antialias=True)  # Blue, slightly transparent, smooth line
        self.plot_widget_hum.plot(self.time_data, self.hum_data, pen=hum_pen, name='Nem')

        # Limit data to last 50 points for better visualization
        if len(self.time_data) > 50:
            self.time_data = self.time_data[-50:]
            self.temp_data = self.temp_data[-50:]
            self.hum_data = self.hum_data[-50:]

        # Log data
        row_position = self.log_table.rowCount()
        self.log_table.insertRow(row_position)
        self.log_table.setItem(row_position, 0, QTableWidgetItem(str(current_time)))
        self.log_table.setItem(row_position, 1, QTableWidgetItem(f"{humidity:.2f}"))
        self.log_table.setItem(row_position, 2, QTableWidgetItem(f"{temperature:.2f}"))

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
