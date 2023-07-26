from django.shortcuts import render
from rest_framework import viewsets
from .serializers import OutgoingMessagesSerializer, AnswerSerializer, IncomingEmbeddingsSerializer, QuestionSerializer
from .models import Answer, Question, OutgoingMessages, IncomingEmbeddings

# Create your views here.

class OutgoingVariationView(viewsets.ModelViewSet):
    serializer_class = OutgoingMessagesSerializer
    queryset = OutgoingMessages.objects.all()

class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

class IncomingVariationView(viewsets.ModelViewSet):
    serializer_class = IncomingEmbeddingsSerializer
    queryset = IncomingEmbeddings.objects.all()

class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
