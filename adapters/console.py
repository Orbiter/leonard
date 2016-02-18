"""
# ADAPTER CURRENTLY NOT WORKING. USE TELEGERAM ADAPTER.
# Config (valid YAML document) must be at __doc__.
name: console # Name of adapter, lowercase, match with
              # file or package name.
description: "Example adapter for testing bot."
config:                          # Config variable that needed to set
  LEONARD_EXAMPLE_VARIABLE: 'aa' # in environment.
                                 # You can set default values after colon.
"""
from os import getlogin
from time import sleep
from random import randint
from leonard.adapter import IncomingMessage, Attachment

# Code running on adapter loading may be here


def get_messages(bot):
    while True:
        # Let plugin thread end
        sleep(1)
        text = input('Enter message: ')

        attachments = []
        # For our example, attachment will be looking like:
        # '[type]_[path]'
        received_attachments = input(
            'Enter a comma-separated attachments'
            '(<type>_<path>):'
        ).split(',')

        # If user don't enter attachment,
        # message_attachments will be empty
        if received_attachments[0]:
            for attachment in received_attachments:
                # Parse incoming attachment:
                # attachment_data[0] will be attachment type
                # attachment_data[1] will be attachment path
                attachment_data = attachment.split('_')
                if len(attachment_data) < 2:
                    print('Incorrect attachment "{}"'.format(attachment))
                    continue
                attachments.append(Attachment(
                    attachment_type=attachment_data[0],
                    attachment_path=attachment_data[1:],
                    attachment_id=randint(1, 1000000000)  # Fake id
                ))
        yield IncomingMessage(adapter_id='console' + str(hash(getlogin())),
                              language=bot.config.get(
                                  'LEONARD_DEFAULT_LANGUAGE',
                                  'en'
                              ),
                              text=text, attachments=attachments,
                              variables={
                                  'first_name': 'John',
                                  'last_name': 'Doe'
                              })
    return []


def send_message(message, bot):
    print('BOT: ', message.text)
    print(message.recipient.data)
    print('Attachments:')
    for attachment in message.attachments:
        print(attachment.id)
        print(attachment.type)
        print(attachment.path)
        print(attachment.text)
