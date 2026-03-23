"""HTML Email Client Agent User Interface

This script creates a web browser based user interface
for the HTML Email Client Agent.

This script requires the streamlit app framework, and
the python io module.

This script needs 1 personal file:
    env.py - which has the following global settings:
        
        RECEIVERS_LIMIT = 20
        
        SMTP_HOST: str = 'smtp.gmail.com'
        SMTP_PORT: int = 465
        SMTP_PORTS: tuple = (465, 25, 26, 587, 2525)

        SENDER_EMAIL: str = 'example@domain.com'
        RECEIVER_EMAIL: str = 'example@example.com'
        RECIEVERS_LIST: list = []
        EMAIL_SUBJECT: str = ''
        HTML_FILENAME: str = 'my_newsletter.html'
        
        SSL_CONTEXT = ssl.create_default_context()
        
"""

from io import StringIO
import pymail_html as ph
import streamlit as st

# import environment variables
import env

# App title and heading section
APP_TITLE = st.title('BULK E-MAIL SENDING AGENT')
HEAD_TITLE = st.header(
    'Send bulk HTML email newsletters using your own email provider or gmail as default.'
    )

# SMTP settings section
st.header('SMTP Settings')
SMTP_HOST = st.text_input("SMTP HOST", 'smtp.gmail.com', placeholder='smtp.gmail.com')
SMTP_PORT = int(st.selectbox(label='SMTP PORT', options=env.SMTP_PORTS))

# Email settings section
st.header('Email connection setup')
env.SENDER_EMAIL = st.text_input("Enter Your E-Mail Address", '', placeholder='john@doe.com')
ph.EMAIL_PASSWORD = st.text_input('Enter Your E-mail Password', '', placeholder='password')

# Email composition section
st.header('Compose Your Message')
env.EMAIL_SUBJECT = st.text_input("Subject", '', placeholder='Re: Free promotional phone')
env.RECIEVERS_LIST = st.text_input("Recievers", '', placeholder='example@nano.com, jane@doe.com, john@doe.com').split(',')
if len(env.RECIEVERS_LIST) > env.RECEIVERS_LIMIT or len(env.RECIEVERS_LIST) <= 0:
    ERROR_MESSAGE = '<p style="font-family:Courier; color:Red; font-size: 20px;">Please enter 1 to 20 receivers</p>'
    st.markdown(ERROR_MESSAGE, unsafe_allow_html=True)
print(env.RECIEVERS_LIST)

# Get html file and convert to string format
HTML = st.file_uploader("Upload HTML E-mail Template file")
if HTML:
    st.write("file uploaded")
    stringio = StringIO(HTML.getvalue().decode("utf-8"))
    HTML = stringio.read()

# Setup send button
if st.button('Send Email'):
    try:
        for receiver in env.RECIEVERS_LIST:
            ph.send_html_email(receiver_email=receiver, html_doc=HTML)
        st.write('Message Sent')
    except Exception as e:
        st.write(f'ERROR: {e}')
else:
    pass
