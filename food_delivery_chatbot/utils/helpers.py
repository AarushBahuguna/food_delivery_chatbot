# utils/helpers.py
def get_user_input(prompt: str) -> str:
    """Gets validated string input from the user."""
    return input(prompt).strip()

def get_int_input(prompt: str, min_val: int = 1, max_val: int = 1000) -> int:
    """Gets validated integer input from the user."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")