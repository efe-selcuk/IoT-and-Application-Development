# -- coding: utf-8 --
#Created on Monday July 8 2024
#@author: Efe Selcuk
#Subject: temperature and humidity UI
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
        # Belirtilen veritabanı dosyasına bağlan
        conn = sqlite3.connect(os.path.join(current_dir, db_file))
        return conn
    except sqlite3.Error as e:
        # Bağlantı hatası durumunda hata mesajını yazdır ve None döndür
        print(e)
        return None

# Veritabanında uyarı logları için tablo oluşturma
def create_table(conn):
    try:
        # Uyarı logları için bir tablo oluştur (varsa mevcut tabloyu kullan)
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
        # Tablo oluşturma hatası durumunda hata mesajını yazdır
        print(e)

# Sıcaklık sınırlarını kontrol etme ve uyarıyı veritabanına yazma
def check_temperature_limits(conn_sensor, conn_log):
    try:
        # Sensör veritabanından son veriyi al
        cursor_sensor = conn_sensor.cursor()
        cursor_sensor.execute('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1')
        row = cursor_sensor.fetchone()

        if row:
            # Son verinin tarihini, sıcaklık ve nem değerlerini al
            timestamp = row[1]
            temperature = row[2]  # Tablodaki sıcaklık sütunu
            humidity = row[3]  # Tablodaki nem sütunu

            # Sıcaklık sınırlarını kontrol et
            if temperature < -5 or temperature > 20:
                # Sıcaklık sınırları aşıldığında uyarı mesajı oluştur
                message = f'Uyarı: Sıcaklık sınırı aşıldı! Son sıcaklık: {temperature:.2f} C (Zaman: {timestamp})'
                # Oluşturulan uyarı mesajını veritabanına kaydet
                write_to_db(conn_log, timestamp, temperature, humidity, message)
                # Kullanıcıya popup uyarısı göster
                show_popup(message)
        else:
            # Veritabanında henüz veri yoksa terminalde bilgi mesajı yazdır
            print('Veritabanında henüz veri yok.')
    except sqlite3.Error as e:
        # SQLite hatası durumunda hata mesajını yazdır
        print(e)

# Uyarı logunu veritabanına yazma
def write_to_db(conn, timestamp, temperature, humidity, message):
    try:
        # Veritabanına uyarı logu eklemek için SQL sorgusu
        sql_insert = '''INSERT INTO uyari_log (timestamp, temperature, humidity, message) VALUES (?, ?, ?, ?)'''
        cursor = conn.cursor()
        cursor.execute(sql_insert, (timestamp, temperature, humidity, message))
        conn.commit()
        # Veritabanına kayıt yapıldığında bilgi mesajı yazdırmak için print komutu (opsiyonel)
        # print("Uyarı veritabanına kaydedildi.")
    except sqlite3.Error as e:
        # SQLite hatası durumunda hata mesajını yazdır
        print(e)

# Popup uyarı gösterme
def show_popup(message):
    try:
        # Tkinter kütüphanesi kullanarak bir popup penceresi oluştur
        root = tk.Tk()
        root.withdraw()  # Ana pencereyi gizle
        messagebox.showwarning("Sıcaklık Uyarısı", message)
        root.destroy()
    except tk.TclError as e:
        # Tkinter hatası durumunda hata mesajını yazdır
        print(e)

# Ana fonksiyon
def main():
    # Sensör ve log veritabanı dosyalarının yollarını tanımla
    sensor_database = 'SQL/terminal_data.db'
    log_database = 'SQL/warnings_log.db'
    
    # Sensör ve log veritabanlarına bağlan
    sensor_conn = create_connection(sensor_database)
    log_conn = create_connection(log_database)
    
    # Log veritabanı bağlantısı başarılıysa uyari_log tablosunu oluştur
    if log_conn is not None:
        create_table(log_conn)
    
    try:
        # Sonsuz döngü: Her 30 saniyede bir sıcaklık sınırlarını kontrol et ve logları oku
        while True:
            check_temperature_limits(sensor_conn, log_conn)
            time.sleep(30)  # Her 30 saniyede bir kontrol et
    finally:
        # İşlem sonlandığında sensör ve log veritabanı bağlantılarını kapat
        if sensor_conn:
            sensor_conn.close()
        if log_conn:
            log_conn.close()

if __name__ == '__main__':
    main()
