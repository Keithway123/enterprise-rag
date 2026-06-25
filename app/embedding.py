import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def get_embedding(text:str)->list[float]:
    response = client.embeddings.create(
        model="text-embedding-v3",
        input=text,
        dimensions=1024,
    )
    return response.data[0].embedding
