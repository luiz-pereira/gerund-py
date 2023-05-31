from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ChatSerializer, MessageSerializer, PersonSerializer
from .models import Chat, Message, Person

# Create your views here.

class ChatView(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
