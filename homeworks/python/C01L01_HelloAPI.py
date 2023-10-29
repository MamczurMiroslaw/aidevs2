from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer

token = get_auth_token('HelloAPI')
task = get_task(token, print_task=True)
send_answer(token, task['cookie'])

