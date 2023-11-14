import os
import openai
import requests
import time
import pandas as pd

from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

from homeworks.utils.aidevsApi import get_auth_token, get_task, send_answer, API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI

token = get_auth_token('search')
task = get_task(token, print_task=True)
question = task['question']


# download arch from unknown news
def download_arch():
    # URL of the JSON file
    url = 'https://unknow.news/archiwum.json'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON content into a DataFrame
        json_arch = response.json()
        return json_arch
    else:
        print(f"Failed to get response:(. Error code: {response.status_code}")
        print(f"Reason: {response.reason}")


# Function to calculate OpenAI Ada-02 embeddings
def calculate_embeddings(text):
    # Call the OpenAI API to get the embedding
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    # return generated embeddings
    return response['data'][0]['embedding']


# take top 300 links so it would be faster ;)
df = pd.DataFrame(download_arch())
print(f'rows: {df.shape[0]}')
df_small = df.head(300)

# Specify the file path to save embeddings to calculate it once
file_path = "../files/C03L04_df_small_embeddings.pkl"

# Check if the file exists
if not os.path.exists(file_path):
    embeddings = []
    # Iterate over rows using iterrows()
    for index, row in tqdm(df_small.iterrows(), total=len(df_small), desc="Processing rows"):
        embeddings.append(calculate_embeddings(row['info']))
        time.sleep(0.1)

    # Add a new column 'embeddings' with the vector values
    df_small['embeddings'] = embeddings

    # save embeddings
    df_small.to_pickle(file_path)
else:
    print('Embeddings exists')
    # Load the DataFrame from the pickle file
    df_small = pd.read_pickle(file_path)


# calculate embedding for question
question_embedding = calculate_embeddings(question)

# Calculate cosine similarity
cosine_similarities = df_small['embeddings'].apply(lambda x: cosine_similarity([x], [question_embedding])[0][0])

# Find the index of the maximum similarity
max_similarity_index = cosine_similarities.idxmax()

# Access the row with the maximum similarity
nearest_row = df_small.loc[max_similarity_index]

print("Index of Nearest Row:", max_similarity_index)
print("URL:", nearest_row['url'])

send_answer(token, nearest_row['url'])




