#from flask import url_for
#from dtp.models import Student
#from dtp import mail
#from flask_mail import Message
#def send_reset_email(student):
#token = student.get_reset_token()
#msg = Message('Şifre Yenileme İsteği', sender='noreply@devamsizliktakip.com', recipients=[student.email])

#msg.body = f"""Şifrenizi yenilemek için lütfen bu linke tıklayınız:
#{url_for('students.reset_token', token=token, _external=True)}

#Eğer bu isteği siz göndermediyseniz, lütfen bu e-postayı görmezden gelin.
#"""
#mail.send(msg)
