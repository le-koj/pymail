"""Global configuration for the pymail HTML email client.

This module defines SMTP settings, email addresses, and runtime constants
consumed by ``pymail_html``, ``streamlit_email``, and related scripts.
Values may be overridden at runtime (e.g. by the Streamlit UI).

Attributes:
    RECEIVERS_LIMIT (int): Maximum number of recipients allowed per bulk send.
    SMTP_HOST (str): SMTP server hostname. Defaults to Gmail.
    SMTP_PORT (int): SMTP server port (465 for SSL, 587 for TLS).
    SMTP_PORTS (tuple): Available port options for UI selection.
    SENDER_EMAIL (str): Sender email address; set by user or UI.
    RECEIVER_EMAIL (str): Default single recipient when not using bulk send.
    RECIEVERS_LIST (list): Comma-separated recipient list for bulk emails.
    EMAIL_SUBJECT (str): Subject line for outgoing messages.
    HTML_FILENAME (str): Default path to HTML template file.
    SSL_CONTEXT (ssl.SSLContext): SSL context for secure SMTP connections.
"""

import ssl

# -----------------------------------------------------------------------------
# Recipient limits
# -----------------------------------------------------------------------------
RECEIVERS_LIMIT: int = 20

# -----------------------------------------------------------------------------
# SMTP server configuration
# Default: Gmail. Override for custom providers (e.g. smtp.sendgrid.net).
# -----------------------------------------------------------------------------
SMTP_HOST: str = 'smtp.gmail.com'
SMTP_PORT: int = 465
SMTP_PORTS: tuple = (465, 25, 26, 587, 2525)

# -----------------------------------------------------------------------------
# Email composition defaults
# Sender, recipients, subject, and template path; often overridden at runtime.
# -----------------------------------------------------------------------------
SENDER_EMAIL: str = ''
RECEIVER_EMAIL: str = ''
RECIEVERS_LIST: list = []
EMAIL_SUBJECT: str = ''
HTML_FILENAME: str = 'no_income_no_asset.html'

# -----------------------------------------------------------------------------
# SSL context for SMTP_SSL / STARTTLS connections
# -----------------------------------------------------------------------------
SSL_CONTEXT: ssl.SSLContext = ssl.create_default_context()


