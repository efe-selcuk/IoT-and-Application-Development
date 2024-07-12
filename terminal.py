import os
import time
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Geçerli çalışma dizinini al
current_dir = os.path.dirname(os.path.abspath(__file__))

# SQLite veritabanı bağlantısı oluşturma
def create_connection(db_file):
    try:
        conn = sqlite3.connect(os.path.join(current_dir, db_file))
        return conn
    except sqlite3.Error as e:
        print(e)
        return None

# Veritabanında uyarı logları için tablo oluşturma
def create_table(conn):
    try:
        sql_create_table = '''CREATE TABLE IF NOT EXISTS uyari_log (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT NOT NULL,
                            temperature REAL NOT NULL,
                            humidity REAL NOT NULL,
                            message TEXT NOT NULL
                          )'''
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Sıcaklık sınırlarını kontrol etme ve uyarıyı veritabanına yazma
def check_temperature_limits(conn_sensor, conn_log):
    try:
        # Son veriyi al
        cursor_sensor = conn_sensor.cursor()
        cursor_sensor.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1')
        row = cursor_sensor.fetchone()

        if row:
            timestamp = row[1]
            temperature = row[2]  # Tablodaki sıcaklık sütunu
            humidity = row[3]  # Tablodaki nem sütunu

            # Sıcaklık sınırlarını kontrol et
            if temperature < -5 or temperature > 20:
                message = f'Uyarı: Sıcaklık sınırı aşıldı! Son sıcaklık: {temperature:.2f} C (Zaman: {timestamp})'
                write_to_db(conn_log, timestamp, temperature, humidity, message)
                show_popup(message)  # Popup uyarı göster
        else:
            print('Veritabanında henüz veri yok.')
    except sqlite3.Error as e:
        print(e)

# Uyarı logunu veritabanına yazma
def write_to_db(conn, timestamp, temperature, humidity, message):
    try:
        sql_insert = '''INSERT INTO uyari_log (timestamp, temperature, humidity, message) VALUES (?, ?, ?, ?)'''
        cursor = conn.cursor()
        cursor.execute(sql_insert, (timestamp, temperature, humidity, message))
        conn.commit()
        print("Uyarı veritabanına kaydedildi.")
    except sqlite3.Error as e:
        print(e)

# Veritabanındaki tüm uyarı loglarını okuma ve yazdırma
def read_logs(conn):
    try:
        sql_read = '''SELECT * FROM uyari_log'''
        cursor = conn.cursor()
        cursor.execute(sql_read)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)

# Popup uyarı gösterme
def show_popup(message):

    # Popup uyarı
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    messagebox.showwarning("Sıcaklık Uyarısı", message)
    root.destroy()

# Ana fonksiyon
def main():
    sensor_database = 'SQL/terminal_data.db'
    log_database = 'SQL/warnings_log.db'
    
    sensor_conn = create_connection(sensor_database)
    log_conn = create_connection(log_database)
    
    if log_conn is not None:
        create_table(log_conn)
    
    try:
        while True:
            check_temperature_limits(sensor_conn, log_conn)
            read_logs(log_conn)  # Logları okuyup yazdırma
            time.sleep(10)  # Her 10 saniyede bir kontrol et
    finally:
        if sensor_conn:
            sensor_conn.close()
        if log_conn:
            log_conn.close()

if __name__ == '__main__':
    main()