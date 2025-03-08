import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    # Mail ayarları
    MAIL_DEFAULT_SENDER = ('Devamsızlık Takip Sistemi', 'support@devamsizliktakip.info.tr')
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # SendGrid için sabit değer
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')  # SendGrid API anahtarı
    MAIL_MAX_EMAILS = 100  # SendGrid ücretsiz limit
    MAIL_ASCII_ATTACHMENTS = False  # Türkçe karakter desteği
    
    # Uygulama URL ayarları
    SERVER_NAME = os.environ.get('SERVER_NAME', 'devamsizliktakip.info.tr')
    PREFERRED_URL_SCHEME = 'https'
    