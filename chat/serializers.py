from rest_framework import serializers, status
from rest_framework.response import Response
#from rest_framework.pagination import PageNumberPagination

from authentication.serializers import AccountSerializer
from authentication.models import Account
from chat.models import Room, Message
from chat.filter import rebuild_text

class RoomSerializer(serializers.ModelSerializer):
    members = AccountSerializer(many=True, read_only=True, required=False)
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'label', 'members', 'messages')
        read_only_fields = ('id', 'name', 'label')

    #def get_validation_exclusions(self, *args, **kwargs):
    #    exclusions = super(ChatMessageSerializer, self).get_validation_exclusions()
    #    return exclusions + ['author']

class MessageSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Message
        fields = ('id', 'room', 'message', 'timestamp', 'author', 'checked')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        validated_data['message'] = rebuild_text(validated_data.get('message'))
        instance = Message.objects.create(**validated_data)
        return instance