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
                              body=item["text"],
                              from_='whatsapp:+14155238886',
                              to=update.From
                          )
            elif item["type"]=="venue":
                client.messages.create(
                              body=item["title"],
                              persistent_action=['geo:{},{}}|{}'.format(item["latitude"], item["longitude"], item["address"])],
                              from_='whatsapp:+14155238886',
                              to=update.From
                          )
            elif item["type"]== "return":
                return item["state"]