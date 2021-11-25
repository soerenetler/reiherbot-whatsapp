import logging
import os
import re
import time
from configparser import ConfigParser
from io import BytesIO

import boto3
import requests
from digitalguide.whatsapp.WhatsAppUpdate import WhatsAppUpdate
from PIL import Image

from actions import utils

config = ConfigParser()
config.read("config.ini")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

session = boto3.session.Session()
s3_client = session.client('s3',
                           region_name=config["space"]["region_name"],
                           endpoint_url=config["space"]["endpoint_url"],
                           aws_access_key_id=os.getenv('SPACES_KEY'),
                           aws_secret_access_key=os.getenv('SPACES_SECRET'))


def send_bahnhof_gif(client, update: WhatsAppUpdate, context):
    if update.MediaUrl0:
        im1_bytes = requests.get(update.MediaUrl0, allow_redirects=True).content

        im1_file = BytesIO(im1_bytes)  # convert image to file-like object
        im1 = Image.open(im1_file)   # img is now PIL Image object

        im2_bytes = requests.get(
            "https://reiherbot-assets.fra1.digitaloceanspaces.com/bahnhof_alt.jpg").content
        im2_file = BytesIO(im2_bytes)  # convert image to file-like object
        im2 = Image.open(im2_file)

        gif = utils.generate_gif(im2, im1)

        time_str = str(round(time.time() * 1000))

        s3_client.put_object(Bucket="reiherbot-whatsapp",
                            Key="bahnhof_gif_gif" + "/" + time_str  + "_" +
                            str(update.WaId) + '.gif',
                            Body=gif,
                            ACL='public-read',
                            ContentType='image/gif'
                            # Metadata={
                            #    'x-amz-meta-my-key': 'your-value'
                            # }
                            )

        client.messages.create(
            media_url="https://reiherbot-whatsapp.fra1.digitaloceanspaces.com/bahnhof_gif_gif/" +
            time_str + "_" + str(update.WaId) + '.gif',
            from_=update.To,
            to=update.From
        )


def eval_schaetzfrage_bahnhof(client, update: WhatsAppUpdate, context):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 106
    if schaetzung == echter_wert:
        client.messages.create(
            body='Nicht schlecht! (Das ist brandenburgisch für "gut gemacht!") 😉',
            from_=update.To,
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.2 and schaetzung <= echter_wert+echter_wert*0.2:
        client.messages.create(
            body='Du bist schon nah dran!',
            from_=update.To,
            to=update.From
        )
    else:
        client.messages.create(
            body='Nicht ganz!',
            from_=update.To,
            to=update.From
        )

    differenz = schaetzung - echter_wert
    if differenz == -1:
        client.messages.create(
            body='Es ist eine Zug mehr als du geschätzt hast',
            from_=update.To,
            to=update.From
        )
    elif differenz < -1:
        client.messages.create(
            body='Es sind {} Züge mehr als du geschätzt hast.'.format(abs(differenz)),
            from_=update.To,
            to=update.From
        )
    elif differenz == 1:
        client.messages.create(
            body='Es ist eine Zug weniger als du geschätzt hast.',
            from_=update.To,
            to=update.From
        )
    elif differenz > 1:
        client.messages.create(
            body='Es sind {} Züge weniger als du geschätzt hast.'.format(abs(differenz)),
            from_=update.To,
            to=update.From
        )


def eval_quiz(client, update: WhatsAppUpdate, context, correct_option_id: str, correct_answer_text: str, wrong_answer_text: str, correct_answer_sticker=None):
    if re.match(correct_option_id, update.Body):
        # if correct_answer_sticker:
        #    update.poll_answer.user.send_sticker(correct_answer_sticker)
        client.messages.create(
            body=correct_answer_text.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )
    else:
        client.messages.create(
            body=wrong_answer_text.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )


def eval_schaetzfrage_reiherberg(client, update: WhatsAppUpdate, context):
    schaetzung = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 68
    if schaetzung == echter_wert:
        client.messages.create(
            body='Richtig!'.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )
    elif schaetzung >= echter_wert-echter_wert*0.1 and schaetzung <= echter_wert+echter_wert*0.1:
        client.messages.create(
            body='Fast!'.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )
    else:
        client.messages.create(
            body='Knapp daneben!'.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )

    differenz = schaetzung - echter_wert
    if differenz == -1:
        client.messages.create(
            body='Es ist eine Meter mehr als du geschätzt hast',
            from_=update.To,
            to=update.From
        )
    elif differenz < -1:
        client.messages.create(
            body='Es sind {} Meter mehr als du geschätzt hast.'.format(abs(differenz)),
            from_=update.To,
            to=update.From
        )
    elif differenz == 1:
        client.messages.create(
            body='Es ist eine Meter weniger als du geschätzt hast.',
            from_=update.To,
            to=update.From
        )
    elif differenz > 1:
        client.messages.create(
            body='Es sind {} Meter weniger als du geschätzt hast.'.format(abs(differenz)),
            from_=update.To,
            to=update.From
        )


def eval_kirche_wortraetsel(client, update: WhatsAppUpdate, context):
    antwort = update.Body
    echter_wert = "Kaiser-Friedrich-Kirche"

    if re.sub('\W+', '', antwort.lower()) == re.sub('\W+', '', echter_wert.lower()):
        client.messages.create(
            body='Richtig!'.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )
    else:
        client.messages.create(
            body='Fast!'.format(name=context["name"]),
            from_=update.To,
            to=update.From
        )


def eval_storchenbank(client, update: WhatsAppUpdate, context):
    antwort = int(re.findall(r"\d{1,}", update.Body)[0])
    echter_wert = 2012
    if antwort == echter_wert:
        client.messages.create(
            body='Du hast die Tafel also entdeckt! Dort werden die Rückkehrzeiten und der Nachwuchs des Storchenpaares festgehalten.'.format(
                name=context["name"]),
            from_=update.To,
            to=update.From
        )
    else:
        client.messages.create(
            body='Fast! Neben der Storchenbank findest du eine Tafel, auf der die Rückkehrzeiten und der Nachwuchs des Storchenpaares festgehalten werden.'.format(
                name=context["name"]),
            from_=update.To,
            to=update.From
        )


def reiherberg_medaille(client, update: WhatsAppUpdate, context):
    # try:
    #    photo_files = update.from_user.get_profile_photos().photos[0][-1].get_file().download_as_bytearray()
    #    # convert image to file-like object
    #    profile_file = BytesIO(photo_files)
    #    # img is now PIL Image object
    #    background = Image.open(profile_file)
    #    logger.info(background.size)
    #    foreground = Image.open('assets/Skyline_02_gelb.png')
    #     update.message.reply_photo(
    #        utils.overlay_images(background, foreground))
    # except:
    client.messages.create(
        media_url="https://reiherbot-assets.fra1.digitaloceanspaces.com/Skyline_02_gelb.png",
        from_=update.To,
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
