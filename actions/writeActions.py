from WhatsAppUpdate import WhatsAppUpdate
import boto3
from datetime import datetime
import os
from configparser import ConfigParser
import requests

config = ConfigParser()
config.read("config.ini")

session = boto3.session.Session()
client = session.client('s3',
                        region_name=config["space"]["region_name"],
                        endpoint_url=config["space"]["endpoint_url"],
                        aws_access_key_id=os.getenv('SPACES_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET'))


def write_photo(client, update: WhatsAppUpdate, bucket, folder):
    user_id = update.effective_user.id
    name = update.effective_user.name
    update.MediaUrl0

    client.put_object(Bucket=bucket,
                      Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.jpg',
                      Body= requests.get(update.MediaUrl0, allow_redirects=True),
                      ACL='private',
                      #Metadata={
                      #    'x-amz-meta-my-key': 'your-value'
                      #}
                      )

def write_message(client, update: WhatsAppUpdate, bucket, folder):
    user_id = update.WaId
    name = update.ProfileName
    message = update.Body

    client.put_object(Bucket=bucket,
                      Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.txt',
                      Body=message,
                      ACL='private',
                      #Metadata={
                      #    'x-amz-meta-my-key': 'your-value'
                      #}
                      )

def write_voice(client, update: WhatsAppUpdate, bucket, folder):
    user_id = update.WaId
    name = update.ProfileName

    client.put_object(Bucket=bucket,
                    Key= folder + "/" + str(datetime.now())+"_"+str(user_id) + "_" + name + '.mp3',
                    Body=requests.get(update.MediaUrl0, allow_redirects=True),
                    ACL='private',
                    #Metadata={
                    #    'x-amz-meta-my-key': 'your-value'
                    #}
                    )

def write(client, update: WhatsAppUpdate, bucket, folder):
    if update.MediaContentType0.startswith("audio"):
        write_voice(client, update, bucket, folder)
    elif update.MediaContentType0.startswith("image"):
        write_photo(client, update, bucket, folder)
    elif update.Body!= "":
        write_message(client, update, bucket, folder)
    else:
        raise NotImplementedError("This type of update can not be saved")

action_functions = {"write_photo": write_photo,
                    "write_message": write_message,
                    "write_voice": write_voice,
                    "write": write
                    }