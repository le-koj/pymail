"""Script Global settings

This script contains constant global settings used
in the module pymail_html.py

"""

# App settings
RECEIVERS_LIMIT = 20

# smtp settings - default: gmail
SMTP_HOST: str = 'smtp.gmail.com'
SMTP_PORT: int = 465
SMTP_PORTS: tuple = (465, 25, 26, 587, 2525)

# email settings
SENDER_EMAIL: str = ''
RECEIVER_EMAIL: str = ''
RECIEVERS_LIST: list = []
EMAIL_SUBJECT: str = ''
HTML_FILENAME: str = 'no_income_no_asset.html'

# email SSL setup
import ssl
SSL_CONTEXT = ssl.create_default_context()


