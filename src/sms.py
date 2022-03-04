from numpy import number
from providers import PROVIDERS
from pw import email_address, PASSWORD
import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def email_message_builder(urls):
    if 'No sellers' in urls:
        return urls    
    
    message = MIMEMultipart("alternative")
    message["Subject"] = 'BMW Parts found!'
    
    
    email_message = """ """
    for url in urls:
        # email_message += f'{url["title"]}: {url["link"]} | '
        email_message += f'<p><a href={url["link"]}>{url["title"]}</a></p>'
    
    html_message = MIMEText(email_message, 'html')
    message.attach(html_message)

    return message


# Build "email" address out of phone number
def number_to_email(number, text_type):
    gateway = PROVIDERS.get('att').get(text_type)
    if not gateway:
        return f'invalid text type. Please use sms or mms'    
    
    return f'{number}@{gateway}'   


def emailer(receiver_email, message):
    port = 465 # for SSL
    password = PASSWORD
    email = email_address
    # html_message = MIMEText(message, 'html')
    
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        if type(message) == str:
            server.sendmail(email, receiver_email, message)
        else:
            server.sendmail(email, receiver_email, message.as_string())
        print('Message sent!')






if __name__ == '__main__':
    number_to_email()
    emailer()
