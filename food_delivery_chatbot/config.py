# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Food Menu Data ---
FOOD_MENU = {
    "1": {"name": "Burger", "price": 150.00, "category": "Fast Food", "description": "Classic beef patty with fresh veggies."},
    "2": {"name": "Pizza", "price": 300.00, "category": "Italian", "description": "Large pepperoni pizza."},
    "3": {"name": "Pasta Alfredo", "price": 250.00, "category": "Italian", "description": "Creamy Alfredo pasta with mushrooms."},
    "4": {"name": "Sushi Platter", "price": 450.00, "category": "Japanese", "description": "Assorted fresh sushi and sashimi."},
    "5": {"name": "Taco Combo", "price": 200.00, "category": "Mexican", "description": "Two crispy tacos with your choice of filling."},
    "6": {"name": "Salad Bowl", "price": 180.00, "category": "Healthy", "description": "Fresh greens with grilled chicken and vinaigrette."},
    "7": {"name": "Biryani", "price": 280.00, "category": "Indian", "description": "Fragrant basmati rice with marinated chicken/mutton."},
    "8": {"name": "Fried Rice", "price": 220.00, "category": "Chinese", "description": "Stir-fried rice with vegetables and your choice of protein."},
    "9": {"name": "Momo Platter", "price": 190.00, "category": "Nepalese", "description": "Steamed dumplings with spicy dipping sauce."},
    "10": {"name": "Cold Drink", "price": 50.00, "category": "Beverage", "description": "Assorted soft drinks."},
}

# --- Customer Support Data ---
CUSTOMER_PROBLEMS_SOLUTIONS = {
    "order tracking": "You can track your order using the 'Track Order' option in the app, or by entering your order ID on our website. Please provide your Order ID if you need further assistance.",
    "delivery delay": "We apologize for the delay. Sometimes, unforeseen circumstances like traffic or weather can cause delays. Please check your order tracking for the latest updates. If it's significantly delayed, we'll notify you and offer a solution.",
    "missing item": "We are sorry to hear an item is missing. Please provide your Order ID and the name of the missing item. We will investigate immediately and arrange for a re-delivery or refund.",
    "wrong order": "We sincerely apologize for the error. Please provide your Order ID and describe the items you received. We will arrange for the correct order to be delivered or issue a full refund.",
    "payment issue": "If you faced a payment issue, please check if the amount was debited from your account. If debited, it usually gets refunded within 5-7 business days. If not, please try again or use an alternative payment method.",
    "cancel order": "You can cancel your order within a few minutes of placing it through the app. If the restaurant has already started preparing, cancellation might not be possible, or a cancellation fee may apply.",
    "refund status": "Refunds typically take 5-7 business days to process after approval. Please check your bank statement. If it's been longer, provide your Order ID, and we'll check the status.",
    "app not working": "Please try restarting the app or your phone. Also, ensure you have a stable internet connection. If the problem persists, try reinstalling the app.",
    "account issues": "For account-related problems like login issues or forgotten passwords, please use the 'Forgot Password' option or contact our live chat support for assistance with account recovery.",
    "restaurant feedback": "We appreciate your feedback! You can leave a review for the restaurant and specific food items after your order is delivered through the app. This helps us improve our service.",
    "general inquiry": "How can I help you today? Please tell me more about your question or concern.",
}

# Add some broader keywords for support
SUPPORT_KEYWORDS = {
    "track": "order tracking", "where is my food": "order tracking",
    "late": "delivery delay", "delivery time": "delivery delay",
    "missing": "missing item", "not received": "missing item",
    "wrong": "wrong order", "incorrect food": "wrong order",
    "paid but failed": "payment issue", "money deducted": "payment issue",
    "how to cancel": "cancel order", "remove order": "cancel order",
    "refund not received": "refund status", "when will i get my money back": "refund status",
    "app crash": "app not working", "bug in app": "app not working",
    "login": "account issues", "password": "account issues",
    "feedback": "restaurant feedback", "review": "restaurant feedback",
    "question": "general inquiry", "help": "general inquiry"
}