import pymail_html as ph
import streamlit as st
from io import StringIO

RECEIVERS_LIMIT = 20
SMTP_PORTS = (465, 25, 26, 587, 2525)

APP_TITLE = st.title('MAIL SENDER')
HEAD_TITLE = st.header('Send HTML emails to multiple recipients')

SMTP_TITLE = st.header('SMTP Settings')
SMTP_HOST = st.text_input("SMTP HOST", 'smtp.gmail.com')
SMTP_PORT = int(st.selectbox(label='SMTP PORT', options=SMTP_PORTS))

st.header('Email connection setup')
ph.email_sender = st.text_input("Enter Your E-Mail Address", 'john@doe.com')
ph.email_password = st.text_input('Enter Your E-mail Connection Password', 'yMKoi09DBwbc')

st.header('Compose Your Message')
ph.email_subject = st.text_input("Subject", 'Re: Free promotional phone')

ph.email_receiver = st.text_input("Recievers", 'example@nano.com, jane@doe.com, john@doe.com').split(',')
if len(ph.email_receiver) > 20 or len(ph.email_receiver) <= 0:
    error_message = '<p style="font-family:Courier; color:Red; font-size: 20px;">Please enter 1 to 20 receivers</p>'
    st.markdown(error_message, unsafe_allow_html=True)
print(ph.email_receiver)

ph.HTML = st.file_uploader("Upload HTML E-mail Template file")

if ph.HTML:
    st.write("file uploaded")
    stringio = StringIO(ph.HTML.getvalue().decode("utf-8"))
    ph.HTML = stringio.read()

if st.button('Send Email'):
    try:
        for receiver in ph.email_receiver:
            ph.send_email(subject=ph.email_subject, receiver=receiver)
        st.write('Message Sent')
    except Exception as e:
        st.write(f'ERROR: {e}')
else:
    pass
