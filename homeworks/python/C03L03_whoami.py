import openai

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI


def guess_person(hints):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant who need to guess who is MYSTERY PERSON."
                                      "If you are not sure for 100% write me NO."
                                      "Only if you know answer for 100% write name and surname of this mystery person."
                                      "User each time will give you new hint."},
        {"role": "user", "content": f"I have information about a person: MYSTERY PERSON. Do you know who this person is?"}
    ]

    for hint in hints:
        # add all hints to conversation
        conversation.append({"role": "assistant", "content": f"hint: {hint}"})

    conversation.append({"role": "user", "content": f"Do you know who MYSTERY PERSON is?"})

    # ask OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=100
    )

    answer = response['choices'][0]['message']['content'].strip()

    # check answer
    if "NO" in answer.upper():
        # if not then continue
        print(f"Assistant is not sure. Trying another hint :)")
        return 0
    else:
        print(answer)
        send_answer(token, answer)
        return 1


hints = []

for i in range(9):
    # get information about task from DevAI2
    token = get_auth_token('whoami')
    hint = get_task(token, print_task=False)['hint']
    hints.append(hint)
    print(f"Try {i}. Hint: {hint}")

    # try to guess
    guess = guess_person(hints)
    if guess:
        break

