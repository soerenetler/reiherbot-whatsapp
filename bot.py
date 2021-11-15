from generateStates import CommandHandler, read_state_yml
from generateActions import read_action_yaml
from WhatsAppUpdate import WhatsAppUpdate
from flask import Flask, request, Response

import os
from twilio.rest import Client

from collections import defaultdict

from actions import reiherbergActions, en_reiherbergActions, writeActions, generalActions


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = Flask(__name__)


def constant_factory(value):
    return lambda: value


user_states = defaultdict(constant_factory("START"))
user_context = defaultdict(dict)

general_actions = read_action_yaml("actions/general.yml", action_functions={
                                         **generalActions.action_functions, **reiherbergActions.action_functions, **writeActions.action_functions})
reiherberg_actions = read_action_yaml("actions/reiherberg.yml", action_functions={
                                         **reiherbergActions.action_functions, **writeActions.action_functions})
en_reiherberg_actions = read_action_yaml("actions/en_reiherberg.yml", action_functions={
                                         **en_reiherbergActions.action_functions, **writeActions.action_functions})

prechecks = [CommandHandler('cancel', general_actions["cancel"]),
             CommandHandler('start', general_actions["start"]),
                ]

general_handler = read_state_yml("states/general.yml", actions={**general_actions, **reiherberg_actions, **en_reiherberg_actions}, prechecks=prechecks)
reiherberg_handler = read_state_yml("states/reiherberg.yml", actions={**general_actions, **reiherberg_actions, **en_reiherberg_actions}, prechecks=prechecks)
en_reiherberg_handler = read_state_yml("states/en_reiherberg.yml", actions={**general_actions, **reiherberg_actions, **en_reiherberg_actions}, prechecks=prechecks)

states_handler = {**general_handler, 
                  **reiherberg_handler,
                  **en_reiherberg_handler}


@app.route('/bot', methods=['POST'])
def bot():
    print(request.values)
    update = WhatsAppUpdate(**request.values)
    icoming_state = user_states[update.From]
    context = user_context[update.From]

    print("Current context: {}".format(context))
    print("Current state: {}".format(icoming_state))

    for handler in states_handler[icoming_state]:
        print("Filter Eval: {}".format(handler))
        if handler.check_update(update):
            print("Filter True: {}".format(handler))
            new_state = handler.callback(client, update, context)
            if new_state:
                user_states[update.From] = new_state
            break
    return Response(status=200)

if __name__ == '__main__':
    app.run()