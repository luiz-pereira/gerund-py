from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .serializers import (
    OutgoingMessageSerializer,
    AnswerSerializer,
    IncomingEmbeddingSerializer,
    QuestionSerializer,
    QuestionSerializerLite,
    ScriptSerializer,
)
from .models import Answer, Question, OutgoingMessage, IncomingEmbedding, Script
from gerund.src.training import script_generation


class OutgoingVariationView(viewsets.ModelViewSet):
    serializer_class = OutgoingMessageSerializer
    queryset = OutgoingMessage.objects.all()


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class IncomingEmbeddingView(viewsets.ModelViewSet):
    serializer_class = IncomingEmbeddingSerializer
    queryset = IncomingEmbedding.objects.all()


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    @action(detail=True, methods=["post"])
    def generate_variations(self, request, pk=None):
        question = self.get_object()
        try:
            script_generation.generate_question_variations(question)
            question.refresh_from_db()
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)


class ScriptView(viewsets.ModelViewSet):
    serializer_class = ScriptSerializer
    queryset = Script.objects.all()

    def partial_update(self, request, pk=None):
        script = Script.objects.get(pk=pk)
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def initial_pitches(self, request, pk=None):
        initial_pitches = OutgoingMessage.objects.filter(
            script=pk, type="initial_pitch"
        )
        serializer = OutgoingMessageSerializer(initial_pitches.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_initial_pitches(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_initial_pitches(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def questions(self, request, pk=None):
        questions = Question.objects.prefetch_related("answer").filter(script=pk)
        serializer = QuestionSerializerLite(questions.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_questions(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_potential_questions(script)
            script.refresh_from_db()
            serializer = ScriptSerializer(script)
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def generate_questions_variations(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_script_questions_variations(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def generate_answers(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_potential_answers(script)
            script.refresh_from_db()
            serializer = ScriptSerializer(script)
            return Response(serializer.data)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def generate_answers_variations(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_script_answers_variations(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def success_triggers(self, request, pk=None):
        success_triggers = IncomingEmbedding.objects.filter(
            script=pk, type="success_trigger"
        )
        serializer = IncomingEmbeddingSerializer(success_triggers.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_success_triggers(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_success_triggers(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def success_endings(self, request, pk=None):
        success_endings = OutgoingMessage.objects.filter(
            script=pk, type="success_ending"
        )
        serializer = OutgoingMessageSerializer(success_endings.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_success_endings(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_success_endings(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def total_fail_triggers(self, request, pk=None):
        total_fail_triggers = IncomingEmbedding.objects.filter(
            script=pk, type="total_fail_trigger"
        )
        serializer = IncomingEmbeddingSerializer(total_fail_triggers.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_total_fail_triggers(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_total_fail_triggers(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def fail_endings(self, request, pk=None):
        fail_endings = OutgoingMessage.objects.filter(script=pk, type="fail_ending")
        serializer = OutgoingMessageSerializer(fail_endings.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_fail_endings(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_fail_endings(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def partial_fail_triggers(self, request, pk=None):
        partial_fail_triggers = IncomingEmbedding.objects.filter(
            script=pk, type="partial_fail_trigger"
        )
        serializer = IncomingEmbeddingSerializer(partial_fail_triggers.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_partial_fail_triggers(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_partial_fail_triggers(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def intermediate_pitches(self, request, pk=None):
        intermediate_pitches = OutgoingMessage.objects.filter(
            script=pk, type="intermediate_pitch"
        )
        serializer = OutgoingMessageSerializer(intermediate_pitches.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_intermediate_pitches(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_intermediate_pitches(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def stallings(self, request, pk=None):
        stallings = OutgoingMessage.objects.filter(script=pk, type="stalling")
        serializer = OutgoingMessageSerializer(stallings.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def generate_stallings(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.generate_stallings(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def fill_embeddings(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.fill_embeddings(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def fill_speeches(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.fill_speeches(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)

    # TODO: remove this. Just for testing purposes
    @action(detail=True, methods=["get"])
    def start_moderation(self, request, pk=None):
        script = self.get_object()
        try:
            script_generation.start_moderation(script)
            return Response(status=HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(status=HTTP_400_BAD_REQUEST)
