"""Global configuration for the pymail HTML email client.

This module defines SMTP settings, email addresses, and runtime constants
consumed by ``pymail_html``, ``streamlit_email``, and related scripts.
Values may be overridden at runtime (e.g. by the Streamlit UI).

Environment Variable Overrides (for containerized / CI usage):
    SMTP_HOST: SMTP server hostname.  Defaults to ``smtp.gmail.com``.
               Set to ``mailpit`` inside the Docker Compose network.
    SMTP_PORT: SMTP server port.  Defaults to ``465`` (SSL).
    MAILPIT_HOST: Mailpit SMTP hostname for local testing.  Defaults to ``localhost``.
                  Set to ``mailpit`` inside the Docker Compose network.
    MAILPIT_PORT: Mailpit SMTP port.  Defaults to ``1025``.

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

import os
import ssl

# -----------------------------------------------------------------------------
# Recipient limits
# -----------------------------------------------------------------------------
RECEIVERS_LIMIT: int = 20

# -----------------------------------------------------------------------------
# SMTP server configuration
# Reads from environment variables for Docker/CI portability.
# Defaults: Gmail (smtp.gmail.com:465).  Inside Docker Compose the env vars
# are set to mailpit:1025 so emails are captured locally.
# -----------------------------------------------------------------------------
SMTP_HOST: str = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT: int = int(os.getenv('SMTP_PORT', '465'))
SMTP_PORTS: tuple = (465, 25, 26, 587, 2525, 1025)

MAILPIT_HOST: str = os.getenv('MAILPIT_HOST', 'localhost')
MAILPIT_PORT: int = int(os.getenv('MAILPIT_PORT', '1025'))

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


