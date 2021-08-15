from generateActions import read_action_yaml
from WhatsAppUpdate import WhatsAppUpdate
from flask import Flask, request

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


user_states = defaultdict(constant_factory("START"))
generalActions = read_action_yaml("general.yml")

@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    update = WhatsAppUpdate(**request.values)
    icoming_state = user_states[update.From]
    print("Current state: {}".format(icoming_state))

    states_handler = {"START": [("hi", generalActions["start_name"])],
                      "NAME": [("ja", generalActions["name_startpunkt"]),
                               ("nein", generalActions["name_frage"])],
                      "STARTPUNKT": [("ja", generalActions["welche_route"]),
                                     ("nein", generalActions["weg_zum_bahnhof"])],
                      "ROUTE_AUSWAEHLEN": [("ja", generalActions["start_name"])]

                      }
                      
    for filter, action in states_handler[icoming_state]:
        print("Filter Eval: {}".format(filter))
        if update.Body == filter:
            print("Filter True: {}".format(filter))
            new_state = action(client, update)
            user_states[update.From] = new_state


if __name__ == '__main__':
    app.run()