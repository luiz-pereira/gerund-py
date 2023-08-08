import io
import time

from pydub import AudioSegment
from pydub.playback import play

from gerund.src.training.coach import Coach

class Robot:
    """Robot class."""

    def __init__(self, initial_prompt = ""):
        """Initialize the robot with an API key."""
        self.chat_log = [self._build_chat_entry("system", initial_prompt)]
        self.coach = Coach()
        self.closed = True

    def __enter__(self):
        """Enter the context manager."""
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        """Exit the context manager."""
        self.closed = True

    def _build_chat_entry(self, role, content):
        """Build a chat entry."""
        return {
            "role": role,
            "content": content
        }

    def greet(self):
        """Greet the user."""
        greeting = self.coach.greeting()
        self.chat_log.append(self._build_chat_entry("assistant", greeting.content))
        self.speak(greeting.speech_binary)

    def initial_pitch(self):
        """Play the initial pitch."""
        initial_pitch = self.coach.initial_pitch()
        self.chat_log.append(self._build_chat_entry("assistant", initial_pitch.content))
        self.speak(initial_pitch.speech_binary)


    def robot_generator(self, incoming_messages_generator):
        """Generate the robot's responses."""
        while not self.closed:
            for message in incoming_messages_generator:
                yield self._respond(message[0])

    def _respond(self, message):
        """Responds to a message"""
        self.chat_log.append(self._build_chat_entry("user", message))
        coach = self.coach
        answer = coach.dumb_interpret(message) or self._smart_answer()
        self.chat_log.append(self._build_chat_entry("assistant", answer.content))
        self.speak(answer.speech_binary)
        return message, answer.content

    def _smart_answer(self):
        """Loop for smart answers."""
        coach = self.coach
        context = self.chat_log
        coach.start_smart_answer_loop(context)
        # plays a stalling message
        self.speak(coach.stall_message().speech_binary)

        while coach.in_smart_answer_loop:
            time.sleep(2)
            # plays a hmmm message
            self.speak(coach.hmmm().speech_binary)

        return coach.smart_answer

    def speak(self, speech_binary):
        """Speak the text."""
        audio_segment = AudioSegment.from_file(io.BytesIO(speech_binary), format="mp3")
        play(audio_segment)

