import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel("gemini-1.5-flash")


def translate_text(text, from_lang, to_lang):
    prompt = f"""
    You are a medical translator.
    Translate the following message from {from_lang} to {to_lang}.
    Only return the translated text.

    Message: {text}
    """

    response = model.generate_content(prompt)
    return response.text.strip()


model = genai.GenerativeModel('gemini-2.5-flash-lite')

response = model.generate_content("Hello!")
print(response.text)
