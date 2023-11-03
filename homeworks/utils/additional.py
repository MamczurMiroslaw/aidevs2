import requests
import openai

from homeworks.utils.aidevsApi import API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI


# function used in C01L04 to return final moderate flag for input text
def moderate_txt(text_to_moderate, print_response=False):
    response = openai.Moderation.create(
        text_to_moderate,
    )

    final_flag = response["results"][0]["flagged"]
    categories_flag = response["results"][0]["categories"]
    if print_response:
        print(categories_flag)

    return int(final_flag)  # return 0 if False and 1 if True


# function used in C01L05 to send question as POST not JSON
def send_question(token, question, print_response=False):
    url = "https://zadania.aidevs.pl/task/" + token

    # creating dictionary
    data = {
        "question": question
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # sending request
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()  # Jeśli odpowiedź jest w formacie JSON
        if print_response:
            print(response_data)
    else:
        print(f"Failed to get response:(. Error code: {response.status_code}")

    return response_data


# function used in C02L02 to find 1 most important word
def find_word_to_filter(txt):
    conversation = [
            {"role": "system", "content": """Twoim zadaniem jest zwrócić tylko imioe z podanego niżej tekstu.
Zwracaj tylko 1 imię. 
Jeśli nie możesz znaleźć imienia zwróć Twoim zdaniem najważniejsze 1 słowo, które jest rzeczownikiem.
Przykład:
zdanie:`Abdon ma czarne oczy, średniej długości włosy i pracuje jako prawnik`
Twoja odpowiedź: 'Abdon'
Zdanie użytkownika jest oznaczone w ###
"""},
        {"role": "user", "content": f"###{txt}###"}
        ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=20
    )

    word = response.choices[0].message.content

    return word

