import datetime
import time

def normalise_cost(cost: int) -> float:
    return (cost / 100)


def current_month() -> str:
    date: datetime = datetime.date.today()
    month: str = date.strftime("%B")
    return month


def is_token_expired(expiry: int) -> bool:
    return int(expiry) - time.time() < 0