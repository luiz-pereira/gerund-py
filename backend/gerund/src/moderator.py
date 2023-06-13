from human.human_transcription import HumanTranscription
from robot.robot import Robot
import sys

INITIAL_PROMPT = "Oi, você é um assistente baiano que responde a perguntas gerais e fala como um caipira. Suas respostas são curtas e diretas, sem emojis. Elas serão depois convertidas para áudio e enviadas para o usuário, portanto, evite respostas muito longas e chatas. Seja bem coloquial e amigável"

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

class Moderator:
    """
    A class that manages the chat between the user and the bot.
    """

    def __init__(self):
        self.human = None
        self.bot = None
        self.closed = True

    def __enter__(self):
        self.human = HumanTranscription()
        self.bot = Robot()
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.human.__exit__(type, value, traceback)


    def start(self):
        """
        Starts the chat between the user and the bot.
        """
        print(YELLOW, '\nListening, say "Quit" or "Exit" to stop.\n\n')
        print(YELLOW, "=====================================================\n")

        with self.human as human, self.bot as bot:
            human_generator = human.transcription_generator()
            bot_generator = bot.robot_generator(human_generator)
            while not human.closed and not bot.closed:
                for (question, answer) in bot_generator:
                    print(YELLOW, f"Q: {question}")
                    print(GREEN, f"A: {answer}")
                    self.bot.speak(answer)
                    print("")

if __name__ == "__main__":
    with Moderator() as moderator:
        moderator.start()
        while not moderator.closed:
            pass