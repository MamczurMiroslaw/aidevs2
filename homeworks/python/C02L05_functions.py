from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
import re

import openai
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('functions')
task = get_task(token, print_task=True)

user_prompt = "Dopisz do listy Mirka Mamczur co ma 39 urodziny 23 kwietnia 2024"

function_descriptions = [
    {
      "name": "addUser",
      "description": "Add new user to database",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "User name, e.g. Mirek, Jagoda, Oti, Elwira"
          },
          "surname": {
            "type": "string",
            "description": "User surname, e.g. Mamczur, Kowalski, Nowak"
          },
          "year": {
            "type": "integer",
            "description": "User year of born, e.g. 1985, 2015, 2017"
          }
        },
        "required": ["name", "surname", "year"]
      }
    }
  ]

# Here answer for task is to send description only
send_answer(token, function_descriptions[0])

# find final answer
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_prompt}],
    # Add function calling
    functions=function_descriptions,
    function_call="auto"
    )

function_call_answer = response.choices[0].message
print(function_call_answer)



