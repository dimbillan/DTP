import os
from datetime import datetime
from flask import url_for
from dtp import app, logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
from dtp.models import Student

def send_reset_email(student):
    token = student.get_reset_token()

    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    sender_email = Email(app.config['MAIL_DEFAULT_SENDER'])

    to_email = To(student.email)
    
    # HTML içeriğini oluştur
    content = Content("text/plain", f"sa")
    try:
        # API anahtarını kontrol et
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            raise ValueError("SendGrid API anahtarı bulunamadı!")
            
        # Mesajı oluştur
        message = Mail(
            from_email=sender_email,
            to_emails=to_email,
            subject='Şifre Sıfırlama İsteği',
            html_content=content
        )
        
        # Debug için mesaj içeriğini yazdır
        print("Gönderilecek mesaj detayları:")
        print(f"From: {sender_email}")
        print(f"To: {to_email}")
        print(f"API Key (ilk 5 karakter): {api_key[:5]}...")
        
        sg = SendGridAPIClient(api_key)
        sg.client.session.verify = "etc/letsencrypt/live/devamsizliktakip.info.tr/fullchain.pem"
        
        message_json = message.get()
        response = sg.client.mail.send.post(request_body=message_json)
        print(f"SendGrid yanıt kodu: {response.status_code}")
        
        if response.status_code != 202:
            error_body = response.body.decode() if response.body else "Hata detayı yok"
            logger.error(f"SendGrid hatası: {error_body}")
            raise Exception(f"SendGrid hatası: {error_body}")
            
    except Exception as e:
        error_msg = f"E-posta gönderilirken hata oluştu: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        raise