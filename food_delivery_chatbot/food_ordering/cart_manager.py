# food_ordering/cart_manager.py
from typing import Dict, List
from config import FOOD_MENU

class CartManager:
    def __init__(self):
        self.cart: Dict[str, Dict] = {} # {item_id: {name: "", price: "", quantity: ""}}

    def add_item(self, item_id: str, quantity: int = 1) -> str:
        if item_id not in FOOD_MENU:
            return "Sorry, that item ID is not valid."
        
        item_info = FOOD_MENU[item_id]
        if item_id in self.cart:
            self.cart[item_id]["quantity"] += quantity
        else:
            self.cart[item_id] = {
                "name": item_info["name"],
                "price": item_info["price"],
                "quantity": quantity
            }
        return f"Added {quantity} x {item_info['name']} to your cart."

    def remove_item(self, item_id: str, quantity: int = 1) -> str:
        if item_id not in self.cart:
            return "That item is not in your cart."
        
        if self.cart[item_id]["quantity"] <= quantity:
            del self.cart[item_id]
            return f"Item removed from cart."
        else:
            self.cart[item_id]["quantity"] -= quantity
            return f"Removed {quantity} x {self.cart[item_id]['name']} from your cart."

    def view_cart(self) -> str:
        if not self.cart:
            return "Your cart is empty."
        
        cart_summary = ["--- Your Cart ---"]
        total = 0
        for item_id, details in self.cart.items():
            item_total = details['price'] * details['quantity']
            cart_summary.append(f"{details['name']} (x{details['quantity']}) - ₹{details['price']:.2f} each | Total: ₹{item_total:.2f}")
            total += item_total
        cart_summary.append(f"-----------------")
        cart_summary.append(f"Subtotal: ₹{total:.2f}")
        return "\n".join(cart_summary)

    def get_total_cost(self) -> float:
        total = 0
        for item_id, details in self.cart.items():
            total += details['price'] * details['quantity']
        return total

    def clear_cart(self):
        self.cart = {}