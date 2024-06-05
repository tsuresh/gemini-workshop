import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('models/gemini-pro')

resp = model.generate_content(
  'Write the first paragraph of a story about a magic backpack')


resp = model.generate_content(
  'Write the first paragraph of a story about a magic backpack')

print(resp.text)
