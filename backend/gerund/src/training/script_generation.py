import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import connection

from gerund.models import Answer, Question, IncomingEmbedding, OutgoingMessage
from gerund.src.ai import apis as ai_apis
from gerund.src.ai.apis import Models


def generate_potential_questions(script, number_of_questions=100):
    """Generate potential questions."""
    script.questions.all().delete()
    _identify_language(script)
    prompt = _build_questions_prompt(script, number_of_questions)
    _do_generate_questions(prompt, script)


def _identify_language(script):
    """Identify the language of the script."""
    # get the language of the script
    prompt = f"""
        You are a language expert and understand what language is mostly used in a text.
        Please tell me the country-language code of the text below ---. Just reply with the code and nothing else, like this: 'en-US'.
        ---
        {script.presentation}
        """
    response = ai_apis.get_chat_completion(
        [{"role": "system", "content": prompt}], model=Models.GPT4
    )
    # set the language of the script
    script.language_code = response
    script.save()


def generate_script_questions_variations(
    script, number_of_variations=100, partial=True
):
    """Generate questions variations for a script in batches and concurrently"""
    if not partial:
        IncomingEmbedding.objects.filter(question__script=script).delete()

    questions = script.questions.filter(incoming_embeddings__isnull=True)
    print("Started generating questions variations")
    _generate_questions_variations_in_batch(questions, number_of_variations)


def _generate_questions_variations_in_batch(
    questions, number_of_variations, batch_size=4
):
    """
    Generate questions variations in batches.

    - The batch size defaults to 4 due to rate limiting on OpenAI API for GPT-4.
    - Each completion is using ~2500 tokens, so we can only do 4 completions per minute.
    - Each completion takes more than one minute to complete, so we can afford the 4 requests.

    Tried using GPT-3, but it returns too much garbage.
    """

    for i in range(0, len(questions), batch_size):
        _concurrent_generate_questions_variations(
            questions[i : i + batch_size], number_of_variations
        )


def _concurrent_generate_questions_variations(questions, number_of_variations):
    """Generate questions variations concurrently using Threads."""

    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for question in questions:
            futures.append(
                executor.submit(
                    generate_question_variations, question, number_of_variations
                )
            )
    for future in as_completed(futures):
        try:
            print(future.result())
        except Exception as exc:
            print(exc)


def generate_question_variations(question, number_of_variations=100):
    """Generate variations to a question."""
    print(f"Generating variations for question {question.id}")

    prompt = _build_question_variations_prompt(question, number_of_variations)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    variations = response.split("--- ")[1:]
    for variation in variations:
        incoming_embedding = IncomingEmbedding(
            content=variation.strip(), question=question, type="question"
        )
        incoming_embedding.save()

    connection.close()

    return f"Generated {len(variations)} variations for question {question.id}"


def generate_script_answers_variations(script, number_of_variations=10, partial=True):
    """
    Generate answers variations for a script in batches and concurrently
    This is used just to provide some randomness to the answers.
    """

    if not partial:
        OutgoingMessage.objects.prefetch_related("answer__question").filter(
            answer__question__script=script
        ).delete()

    answers = Answer.objects.prefetch_related("question").filter(
        question__script=script
    )
    print("Started generating answers variations")
    _generate_answers_variations_in_batch(answers, number_of_variations)


def _generate_answers_variations_in_batch(answers, number_of_variations, batch_size=7):
    """
    Generate answers variations in batches.

    - The batch size defaults to 7 due to rate limiting on OpenAI API for GPT-4.
    - Each completion is using ~1250 tokens, so we can only do 7 completions per minute.
    - Each completion takes more than one minute to complete, so we can afford the 7 requests.

    """

    for i in range(0, len(answers), batch_size):
        _concurrent_generate_answers_variations(
            answers[i : i + batch_size], number_of_variations
        )


