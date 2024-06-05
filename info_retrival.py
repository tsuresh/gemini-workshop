import google.generativeai as genai
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-pro')

document = pathlib.Path('document.txt').read_text()

result = model.generate_content(f"""
  What is this organisation?

  Please answer based on the following document:
  {document}""")

print(result.text)