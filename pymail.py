import smtplib
import ssl
import env, secrets
from email.message import EmailMessage

email_sender = env.EMAIL_ADDRESS
email_password = secrets.EMAIL_PASSWORD
email_receiver = env.EMAIL_RECEIVERS

SUBJECT = 'check out my new site'
BODY = """
check out my website
https://lekoj.com
"""

mail = EmailMessage()
mail['From'] = email_sender
mail['To'] = email_receiver
mail['Subject'] = SUBJECT
mail.set_content(BODY)

context = ssl.create_default_context()

def send_mail():
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, mail.as_string())
    print(f'Mail delivered')

if __name__  == "__main__":
    send_mail()