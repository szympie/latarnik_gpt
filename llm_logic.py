from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI

from prompts import create_advise_prompt

def question_dict_to_text(question_dict):
    text = ''
    for question in question_dict:
        text += f"Stwierdzenie: \n{question['question']}\n\n"
        text += f"Odpowiedź użytkownika:\n{question['user_comment']}\n\n"
    return text


def run_advise_chain(question_dict):
    model = AzureChatOpenAI(deployment_name='gpt-4-32k',
                            temperature=0)

    chain = LLMChain(llm=model,
                     verbose=True,
                     prompt=create_advise_prompt)

    with open('./data/justifications_message.txt', 'r') as f:
        parties_comments = f.read()

    users_comments = question_dict_to_text(question_dict)
    results = chain.predict(parties_comments=parties_comments,
                    users_comments=users_comments)

    return results

