# food_ordering/recommendations.py
# Fix: Import GeminiService absolutely from the project root
from gemini_service import GeminiService # Corrected import
from config import FOOD_MENU # Keep this as it's correct for config

class FoodRecommender:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def get_recommendations_for_user(self, user_preference_query: str) -> str:
        """
        Gets food recommendations based on user's natural language preferences.
        """
        print(f"DEBUG: Asking Gemini for recommendations based on: {user_preference_query}")
        recommendations = self.gemini_service.get_food_recommendations(user_preference_query)
        
        # Parse Gemini's response and link back to our menu if possible
        recommended_items = []
        for line in recommendations.split('\n'):
            for item_id, item_data in FOOD_MENU.items():
                if item_data['name'].lower() in line.lower():
                    recommended_items.append(f"{item_data['name']} (₹{item_data['price']:.2f})")
                    break
        
        if recommended_items:
            return "Based on your preferences, you might like:\n- " + "\n- ".join(recommended_items)
        else:
            return "I couldn't find specific recommendations based on your input, but here are some popular items:\n" + \
                   ", ".join([FOOD_MENU['1']['name'], FOOD_MENU['2']['name'], FOOD_MENU['7']['name']])