import random
import string
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from haikunator import Haikunator

from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from .permissions import IsMemberOfRoom, IsAuthorOfMessage
from authentication.models import Account

haikunator = Haikunator()

def about(request):
    return render(request, "chat/about.html")

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)

def chat_room(request, label):
    """
    Room view - show the room, with latest messages.

    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by('-timestamp')
    serializer_class = MessageSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),) #IsAuthenticated(),) 
        return (permissions.IsAuthenticated(),)    #IsAuthenticated(),

    def perform_create(self, serializer):
        #print("user id: ", self.request.user.id)
        #print(self.request.data)
        instance = serializer.save(author_id=self.request.user.id)
        return super(MessagesViewSet, self).perform_create(serializer)


class RoomsViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def paginate_queryset(self, queryset, view=None): # turn off pagination
        return None

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(), )
        return (permissions.IsAuthenticated(), IsMemberOfRoom(),)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #print(self.request.data)
        if len(self.request.data['members']) == 2:
            user1_id = self.request.data['members'][0]['id']
            user2_id = self.request.data['members'][1]['id']
            #print(user1, user2)
            try:                  # trying to find room with only two exact users
                instance = list(Room.objects.annotate(members_count=Count('members')) \
                          .filter(members_count=2).filter(members__id=user1_id) \
                          .filter(members__id=user2_id))
                if len(instance) == 1:  # found one
                    serializer = self.get_serializer(instance[0])
                    return Response(serializer.data)
                else:
                    raise(ObjectDoesNotExist)

            except ObjectDoesNotExist:      # if didn't find, create new room
                print('no results, creating new')
                member1_pk = user2 = self.request.data['members'][0]['id']
                member2_pk = user2 = self.request.data['members'][1]['id']
                new_chat = Room.objects.create(label = haikunator.haikunate())
                new_chat.members = [member1_pk, member2_pk]
                serializer = self.get_serializer(new_chat)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.members.count() > 1:
            instance.members.remove(self.request.user)
            instance.save()
        else:
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomMessagesViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('room').order_by('timestamp')
    serializer_class = MessageSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.IsAuthenticated(),)
        return (permissions.IsAuthenticated(), IsAuthorOfMessage(),)
    
    def get_queryset(self):
        queryset = self.queryset.filter(room__id=self.kwargs['room_pk'])
        return queryset