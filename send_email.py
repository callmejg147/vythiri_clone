import os
import smtplib
from ssl import create_default_context
import sys
from email.message import EmailMessage

reciever = f"{sys.argv[1]}"
# sending an email to the customer
email_sender = "jithin.dev.work@gmail.com"
password = f"{sys.argv[2]}"

email_reciever = reciever

subject = "vythiri reservation"
body = '''
We have recieved your reservation request. Our staff will contact you regarding further details.
please feel free to explore our resort at our website: vythiri-clone.onrender.com
'''

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciever
em['Subject'] = subject
em.set_content(body)

context = create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    # mail login
    server.login(email_sender,password)
    # send mail with from, to and content
    server.sendmail(email_sender,email_reciever,em.as_string())

