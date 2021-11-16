from WhatsAppUpdate import WhatsAppUpdate
from PIL import Image
import re

from io import BytesIO

from actions import utils
from actions.utils import log

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

logger = logging.getLogger(__name__)

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

def eval_schaetzfrage_bahnhof(client, update: WhatsAppUpdate, context):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 106
    if schaetzung == echter_wert:
        client.messages.create(
            body='Not bad! You nailed it 😉',
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.2 and schaetzung <= echter_wert+echter_wert*0.2:
        client.messages.create(
            body='That is close!',
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    else:
        client.messages.create(
            body='Not quite right!',
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )

def eval_schaetzfrage_reiherberg(client, update: WhatsAppUpdate, context):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 68
    if schaetzung == echter_wert:
        client.messages.create(
            body='Correct!'.format(name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.1 and schaetzung <= echter_wert+echter_wert*0.1:
        client.messages.create(
            body='Close!'.format(name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    else:
        client.messages.create(
            body='Not quite right!'.format(name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )

def eval_kirche_wortraetsel(client, update: WhatsAppUpdate, context):
    antwort = update.Body
    echter_wert = "Kaiser-Friedrich-Kirche"

    if re.sub('\W+', '', antwort.lower()) == re.sub('\W+', '', echter_wert.lower()):
        client.messages.create(
            body='Richtig!'.format(name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    else:
        client.messages.create(
            body="No, that's not the correct answer!".format(name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )

def eval_storchenbank(client, update: WhatsAppUpdate, context):
    antwort = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 2012
    if antwort.lower() == echter_wert:
        client.messages.create(
            body='You found the board! All the return dates and the litter of the stork family are marked here.'.format(
                name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )
    else:
        client.messages.create(
            body='Close! Next to the bench there is a board with all the return dates and the litter of the stork family.'.format(
                name=context["name"]),
            from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
            to=update.From
        )

def reiherberg_medaille(client, update: WhatsAppUpdate, context):
    #try:
    #    photo_files = update.from_user.get_profile_photos().photos[0][-1].get_file().download_as_bytearray()
    #    # convert image to file-like object
    #    profile_file = BytesIO(photo_files)
    #    # img is now PIL Image object
    #    background = Image.open(profile_file)
    #    logger.info(background.size)
    #    foreground = Image.open('assets/Skyline_02_gelb.png')

    #    update.message.reply_photo(
    #        utils.overlay_images(background, foreground))
    #except:
    client.messages.create(
    media_url="https://reiherbot-assets.fra1.digitaloceanspaces.com/Skyline_02_gelb.png",
    from_='whatsapp:{}'.format(config["twilio"]["from_number"]),
    to=update.From
)

action_functions = {"eval_schaetzfrage_bahnhof": eval_schaetzfrage_bahnhof,
                    "eval_schaetzfrage_reiherberg": eval_schaetzfrage_reiherberg,
                    "eval_kirche_wortraetsel": eval_kirche_wortraetsel,
                    "eval_storchenbank": eval_storchenbank,
                    "reiherberg_medaille": reiherberg_medaille
                    }