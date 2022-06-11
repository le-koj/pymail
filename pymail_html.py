# Import modules
import smtplib, ssl

# import environment variables
import env, secrets

## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the HTML document
HTML = ''

# Set up the email addresses and password.
email_sender: str = env.EMAIL_ADDRESS
email_password: str = secrets.EMAIL_PASSWORD
email_receiver: list = env.EMAIL_RECEIVERS

# Set email SSL
context = ssl.create_default_context()

def html_email() -> str:
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
    mail['To'] = ", ".join(email_receiver)
    mail['Subject'] = f'KB Capital campaign'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    mail.attach(MIMEText(HTML, "html"))
    # Convert it as a string
    email_string = mail.as_string()
    
    return email_string
    
def send_email() -> None:
    """Log into the stmp server and send the generated email content
    """
    email_string = html_email()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email_string)
    
    print(f'Mail delivered')
    

if __name__  == "__main__":
    send_email()