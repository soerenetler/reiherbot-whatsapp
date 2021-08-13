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
generalActions={"start_name": start_name}
