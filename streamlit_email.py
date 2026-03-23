"""Streamlit-based web UI for the HTML Email Client Agent.

This module provides a browser-based interface for sending bulk HTML email
newsletters. Users can configure SMTP settings, authenticate with their email
provider (Gmail or custom), compose messages, upload HTML templates, and send
to multiple recipients in a single session.

Dependencies:
    streamlit: Web application framework for building the UI.
    pymail_html: Core email sending logic (HTML parsing, SMTP delivery).
    env: Project configuration and runtime settings.

Configuration:
    Requires an ``env.py`` module in the project root with the following
    global settings:

    Attributes:
        RECEIVERS_LIMIT (int): Maximum number of recipients per bulk send.
        SMTP_HOST (str): SMTP server hostname (e.g. ``smtp.gmail.com``).
        SMTP_PORT (int): SMTP server port (typically 465 for SSL, 587 for TLS).
        SMTP_PORTS (tuple): Available port options for the UI selector.
        SENDER_EMAIL (str): Default sender email address.
        RECEIVER_EMAIL (str): Default recipient email address.
        RECIEVERS_LIST (list): List of recipient email addresses.
        EMAIL_SUBJECT (str): Default email subject line.
        HTML_FILENAME (str): Default HTML template filename.
        SSL_CONTEXT (ssl.SSLContext): SSL context for secure SMTP connections.

Example:
    Run the application from the command line::

        $ streamlit run streamlit_email.py

    The UI will open in the default browser. Configure SMTP and credentials,
    upload an HTML template, and click "Send Email" to deliver to all recipients.

Note:
    For Gmail, use an App Password rather than the account password when
    2-Step Verification is enabled. See https://support.google.com/accounts/answer/185833
"""

from io import StringIO

import streamlit as st

import env
import pymail_html as ph

# -----------------------------------------------------------------------------
# Application header and branding
# -----------------------------------------------------------------------------
APP_TITLE = st.title('BULK E-MAIL SENDING AGENT')
HEAD_TITLE = st.header(
    'Send bulk HTML email newsletters using your own email provider or gmail as default.'
)

# -----------------------------------------------------------------------------
# SMTP server configuration
# Users select host and port for their email provider (Gmail, custom, etc.)
# -----------------------------------------------------------------------------
st.header('SMTP Settings')
SMTP_HOST = st.text_input("SMTP HOST", 'smtp.gmail.com', placeholder='smtp.gmail.com')
SMTP_PORT = int(st.selectbox(label='SMTP PORT', options=env.SMTP_PORTS))

# -----------------------------------------------------------------------------
# Email authentication
# Sender address and password (or App Password for Gmail with 2FA)
# -----------------------------------------------------------------------------
st.header('Email connection setup')
env.SENDER_EMAIL = st.text_input("Enter Your E-Mail Address", '', placeholder='john@doe.com')
ph.EMAIL_PASSWORD = st.text_input('Enter Your E-mail Password', '', placeholder='password')

# -----------------------------------------------------------------------------
# Message composition
# Subject line and comma-separated recipient list with validation
# -----------------------------------------------------------------------------
st.header('Compose Your Message')
env.EMAIL_SUBJECT = st.text_input("Subject", '', placeholder='Re: Free promotional phone')
env.RECIEVERS_LIST = st.text_input(
    "Recievers", '', placeholder='example@nano.com, jane@doe.com, john@doe.com'
).split(',')
if len(env.RECIEVERS_LIST) > env.RECEIVERS_LIMIT or len(env.RECIEVERS_LIST) <= 0:
    ERROR_MESSAGE = '<p style="font-family:Courier; color:Red; font-size: 20px;">Please enter 1 to 20 receivers</p>'
    st.markdown(ERROR_MESSAGE, unsafe_allow_html=True)
print(env.RECIEVERS_LIST)

# -----------------------------------------------------------------------------
# HTML template upload
# Decode uploaded file to UTF-8 string for pymail_html processing
# -----------------------------------------------------------------------------
HTML = st.file_uploader("Upload HTML E-mail Template file")
if HTML:
    st.write("file uploaded")
    stringio = StringIO(HTML.getvalue().decode("utf-8"))
    HTML = stringio.read()

# -----------------------------------------------------------------------------
# Send action
# Iterates over recipients and dispatches via pymail_html.send_html_email
# -----------------------------------------------------------------------------
if st.button('Send Email'):
    try:
        for receiver in env.RECIEVERS_LIST:
            ph.send_html_email(receiver_email=receiver.strip(), html_doc=HTML)
        st.write('Message Sent')
    except Exception as e:
        st.write(f'ERROR: {e}')
