from src.fx0post_scraper import fx0post_scraper
from numpy import number
from src.providers import PROVIDERS
from src.pw import email_address, PASSWORD
import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    # Internal model code F30: 335i & F80: M3
    f30 = 'F30'
    f80 = 'F80'
    item = '437M'

    # URLs for f30post & f80post
    F30POST_URL = f'https://f30.bimmerpost.com/forums/forumdisplay.php?f=400'    
    F80POST_URL = f'https://f80.bimmerpost.com/forums/forumdisplay.php?f=584'
    

    # Version 3
    f30_links = fx0post_scraper(f30, F30POST_URL, item)
    f80_links = fx0post_scraper(f80, F80POST_URL, item)

    f30_message = email_message_builder(f30_links)
    f80_message = email_message_builder(f80_links)
    
    # send text
    # receiver_email = number_to_email('3472914973', 'mms')

    # send email
    receiver_email = 'dchapo@gmail.com'

    # send email
    emailer(receiver_email, f30_message)
    emailer(receiver_email, f80_message)

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
    main()
