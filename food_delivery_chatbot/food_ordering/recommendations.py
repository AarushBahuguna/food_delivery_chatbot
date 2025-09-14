# food_ordering/recommendations.py
import json
from gemini_service import GeminiService
from config import FOOD_MENU

class FoodRecommender:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def get_recommendations_for_user(self, user_preference_query: str):
        """
        Analyzes a complex user query, decides on an action (like building a cart),
        and returns a structured JSON response or a simple text fallback.
        """
        # Create a detailed menu string with all necessary info for the AI
        menu_for_prompt = []
        for item_id, details in FOOD_MENU.items():
            # Assuming 'tags' like ['indian', 'healthy'] exist in your FOOD_MENU items
            tags = ", ".join(details.get('tags', []))
            menu_for_prompt.append(f"ID: {item_id}, Name: {details['name']}, Price: {details['price']:.2f}, Tags: [{tags}]")
        
        menu_as_string = "\n".join(menu_for_prompt)

        # This is the new, more powerful prompt
        prompt = (
            f"You are an intelligent food ordering assistant. A customer said: '{user_preference_query}'.\n"
            f"Analyze their request. Your goal is to fulfill it completely.\n"
            f"If they ask you to create a cart, find the best combination of items from the menu below that fits their criteria (like budget, cuisine, health preferences).\n\n"
            f"MENU:\n{menu_as_string}\n\n"
            f"Based on the user's request, decide on an action. Respond ONLY with a JSON object in the following format:\n"
            f'{{"action": "add_to_cart", "items_to_add": ["item_id_1", "item_id_2", ...], "reasoning": "A brief explanation of your choices."}}\n'
            f"If you are only recommending, use action 'recommend' and put your text in 'reasoning'.\n"
            f"If you cannot fulfill the request, use action 'cannot_fulfill' and explain why in 'reasoning'."
        )

        print(f"DEBUG: Asking Gemini for intelligent action based on: {user_preference_query}")
        
        try:
            response_text = self.gemini_service.generate_response(prompt)
            # Clean up the response to ensure it's valid JSON
            cleaned_response = response_text.strip().replace("```json", "").replace("```", "")
            return json.loads(cleaned_response)
        except (json.JSONDecodeError, TypeError):
            # Fallback for simple text responses or errors
            print("DEBUG: Gemini response was not valid JSON. Falling back to text.")
            return {"action": "recommend", "reasoning": "I can suggest some items for you: Salad Bowl, Biryani, and Momos are great options!"}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"action": "cannot_fulfill", "reasoning": "I'm having a bit of trouble thinking right now. Could you try asking in a simpler way?"}

    def get_recommendations_for_item(self, item_name: str) -> str:
        """
        Gets recommendations for items that pair well with the given item.
        """
        menu_as_string = "\n".join([f"- {item['name']}" for item in FOOD_MENU.values()])
        
        prompt = (f"A customer just added '{item_name}' to their cart. "
                  f"Based on the following menu, what are 2-3 other items (like sides, drinks, or desserts) that would pair well with it? "
                  f"Keep the suggestions brief and enticing.\n\n"
                  f"Here is the menu:\n{menu_as_string}")

        try:
            recommendations = self.gemini_service.generate_response(prompt)
            # Simple check to ensure we don't return an empty or error response
            if recommendations and "sorry" not in recommendations.lower():
                return recommendations
            return "" # Return empty if no good recommendations were found
        except Exception:
            return "" # Return empty on error