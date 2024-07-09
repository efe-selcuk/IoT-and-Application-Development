import sys
import random
import threading
import time
import socket
import json

# Simulated data producer
def send_data():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    
    while True:
        for fridge_id in range(1, 101):  # 100 fridges
            data = {
                'id': fridge_id,
                'temperature': round(random.uniform(-20, 5), 2),
                'humidity': round(random.uniform(30, 70), 2)
            }
            message = json.dumps(data).encode()
            sock.sendto(message, server_address)
        
        time.sleep(60)  # Wait for 1 minute

if __name__ == '__main__':
    data_thread = threading.Thread(target=send_data)
    data_thread.start()
