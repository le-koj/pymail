"""HTML Email Client Agent

This script allows the user to send an html file as 
email using google gmail or their own email service provider

This script requires the senders email address, email password,
the receiver's email, and the email subject.

This script needs 2 personal files:
    env.py - which has the following global settings:
        
        SMTP_HOST: str = 'smtp.gmail.com'
        SMTP_PORT: int = 465

        SENDER_EMAIL: str = 'example@domain.com'
        RECEIVER_EMAIL: str = 'example@example.com'
        RECIEVERS_LIST: list = []
        EMAIL_SUBJECT: str = ''
        HTML_FILENAME: str = 'my_newsletter.html'
        
    app_secrets.py - which holds the password for your sender email
        EMAIL_PASSWORD = 'sender email password'

This file can also be imported as a module and contains the following
functions:

    * get_html_doc - returns html file in string format
    * html_email_str - generate a string version of the html email content
    * smtp_send - sends an email using the stmp settings
    * send_html_email - process and sends an html email content
    * send_bulk_email - Send html emails to several recipients
"""

# Import required modules
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import environment variables
import env
import app_secrets

# set smtp password
EMAIL_PASSWORD = app_secrets.EMAIL_PASSWORD

def get_html_doc(file_path: str) -> str:
    """Open html file and return a string version
    
    Parameters
    ----------
    file_path : str
        The file path of the html document

    Returns
    -------
        str: string representation the full html content
    """
    html = ''
    
    with open(file_path, 'r', encoding='UTF-8') as f:
        print('getting email')
        html = f.read()
    return html

def html_email_str(receiver_email: str, html_doc: str) -> str:
    """Generate a string version of the html email content
    
    Uses the pre-configured settings in the env.py file
    
    Parameters
    ----------
    receiver_email : str
        The email address of the recipient
    html_doc : str
        The string format of the html content

    Returns
    -------
        str: string representation the full email content
    """
    
    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    mail = MIMEMultipart()
    mail['From'] = env.SENDER_EMAIL
    mail['To'] = receiver_email
    mail['Subject'] = env.EMAIL_SUBJECT

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    mail.attach(MIMEText(html_doc, "html"))
    # Convert it as a string
    email_string = mail.as_string()
    return email_string

def smtp_send(receiver_email, email_string) -> None:
    """Send email using smtp
    
    Uses the pre-configured settings in the env.py file
    
    Parameters
    ----------
    receiver_email : str
        The email address of the recipient
    email_string : str
        email content in string format generated using html_email_str() function
    """
    with smtplib.SMTP_SSL(env.SMTP_HOST, env.SMTP_PORT, context=env.SSL_CONTEXT) as smtp:
        smtp.login(env.SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.sendmail(env.SENDER_EMAIL, receiver_email, email_string)
    
    print('smtp sent', '\n')
    return
   
def send_html_email(receiver_email: str, html_doc: str) -> None:
    """Send an html email to the provided email address
    
    Uses the pre-configured settings in the env.py file
    
    Parameters
    ----------
    receiver_email : str
        The email address of the recipient
    html_doc : str
        The string format of the html content
    """
    
    # process html email for sending
    email_string = html_email_str(receiver_email=receiver_email, html_doc=html_doc)
    
    # send processed email to recipient
    smtp_send(receiver_email=receiver_email, email_string=email_string)
    
    print('Mail delivered', '\n')
    return

def send_bulk_email(html_doc: str) -> None:
    """Send html emails to several recipients
    
    Uses the pre-configured settings in the env.py file
    
    Parameters
    ----------
    html_doc : str
        The string format of the html content
    """
    print('### SENDING BULK EMAIL ###', '\n')
    
    counter = 0
    for receiver in env.RECIEVERS_LIST:
        send_html_email(receiver_email=receiver, html_doc=html_doc)
        counter += 1
    print(f'{counter} Emails delivered', '\n')
    return
    

if __name__  == "__main__":
    start = time.time()
    
    HTML = get_html_doc(env.HTML_FILENAME)
        
    #send_html_email(receiver_email=env.RECEIVER_EMAIL, html_doc=HTML)
    
    send_bulk_email(HTML)
    end = time.time()
    print(f"Time Difference: {end - start}")

