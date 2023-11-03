from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI
import re

import openai
openai.api_key = API_KEY_OPENAI

# get information about task from DevAI2
token = get_auth_token('embedding')
task = get_task(token, print_task=True)

# Define the pattern to match the desired text
pattern = r"Send me just array of params: (.*)"

# Use re.search to find the matching text
match = re.search(pattern, task['msg'])

# Check if there's a match and get the text after the specified pattern
if match:
    extracted_text = match.group(1)
    print(f"Text for embedding: {extracted_text}")
else:
    print("Pattern not found in the sentence :(")

# Call the OpenAI API to get the embedding
response = openai.Embedding.create(
    input=extracted_text,
    model="text-embedding-ada-002"
)

# Extract the embedding from the API response
embeddings = response['data'][0]['embedding']

send_answer(token, embeddings)

