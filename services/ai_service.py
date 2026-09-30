from dotenv import load_dotenv
from google import genai
import os


class AIService:
    def __init__(self):
        load_dotenv("api.env")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    def explain(self, selected_text, context=None):
        context_text=(
            f"dans le contexte « {context['before']} "
            f"{context['selected']} {context['after']} », "
            if context
            else ""
        )
        prompt = (
            f"tu es un assistant de lecture. "
            f"Explique uniquement '{selected_text}' {context_text}"
            f"de façon très simple et courte, sans introduction ni détour. "
            f"Va directement à l\'explication."
        )
        response=self.client.models.generate_content(model="gemini-3.1-flash-lite", 
        contents=prompt)
        return response.text