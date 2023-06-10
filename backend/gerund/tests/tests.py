from django.test import TestCase
from ..src.listening import audio_capture

# Create your tests here.
class ModelTest(TestCase):
    def test_stream(self):
        a = audio_capture.MicrophoneStream()
        self.assertEqual(1, 1)
        print("Hello World!")