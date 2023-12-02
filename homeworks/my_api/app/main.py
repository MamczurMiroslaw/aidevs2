from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

import os
import requests


class Item(BaseModel):
    name: str
    price: float


class Question(BaseModel):
    question: str


app = FastAPI()
client = OpenAI(api_key="___YOUR_API_KEY___")
content_path = '../history.txt'


def read_history_file(file_path=content_path):
    try:
        # Check if the file exists
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # If the file is not empty, concatenate lines into a string
            content = ''.join(lines).strip() if lines else ''
            return content
    except FileNotFoundError:
        print(f"{file_path} does not exist.")
        return ""
    except IOError as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return ""


def save_history_content(new_info, file_path=content_path):
    # Check if the file exists
    try:
        with open(file_path, 'r') as file:
            history_content = file.read()
            print(f"Existing content in {file_path}:\n{history_content}")
    except FileNotFoundError:
        print(f"{file_path} does not exist. Creating the file.")

        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            history_content = ''

    # Append "great day" to the content
    history_content = history_content + f"\n{new_info}"

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(history_content)


def remove_file_if_over_limit(file_path=content_path, limit=100):
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Check if the file has more than the specified limit
                if len(lines) > limit:
                    print(f"{file_path} has more than {limit} lines. Removing the file.")
                    # Remove the file
                    os.remove(file_path)
                    print(f"{file_path} has been removed.")
    except IOError as e:
        print(f"An error occurred while processing {file_path}: {e}")


def answer_for_question(q):
    context = read_history_file()

    messages = [
        {"role": "system", "content": "Jesteś pomocnym asystentem. "
                                      "Odpowiadaj najkrócej i zwięźle jak się da na pytania używkownika."
                                      "Jeśli użytkownik o nic nie pyta podziękuj mu za informacje odposując tylko "
                                      "'OK. Dzięki za info!'"
                                      f"Tutaj dodatkowe informacje o użytkowniku: ### {context} ###"},
        {"role": "user", "content": q}
    ]

    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=messages,
        max_tokens=200
    )

    answer = response.choices[0].message.content

    # Save as content ealier questions
    if answer == 'OK. Dzięki za info!':
        save_history_content(q)

    # Cleaning file if history is too long
    remove_file_if_over_limit()

    return answer


def google_search_question(question_url):
    # ask LLM compressing
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "Transform given prompt into a google search query."},
            {"role": "user", "content": f"User prompt: ###{question_url}###"}
        ],
        )

    q = response.choices[0].message.content

    return q


def serp_api_question(prompt):
    # SerpApi endpoint
    url = "https://serpapi.com/search"

    # Your SerpApi private key
    api_key = "___YOUR_API_KEY___"

    # Parameters for the search query
    params = {
        "q": prompt,
        "engine": "google",
        "device": "desktop",
        "api_key": api_key,
    }

    # Send the GET request to SerpApi
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the JSON response
        return(response.json())
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")


def answer_url_for_question(q):
    # change question for google prompt
    google_prompt = google_search_question(q).replace('"', '')

    # download answer from serpApi
    serp_answer = serp_api_question(google_prompt)

    # first link (easier solution :)
    answer = serp_answer['organic_results'][0]['link']

    return answer


def md2html(q):
    response = client.chat.completions.create(
      model="ft:gpt-3.5-turbo-1106:mirek::8RQSzYwt",
      messages=[
        {"role": "system", "content": "Change user Markdown to HTML"},
        {"role": "user", "content": q}
      ]
    )

    answer = response.choices[0].message.content

    return answer


@app.get("/")
async def read_item():
    return {"message": "Welcome to my app"}


@app.get("/hello/{name}")
async def read_item(name):
    return {"message": f"Hello {name}, how are you?"}


@app.post("/items/")
async def create_item(item: Item):
    return {"message": f"{item.name} is priced at {item.price}"}


@app.post("/q/")
async def answer_question(item: Question):
    return {"reply": answer_for_question(item.question)}


@app.post("/question_url/")
async def answer_question(item: Question):
    return {"reply": answer_url_for_question(item.question)}


@app.post("/md2html/")
async def answer_question(item: Question):
    return {"reply": md2html(item.question)}
