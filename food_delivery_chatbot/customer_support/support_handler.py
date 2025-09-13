# customer_support/support_handler.py
from gemini_service import GeminiService
from config import CUSTOMER_PROBLEMS_SOLUTIONS # Import this here

class SupportHandler:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.current_support_topic = None # To track if we're in a follow-up
        self.expected_info = None         # What information we are currently expecting

    def get_solution(self, user_query: str) -> str:
        user_query_lower = user_query.lower().strip()

        # --- Handle follow-up inputs ---
        if self.expected_info:
            if self.current_support_topic == "missing item":
                # Assuming the user directly provides Order ID + Item Name after being prompted
                # A more robust system would use NLU to extract these.
                self.expected_info = None # Reset for next turn
                self.current_support_topic = None
                return self.process_missing_item_info(user_query)
            # Add other follow-up handling here (e.g., for 'delivery delay' needing order ID)
            
            # If nothing specific handled, just pass to Gemini as a general query
            self.expected_info = None # Reset
            self.current_support_topic = None
            return self.gemini_service.get_customer_support_solution(user_query)


        # --- Initial query processing ---
        # First, try to find a direct match or keyword match
        matched_problem_key = None
        for problem_key in CUSTOMER_PROBLEMS_SOLUTIONS.keys():
            if problem_key in user_query_lower:
                matched_problem_key = problem_key
                break
        
        # If no direct match, check general keywords
        if not matched_problem_key:
            for keyword, problem_key in self.gemini_service.SUPPORT_KEYWORDS.items():
                if keyword in user_query_lower:
                    matched_problem_key = problem_key
                    break

        if matched_problem_key:
            solution = CUSTOMER_PROBLEMS_SOLUTIONS.get(matched_problem_key)
            if "Please provide your Order ID and the name of the missing item" in solution:
                self.current_support_topic = "missing item"
                self.expected_info = "order_id_and_item_name"
                return solution + " Please provide it now." # Add a clear call to action
            # Add other cases that require follow-up
            
            self.current_support_topic = None
            self.expected_info = None
            return solution
        else:
            # If no keyword match, use Gemini for broader queries
            self.current_support_topic = None
            self.expected_info = None
            return self.gemini_service.get_customer_support_solution(user_query)

    def process_missing_item_info(self, user_input: str) -> str:
        # Here, you'd ideally use more advanced NLP (Gemini) to extract
        # "Order ID" and "item name". For simplicity, let's just confirm receipt.
        
        # You could try to parse, e.g., using regex:
        # import re
        # order_id_match = re.search(r'order id[:\s]*(\w+)', user_input, re.IGNORECASE)
        # item_name_match = re.search(r'item[:\s]*(.+)', user_input, re.IGNORECASE)
        # order_id = order_id_match.group(1) if order_id_match else "N/A"
        # item_name = item_name_match.group(1) if item_name_match else "N/A"

        # For now, let's just confirm receipt of information
        response_from_gemini = self.gemini_service.generate_response(
            prompt=f"User reported a missing item and provided this information: '{user_input}'. "
                   "Acknowledge receipt, confirm we are investigating, and mention typical resolution time (e.g., 24-48 hours). "
                   "Be polite and reassuring.",
            temperature=0.7
        )
        return response_from_gemini