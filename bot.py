from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

import os
from twilio.rest import Client

from collections import defaultdict


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = Flask(__name__)

def constant_factory(value):
    return lambda: value

usser_states = defaultdict(constant_factory("START"))

@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    incoming_msg = request.values.get('Body', '').lower()
    incoming_from = request.values.get('From')

    state = usser_states.get(incoming_from, "START")

    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    
    message = client.messages.create(
                              body='Hello there!',
                              from_='whatsapp:+14155238886',
                              to=incoming_from
                          )
    return message


if __name__ == '__main__':
    app.run()