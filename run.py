import requests
import time
from dtp import app
from waitress import serve

if __name__ == "__main__":
    serve(app)