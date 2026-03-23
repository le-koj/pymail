"""HTML Email Client Agent for sending HTML emails via SMTP.

This module provides functions to send HTML-formatted emails using Gmail or
any SMTP provider. It supports single recipients and bulk sending to a list,
with configuration sourced from ``env.py`` and ``app_secrets.py``.

Dependencies:
    env: SMTP settings, sender/recipient addresses, subject, and HTML filename.
    app_secrets: Sender email password or App Password (see ``EMAIL_PASSWORD``).

Configuration:
    Requires two configuration modules:

    ``env.py`` must define:
        SMTP_HOST (str): SMTP server hostname (e.g. ``smtp.gmail.com``).
        SMTP_PORT (int): SMTP port (typically 465 for SSL).
        SENDER_EMAIL (str): Sender email address.
        RECEIVER_EMAIL (str): Default recipient email address.
        RECIEVERS_LIST (list): List of recipient emails for bulk send.
        EMAIL_SUBJECT (str): Email subject line.
        HTML_FILENAME (str): Default HTML template file path.
        SSL_CONTEXT (ssl.SSLContext): SSL context for secure SMTP.

    ``app_secrets.py`` must define:
        EMAIL_PASSWORD (str): Sender password or Gmail App Password.

Module Attributes:
    EMAIL_PASSWORD (str): Loaded from ``app_secrets``; may be overridden by
        consumers (e.g. Streamlit UI) with user-supplied credentials.
"""

import smtplib
import time

import app_secrets
import env
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Sender password; may be overridden by UI or calling code
EMAIL_PASSWORD = app_secrets.EMAIL_PASSWORD

def get_html_doc(file_path: str) -> str:
    """Read an HTML file and return its contents as a string.

    Args:
        file_path: Path to the HTML file on disk.

    Returns:
        The full HTML content as a UTF-8 decoded string.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file is not valid UTF-8.
    """
    html = ''
    with open(file_path, 'r', encoding='UTF-8') as f:
        print('getting email')
        html = f.read()
    return html

def html_email_str(receiver_email: str, html_doc: str) -> str:
    """Build a MIME multipart email string from HTML content.

    Uses sender, subject, and other headers from ``env``. The HTML body is
    attached as ``MIMEText`` with content type ``text/html``.

    Args:
        receiver_email: Recipient email address.
        html_doc: HTML body content as a string.

    Returns:
        The complete email as a string suitable for ``smtplib.sendmail()``.
    """
    mail = MIMEMultipart()
    mail['From'] = env.SENDER_EMAIL
    mail['To'] = receiver_email
    mail['Subject'] = env.EMAIL_SUBJECT
    mail.attach(MIMEText(html_doc, "html"))
    return mail.as_string()

def smtp_send(receiver_email: str, email_string: str) -> None:
    """Send an email via SMTP over SSL.

    Connects to the SMTP server configured in ``env`` (host, port, SSL context),
    authenticates with the sender credentials, and delivers the message.

    Args:
        receiver_email: Recipient email address.
        email_string: Full email content as string (e.g. from ``html_email_str()``).

    Raises:
        smtplib.SMTPAuthenticationError: If login credentials are invalid.
        smtplib.SMTPException: For other SMTP-related errors.
    """
    with smtplib.SMTP_SSL(env.SMTP_HOST, env.SMTP_PORT, context=env.SSL_CONTEXT) as smtp:
        smtp.login(env.SENDER_EMAIL, EMAIL_PASSWORD)
        smtp.sendmail(env.SENDER_EMAIL, receiver_email, email_string)
    print('smtp sent', '\n')
   
def send_html_email(receiver_email: str, html_doc: str) -> None:
    """Compose and send an HTML email to a single recipient.

    Builds the MIME message from the HTML content, then delivers it via
    ``smtp_send()`` using settings from ``env``.

    Args:
        receiver_email: Recipient email address.
        html_doc: HTML body content as a string.
    """
    email_string = html_email_str(receiver_email=receiver_email, html_doc=html_doc)
    smtp_send(receiver_email=receiver_email, email_string=email_string)
    print('Mail delivered', '\n')

def send_bulk_email(html_doc: str) -> None:
    """Send the same HTML email to all recipients in ``env.RECIEVERS_LIST``.

    Iterates over the list and calls ``send_html_email()`` for each address.

    Args:
        html_doc: HTML body content as a string.
    """
    print('### SENDING BULK EMAIL ###', '\n')
    counter = 0
    for receiver in env.RECIEVERS_LIST:
        send_html_email(receiver_email=receiver.strip(), html_doc=html_doc)
        counter += 1
    print(f'{counter} Emails delivered', '\n')


if __name__ == "__main__":
    # Load HTML template and send to all recipients in RECIEVERS_LIST
    start = time.time()
    HTML = get_html_doc(env.HTML_FILENAME)
    # send_html_email(receiver_email=env.RECEIVER_EMAIL, html_doc=HTML)
    send_bulk_email(HTML)
    end = time.time()
    print(f"Time Difference: {end - start}")

