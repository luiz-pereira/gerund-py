import openai

API_KEY = "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"
MODEL = "gpt-3.5-turbo"

class Robot:
    """Robot class."""

    def __init__(self, initial_prompt = ""):
        """Initialize the robot with an API key."""
        openai.api_key = API_KEY
        self.chat_log = [self._build_chat_entry("system", initial_prompt)]
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

    def robot_generator(self, questions_generator):
        """Generate the robot's responses."""
        while not self.closed:
            for question in questions_generator:
                yield self.ask(question[0], self.chat_log)

    def ask(self, question, context):
        """Ask a question to the robot."""
        self.chat_log.append(self._build_chat_entry("user", question))
        # just simple answers for now. Maybe we can stream chunks later on.
        # See here:https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
        chat_completion = openai.ChatCompletion.create(model=MODEL, messages=context)
        answer = chat_completion.choices[0].message.content
        self.chat_log.append(self._build_chat_entry("assistant", answer))
        return question, answer

