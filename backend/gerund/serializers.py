from rest_framework import serializers
from .models import Answer, Question, OutgoingMessages, IncomingEmbeddings

class OutgoingMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingMessages
        fields = ('id', 'content', 'type', 'speech_binary')

class AnswerSerializer(serializers.ModelSerializer):
    outgoing_message_set = OutgoingMessagesSerializer(many=True, read_only=True)
    class Meta:
        model = Answer
        fields = ('id', 'content', 'question')

class IncomingEmbeddingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingEmbeddings
        fields = ('id', 'content', 'type', 'embedding')

class QuestionSerializer(serializers.ModelSerializer):
    incoming_embedding_set = IncomingEmbeddingsSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'content', 'answer')
