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
    
    # HTML içeriğini oluştur
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Şifre Sıfırlama İsteği</h2>
                <p>Merhaba {student.name},</p>
                <p>Hesabınız için bir şifre sıfırlama isteği aldık. Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:</p>
                <p style="margin: 25px 0;">
                    <a href="{reset_url}" style="background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Şifremi Sıfırla
                    </a>
                </p>
                <p>Bu bağlantı 30 dakika süreyle geçerlidir.</p>
                <p>Eğer şifre sıfırlama isteğinde bulunmadıysanız, bu e-postayı görmezden gelebilirsiniz.</p>
                <p style="color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
                    Bu e-posta {current_time} tarihinde gönderilmiştir.
                </p>
            </div>
        </body>
    </html>
    """
    
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
            html_content=html_content
        )
        
        # Debug için mesaj içeriğini yazdır
        logger.info(f"E-posta gönderiliyor: {student.email}")
        
        sg = SendGridAPIClient(api_key)
        sg.client.session.verify = "etc/letsencrypt/live/devamsizliktakip.info.tr/fullchain.pem"
        
        response = sg.send(message)
        
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