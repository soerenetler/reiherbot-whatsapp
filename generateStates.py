from typing import List
from telegram import Update
import yaml
from WhatsAppUpdate import WhatsAppUpdate

def read_state_yml(filename, actions={}, prechecks:List=[]):
    with open(filename) as file:
        yaml_dict = yaml.load(file)

    states_dict = {}

    for state, handlers in yaml_dict.items():
        handler_list = prechecks[:]
        for handler in handlers:
            if handler["handler"] == "MessageHandler":
                if handler["filter"] == "regex":
                    newHandler = MessageHandler(RegexFilter(handler["regex"]), actions[handler["action"]])
                elif handler["filter"] == "text":
                    newHandler = MessageHandler(TextFilter, actions[handler["action"]])
            elif handler["handler"] == "CommandHandler":
                newHandler = CommandHandler(handler["command"], actions[handler["action"]])
            elif handler["handler"] == "TypeHandler":
                if handler["type"] == "Update":
                    type_ = WhatsAppUpdate
                newHandler = TypeHandler(type_, actions[handler["action"]])
                
            handler_list.append(newHandler)

        states_dict[state]= handler_list

    return states_dict

class MessageHandler:
    def __init__(self, filters, callback):
        self.filters = filters
        self.callback = callback

    def check_update(self, update: WhatsAppUpdate):
        return self.filters(update)

class CommandHandler:
    def __init__(self, command, callback):
        self.command = command
        self.callback = callback

    def check_update(self, update: WhatsAppUpdate):
        text_list = update.Body.split()
        if text_list[0].lower() == "/" + self.command:
            return None
        else:
            return text_list[1:]

class TypeHandler:
    def __init__(self, type_, callback):
        self.type_ = type_
        self.callback = callback

    def check_update(self, update: WhatsAppUpdate):
        return type(update) is self.type_

class RegexFilter:
    def __init__(self, regex) -> None:
        self.regex = regex

    def __call__(self, update: WhatsAppUpdate) -> bool:
        pass

class TextFilter:
    def __call__(self, update: WhatsAppUpdate) -> bool:
        return update.Body != ""