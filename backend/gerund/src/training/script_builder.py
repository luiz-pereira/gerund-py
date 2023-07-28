from gerund.models import IncomingEmbeddings, OutgoingMessages
from gerund.src.ai import apis as ai_apis

class ScriptBuilder:
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
