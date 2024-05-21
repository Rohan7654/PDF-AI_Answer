import io
from PyPDF2 import PdfReader, PdfWriter
import requests
import os

def llm_prompt(question, model="gpt-4-1106-preview", temperature=0.5):
    API_URL = "https://api.openai.com/v1/completions"
    API_KEY = os.environ.get("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": model,
        "prompt": question,
        "temperature": temperature,
        "max_tokens": 150
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json().get("choices", [{}])[0].get("text", "").strip()


def process_pdf_questions(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        text = page.extract_text()
        questions = [line for line in text.split('\n') if line.endswith('?')]
        for question in questions:
            answer = llm_prompt(question, model="gpt-4-1106-preview", temperature=0.5)
            page.add_annotation({
                'text': answer,
                'rect': [0, 0, 100, 100],
                'border': {'width': 1},
                'color': [0, 0, 0]
            })
        writer.add_page(page)
    output = io.BytesIO()
    writer.write(output)
    return output