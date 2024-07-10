from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import pyqtgraph as pg

class RealtimeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel("Realtime Widget")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 24))
        self.title_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.title_label)

        self.indicators_layout = QHBoxLayout()

        self.humidity_frame = QFrame()
        self.humidity_frame.setFrameShape(QFrame.StyledPanel)
        self.humidity_frame.setStyleSheet("background-color: #555; border: 2px solid #777; border-radius: 10px;")
        self.humidity_layout = QVBoxLayout(self.humidity_frame)
        self.humidity_label = QLabel("Nem: -- %")
        self.humidity_label.setFont(QFont('Arial', 20))
        self.humidity_label.setStyleSheet("color: white; margin: 5px;")
        self.humidity_indicator = QLabel()
        self.humidity_indicator.setFixedSize(QSize(50, 50))  # Set fixed size for indicator
        self.humidity_layout.addWidget(self.humidity_label, alignment=Qt.AlignCenter)
        self.humidity_layout.addWidget(self.humidity_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.humidity_frame)

        self.temperature_frame = QFrame()
        self.temperature_frame.setFrameShape(QFrame.StyledPanel)
        self.temperature_frame.setStyleSheet("background-color: #555; border: 2px solid #777; border-radius: 10px;")
        self.temperature_layout = QVBoxLayout(self.temperature_frame)
        self.temperature_label = QLabel("Sıcaklık: -- °C")
        self.temperature_label.setFont(QFont('Arial', 20))
        self.temperature_label.setStyleSheet("color: white; margin: 5px;")
        self.temperature_indicator = QLabel()
        self.temperature_indicator.setFixedSize(QSize(50, 50))  # Set fixed size for indicator
        self.temperature_layout.addWidget(self.temperature_label, alignment=Qt.AlignCenter)
        self.temperature_layout.addWidget(self.temperature_indicator, alignment=Qt.AlignCenter)
        self.indicators_layout.addWidget(self.temperature_frame)

        self.layout.addLayout(self.indicators_layout)

        # Initialize plot widgets
        self.plot_widget_temp = pg.PlotWidget()
        self.plot_widget_temp.setBackground('#121212')  # Dark background
        self.plot_widget_temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_widget_temp.getAxis('left').setLabel('Sıcaklık (°C)', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_temp.getAxis('bottom').setLabel('Zaman', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_temp.addLegend(offset=(50, 50), brush=(50, 50, 50, 150))  # Legend settings
        self.plot_widget_temp.showGrid(x=True, y=True, alpha=0.3)  # Grid settings
        self.plot_widget_temp.setMouseEnabled(x=True, y=False)
        self.layout.addWidget(self.plot_widget_temp)

        self.plot_widget_hum = pg.PlotWidget()
        self.plot_widget_hum.setBackground('#121212')  # Dark background
        self.plot_widget_hum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_widget_hum.getAxis('left').setLabel('Nem (%)', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_hum.getAxis('bottom').setLabel('Zaman', **{'color': 'darkgray', 'font-size': '16pt', 'font-family': 'Arial', 'font-weight': 'bold'})
        self.plot_widget_hum.addLegend(offset=(50, 50), brush=(50, 50, 50, 150))  # Legend settings
        self.plot_widget_hum.showGrid(x=True, y=True, alpha=0.3)  # Grid settings
        self.plot_widget_hum.setMouseEnabled(x=True, y=False)
        self.layout.addWidget(self.plot_widget_hum)

        # Initialize empty plots
        self.plot_data_temp = {'x': [], 'y': []}
        self.plot_data_hum = {'x': [], 'y': []}

    def update_data(self, temperature, humidity):
        self.humidity_label.setText(f"Nem: {humidity:.2f}%")
        self.temperature_label.setText(f"Sıcaklık: {temperature:.2f}°C")

        # Example: Update indicator images based on conditions
        if humidity > 50:
            self.humidity_indicator.setPixmap(QPixmap("path_to_high_humidity_icon.png"))
        else:
            self.humidity_indicator.setPixmap(QPixmap("path_to_normal_humidity_icon.png"))

        if temperature > 25:
            self.temperature_indicator.setPixmap(QPixmap("path_to_high_temperature_icon.png"))
        else:
            self.temperature_indicator.setPixmap(QPixmap("path_to_normal_temperature_icon.png"))

        # Append new data points
        self.plot_data_temp['x'].append(len(self.plot_data_temp['x']) + 1)
        self.plot_data_temp['y'].append(temperature)

        self.plot_data_hum['x'].append(len(self.plot_data_hum['x']) + 1)
        self.plot_data_hum['y'].append(humidity)

        # Limit data points to last 50 for better visualization
        if len(self.plot_data_temp['x']) > 50:
            self.plot_data_temp['x'] = self.plot_data_temp['x'][-50:]
            self.plot_data_temp['y'] = self.plot_data_temp['y'][-50:]

        if len(self.plot_data_hum['x']) > 50:
            self.plot_data_hum['x'] = self.plot_data_hum['x'][-50:]
            self.plot_data_hum['y'] = self.plot_data_hum['y'][-50:]

        # Update plots
        self.plot_widget_temp.clear()
        self.plot_widget_temp.plot(self.plot_data_temp['x'], self.plot_data_temp['y'], pen='r', name='Sıcaklık')

        self.plot_widget_hum.clear()
        self.plot_widget_hum.plot(self.plot_data_hum['x'], self.plot_data_hum['y'], pen='b', name='Nem')
