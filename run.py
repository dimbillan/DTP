from dtp import app
from waitress import serve

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)