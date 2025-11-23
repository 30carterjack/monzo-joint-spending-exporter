import datetime

def normalise_cost(cost: int) -> float:
    return (cost / 100)

def current_month() -> str:
    date: datetime = datetime.date.today()
    month: str = date.strftime("%B")
    return month