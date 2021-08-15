from flask import Flask, request

import os
from twilio.rest import Client

from generalActions import generalActions

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
    WhatsAppUpdate(**request.values)
    incoming_msg = request.values.get('Body', '').lower()
    incoming_from = request.values.get('From')
    incoming_ProfileName = request.values.get('ProfileName')
    icoming_state = usser_states[incoming_from]

    state = usser_states.get(incoming_from, "START")

    states_handler = {"START": [("hi", generalActions["start_name"])],
                      "NAME": [("ja", generalActions["name_startpunkt"]),
                               ("nein", generalActions["name_frage"])],
                      "STARTPUNKT": [("ja", generalActions["welche_route"]),
                                     ("nein", generalActions["weg_zum_bahnhof"])],
                      "ROUTE_AUSWAEHLEN": [("ja", generalActions["start_name"])]

    }

    for filter, action in states_handler[icoming_state]:
        if incoming_msg == filter:
            new_state = action(client, request.values)
            usser_states[incoming_from] = new_state


if __name__ == '__main__':
    app.run()


class WhatsAppUpdate:

#CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('SmsMessageSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('NumMedia', '0'), ('ProfileName', 'Sören'), ('SmsSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('WaId', '4917652163847'), ('SmsStatus', 'received'), ('Body', 'Hi'), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), ('MessageSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('AccountSid', 'AC8f3944b5604c359ee4e1c882e64765e2'), ('From', 'whatsapp:+4917652163847'), ('ApiVersion', '2010-04-01')])])

    def __init__(self, SmsMessageSid, NumMedia, ProfileName, SmsSid, WaId, SmsStatus, Body, To, NumSegments, MessageSid, AccountSid, From, ApiVersion) -> None:
        self.SmsMessageSid = SmsMessageSid
        self.NumMedia = NumMedia
        self.ProfileName = ProfileName
        self.SmsSid = SmsSid
        self.WaId = WaId
        self.SmsStatus = SmsStatus
        self.Body = Body
        self.To = To
        self.NumSegments = NumSegments
        self.MessageSid = MessageSid
        self.AccountSid = AccountSid
        self.From = From
        self.ApiVersion = ApiVersion
