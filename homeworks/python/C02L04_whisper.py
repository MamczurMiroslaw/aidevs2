from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

import re
import requests

import openai
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('whisper')
task = get_task(token, print_task=False)

# Step 1: Extracting the HTTPS Link
url_match = re.search(r'https://[^\s]+', task['msg'])
if url_match:
    https_link = url_match.group()
    print(f'link to download:{https_link}')

# Step 2: Download the MP3 file
response = requests.get(https_link)

if response.status_code == 200:
    with open('../files/mateusz.mp3', 'wb') as f:
        f.write(response.content)
        print("File downloaded successfully.")
else:
    print("Failed to download the file.")

# Step 3: Send file to openAI
audio_file = open("../files/mateusz.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

answer = transcript['text']
send_answer(token, answer)
