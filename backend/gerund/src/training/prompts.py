"""This module contains the functions that build the prompts for the script generation."""


def build_questions_prompt(script, number_of_questions):
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


""


def build_answers_prompt(script, questions):
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


""


def build_question_variations_prompt(question, number_of_variations):
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


""


def build_answer_variations_prompt(answer, number_of_variations):
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


""


def build_initial_pitches_prompt(script, number_of_pitches=10):
    """Builds the prompt for generating initial pitches for a customer call."""
    prompt = f"""
        You are an expert in over-the-phone sales and a master at convincing people to buy a product.
        You are trying to sell a new product to a customer.
        Please always follow the following instructions to generate the initial pitches:
        - generate {number_of_pitches} initial pitches for the customer call.
        - Always use the same languange used in the provided context.
        - Try to generate pitches that are as different as possible among themselves.
        - The pitches must be a representation of how people chat in real life over a phone call.
        - The pitches must include a greeting.
        - The pitches must include a very brief introduction of the company.
        - The pitches must be brief and direct, but also polite and charming.
        - The pitches should be short enough to be said in less than 10 seconds.
        - Present the pitches in a unordered/unnumbered list using --- as a separator.
            --- pitch
            --- pitch
        - To create the pitches, use the company presentation and the new product below as context.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        """
    return [{"role": "system", "content": prompt}]


def build_intermediate_pitches_prompt(script, number_of_pitches=20):
    """Builds the prompt for generating intermediate pitches for a customer call."""
    prompt = f"""
        You are an expert in over-the-phone sales and a master at convincing people to buy a product.
        You are trying to sell a new product to a customer, however the call is not going too well or the customer does not seem to be interested.
        Please always follow the following instructions to generate the intermediate pitches:
        - generate {number_of_pitches} intermediate pitches for the customer call.
        - Always use the same languange used in the provided context.
        - Try to generate pitches that are as different as possible among themselves.
        - The pitches must be a representation of how people chat in real life over a phone call.
        - The pitches must be brief and direct, but also polite and charming.
        - They must try to keep the conversation going and convince the customer to buy the product.
        - The pitches should be short enough to be said in less than 10 seconds.
        - Present the pitches in a unordered/unnumbered list using --- as a separator.
            --- pitch
            --- pitch
        - To create the pitches, use the company presentation and the new product below as context.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        """
    return [{"role": "system", "content": prompt}]


def build_fail_endings_prompt(script, number_of_endings=10):
    """Builds the prompt for generating fail endings for a customer call."""
    prompt = f"""
        You are an expert in over-the-phone sales and a master at convincing people to buy a product.
        You are trying to sell a new product, however it does look like the customer will not buy the product.
        Please always follow the following instructions to generate the fail endings:
        - generate {number_of_endings} fail endings for the customer call.
        - Always use the same languange used in the provided context.
        - Try to generate endings that are as different as possible among themselves.
        - The endings must be a representation of how people chat in real life over a phone call.
        - The endings must be brief and direct, but also polite and charming.
        - The endings should thank the customer for their time and tell them that we're always available if they change their mind.
        - The endings should be short enough to be said in less than 10 seconds.
        - Present the endings in a unordered/unnumbered list using --- as a separator.
            --- ending
            --- ending
        - To create the endings, use the company presentation and the new product below as context.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        """
    return [{"role": "system", "content": prompt}]


def build_success_endings_prompt(script, number_of_endings=10):
    """Builds the prompt for generating success endings for a customer call."""
    prompt = f"""
        You are an expert in over-the-phone sales and a master at convincing people to buy a product.
        You are trying to sell a new product, and it looks like the customer will buy the product.
        The call is going well and the customer is interested in the product.
        Please always follow the following instructions to generate the success endings:
        - generate {number_of_endings} success endings for the customer call.
        - Always use the same languange used in the provided context.
        - Try to generate endings that are as different as possible among themselves.
        - The endings must be a representation of how people chat in real life over a phone call.
        - The endings must be brief and direct, but also polite and charming.
        - The endings should thank the customer and tell them a supervisor will call them to finalize details.
        - The endings should be short enough to be said in less than 15 seconds.
        - Present the endings in a unordered/unnumbered list using --- as a separator.
            --- ending
            --- ending
        - To create the endings, use the company presentation and the new product below as context.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        """
    return [{"role": "system", "content": prompt}]


def build_stallings_prompt(script, number_of_stallings=50):
    """Builds the prompt for generating stallings for a customer call."""
    prompt = f"""
        You are an expert in over-the-phone sales and a master at convincing people to buy a product.
        While we're searching for an answer to a customer question, we need to stall the customer.
        Please always follow the following instructions to generate the stallings:
        - generate {number_of_stallings} stallings for the customer call.
        - Always use the same languange used in the provided context.
        - Try to generate stallings that are as different as possible among themselves.
        - The stallings must be a representation of how people chat in real life over a phone call.
        - The stallings must be brief and direct, but also polite and charming.
        - The stallings should be short enough to be said in less than 4 seconds.
        - Present the stallings in a unordered/unnumbered list using --- as a separator.
            --- stalling
            --- stalling
        - The company presentation and the new product below are provided as context, but you do not need to use them to create the stallings.

        Context:
        Company Presentation:
        {script.presentation}

        New Product:
        {script.new_product}
        """
    return [{"role": "system", "content": prompt}]
