"""
def send_reset_email(student):
    token = student.get_reset_token()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    msg = Message('Şifre Sıfırlama İsteği',
                  sender=app.config['MAIL_DEFAULT_SENDER'],  # Sistem mail adresi
                  recipients=[student.email])
    
    msg.body = f'''Sayın {student.name},

{current_time} tarihinde hesabınız için şifre sıfırlama talebinde bulundunuz.
Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:

{url_for('students.reset_token', token=token, _external=True, _scheme='https')}

Bu link 30 dakika süreyle geçerlidir.

Bu e-postayı siz istemediyseniz, lütfen dikkate almayın.

İyi günler dileriz,
Devamsızlık Takip Sistemi
'''
    mail.send(msg)
"""
import os
from datetime import datetime
from flask import url_for
from dtp import app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dtp.models import Student

def send_reset_email(student):
    token = student.get_reset_token()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    message = Mail(
        from_email=app.config['MAIL_DEFAULT_SENDER'],
        to_emails=student.email,
        subject='Şifre Sıfırlama İsteği',
        html_content=f"""Sayın {student.name},<br><br>

{current_time} tarihinde hesabınız için şifre sıfırlama talebinde bulundunuz.<br>
Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:<br><br>

<a href="{url_for('students.reset_token', token=token, _external=True, _scheme='https')}">Şifremi Sıfırla</a><br><br>

Bu link 30 dakika süreyle geçerlidir.<br><br>

Bu e-postayı siz istemediyseniz, lütfen dikkate almayın.<br><br>

İyi günler dileriz,<br>
Devamsızlık Takip Sistemi""")
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.client.session.verify = '/etc/letsencrypt/live/devamsizliktakip.info.tr/fullchain.pem'
        
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {str(e)}")