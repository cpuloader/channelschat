from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from authentication.models import Account
from chat.filter import rebuild_text


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
    members = models.ManyToManyField(Account, related_name='rooms')

    def __unicode__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    author = models.ForeignKey(Account)
    checked = models.BooleanField(default=False)

    def __unicode__(self):
        return '[{timestamp}] {author}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%A, %d. %B %Y %I:%M%p')
    
    def as_dict(self):
        return {'room': self.room.pk, 
                'message': self.message, 
                'timestamp': self.timestamp.isoformat(),
                'id': self.pk,
                'author': self.author.as_dict(),
                'checked': self.checked
               }