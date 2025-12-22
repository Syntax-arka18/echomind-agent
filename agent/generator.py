import vertexai
from vertexai.generative_models import GenerativeModel
from config import PROJECT_ID, REGION, GEMINI_MODEL

vertexai.init(project=PROJECT_ID, location=REGION)
model = GenerativeModel(GEMINI_MODEL)

def generate_reply(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
