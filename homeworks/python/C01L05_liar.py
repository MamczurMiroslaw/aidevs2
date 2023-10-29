from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, send_question, API_KEY_OPENAI

import openai
openai.api_key = API_KEY_OPENAI


def prompt(q, a):
    return f"### Task: Answer Verification ###" \
           f"Question: {q}" \
           f"Answer: {a}" \
           f"" \
           f"Please verify whether the answer is correct. " \
           f"Respond with either 'YES' or 'NO' based on your knowledge and assessment." \
           f"" \
           f"Response:"


# get information about task from DevAI2
token = get_auth_token('liar')
task = get_task(token, print_task=False)

question = "What is the capital of Poland?"
task_answer = send_question(token, question)

print(f"question: {question}")
print(f"answer: {task_answer['answer']}")

conversation = [{
    "role": "system",
    "content": prompt(question,
                      answer=task_answer['answer'])}]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    max_tokens=200  # Maksymalna liczba słów
)

guardrail = response.choices[0].message.content
print(f"guardrail: {guardrail}")

send_answer(token, guardrail)


