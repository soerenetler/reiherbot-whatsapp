from generateStates import CommandHandler, read_state_yml
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
generalActions = read_action_yaml("actions/general.yml")
reiherberglActions = read_action_yaml("actions/reiherberg.yml")
en_reiherbergActions = read_action_yaml("actions/en_reiherberg.yml")

prechecks = [CommandHandler('cancel', generalActions["cancel"]),
             CommandHandler('start', generalActions["start_name"]),
                ]

general_handler = read_state_yml("states/general.yml", actions={**generalActions, **reiherberglActions, **en_reiherbergActions}, prechecks=prechecks)
reiherberg_handler = read_state_yml("states/reiherberg.yml", actions={**generalActions}, prechecks=prechecks)
en_reiherberg_handler = read_state_yml("states/en_reiherberg.yml", actions={**generalActions}, prechecks=prechecks)

states_handler = {**general_handler, 
                  **reiherberg_handler,
                  **en_reiherberg_handler}


@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    update = WhatsAppUpdate(**request.values)
    icoming_state = user_states[update.From]
    print("Current state: {}".format(icoming_state))

    for filter, action in states_handler[icoming_state]:
        print("Filter Eval: {}".format(filter))
        if update.Body == filter:
            print("Filter True: {}".format(filter))
            new_state = action(client, update)
            user_states[update.From] = new_state


if __name__ == '__main__':
    app.run()