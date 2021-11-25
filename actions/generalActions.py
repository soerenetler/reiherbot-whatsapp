import logging

from WhatsAppUpdate import WhatsAppUpdate

import mongoengine
import datetime
import os

from actions.utils import log

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
user_dbname = "reiherbot_whatsapp_user"
interaction_dbname = "reiherbot_whatsapp_interaction"
with open("ca-certificate.crt", "w") as text_file:
            text_file.write(os.getenv('DATABASE_CERT'))
mongoengine.connect(alias=user_dbname, host="mongodb+srv://"+ os.getenv("DATABASE_USERNAME")+":"+ os.getenv("DATABASE_PASSWORD") + "@" +os.getenv("DATABASE_HOST") +"/"+user_dbname+"?authSource=admin&tls=true&tlsCAFile=ca-certificate.crt")
mongoengine.connect(alias=interaction_dbname, host="mongodb+srv://"+ os.getenv("DATABASE_USERNAME")+":"+ os.getenv("DATABASE_PASSWORD") + "@" +os.getenv("DATABASE_HOST") +"/"+interaction_dbname+"?authSource=admin&tls=true&tlsCAFile=ca-certificate.crt")

class User(mongoengine.Document):
    user_id = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True, max_length=50)
    username = mongoengine.StringField(max_length=50)
    entry_time = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'db_alias': user_dbname}

def entry_conversation(client, update: WhatsAppUpdate, context):
    db_user = User(user_id=update.WaId, name=update.ProfileName, username=update.From)
    db_user.save()
    context["user_id"] = db_user
    
def default_data(client, update: WhatsAppUpdate, context):
    context["daten"] = False

def default_name(client, update: WhatsAppUpdate, context):
    context["name"] = update.ProfileName

def change_data(client, update: WhatsAppUpdate, context):
    if update.Body == "Ja" or update.Body == "Ja, klar 🌻" or update.Body == "/Ja":
        context["daten"] = True
    else:
        context["daten"] = False

def change_name(client, update: WhatsAppUpdate, context):
    context["name"] = update.Body

action_functions = {"change_name": change_name,
                    "change_data": change_data,
                    "default_name": default_name,
                    "default_data": default_data,
                    "entry_conversation": entry_conversation}