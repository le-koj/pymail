"""Simple plain-text email sender using Gmail SMTP.

This module sends a single plain-text email via Gmail's SMTP server (port 465,
SSL). It is intended for quick one-off sends and uses configuration from
``env`` and ``secrets`` modules.

Dependencies:
    env: Must define ``EMAIL_ADDRESS`` (sender) and ``EMAIL_RECEIVERS``.
    secrets: Must define ``EMAIL_PASSWORD`` (Gmail App Password recommended).

Configuration:
    The following module-level variables must be set before calling
    ``send_mail()``:

    - ``env.EMAIL_ADDRESS``: Sender email address (str).
    - ``env.EMAIL_RECEIVERS``: Recipient email address (str).
    - ``secrets.EMAIL_PASSWORD``: Sender password or Gmail App Password (str).

Example:
    Run as a script to send the default message::

        $ python pymail.py

    Or import and call programmatically::

        from pymail import send_mail
        send_mail()

Note:
    For Gmail with 2-Step Verification, use an App Password rather than
    the account password. See https://support.google.com/accounts/answer/185833
"""

import smtplib
import ssl

import env
import secrets
from email.message import EmailMessage

# Load credentials and recipient from configuration modules
email_sender = env.EMAIL_ADDRESS
email_password = secrets.EMAIL_PASSWORD
email_receiver = env.EMAIL_RECEIVERS

# Default message content (customize as needed)
SUBJECT = 'check out my new site'
BODY = """
check out my website
https://lekoj.com
"""

# Build the email message
mail = EmailMessage()
mail['From'] = email_sender
mail['To'] = email_receiver
mail['Subject'] = SUBJECT
mail.set_content(BODY)

# SSL context for secure SMTP connection
context = ssl.create_default_context()


def send_mail() -> None:
    """Send the composed email via Gmail SMTP over SSL.

    Establishes an SMTP_SSL connection to smtp.gmail.com:465, authenticates
    using the configured sender and password, and delivers the message.

    Raises:
        smtplib.SMTPAuthenticationError: If login credentials are invalid.
        smtplib.SMTPException: For other SMTP-related errors.
    """
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, mail.as_string())
    print(f'Mail delivered')


if __name__ == "__main__":
    send_mail()