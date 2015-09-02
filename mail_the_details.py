__author__ = 'mullapudi'
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address

# Create message container - the correct MIME type is multipart/alternative.
def send_Email(you,text,subject):
    me='ordershipmentnotification@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).

    # Record the MIME types of both parts - text/plain and text/html.
    part = MIMEText(text, 'plain')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('ordershipmentnotification@gmail.com', 'it26120913')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()