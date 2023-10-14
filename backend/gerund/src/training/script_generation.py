import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import connection

from gerund.models import Answer, Question, IncomingEmbedding, OutgoingMessage
from gerund.src.ai import apis as ai_apis
from gerund.src.ai.apis import Models
from gerund.src.training import prompts


def generate_potential_questions(script, number_of_questions=100):
    """Generate potential questions."""
    script.questions.all().delete()
    _identify_language(script)
    prompt = prompts.build_questions_prompt(script, number_of_questions)
    _do_generate_questions(prompt, script)


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
        IncomingEmbedding.objects.filter(script=script).delete()

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

    prompt = prompts.build_question_variations_prompt(question, number_of_variations)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    variations = response.split("--- ")[1:]
    for variation in variations:
        incoming_embedding = IncomingEmbedding(
            content=variation.strip(),
            question=question,
            script=question.script,
            type="question",
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
        OutgoingMessage.objects.filter(script=script).delete()

    answers = Answer.objects.filter(script=script)
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

    prompt = prompts.build_answer_variations_prompt(answer, number_of_variations)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    variations = response.split("--- ")[1:]
    for variation in variations:
        outgoing_message = OutgoingMessage(
            content=variation.strip(),
            answer=answer,
            script=answer.script,
            type="answer",
        )
        outgoing_message.save()

    # save the original answer as well
    outgoing_message = OutgoingMessage(
        content=answer.content, answer=answer, script=answer.script, type="answer"
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
    prompt = prompts.build_answers_prompt(script, questions)
    _do_generate_answers(prompt, questions)


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

        question = questions.get(id=question_id)
        question.answerable = answerable
        question.answered = True
        question.save()
        answer = Answer(
            content=answer_content.strip(),
            question_id=question_id,
            script=question.script,
        )
        answer.save()


def generate_initial_pitches(script):
    """Generate initial pitches for customer call."""
    prompt = prompts.build_initial_pitches_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    pitches = response.split("--- ")[1:]
    for pitch in pitches:
        pitch = OutgoingMessage(
            content=pitch.strip(), script=script, type="initial_pitch"
        )
        pitch.save()


def generate_intermediate_pitches(script):
    """Generate intermediate pitches for customer call."""
    prompt = prompts.build_intermediate_pitches_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    pitches = response.split("--- ")[1:]
    for pitch in pitches:
        pitch = OutgoingMessage(
            content=pitch.strip(), script=script, type="intermediate_pitch"
        )
        pitch.save()


def generate_fail_endings(script):
    """Generate fail endings for customer call."""
    prompt = prompts.build_fail_endings_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    endings = response.split("--- ")[1:]
    for ending in endings:
        ending = OutgoingMessage(
            content=ending.strip(), script=script, type="fail_ending"
        )
        ending.save()


def generate_success_endings(script):
    """Generate success endings for customer call."""
    prompt = prompts.build_success_endings_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    endings = response.split("--- ")[1:]
    for ending in endings:
        ending = OutgoingMessage(
            content=ending.strip(), script=script, type="success_ending"
        )
        ending.save()


def generate_total_fail_triggers(script):
    """Generate total fail triggers for customer call."""
    prompt = prompts.build_total_fail_triggers_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    triggers = response.split("--- ")[1:]
    for trigger in triggers:
        trigger = IncomingEmbedding(
            content=trigger.strip(), script=script, type="total_fail_trigger"
        )
        trigger.save()


def generate_partial_fail_triggers(script):
    """Generate partial fail triggers for customer call."""
    prompt = prompts.build_partial_fail_triggers_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    triggers = response.split("--- ")[1:]
    for trigger in triggers:
        trigger = IncomingEmbedding(
            content=trigger.strip(), script=script, type="partial_fail_trigger"
        )
        trigger.save()


def generate_success_triggers(script):
    """Generate success triggers for customer call."""
    prompt = prompts.build_success_triggers_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    triggers = response.split("--- ")[1:]
    for trigger in triggers:
        trigger = IncomingEmbedding(
            content=trigger.strip(), script=script, type="success_trigger"
        )
        trigger.save()


def generate_stallings(script):
    """Generate stallings for customer call."""
    prompt = prompts.build_stallings_prompt(script)
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    stallings = response.split("--- ")[1:]
    for stalling in stallings:
        stalling = OutgoingMessage(
            content=stalling.strip(), script=script, type="stalling"
        )
        stalling.save()


def fill_embeddings(script):
    """Fill the embeddings for incomming messages."""
    # filter for embeddings that have not been filled
    filtered_incomming_embeddings = IncomingEmbedding.objects.filter(
        script=script, embedding=None
    )
    # then loop through them and fill them with openai embeddings
    for incomming_embedding in filtered_incomming_embeddings:
        incomming_embedding.embedding = ai_apis.produce_embedding(
            incomming_embedding.content
        )
        incomming_embedding.save()


def fill_speeches(script):
    """Fill the speech binaries for outgoing messages."""
    # filter for outgoing messages with no speech binary
    filtered_outgoing = OutgoingMessage.objects.filter(
        script=script, speech_binary=None
    )
    # then loop through them and fill them with google binaries
    for outgoing in filtered_outgoing:
        outgoing.speech_binary = ai_apis.produce_speech_binary(outgoing.content)
        outgoing.save()
