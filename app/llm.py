import os 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def generate_answer(prompt:str) ->str:
    response = client.responses.create(
        model="qwen3.7-plus",
        input=[
            {"role":"user","content":prompt}
        ],
    )
    
    return response.output_text