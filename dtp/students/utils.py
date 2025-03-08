import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
def send_reset_email(student):
    token = student.get_reset_token()
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('MAIL_DEFAULT_SENDER'))
    to_email = To(f"{student.email}")
    subject = "Şifre Sıfırlama İsteği"
    content = Content(f"text/plain", "Lütfen bağlantıya tıklayarak şifrenizi sıfırlayın: https://www.devamsizliktakip.info.tr/reset-password/{token}")
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    print(student)
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)