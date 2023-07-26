import io
import time

from pydub import AudioSegment
from pydub.playback import play
from google.cloud import texttospeech

DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_VOICE = "pt-BR-Standard-C"
DEFAULT_GENDER = texttospeech.SsmlVoiceGender.FEMALE
ENCODING = texttospeech.AudioEncoding.MP3

class VoiceBox:
    """
    This class is responsible for producing speech from text.
    """
    def __init__(self, language = DEFAULT_LANGUAGE, voice = DEFAULT_VOICE, gender = DEFAULT_GENDER):
        self.closed = True
        self.speech_client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice,
            ssml_gender=gender,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=ENCODING,
            effects_profile_id=["telephony-class-application"],
        )

    def __enter__(self):
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.closed = True

    def say(self, text):
        input_text = texttospeech.SynthesisInput(text=text)

        start_time = time.time()
        response = self.speech_client.synthesize_speech(
            request={"input": input_text, "voice": self.voice, "audio_config": self.audio_config}
        )
        print("Time taken to synthesize speech: {} seconds".format(time.time() - start_time))

        audio_segment = AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3")
        play(audio_segment)
