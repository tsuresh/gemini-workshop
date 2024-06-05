import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-pro')

chat = model.start_chat()

response = chat.send_message(
    "Hello, what should I have for dinner?")

print(response.text)
    # 'Here are some suggestions...'

response = chat.send_message(
    "How do I cook the first one?")