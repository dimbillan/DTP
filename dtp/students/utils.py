import os
from datetime import datetime
from flask import url_for
from dtp import app, logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent
from dtp.models import Student

def send_reset_email(student):
    token = student.get_reset_token()
    reset_url = url_for('students.reset_token', token=token, _external=True)
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    sender_email = Email(app.config['MAIL_DEFAULT_SENDER'])
    to_email = To(student.email)
    
    # Basit text içeriği
    text_content = "Merhaba! Bu bir test e-postasıdır."
    
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
            html_content=text_content
        )
        
        # Debug için mesaj içeriğini yazdır
        logger.info(f"E-posta gönderiliyor: {student.email}")
        
        sg = SendGridAPIClient(api_key)
        sg.client.session.verify = "etc/letsencrypt/live/devamsizliktakip.info.tr/fullchain.pem"
        
        response = sg.send(message.get())
        
        if response.status_code != 202:
            error_body = response.body.decode() if response.body else "Hata detayı yok"
            logger.error(f"SendGrid hatası: {error_body}")
            raise Exception(f"SendGrid hatası: {error_body}")
        else:
            logger.info(f"E-posta başarıyla gönderildi: {student.email}")
            
    except Exception as e:
        error_msg = f"E-posta gönderilirken hata oluştu: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        raise