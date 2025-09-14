# gemini_service.py
import google.generativeai as genai
from config import GEMINI_API_KEY, FOOD_MENU, CUSTOMER_PROBLEMS_SOLUTIONS, SUPPORT_KEYWORDS

class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Make these accessible if SupportHandler needs to reference them directly
        self.CUSTOMER_PROBLEMS_SOLUTIONS = CUSTOMER_PROBLEMS_SOLUTIONS
        self.SUPPORT_KEYWORDS = SUPPORT_KEYWORDS

    # ... (rest of the class remains the same) ...
    def generate_response(self, prompt: str, temperature: float = 0.5) -> str:
        """
        Sends a prompt to the Gemini model and returns the text response.
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            print(f"An error occurred with the Gemini API: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."
    def get_customer_support_solution(self, user_query: str) -> str:
        # Removed the direct keyword matching here as SupportHandler will now manage the initial routing
        # and only call Gemini for unhandled/broader queries.
        
        prompt = (f"The user has a customer support query: '{user_query}'. "
                  "Based on common food delivery app problems, provide a helpful and empathetic solution. "
                  "Keep it concise, generally 2-3 sentences. "
                  "If you need more info, ask for it. "
                  "Consider these common themes: order tracking, delivery issues, missing/wrong items, payment, refunds, app problems.")
        return self.generate_response(prompt, temperature=0.6)