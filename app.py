from flask import Flask, jsonify, render_template
import random
import threading
import time

app = Flask(__name__)

# Veri simülasyonu için fonksiyon
def veri_simulasyonu(dondurucu_id):
    sicaklik = round(random.uniform(-20, 5), 2)  # -20°C ile 5°C arasında rastgele sıcaklık
    nem = round(random.uniform(40, 80), 2)      # %40 ile %80 arasında rastgele nem
    return {
        "dondurucu_id": dondurucu_id,
        "sicaklik": sicaklik,
        "nem": nem
    }

# Ana sayfa için HTML dosyasını render etme
@app.route('/')
def index():
    # 30 dondurucu için rastgele veri oluştur
    dondurucular = []
    for i in range(1, 31):
        veri = veri_simulasyonu(i)
        dondurucular.append(veri)
    return render_template('index.html', dondurucular=dondurucular)

# Zamanlayıcı işlevi: Her 30 saniyede bir veri gönder
def zamanlayici():
    while True:
        # Her 30 saniyede bir veri simülasyonu yap
        for i in range(1, 31):
            veri = veri_simulasyonu(i)
            print(f"Simüle edilen veri: {veri}")
        time.sleep(30) # 30 saniye bekle

# Flask uygulamasını başlatma
if __name__ == '__main__':
    # Zamanlayıcı iş parçacığını başlatma
    thread = threading.Thread(target=zamanlayici)
    thread.start()
    
    # Flask uygulamasını çalıştırma
    app.run(debug=True)
