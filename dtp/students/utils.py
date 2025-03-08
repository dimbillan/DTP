import os
from datetime import datetime
from flask import url_for
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Content, To

def send_reset_email(student):
    token = student.get_reset_token()
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    message = Mail(
        from_email=Email(os.environ.get('MAIL_DEFAULT_SENDER')),
        to_emails=To(student.email),
        subject='Şifre Sıfırlama İsteği',
        html_content=Content('text/html', f"""Sayın {student.name},<br><br>

{current_time} tarihinde hesabınız için şifre sıfırlama talebinde bulundunuz.<br>
Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:<br><br>

<a href="{url_for('students.reset_token', token=token, _external=True, _scheme='https')}">Şifremi Sıfırla</a><br><br>

Bu link 30 dakika süreyle geçerlidir.<br><br>

Bu e-postayı siz istemediyseniz, lütfen dikkate almayın.<br><br>

İyi günler dileriz,<br>
Devamsızlık Takip Sistemi"""))

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.headers)
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
            return False
            
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {str(e)}")
        return False

    