from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import OutgoingMessageSerializer, AnswerSerializer, IncomingEmbeddingSerializer, QuestionSerializer, ScriptSerializer
from .models import Answer, Question, OutgoingMessage, IncomingEmbedding, Script

# Create your views here.

class OutgoingVariationView(viewsets.ModelViewSet):
    serializer_class = OutgoingMessageSerializer
    queryset = OutgoingMessage.objects.all()

class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

class IncomingVariationView(viewsets.ModelViewSet):
    serializer_class = IncomingEmbeddingSerializer
    queryset = IncomingEmbedding.objects.all()

class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class ScriptView(viewsets.ModelViewSet):
    serializer_class = ScriptSerializer
    queryset = Script.objects.all()

    def partial_update(self, request, pk=None):
        script = Script.objects.get(pk=pk)
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        try:
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)
