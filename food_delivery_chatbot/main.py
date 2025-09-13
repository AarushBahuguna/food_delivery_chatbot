# main.py
from food_ordering.cart_manager import CartManager
from food_ordering.order_processor import OrderProcessor
from food_ordering.recommendations import FoodRecommender
from customer_support.support_handler import SupportHandler
from gemini_service import GeminiService
from utils.helpers import get_user_input, get_int_input
from config import FOOD_MENU # Import FOOD_MENU here for initial display
# main.py (TEMPORARY ADDITION FOR DEBUGGING)
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found. Please set it in your .env file.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Available Gemini Models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
# END TEMPORARY ADDITION
class FoodDeliveryChatbot:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.cart_manager = CartManager()
        self.order_processor = OrderProcessor(self.cart_manager)
        self.food_recommender = FoodRecommender(self.gemini_service)
        self.support_handler = SupportHandler(self.gemini_service)
        self.running = True

    def display_main_menu(self):
        print("\n--- Main Menu ---")
        print("1. Food Order")
        print("2. Customer Support")
        print("3. Exit")
        return get_user_input("Enter your choice: ")

    def handle_food_order(self):
        while True:
            print("\n--- Food Order Menu ---")
            print("1. View Menu")
            print("2. Add Item to Cart")
            print("3. View Cart")
            print("4. Remove Item from Cart")
            print("5. Get Food Recommendations (AI Powered)")
            print("6. Place Order")
            print("7. Back to Main Menu")

            choice = get_user_input("Enter your choice: ")

            if choice == '1':
                print(self.order_processor.display_menu())
            elif choice == '2':
                item_id = get_user_input("Enter item ID to add: ")
                quantity = get_int_input("Enter quantity (default 1): ", min_val=1)
                print(self.cart_manager.add_item(item_id, quantity))
            elif choice == '3':
                print(self.cart_manager.view_cart())
            elif choice == '4':
                item_id = get_user_input("Enter item ID to remove: ")
                quantity = get_int_input("Enter quantity (default 1): ", min_val=1)
                print(self.cart_manager.remove_item(item_id, quantity))
            elif choice == '5':
                preference = get_user_input("Tell me what you're in the mood for (e.g., 'something spicy', 'healthy options', 'Italian food'): ")
                print(self.food_recommender.get_recommendations_for_user(preference))
            elif choice == '6':
                if not self.cart_manager.cart:
                    print("Your cart is empty. Add items before placing an order.")
                    continue
                print("\n--- Payment Options ---")
                print("1. UPI")
                print("2. Pay on Delivery")
                payment_choice = get_user_input("Select payment method (1 or 2): ")
                payment_method = "UPI" if payment_choice == '1' else "Pay on Delivery" if payment_choice == '2' else None

                if payment_method:
                    print(self.order_processor.place_order(payment_method))
                else:
                    print("Invalid payment method selected.")
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def handle_customer_support(self):
        while True:
            print("\n--- Customer Support ---")
            user_query = get_user_input("What can I help you with today? (e.g., 'track my order', 'my food is late', 'missing item', 'back to main menu')\nYour query: ")
            
            if user_query.lower() == 'back to main menu':
                break
            
            solution = self.support_handler.get_solution(user_query)
            print(f"\nChatbot: {solution}")

    def run(self):
        print("Welcome to the Food Delivery Chatbot!")
        print("Initializing Gemini AI...")
        # A small delay for perception
        
        while self.running:
            main_choice = self.display_main_menu()
            if main_choice == '1':
                self.handle_food_order()
            elif main_choice == '2':
                self.handle_customer_support()
            elif main_choice == '3':
                print("Thank you for using the chatbot. Goodbye!")
                self.running = False
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Display a chatbot icon. This will be replaced by an image.
    print("Initializing your Food Delivery Chatbot...")
    # This ` ` tag indicates an image should be generated here.
    # The prompt for this image would ideally be something like:
    # "A friendly, futuristic robot chatbot logo with food delivery elements, digital art style."
    
    chatbot = FoodDeliveryChatbot()
    chatbot.run()