from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
from homeworks.utils.additional import find_word_to_filter

import openai
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('inprompt')
task = get_task(token, print_task=False)

task_question = task['question']
task_input = task['input']

# find 1 word to filter context
word = find_word_to_filter(task_question)

# filter list
filtered_context = [element for element in task_input if word in element]

# find final answer
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Context```{filtered_context}```"},
        {"role": "user", "content": f"Odpowiedz na pytanie: {task_question}"}
    ],
    max_tokens=20
    )

answer = response.choices[0].message.content

print(f"Context list {len(task_input)}. Context list after filltering: {len(filtered_context)}.")
print(f"task_question: {task_question}")
print(f"answer: {answer}")

send_answer(token, answer)
