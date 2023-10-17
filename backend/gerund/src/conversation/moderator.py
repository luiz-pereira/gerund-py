from gerund.src.conversation.human.human_transcription import HumanTranscription
from gerund.src.conversation.robot.robot import Robot
import time

OKCYAN = "\033[96m"


class Moderator:
    """
    A class that manages the chat between the user and the bot.
    """

    def __init__(self, script):
        self.human = None
        self.script = script
        self.bot = None
        self.closed = True

    def __enter__(self):
        self.human = HumanTranscription()
        self.bot = Robot(self.script)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.human.__exit__(type, value, traceback)

    def start(self):
        """
        Starts the chat between the user and the bot.
        """
        print(OKCYAN, "\nConversation between Robot and Human.\n\n")
        print(OKCYAN, "=====================================================\n")

        with self.human as human, self.bot as bot:
            bot.initial_pitch()
            human_generator = human.transcription_generator(
                language_code=self.script.language_code
            )
            bot_generator = bot.robot_generator(human_generator)
            while not human.closed and not bot.closed:
                for question, answer in bot_generator:
                    print(OKCYAN, "Waiting for next question")
                    print("")


if __name__ == "__main__":
    with Moderator(script=script) as moderator:
        moderator.start()
        while not moderator.closed:
            pass
