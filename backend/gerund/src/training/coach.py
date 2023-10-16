from threading import Thread

from gerund.models import IncomingEmbedding, OutgoingMessage
from gerund.src.ai import apis as ai_apis

from pgvector.django import L2Distance

DEFAULT_MIN_DISTANCE = 0.7

TRIGGER_MAP = {
    "fail_trigger": "fail_ending",
    "success_trigger": "success_ending",
    "partial_fail_trigger": "intermediate_pitch",
}


class Coach:
    """The coach class that handles the training of the AI."""

    def __init__(self, script):
        self.script = script
        self.in_smart_answer_loop = False
        self.smart_answer = None

    def __exit__(self, type, value, traceback):
        self.in_smart_answer_loop = False

    def dumb_interpret(self, message):
        """
        Interprets a message.
        Returns an OutgoingMessage if the message is understood. Otherwise returns None.
        """
        nearest_neighbor = self._find_nearest_neighbor(message)
        if nearest_neighbor is None:
            return None
        else:
            return self.get_answer(nearest_neighbor)

    def _find_nearest_neighbor(self, message, min_distance=DEFAULT_MIN_DISTANCE):
        """Find the nearest embedding. Returns None if the distance is too big to the nearest neighbor."""
        message_embedding = ai_apis.produce_embedding(message)
        nearest_neighbor = IncomingEmbedding.objects.annotate(
            distance=L2Distance("embedding", message_embedding)
        ).order_by("distance")[0]

        print(nearest_neighbor.distance)

        if nearest_neighbor.distance < min_distance:
            return nearest_neighbor

        else:
            return None

    def get_answer(self, nearest_message):
        """Gets an answer for a message."""
        if nearest_message.type == "question":
            return self._get_answer_for_question(nearest_message)
        else:
            return self._react_on_trigger(nearest_message)

    def _get_answer_for_question(self, nearest_message):
        """Gets an answer for a question."""
        original_answer = nearest_message.question.answer_set.first()
        # Randomly select an outgoing message
        outgoing = (
            OutgoingMessage.objects.filter(answer=original_answer).order_by("?").first()
        )
        return outgoing

    def _react_on_trigger(self, nearest_message):
        """Gets an answer for a question."""
        reaction = TRIGGER_MAP[nearest_message.type]
        outgoing = OutgoingMessage.objects.filter(type=reaction).order_by("?").first()
        return outgoing

    def start_smart_answer_loop(self, context):
        self.in_smart_answer_loop = True
        self.smart_answer = None
        Thread(target=self._get_smart_answer, args=(context,)).start()

    def _get_smart_answer(self, context):
        """Gets a smart answer for a message."""
        text_answer = ai_apis.get_chat_completion(context)
        speech_answer = ai_apis.produce_speech_binary(text_answer)
        self.smart_answer = SmartAnswer(text_answer, speech_answer)
        self.in_smart_answer_loop = False

    def stall_message(self):
        """Stall message."""
        return OutgoingMessage.objects.filter(type="stalling").order_by("?").first()

    def hmmm(self):
        """Hmmm message."""
        return OutgoingMessage.objects.filter(type="hmmm").order_by("?").first()

    def greeting(self):
        """Greet message."""
        return (
            OutgoingMessage.objects.filter(type="greeting", script=self.script)
            .order_by("?")
            .first()
        )

    def initial_pitch(self):
        """Initial pitch message."""
        return (
            OutgoingMessage.objects.filter(type="initial_pitch", script=self.script)
            .order_by("?")
            .first()
        )


class SmartAnswer:
    def __init__(self, content, speech_binary):
        self.content = content
        self.speech_binary = speech_binary