def _concurrent_generate_answers_variations(answers, number_of_variations):
    """Generate answers variations concurrently using Threads."""

    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for answer in answers:
            futures.append(
                executor.submit(
                    generate_answer_variations, answer, number_of_variations
                )
            )
    for future in as_completed(futures):
        try:
            print(future.result())
        except Exception as exc:
            print(exc)


def generate_answer_variations(answer, number_of_variations=100):
    """Generate variations to an answer."""
    print(f"Generating variations for answer {answer.id}")

    prompt = _build_answer_variations_prompt(answer, number_of_variations)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    variations = response.split("--- ")[1:]
    for variation in variations:
        outgoing_message = OutgoingMessage(
            content=variation.strip(), answer=answer, type="answer"
        )
        outgoing_message.save()

    # save the original answer as well
    outgoing_message = OutgoingMessage(
        content=answer.content, answer=answer, type="answer"
    )
    outgoing_message.save()

    connection.close()

    return f"Generated {len(variations)} variations for answer {answer.id}"


def generate_potential_answers(script, partial=True):
    """Generate potential answers."""
    if partial:
        questions = script.questions.select_related("answer").filter(answered=False)
    else:
        questions = script.questions.all()
    prompt = _build_answers_prompt(script, questions)
    _do_generate_answers(prompt, questions)


def _do_generate_questions(prompt, script):
    """Generate questions."""
    # get the questions
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    # split the response into a list of questions
    questions = response.split("--- ")[1:]
    # then loop through them and save them
    for question in questions:
        question = Question(content=question.strip(), script=script)
        question.save()


def _do_generate_answers(prompt, questions):
    """Generate answers."""
    # get the answers
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    # split the response into a list of answers
    answers = response.split("--- ")[1:]
    # then loop through them and save them
    for answer in answers:
        # q: how to use regex to get the number between brackets?
        found_id = re.findall(r"\[.*?\]", answer)
        if len(found_id) == 0:
            continue

        id_str = found_id[0]
        question_id = id_str.strip("[]")
        answer_content = answer.replace(id_str, "").strip()

        # It means that the answer is answerable, but not with the provided context.
        if answer_content.find("(***)") != -1:
            continue

        if answer_content.find("(###)") != -1:
            answerable = False
            answer_content = answer_content.replace("(###)", "")
        else:
            answerable = True

        answer = Answer(content=answer_content.strip(), question_id=question_id)
        question = questions.get(id=question_id)
        question.answerable = answerable
        question.answered = True
        question.save()
        answer.save()


def fill_incomming_embeddings():
    """Fill the embeddings for incomming messages."""
    # filter for embeddings that have not been filled
    filtered_incomming_embeddings = IncomingEmbedding.objects.filter(embedding=None)
    # then loop through them and fill them with openai embeddings
    for incomming_embedding in filtered_incomming_embeddings:
        incomming_embedding.embedding = ai_apis.produce_embedding(
            incomming_embedding.content
        )
        incomming_embedding.save()


def fill_speech_binaries():
    """Fill the speech binaries for outgoing messages."""
    # filter for outgoing messages with no speech binary
    filtered_outgoing = OutgoingMessage.objects.filter(speech_binary=None)
    # then loop through them and fill them with google binaries
    for outgoing in filtered_outgoing:
        outgoing.speech_binary = ai_apis.produce_speech_binary(outgoing.content)
        outgoing.save()


