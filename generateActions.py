from WhatsAppUpdate import WhatsAppUpdate
import yaml

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")


def read_action_yaml(filename, action_functions={}):
    with open(filename) as file:
        yaml_dict = yaml.load(file, Loader=yaml.FullLoader)


    actions_dict = {}

    for key, value in yaml_dict.items():
        actions_dict[key] = Action(value, action_functions=action_functions)

    return actions_dict


class Action():
    def __init__(self, actions, action_functions={}):
        self.actions = actions
        self.action_functions = action_functions

    def __call__(self, client, update: WhatsAppUpdate, context):
        for item in self.actions:
            if item["type"] == "message":
                client.messages.create(
                    body=item["text"].format(
                        **{"name": update.ProfileName, "echo": update.Body}),
                    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
                    to=update.From
                )
            elif item["type"] == "venue":
                client.messages.create(
                    body=item["title"],
                    persistent_action=['geo:{},{}|{}'.format(
                        item["latitude"], item["longitude"], item["address"])],
                    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
                    to=update.From
                )
            elif item["type"] == "photo":
                client.messages.create(
                    media_url=item["url"],
                    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
                    to=update.From
                )
            elif item["type"] == "audio":
                client.messages.create(
                    media_url=[item["url"]],
                    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
                    to=update.From
                )
            elif item["type"] == "poll":
                message = "*" + item["question"] + "*%0a"
                numbers = ["1️⃣ ","2️⃣ ","3️⃣ ","4️⃣ ","5️⃣ ","6️⃣ "]
                for number, option in zip(numbers, item["options"]):
                    message += number + option + "%0a"
                client.messages.create(
                    body=message,
                    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
                    to=update.From
                )
            elif item["type"] == "function":
                arguments = {i:item[i] for i in item if i!='type' and i!='func'}
                self.action_functions[item["func"]](client, update, context, **arguments)

            elif item["type"] == "return":
                return item["state"]
