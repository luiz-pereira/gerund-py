from threading import Thread

from gerund.models import IncomingEmbeddings, OutgoingMessages
from gerund.src.ai import apis as ai_apis

from pgvector.django import L2Distance


DEFAULT_MIN_DISTANCE = 0.6

TRIGGER_MAP = {
    "fail_trigger": "fail_ending",
    "success_trigger": "success_ending",
    "partial_fail_trigger": "intermediate_pitch"
}

class Coach:
    """The coach class that handles the training of the AI."""
    def __init__(self):
        self.in_smart_answer_loop = False
        self.smart_answer = None

    def __exit__(self, type, value, traceback):
        self.in_smart_answer_loop = False

    def fill_incomming_embeddings(self):
        """Fill the embeddings for incomming messages."""
        # filter for embeddings that have not been filled
        filtered_incomming_embeddings = IncomingEmbeddings.objects.filter(embedding=None)
        # then loop through them and fill them with openai embeddings
        for incomming_embedding in filtered_incomming_embeddings:
            incomming_embedding.embedding = ai_apis.produce_embedding(incomming_embedding.content)
            incomming_embedding.save()

    def fill_speech_binaries(self):
        """Fill the speech binaries for outgoing messages."""
        # filter for outgoing messages with no speech binary
        filtered_outgoing = OutgoingMessages.objects.filter(speech_binary=None)
        # then loop through them and fill them with google binaries
        for outgoing in filtered_outgoing:
            outgoing.speech_binary = ai_apis.produce_speech_binary(outgoing.content)
            outgoing.save()

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
        nearest_neighbor = IncomingEmbeddings.objects.annotate(
            distance=L2Distance('embedding', message_embedding)).order_by('distance')[0]

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
        outgoing = OutgoingMessages.objects.filter(answer=original_answer).order_by('?').first()
        return outgoing

    def _react_on_trigger(self, nearest_message):
        """Gets an answer for a question."""
        reaction = TRIGGER_MAP[nearest_message.type]
        outgoing = OutgoingMessages.objects.filter(type=reaction).order_by('?').first()
        return outgoing

    def start_smart_answer_loop(self, context, message):
        self.in_smart_answer_loop = True
        self.smart_answer = None
        Thread(target=self._get_smart_answer, args=(message,)).start()

    def _get_smart_answer(self, context, message):
        """Gets a smart answer for a message."""
        text_answer = ai_apis.get_chat_completion(message)
        speech_answer = ai_apis.produce_speech_binary(text_answer)
        self.smart_answer = {"content": text_answer, "speech_binary": speech_answer}
        self.in_smart_answer_loop = False

    def stall_message(self):
        """Stall message."""
        return OutgoingMessages.objects.filter(type="stall").order_by('?').first()

    def hmmm(self):
        """Hmmm message."""
        return OutgoingMessages.objects.filter(type="hmmm").order_by('?').first()

    def greeting(self):
        """Greet message."""
        return OutgoingMessages.objects.filter(type="greeting").order_by('?').first()

    def initial_pitch(self):
        """Initial pitch message."""
        return OutgoingMessages.objects.filter(type="initial_pitch").order_by('?').first()
