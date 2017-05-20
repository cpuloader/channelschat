from django.db.models.signals import post_save
from django.dispatch import receiver

import json
from channels import Group
from .models import Message, Room
#from authentication.models import Account

@receiver(post_save, sender=Message)
def new_message_handler(**kwargs):
    if kwargs['created']:
        message = kwargs['instance']
        room = message.room
        receivers = room.members.all()
        for receiver in receivers:
            if receiver.pk!= message.author.pk:
            #avail_serializer = GameSerializer(avail_game_list, many=True)
                print('signal to ', receiver.pk);
                Group('chat-' + str(receiver.pk)).send({'text': json.dumps(message.as_dict())})