def _build_questions_prompt(script, number_of_questions):
    """Builds the prompt for the chatbot."""
    if number_of_questions > 100:
        raise Exception("Too many questions")

    if script.custom_prompt == "" or script.custom_prompt is None:
        custom_prompt = ""
    else:
        custom_prompt = f"\nOther details:\n{script.custom_prompt}\n"

    prompt = f"""
        You are an expert in sales and understand what customers may want to know about a new product or service.
        I am building a script for cold calling customers to sell a new product, so I need potential questions that customers may ask.
        I need you to come up with at {number_of_questions} questions that customers may ask about the new product.
        Please follow the instructions below to generate the questions.
        - Most questions must make sense in the context of the company and/or the product.
        - Also include some questions that do not make complete sense, but are still related to the company or the product.
        - Also include some questions that are not completely related to the company or the product.
        - Also include some questions that are not related to the company or the product, and do not make much sense under the context.
        - Each question must be unique, in terms of meaning.
        - The questions are short, and can be answered with a short answer.
        - Use the languange that is used after "Company Presentation:"
        - Present the questions in a unordered/unnumbered list , without a line break using --- as a separator like this:
            --- question --- question --- question

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        {custom_prompt}
        """
    return [{"role": "system", "content": prompt}]


def _build_answers_prompt(script, questions):
    """Builds the prompt for the chatbot."""

    questions_prompt = ""
    for question in questions:
        questions_prompt += f"{question.id}. {question.content} \n"

    prompt = f"""
        You are an expert in sales and understand what customers may want to know about a new product or service.
        I am building a script for cold calling customers to sell a new product, so I need potential answers to the questions that customers may ask.
        I need you to look at the questions below and also at established common sense to answer each of them.
        Please follow the instructions below to generate the answers.
        - Be polite, charming and convincing. You are trying to sell a product.
        - Each answer must be answereable using the context provided unless it is very obvious to an average adult person.
        - The answers must be short and direct.
        - Always reply using the same languange used in the question.
        - Present the answers in a unordered/unnumbered list using --- as a separator and prepended by the question id, like this:
            --- [123] answer
            --- [124] answer
            --- [125] answer
        - if the questions is potentially valid and within the service main context, but not answerable with the context provided, answer with (***) like this:
            --- [123] (***)
        - if the questions are way out of context, prefix the answer answer with (###) and then politely declining to answer, like this:
            --- [123] (###) Unfortunately, I have no information about this.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}

        Questions:
        {questions_prompt}
        """
    return [{"role": "system", "content": prompt}]


def _build_question_variations_prompt(question, number_of_variations):
    """Builds the prompt for generating variations to a question so that we can store in vector DB."""
    prompt = f"""
        You are an expert in coloquial spoken language and customer service and know how users usually ask questions.
        That question would have come from a customer in spoken language, so it is important to cover the many ways people can ask the same question.
        Please always follow the following instructions to generate the variations:
        - generate {number_of_variations} variations of the question presented at the end of this prompt in 'Question'.
        - for some context, see 'Context' and 'New Product' below.
        - Always use the same languange used in the question.
        - Try to generate variations that are as different as possible among themselves.
        - Do not censor bad words.
        - The variations must be a representation of how people chat in real life over a phone call.
        - Include regionalisms in some variations.
        - Ensure that you cover different personas, under different levels of patience and politeness.
        - Present the answers in a unordered/unnumbered list using --- as a separator.
            --- variation
            --- variation

        Context:
        Company Presentation:
        {question.script.presentation}

        New Product:
        {question.script.new_product}

        Question:
        {question.content}
        """
    return [{"role": "system", "content": prompt}]


def _build_answer_variations_prompt(answer, number_of_variations):
    """Builds the prompt for generating variations to an answer so that we can store in vector DB."""
    prompt = f"""
        You are an expert in over-the-phone sales and can answer questions truthly but convincingly, in order to sell a product.
        The original question would have come from a customer in spoken language, so it is important that the answers are also in spoken language.
        Please always follow the following instructions to generate the variations:
        - generate {number_of_variations} variations of the answer presented at the end of this prompt in 'Answer'.
        - Always use the same languange used in the original answer.
        - Try to generate variations that are as different as possible among themselves.
        - The variations must be a representation of how people chat in real life over a phone call.
        - Present the answers in a unordered/unnumbered list using --- as a separator.
            --- variation
            --- variation

        Answer:
        {answer.content}
        """
    return [{"role": "system", "content": prompt}]
