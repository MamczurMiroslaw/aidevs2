from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
import openai

# openai key
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('blogger')
task = get_task(token, print_task=True)

chapters_list = task['blog']

conversation_base = [{
    "role": "system",
    "content": "Jesteś najlepszym polskim pisarzem kulinarnym piszącym o pizzy i lubiącym robić śmieszne porównania "
               "nawiązujące do historycznych ciekawostek."}]


def prompt(title):
    return f"Napisz tylko akapit (bez żadnych wstępów) do książki na temat: {title}"


written_chapters = []
for chapter in chapters_list:
    conversation = conversation_base
    conversation.append({"role": "user", "content": prompt(chapter)})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=500  # Maksymalna liczba słów
    )

    written_chapters.append(response.choices[0].message.content)

# print(written_chapters)

send_answer(token, written_chapters)
