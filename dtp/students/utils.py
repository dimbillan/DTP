from flask import url_for
from flask_mail import Message
from dtp import mail, app

def send_reset_email(student):
    token = student.get_reset_token()
    msg = Message('Şifre Sıfırlama İsteği',
                  sender=app.config['MAIL_USERNAME'],  # Kimlik doğrulaması yapılan Gmail adresi
                  recipients=[student.email])
    msg.body = f'''Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:
{url_for('students.reset_token', token=token, _external=True)}

Bu e-postayı siz istemediyseniz, lütfen dikkate almayın.
'''
    mail.send(msg) 