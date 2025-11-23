import datetime

def normalise_cost(cost: int):
    return (cost / 100)

def current_month():
    date = datetime.date.today()
    month = date.strftime("%B")
    return month
