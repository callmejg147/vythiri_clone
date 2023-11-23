import twilio
from twilio.rest import Client
import sys
phnum = sys.argv[1]

# send recieved request sms with twilio
acc_sid = 'AC97700204f377ac674556db400c185dbb'
acc_token = 'eed892074009beea30039816f33f0119'
twilio_num = "+14845562616"
reciever = f"+91{phnum}"

client = Client(acc_sid,acc_token)
message = client.messages.create(
    body="Greetings from Vythiri Resorts,"
         "We have recieved your reservation request. An operator will contact you for further proceedures.",
    from_=twilio_num,
    to=reciever
    )