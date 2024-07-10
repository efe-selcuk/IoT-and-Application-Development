import time
import sqlite3

# SQLite veritabanı bağlantısı oluşturma
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Sıcaklık sınırlarını kontrol etme ve uyarıyı dosyaya yazma
def check_temperature_limits(conn, log_file):
    sql = '''SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1'''
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()

    if row:
        timestamp = row[1]
        temperature = row[2]  # Tablodaki sıcaklık sütunu
        if temperature < -5 or temperature > 20:
            message = f'Uyarı: Sıcaklık sınırı aşıldı! Son sıcaklık: {temperature:.2f} C (Zaman: {timestamp})\n'
            write_to_log(log_file, message)
    else:
        print('Veritabanında henüz veri yok.')

# Log dosyasına yazma
def write_to_log(log_file, message):
    log_path = r'C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\{}'.format(log_file)
    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(message)

# Ana fonksiyon
def main():
    database = r'C:\Users\HP\OneDrive\Masaüstü\IoT and Application Development\terminal_data.db'
    log_file = 'uyari_log.txt'
    conn = create_connection(database)
    while True:
        check_temperature_limits(conn, log_file)
        time.sleep(10)  # Her 10 saniyede bir kontrol et

if __name__ == '__main__':
    main()
