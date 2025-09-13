# food_ordering/order_processor.py
import time
from food_ordering.cart_manager import CartManager
from config import FOOD_MENU # <--- This import is correct and needed

class OrderProcessor:
    def __init__(self, cart_manager: CartManager):
        self.cart_manager = cart_manager

    def display_menu(self) -> str:
        menu_str = ["--- Our Menu ---"]
        # FIX: Directly use the imported FOOD_MENU, not through cart_manager
        for item_id, item_info in FOOD_MENU.items(): # <--- CORRECTED THIS LINE
            menu_str.append(f"{item_id}. {item_info['name']} - ₹{item_info['price']:.2f} ({item_info['category']})")
            menu_str.append(f"   Description: {item_info['description']}")
        menu_str.append("----------------")
        return "\n".join(menu_str)

    def place_order(self, payment_method: str) -> str:
        if not self.cart_manager.cart:
            return "Your cart is empty. Please add items before placing an order."

        total_cost = self.cart_manager.get_total_cost()
        order_details = self.cart_manager.view_cart()

        order_confirmation = [
            f"Placing your order with {payment_method}...",
            order_details,
            f"Total Amount: ₹{total_cost:.2f}"
        ]

        # Simulate payment processing
        time.sleep(1)
        if payment_method.lower() == "upi":
            order_confirmation.append("Initiating UPI payment... Please complete payment on your UPI app.")
            order_confirmation.append("Payment successful! Your order has been placed.")
        elif payment_method.lower() == "pay on delivery":
            order_confirmation.append("Order placed successfully! Please pay cash on delivery.")
        else:
            return "Invalid payment method. Please choose 'UPI' or 'Pay on Delivery'."

        order_confirmation.append(f"Your order will be delivered shortly! Order ID: {int(time.time())}")
        self.cart_manager.clear_cart()
        return "\n".join(order_confirmation)