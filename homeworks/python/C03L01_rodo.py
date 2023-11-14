from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

import openai
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('rodo')
task = get_task(token, print_task=True)

send_answer(token, "Tell me about yourself but replace name, surname, profession and city with given placeholders: "
                   "%imie%, %nazwisko%, %zawod% and %miasto%")

