from datetime import datetime

def normalize_date(user_input: str) -> str:
    current_year = datetime.now().year
    try:
        parsed = datetime.strptime(f"{user_input} {current_year}", "%b %d %Y")
    except ValueError:
        parsed = datetime.strptime(f"{user_input} {current_year}", "%B %d %Y")
    return parsed.strftime("%Y-%m-%d")


def validate_future_date(date_str: str):
    if datetime.strptime(date_str, "%Y-%m-%d") < datetime.now():
        raise ValueError("Travel date is in the past")


def fallback_iata(city: str) -> str:
    mapping = {
        "dubai": "DXB",
        "bangkok": "BKK",
        "bankok": "BKK",
        "london": "LHR"
    }
    return mapping.get(city.lower(), "DXB")