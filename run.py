import requests
import time
from dtp import app
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
    #app.run(host="0.0.0.0", port=80, debug=True)