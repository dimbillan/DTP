import os
from datetime import datetime
from flask import url_for
from dtp import app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dtp.models import Student

def send_reset_email(student):
    token = student.get_reset_token()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # HTML içeriğini oluştur
    html_content = f"""Sayın {student.name},<br><br>
{current_time} tarihinde hesabınız için şifre sıfırlama talebinde bulundunuz.<br>
Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:<br><br>
<a href="{url_for('students.reset_token', token=token, _external=True, _scheme='https')}">Şifremi Sıfırla</a><br><br>
Bu link 30 dakika süreyle geçerlidir.<br><br>
Bu e-postayı siz istemediyseniz, lütfen dikkate almayın.<br><br>
İyi günler dileriz,<br>
Devamsızlık Takip Sistemi"""

    # SendGrid mesajını basitleştirilmiş formatta oluştur
    message = Mail(
        from_email=app.config['MAIL_DEFAULT_SENDER'],
        to_emails=student.email,
        subject='Şifre Sıfırlama İsteği',
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.client.session.verify = "etc/letsencrypt/live/devamsizliktakip.info.tr/fullchain.pem"  # SSL doğrulamasını geçici olarak devre dışı bırak
        
        response = sg.send(message)
        if response.status_code != 202:  # SendGrid başarılı gönderimde 202 döner
            print(f"SendGrid Yanıt Kodu: {response.status_code}")
            print(f"SendGrid Yanıt Gövdesi: {response.body.decode()}")  # JSON yanıtı decode et
            print(f"SendGrid Başlıkları: {response.headers}")
            raise Exception(f"SendGrid hatası: {response.body.decode()}")
            
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise  # Hatayı yukarı ilet