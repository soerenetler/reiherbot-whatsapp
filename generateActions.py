from WhatsAppUpdate import WhatsAppUpdate
import yaml


def read_action_yaml(filename, action_functions={}):
    with open(filename) as file:
        yaml_dict = yaml.load(file)

    actions_dict = {}

    for key, value in yaml_dict.items():
        actions_dict[key] = Action(value, action_functions=action_functions)

    return actions_dict


class Action():
    def __init__(self, actions, action_functions={}):
        self.actions = actions
        self.action_functions = action_functions

    def __call__(self, client, update: WhatsAppUpdate):
        for item in self.actions:
            if item["type"] == "message":
                client.messages.create(
                    body=item["text"].format(
                        **{"name": update.ProfileName, "echo": update.Body}),
                    from_='whatsapp:+14155238886',
                    to=update.From
                )
            elif item["type"] == "venue":
                client.messages.create(
                    body=item["title"],
                    persistent_action=['geo:{},{}|{}'.format(
                        item["latitude"], item["longitude"], item["address"])],
                    from_='whatsapp:+14155238886',
                    to=update.From
                )
            elif item["type"] == "photo":
                client.messages.create(
                    media_url=item["url"],
                    from_='whatsapp:+14155238886',
                    to=update.From
                )
            elif item["type"] == "audio":
                client.messages.create(
                    media_url=[item["url"]],
                    from_='whatsapp:+14155238886',
                    to=update.From
                )
            elif item["type"] == "poll":
                message = "*" + item["question"] + "*%0a"
                numbers = ["1️⃣ ","2️⃣ ","3️⃣ ","4️⃣ ","5️⃣ ","6️⃣ "]
                for number, option in zip(numbers, item["options"]):
                    message += number + option + "%0a"
                client.messages.create(
                    body=item["question"],
                    from_='whatsapp:+14155238886',
                    to=update.From
                )
            elif item["type"] == "function":
                self.action_functions[item["func"]](client, update)

            elif item["type"] == "return":
                return item["state"]
