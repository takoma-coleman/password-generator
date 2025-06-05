import randomAdd commentMore actions
import string

def generate_password(length, use_numbers, use_specials):
    letters = string.ascii_letters  # a-zA-Z
    numbers = string.digits         # 0-9
    specials = "!@#$%^&*()-_=+[]{};:,.<>?/|"

    character_pool = letters
    if use_numbers:
        character_pool += numbers
    if use_specials:
        character_pool += specials

    if not character_pool:
        raise RuntimeError("Error: No character pool selected.")

    return ''.join(random.choice(character_pool) for _ in range(length))

def get_valid_int(prompt, min_val=1):
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Please enter an integer >= {min_val}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'n'):
            return response == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    print("Password Generator")
    length = get_valid_int("Password length: ")
    use_numbers = get_yes_no("Include numbers? (y/n): ")
    use_specials = get_yes_no("Include special characters? (y/n): ")
    
    count_input = input("How many passwords to generate? (default 1): ").strip()
    if count_input == "":
        count = 1
    else:
        try:
            count = int(count_input)
            if count < 1:
                raise ValueError
        except ValueError:
            raise RuntimeError("Error: Password count must be a positive integer.")

    print("\nGenerated Password(s):")
    for _ in range(count):
        print(generate_password(length, use_numbers, use_specials))

if __name__ == "__main__":
    main()