from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import OutgoingMessageSerializer, AnswerSerializer, IncomingEmbeddingSerializer, QuestionSerializer, ScriptSerializer
from .models import Answer, Question, OutgoingMessage, IncomingEmbedding, Script
from gerund.src.training import script_generation

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

    def retrieve(self, request, pk=None):
        script = Script.objects.get(pk=pk)
        serializer = ScriptSerializer(script)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        script = Script.objects.get(pk=pk)
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def generate_questions(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_potential_questions(script)
            serializer = ScriptSerializer(script.refresh_from_db())
            return Response(serializer.data)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def generate_answers(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_potential_answers(script)
            serializer = ScriptSerializer(script.refresh_from_db())
            return Response(serializer.data)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)
