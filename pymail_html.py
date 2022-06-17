# Import modules
import smtplib, ssl, time

# import environment variables
import env, secrets

## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the HTML document
HTML = ''

# smtp settings
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

# Set up the email addresses and password.
email_sender: str = env.EMAIL_ADDRESS
email_password: str = '' #secrets.EMAIL_PASSWORD
email_receiver: list = env.EMAIL_RECEIVERS
email_subject: str = 'KB Capital Campaign'

# Set email SSL
context = ssl.create_default_context()

def html_email(subject, receiver) -> str:
    """Generate the full html email content and return a string version

    Returns:
        str: string representing the full email content
    """
    
    # read html email template and assign contents to HTML variable
    with open(env.HTML_FILE, 'r') as f:
        HTML = f.read()
    
    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    mail = MIMEMultipart()
    mail['From'] = email_sender
    mail['To'] = receiver
    mail['Subject'] = subject

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    mail.attach(MIMEText(HTML, "html"))
    # Convert it as a string
    email_string = mail.as_string()
    
    return email_string

def streamlit_html_email(subject, receiver) -> str:
    """Generate the full html email content and return a string version

    Returns:
        str: string representing the full email content
    """

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    mail = MIMEMultipart()
    mail['From'] = email_sender
    mail['To'] = receiver
    mail['Subject'] = subject

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    mail.attach(MIMEText(HTML, "html"))
    # Convert it as a string
    email_string = mail.as_string()
    
    return email_string
    
def send_email(subject, receiver) -> None:
    """Log into the stmp server and send the generated email content
    """
    #email_string = html_email(subject=subject, receiver=receiver)
    email_string = streamlit_html_email(subject=subject, receiver=receiver)
    
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, email_string)
    
    print(f'Mail delivered')

# convert list of receivers to dictionary of receivers
def email_dict(subject, receivers: list) -> dict:
    _mail_dict = {}
    for receiver in receivers:
        _mail_dict[receiver] = html_email(subject=subject, receiver=receiver)
    return _mail_dict

def send_email_dict():
    mail_dict = email_dict(email_subject, email_receiver)

    for key, value in mail_dict.items():
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, key, value)
    
    print(f'Mail delivered')

if __name__  == "__main__":
    start = time.time()
    for receiver in email_receiver:
        send_email(subject=email_subject, receiver=receiver)
    end = time.time()
    print(f"Time Difference: {end - start}")

