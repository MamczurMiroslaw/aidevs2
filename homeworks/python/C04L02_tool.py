import openai
import json

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI

token = get_auth_token('tools')
task = get_task(token, print_task=False)

question = task['question']

conversation = [
        {"role": "system", "content": """Jesteś pomocnym asystentem, który analizuje zadanie podane przez użytkownika.
Masz je zakwalifikować do jednej z 2 kategorii: lista `ToDo` lub `Calendar`.
Jeśli występuje data zmień ją na format RRRR-MM-DD.
Dzisiaj jest 2023-11-14.
Zwróć wynik tylko zapisany w JSON.
Przykład dla 'ToDo': Przypomnij mi, że mam kupić mleko = {"tool":"ToDo","desc":"Kup mleko" }
Przykład dla `Calendar`: Jutro mam spotkanie z Marianem = {"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2023-11-15"}
"""},
        {"role": "user", "content": question}
    ]

# ask OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=conversation,
    max_tokens=1000
)

answer = response['choices'][0]['message']['content'].strip()

send_answer(token, json.loads(answer), prnt=True)

print(f'question:{question}')
print(f'answer:{answer}')
