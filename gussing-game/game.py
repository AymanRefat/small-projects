import random

intro = """
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
You have 5 chances to guess the correct number.
"""

win = "Congratulations! You have guessed the correct number."
levels = {"easy": 10, "medium": 5, "hard": 3}


def print_levels():
    print("Choose a difficulty level:")
    for i, level in enumerate(levels):
        print(f"{i + 1}. {level}")


def choose_level() -> int:
    while True:
        try:
            level = input("Enter the level number: ")
            level = int(level)
            if level in range(1, len(levels) + 1):
                break
            else:
                print("Invalid level. Please enter a valid level number.")
        except ValueError:
            print("Invalid level. Please enter a valid level number.")
    return level


def print_chosen_level(level: int):
    print(f"You have chosen the {list(levels.keys())[level - 1]} level.")


def get_random_number():
    return random.randint(1, 100)


def get_user_guess():
    while True:
        try:
            guess = input("Make a guess: ")
            guess = int(guess)
            if guess not in range(1, 101):
                print("Invalid guess. Please enter a number between 1 and 100.")
                break
            else:
                break
        except ValueError:
            print("Invalid guess. Please enter a number between 1 and 100.")
    return guess


def check_guess(guess: int, number: int) -> bool:
    if guess == number:
        return True
    elif guess < number:
        print("Too low.")
    else:
        print("Too high.")
    return False


def play_game():
    print(intro)
    print_levels()
    level = choose_level()
    print_chosen_level(level)
    number = get_random_number()

    tries = levels[list(levels.keys())[level - 1]]
    print(f"You have {tries} chances to guess the correct number.")
    while tries > 0:
        guess = get_user_guess()
        if check_guess(guess, number):
            print(win)
            break
        else:
            print("Try again.")
        tries -= 1
        print(f"You have {tries} tries left.")
    else:
        print(f"Game over! The correct number was {number}.")
        print("Better luck next time!")


if __name__ == "__main__":
    play_game()
