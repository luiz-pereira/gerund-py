from gerund.models import IncomingEmbeddings
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

