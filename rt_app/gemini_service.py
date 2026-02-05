import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY_2"))

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


def generate_medical_summary(conversation_text):
    prompt = f"""
    You are a medical assistant.

    Given the following doctor–patient conversation, generate a concise and structured summary.

    Rules:
    - Do NOT invent information.
    - Only use what is present in the conversation.
    - Be clinically relevant and brief.
    - Use bullet points.
    - If a section is not mentioned, write "Not mentioned".

    Extract and organize the summary into these sections:

    1. Symptoms
    2. Diagnosis / Clinical Impression
    3. Medications / Treatment
    4. Follow-up Instructions or Advice

    Conversation:
    \"\"\"
    {conversation_text}
    \"\"\"

    Return only the summary. No extra commentary.
"""

    response = model.generate_content(prompt)
    return response.text.strip()
model = genai.GenerativeModel('gemini-2.5-flash-lite')


