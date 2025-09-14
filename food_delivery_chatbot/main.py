# main.py
from food_ordering.cart_manager import CartManager
from food_ordering.order_processor import OrderProcessor
from food_ordering.recommendations import FoodRecommender
from customer_support.support_handler import SupportHandler
from gemini_service import GeminiService
from utils.helpers import get_user_input, get_int_input
from config import FOOD_MENU

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
            print("5. Chat with Chatori")
            print("6. Place Order")
            print("7. Back to Main Menu")

            choice = get_user_input("Enter your choice: ")

            if choice == '1':
                print(self.order_processor.display_menu())
            elif choice == '2':
                item_id = get_user_input("Enter item ID to add: ")
                quantity = get_int_input("Enter quantity (default 1): ", min_val=1)
                
                add_status_message = self.cart_manager.add_item(item_id, quantity)
                print(add_status_message)

                # Check if the item was added successfully before recommending
                if item_id in FOOD_MENU:
                    item_name = FOOD_MENU[item_id]["name"]
                    # Call the new recommender method
                    item_recommendations = self.food_recommender.get_recommendations_for_item(item_name)
                    if item_recommendations:
                        print("\n🤖 You might also like...")
                        print(item_recommendations)
                
            elif choice == '3':
                print(self.cart_manager.view_cart())
            elif choice == '4':
                item_id = get_user_input("Enter item ID to remove: ")
                quantity = get_int_input("Enter quantity (default 1): ", min_val=1)
                print(self.cart_manager.remove_item(item_id, quantity))
            elif choice == '5':
                preference = get_user_input("Tell me what you're in the mood for (e.g., 'something spicy', 'healthy options', 'Italian food'): ")
                
                ai_response = self.food_recommender.get_recommendations_for_user(preference)

                if isinstance(ai_response, dict):
                    action = ai_response.get("action")
                    reasoning = ai_response.get("reasoning", "Here's what I did.")
                    
                    print(f"\n🤖 Chatbot: {reasoning}")

                    if action == "add_to_cart":
                        items_to_add = ai_response.get("items_to_add", [])
                        if not items_to_add:
                            print("It looks like I couldn't find any items that matched perfectly.")
                        else:
                            for item_id in items_to_add:
                                # Add one of each suggested item
                                print(self.cart_manager.add_item(item_id, 1))
                            print("\nI've added these items to your cart for you!")
                            print(self.cart_manager.view_cart())
                    
                else: # Fallback for plain string responses
                    print(f"\nChatbot: {ai_response}")

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
        print("\n--- Customer Support ---") # Print the header only once
        while True:
            # Check if the support handler is expecting follow-up information
            if self.support_handler.expected_info:
                prompt = "Your response: "
            else:
                prompt = "What can I help you with today? (e.g., 'track my order', 'my food is late', 'missing item', 'back to main menu')\nYour query: "
            
            user_query = get_user_input(prompt)
            
            if user_query.lower() == 'back to main menu':
                # Reset support state when leaving
                self.support_handler.current_support_topic = None
                self.support_handler.expected_info = None
                break
            
            solution = self.support_handler.get_solution(user_query)
            print(f"\nChatbot: {solution}")

    def run(self):
        print("Welcome to the Food Delivery Chatbot!")
        
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
    chatbot = FoodDeliveryChatbot()
    chatbot.run()