import openai
from google.cloud import texttospeech

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


class Models:
    GPT3 = "gpt-3.5-turbo-0613"
    GPT3_16K = "gpt-3.5-turbo-16k-0613"
    GPT4 = "gpt-4-0613"


class Genders:
    MALE = texttospeech.SsmlVoiceGender.MALE
    FEMALE = texttospeech.SsmlVoiceGender.FEMALE


def produce_embedding(text):
    """Produce an embedding for the text."""
    model = "text-embedding-ada-002"
    response = openai.Embedding.create(input=[text], model=model)
    embedding = response["data"][0]["embedding"]
    return embedding


DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_VOICE = "Neural2-A"
DEFAULT_GENDER = texttospeech.SsmlVoiceGender.FEMALE
ENCODING = texttospeech.AudioEncoding.MP3


def produce_speech_binary(
    text,
    language=DEFAULT_LANGUAGE,
    voice=DEFAULT_VOICE,
    gender=Genders.MALE,
    speaking_rate=1.0,
):
    client = texttospeech.TextToSpeechClient()
    voice_config = texttospeech.VoiceSelectionParams(
        language_code=language,
        name=language + "-" + voice,
        ssml_gender=gender,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=ENCODING, speaking_rate=speaking_rate
    )
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_config, audio_config=audio_config
    )

    return response.audio_content


def get_chat_completion(context, model=Models.GPT3):
    # TODO: Add an exception handler here.
    chat_completion = openai.ChatCompletion.create(model=model, messages=context)
    return chat_completion.choices[0].message.content
