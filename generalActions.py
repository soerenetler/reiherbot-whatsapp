def start_name(client, update):

    client.messages.create(
                              body='Hi, ich bin Ronni der Reiher! Ich führe dich heute durch Golm.',
                              from_='whatsapp:+14155238886',
                              to=update["From"]
                          )
    client.messages.create(
                              body='Darf ich dich {name} nennen?'.format(name=update["ProfileName"]),
                              from_='whatsapp:+14155238886',
                              to=update["From"]
    )
    return "NAME"

def name_startpunkt(client, update):
        client.messages.create(
                              body='Super!',
                              from_='whatsapp:+14155238886',
                              to=update["From"]
                          )
        client.messages.create(
                              body='Unsere Reise startet am Bahnhof Golm. Ich warte direkt vor dem orangen Bahnhofsgebäude auf dich. 🚉',
                              from_='whatsapp:+14155238886',
                              to=update["From"]
                          )
        client.messages.create(
                              body='Bist du auch schon dort?',
                              from_='whatsapp:+14155238886',
                              to=update["From"]
                          )

        return "STARTPUNKT"

def name_frage(client, update):
        client.messages.create(
                              body='Wie darf ich dich nennen?',
                              from_='whatsapp:+14155238886',
                              to=update["From"]
                          )
        return "NAME_AENDERN"
                        
generalActions={"start_name": start_name,
                "name_startpunkt": name_startpunkt,
                "name_frage": name_frage}
