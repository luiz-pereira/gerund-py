from rest_framework import serializers
from .models import Chat, Message, Person

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'content', 'chat', 'person')

class ChatSerializer(serializers.ModelSerializer):
    message_set = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'message_set')

class PersonSerializer(serializers.ModelSerializer):
    message_set = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('id', 'name', 'message_set')
