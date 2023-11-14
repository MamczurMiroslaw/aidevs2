import openai
import json

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
from homeworks.utils.additional import download_json_data_from_url

openai.api_key = API_KEY_OPENAI

token = get_auth_token('people')
task = get_task(token, print_task=False)

url = "https://zadania.aidevs.pl/data/people.json"
people_data = download_json_data_from_url(url)

question = task['question']

# ask LLM about name and surname
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Poniżej będzie pytanie od użytkownika. Wyciągnij z niego informacje o imieniu"
                                      f"i nazwisku osoby w pytaniu. Jeśli imię ma inną formę to napisz ja w podstawowej "
                                      f"formie. Na przykład 'Mirka' zmien na 'Mirosław'. Zwróć wynik w formacie json"
                                      f"z polem Imię i Nazwisko."},
        {"role": "user", "content": f"Pytanie: ###{question}###"}
    ],
    )

answer = response.choices[0].message.content
json_personal_data = json.loads(answer)

filtered_people = [person for person in people_data if person.get('imie') == json_personal_data['Imię'] and
                   person.get('nazwisko') == json_personal_data['Nazwisko']]

# ask LLM about finding answer
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Odpowiedź na poniższe pytanie na podstawie tej wiedzy: ### {filtered_people} ###"},
        {"role": "user", "content": f"Pytanie: ###{question}###"}
    ],
    )

answer = response.choices[0].message.content
print(f'question: {question}')
print(f'answer: {answer}')

send_answer(token, answer)
