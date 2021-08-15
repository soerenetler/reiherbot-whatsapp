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
            new_state = action(client, WhatsAppUpdate)
            usser_states[incoming_from] = new_state


if __name__ == '__main__':
    app.run()


class WhatsAppUpdate:

    #CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('SmsMessageSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('NumMedia', '0'), ('ProfileName', 'Sören'), ('SmsSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('WaId', '4917652163847'), ('SmsStatus', 'received'), ('Body', 'Hi'), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), ('MessageSid', 'SM1cea0a82154a503875f26e1898d972f2'), ('AccountSid', 'AC8f3944b5604c359ee4e1c882e64765e2'), ('From', 'whatsapp:+4917652163847'), ('ApiVersion', '2010-04-01')])])
    #CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('MediaContentType0', 'image/jpeg'), ('SmsMessageSid', 'MM94942a74f3cfc4fceed98eb6ec1ab15b'), ('NumMedia', '1'), ('ProfileName', 'Sören'), ('SmsSid', 'MM94942a74f3cfc4fceed98eb6ec1ab15b'), ('WaId', '4917652163847'), ('SmsStatus', 'received'), ('Body', ''), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), ('MessageSid', 'MM94942a74f3cfc4fceed98eb6ec1ab15b'), ('AccountSid', 'AC8f3944b5604c359ee4e1c882e64765e2'), ('From', 'whatsapp:+4917652163847'), ('MediaUrl0', 'https://api.twilio.com/2010-04-01/Accounts/AC8f3944b5604c359ee4e1c882e64765e2/Messages/MM94942a74f3cfc4fceed98eb6ec1ab15b/Media/ME1eb56f5a20a667e7f4dc8428c04c1c36'), ('ApiVersion', '2010-04-01')])])
    # CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('Latitude', '52.406563'), ('Longitude', '12.969897'), ('SmsMessageSid', 'SM69ee3cde6532bdcedc2c44b83ee53f41'), ('NumMedia', '0'), ('ProfileName', 'Sören'), ('SmsSid', 'SM69ee3cde6532bdcedc2c44b83ee53f41'), ('WaId', '4917652163847'), ('SmsStatus', 'received'), ('Body', ''), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), ('MessageSid', 'SM69ee3cde6532bdcedc2c44b83ee53f41'), ('AccountSid', 'AC8f3944b5604c359ee4e1c882e64765e2'), ('From', 'whatsapp:+4917652163847'), ('ApiVersio
    def __init__(self, SmsMessageSid, NumMedia, ProfileName, SmsSid, WaId, SmsStatus, Body, To, NumSegments, MessageSid, AccountSid, From, ApiVersion, MediaContentType0=None, MediaUrl0=None, Latitude=None, Longitude=None) -> None:
        self.Latitude = Latitude
        self.Longitude = Longitude
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
        self.MediaContentType0 = MediaContentType0
        self.MediaUrl0 = MediaUrl0
