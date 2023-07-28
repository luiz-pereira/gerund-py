import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def produce_embedding(text):
    """Produce an embedding for the text."""
    model = "text-embedding-ada-002"
    response = openai.Embedding.create(input = [text], model=model)
    embedding = response['data'][0]['embedding']
    return embedding
