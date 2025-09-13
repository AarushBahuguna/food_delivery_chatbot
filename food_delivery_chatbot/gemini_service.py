# gemini_service.py
import google.generativeai as genai
from config import GEMINI_API_KEY, FOOD_MENU, CUSTOMER_PROBLEMS_SOLUTIONS, SUPPORT_KEYWORDS

class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-pro')
        
        # Make these accessible if SupportHandler needs to reference them directly
        self.CUSTOMER_PROBLEMS_SOLUTIONS = CUSTOMER_PROBLEMS_SOLUTIONS
        self.SUPPORT_KEYWORDS = SUPPORT_KEYWORDS

    # ... (rest of the class remains the same) ...

    def get_customer_support_solution(self, user_query: str) -> str:
        # Removed the direct keyword matching here as SupportHandler will now manage the initial routing
        # and only call Gemini for unhandled/broader queries.
        
        prompt = (f"The user has a customer support query: '{user_query}'. "
                  "Based on common food delivery app problems, provide a helpful and empathetic solution. "
                  "Keep it concise, generally 2-3 sentences. "
                  "If you need more info, ask for it. "
                  "Consider these common themes: order tracking, delivery issues, missing/wrong items, payment, refunds, app problems.")
        return self.generate_response(prompt, temperature=0.6)