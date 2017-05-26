import re
import json
import logging
from channels import Group
from channels.sessions import channel_session

from .models import Room
from authentication.models import Account
from .serializers import MessageSerializer
from chat import signals

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, user_id = message['path'].decode('ascii').strip('/').split('/')
        print('room connect:', user_id)
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return

        user = Account.objects.get(pk=user_id)
    except ValueError:
        log.debug('invalid user=%s', user_id)
        return
    except Account.DoesNotExist:
        log.debug('ws user does not exist id=%s', user_id)
        return

    log.debug('chat connect room=%s client=%s:%s', 
        user.pk, message['client'][0], message['client'][1])

    message.reply_channel.send({"accept": True})
    message.channel_session['room'] = user_id
    print('room connect:', user_id)
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-' + str(user_id), channel_layer=message.channel_layer).add(message.reply_channel)

    

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        user_id = message.channel_session['room']
        user = Account.objects.get(pk=user_id)
    except KeyError:
        log.debug('no user in channel_session')
        return
    except Account.DoesNotExist:
        log.debug('recieved message, but user does not exist id=%s', user_id)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    #if set(data.keys()) != set(('handle', 'message', 'room')):
    #    log.debug("ws message unexpected format data=%s", data)
    #    return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            user.user_id, data['message'])
        #a = Account.objects.get(pk=data['author']['id'])
        #m = room.messages.create(handle=data['handle'], message=data['message'], author=a)
        print('room receive:', user_id)
        # See above for the note about Group
        #serializer = MessageSerializer(m)
        #print(serializer.data)
        #Group('chat-' + str(user_id), channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    try:
        user_id = message.channel_session['room']
        user = Account.objects.get(pk=user_id)
        print('room disconnect:', user_id)
        Group('chat-' + str(user_id), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Account.DoesNotExist):
        pass
