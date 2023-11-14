import requests
import time
import openai
from fake_useragent import UserAgent

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('scraper')
task = get_task(token, print_task=True)

url = task["input"]
question = task["question"]


# Funkcja do pobierania tekstu z adresu URL
def fetch_url_with_retries(url, max_retries=10, timeout=30):
    retries = 0
    while retries < max_retries:
        start_time = time.time()
        try:
            ua = UserAgent()
            headers = {
                "User-Agent": ua.random
            }
            response = requests.get(url, headers=headers, timeout=timeout)

            # Sprawdź, czy odpowiedź jest prawidłowa (status 200)
            if response.status_code == 200:
                print(f"Downloaded data :)")
                return response.text
            else:
                print(f"Nieudane zapytanie. Status: {response.status_code}. "
                      f"Time: {round(time.time()-start_time,2)} sec.")

        except requests.exceptions.RequestException as e:
            print(f"Błąd podczas pobierania zasobu: {e}")

        retries += 1

    print(f"Nie udało się pobrać zasobu po {max_retries} próbach.")
    return None


# Wywołaj funkcję do pobrania tekstu
context = fetch_url_with_retries(url)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": f"You are system to answer question based on below context. "
                                            f"Please answer in polish."
                                            f"Context: ### {context} ###"},
              {"role": "user", "content": f"Question: {question}"},
              ],
    )


answer = response.choices[0].message.content
print(answer)
send_answer(token, answer)

