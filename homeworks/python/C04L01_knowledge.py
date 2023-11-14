import openai
import json

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
from homeworks.utils.additional import currency_rate, country_population

openai.api_key = API_KEY_OPENAI

token = get_auth_token('knowledge')
task = get_task(token, print_task=True)

question = task['question']

# ask LLM about task. Let it give answer as function calling for 3 functions
# 1 - general question; 2- currency; 3 - population
function_descriptions = [
    {
        "name": "general_info",
        "description": "Answering for general information question",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "Copy of user question"
                },
                "answer": {
                    "type": "string",
                    "description": "Answer for user question"
                },
            },
            "required": ["question", "answer"]
        }
    },
    {
        "name": "currency_rate",
        "description": "Answering for question about currency rate",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "a three letter currency code (ISO 4217 standard), for example USD for United States"
                },
            },
            "required": ["code"]
        }
    },
    {
        "name": "country_population",
        "description": "Answering for question about population number",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "name of country written with small letter, for example for Poland: poland"
                },
            },
            "required": ["country"]
        }
    },
]

# find final answer
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
    # Add function calling
    functions=function_descriptions,
    function_call="auto"
)

function_call_answer = response.choices[0].message
arguments = json.loads(function_call_answer["function_call"]["arguments"])

# print(function_call_answer)
# print(arguments)
# print(function_call_answer['function_call']['name'])

if function_call_answer['function_call']['name'] == 'country_population':
    print(f'country_population arguments: {arguments}')
    answer = country_population(arguments['country'])
elif function_call_answer['function_call']['name'] == 'currency_rate':
    print(f'currency_rate arguments: {arguments}')
    answer = currency_rate(arguments['code'])
else:
    answer = arguments['answer']
    print(answer)

print(answer)
# print(function_call_answer['function_call']['name'])
# print(function_call_answer)
# print(arguments)
# print(answer)
# Here answer for task is to send description only
send_answer(token, answer)
