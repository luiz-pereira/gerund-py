from gerund.models import Answer, Question, IncomingEmbedding, OutgoingMessage
from gerund.src.ai import apis as ai_apis
from gerund.src.ai.apis import Models
import re

import asyncio

def generate_potential_questions(script, number_of_questions=100):
    """Generate potential questions."""
    script.question_set.all().delete()
    prompt = _build_questions_prompt(script, number_of_questions)
    _do_generate_questions(prompt, script)

def generate_potential_answers(script, partial=True):
    """Generate potential answers."""
    if partial:
        questions = script.question_set.select_related('answer').filter(answer__isnull=True)
    else:
        questions = script.question_set.all()
    prompt = _build_answers_prompt(script, questions)
    _do_generate_answers(prompt)

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

def _do_generate_answers(prompt):
    """Generate answers."""
    # get the answers
    response = ai_apis.get_chat_completion(prompt, model=Models.GPT4)
    # split the response into a list of answers
    answers = response.split("--- ")[1:]
    # then loop through them and save them
    for answer in answers:
        # q: how to use regex to get the number between brackets?
        found_id = re.findall(r'\[.*?\]', answer)
        if len(found_id) == 0:
            continue
        id_str = found_id[0]
        question_id = id_str.strip("[]")
        answer_content = answer.replace(id_str, "").strip()
        answer = Answer(content=answer_content, question_id=question_id)
        answer.save()

def fill_incomming_embeddings():
    """Fill the embeddings for incomming messages."""
    # filter for embeddings that have not been filled
    filtered_incomming_embeddings = IncomingEmbedding.objects.filter(embedding=None)
    # then loop through them and fill them with openai embeddings
    for incomming_embedding in filtered_incomming_embeddings:
        incomming_embedding.embedding = ai_apis.produce_embedding(incomming_embedding.content)
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
        - Most questions must make sense in the context of the company or the product.
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
        - Each answer must be answereable using the context provided unless it is very obvious to an average adult person.
        - The answers must be short and direct.
        - Use the languange that is used in the question.
        - Present the answers in a unordered/unnumbered list using --- as a separator and prepended by the question id, like this:
            --- [123] answer
            --- [124] answer
            --- [125] answer
        - if the questions is potentially valid and within the service main context, but not answerable with the context provided, answer with "******" like this:
            --- [123] ******
        - if the questions are way out of context, answer with "??????" like this:
            --- [123] ??????

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}

        Questions:
        {questions_prompt}
        """
    return [{"role": "system", "content": prompt}]
