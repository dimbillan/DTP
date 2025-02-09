import requests
import time
from dtp import app
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
   #app.run(host="0.0.0.0", port=5000)

"""
    url = "https://dtp-rdxy.onrender.com"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Başarıyla siteye bağlanıldı: {url}")
        else:
            print(f"Siteye bağlanırken hata oluştu: {response.status_code}")
        time.sleep(60)

"""