from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Answer, Question, OutgoingMessage, IncomingEmbedding, Script


class OutgoingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingMessage
        fields = ("id", "content", "type", "speech_binary")


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "content", "question")


class IncomingEmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingEmbedding
        fields = ("id", "content", "type", "embedding")


class QuestionSerializer(serializers.ModelSerializer):
    incoming_embeddings = IncomingEmbeddingSerializer(many=True, read_only=True)
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ("id", "content", "answer", "answerable", "incoming_embeddings")


class ScriptSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Script
        fields = (
            "id",
            "name",
            "language_code",
            "custom_prompt",
            "presentation",
            "new_product",
            "questions",
        )
        name = serializers.CharField(
            validators=[UniqueValidator(queryset=Script.objects.all())]
        )
