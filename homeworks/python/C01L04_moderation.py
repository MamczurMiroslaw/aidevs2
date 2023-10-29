from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer
from homeworks.utils.additional import moderate_txt

# get information about task from DevAI2
token = get_auth_token('moderation')
task = get_task(token, print_task=True)

task_input = task['input']

values = []
for txt in task_input:
    moderate_flg = moderate_txt(txt)
    print(f'{txt}: {moderate_flg}')
    values.append(moderate_flg)

send_answer(token, values)

