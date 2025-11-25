import datetime
import time

def normalise_cost(cost: int) -> float:
    return (cost / 100)

def wait_event():
    while True:
        user_input: str = str(input("\nType 'done' once approved, or type 'cancel' to abort: ").strip().lower())
        if user_input.lower() == 'done':
            print("\ncontinuing...")
            break
        elif user_input.lower() == "cancel":
            print("\nOperation cancelled by user.")
            exit(0)
        else:
            print("\nInvalid input. Please type 'done' after completing the request.")


def current_month() -> str:
    date: datetime = datetime.date.today()
    month: str = date.strftime("%B")
    return month


def is_token_expired(expiry: int) -> bool:
    return int(expiry) - time.time() < 0
