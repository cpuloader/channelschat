from rest_framework import serializers, status
from rest_framework.response import Response
#from rest_framework.pagination import PageNumberPagination

from chat.models import Room, Message


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id', 'name', 'label')
        read_only_fields = ('id',)

    #def get_validation_exclusions(self, *args, **kwargs):
    #    exclusions = super(ChatMessageSerializer, self).get_validation_exclusions()
    #    return exclusions + ['author']

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'room', 'handle', 'message', 'timestamp')
        read_only_fields = ('id',)