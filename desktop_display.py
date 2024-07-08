import sys
import json
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESP8266 AWS IoT Data Visualization")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("Nem ve Sıcaklık Değerleri")
        self.layout.addWidget(self.label)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(ca_certs="root-CA.crt", certfile="certificate.pem.crt", keyfile="private.pem.key")
        self.client.connect("your_aws_iot_endpoint", 8883)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)  # Update data every 5 seconds

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        self.client.subscribe("your/topic")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print("Received message:", message)
        data = json.loads(message)
        humidity = data.get("humidity", 0.0)
        temperature = data.get("temperature", 0.0)
        self.label.setText(f"Nem: {humidity}% - Sıcaklık: {temperature}°C")

    def update_data(self):
        self.client.loop()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
