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

def send_bahnhof_gif(client, update: WhatsAppUpdate):
    #im_bytes = update.message.photo[-1].get_file().download_as_bytearray()

    im_file = BytesIO(im_bytes)  # convert image to file-like object
    im1 = Image.open(im_file)   # img is now PIL Image object
    im2 = Image.open('assets/bahnhof_alt.jpg')

    gif = utils.generate_gif(im1, im2)

    # TODO send gif
    #update.message.reply_document(gif)

def eval_schaetzfrage_bahnhof(client, update: WhatsAppUpdate):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 106
    if schaetzung == echter_wert:
        client.messages.create(
            body='Nicht schlecht! (Das ist brandenburgisch für "gut gemacht!") 😉',
            from_='whatsapp:+14155238886',
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.2 and schaetzung <= echter_wert+echter_wert*0.2:
        client.messages.create(
            body='Du bist schon nah dran!',
            from_='whatsapp:+14155238886',
            to=update.From
        )
    else:
        client.messages.create(
            body='Nicht ganz!',
            from_='whatsapp:+14155238886',
            to=update.From
        )

def eval_schaetzfrage_reiherberg(client, update: WhatsAppUpdate):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 68
    if schaetzung == echter_wert:
        client.messages.create(
            body='Richtig!'.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.1 and schaetzung <= echter_wert+echter_wert*0.1:
        client.messages.create(
            body='Fast!'.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )
    else:
        client.messages.create(
            body='Knapp daneben!'.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )

def eval_kirche_wortraetsel(client, update: WhatsAppUpdate):
    antwort = update.Body
    echter_wert = "Kaiser-Friedrich-Kirche"

    if re.sub('\W+', '', antwort.lower()) == re.sub('\W+', '', echter_wert.lower()):
        client.messages.create(
            body='Richtig!'.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )
    else:
        client.messages.create(
            body='Fast!'.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )

def eval_storchenbank(client, update: WhatsAppUpdate):
    antwort = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 2012
    if antwort.lower() == echter_wert:
        client.messages.create(
            body='Du hast die Tafel also entdeckt! Dort werden die Rückkehrzeiten und der Nachwuchs des Storchenpaares festgehalten.'.format(
                name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )
    else:
        client.messages.create(
            body='Fast! Neben der Storchenbank findest du eine Tafel, auf der die Rückkehrzeiten und der Nachwuchs des Storchenpaares festgehalten werden.'.format(
                name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )

def reiherberg_medaille(client, update: WhatsAppUpdate):
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
    from_='whatsapp:+14155238886',
    to=update.From
)

def eval_quiz(client, update: WhatsAppUpdate, correct_option_id:int, correct_answer_text:str, wrong_answer_text:str, correct_answer_sticker=None):
    if update.Body == [correct_option_id]:
        # if correct_answer_sticker:
        #    update.poll_answer.user.send_sticker(correct_answer_sticker)
        client.messages.create(
            body=correct_answer_text.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )
    else:
        client.messages.create(
            body=wrong_answer_text.format(name=update.ProfileName),
            from_='whatsapp:+14155238886',
            to=update.From
        )

action_functions = {"send_bahnhof_gif": send_bahnhof_gif,
                    "eval_schaetzfrage_bahnhof": eval_schaetzfrage_bahnhof,
                    "eval_schaetzfrage_reiherberg": eval_schaetzfrage_reiherberg,
                    "eval_kirche_wortraetsel": eval_kirche_wortraetsel,
                    "eval_storchenbank": eval_storchenbank,
                    "reiherberg_medaille": reiherberg_medaille,
                    "eval_quiz": eval_quiz
                    }