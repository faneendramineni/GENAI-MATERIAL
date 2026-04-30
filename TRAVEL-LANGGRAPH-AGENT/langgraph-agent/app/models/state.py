from typing import TypedDict, List, Annotated
import operator

class TravelState(TypedDict, total=False):
    origin: str
    destination: str
    travel_date_input: str
    travel_date_formatted: str

    origin_iata: str
    destination_iata: str

    total_budget: float
    remaining_budget: float

    selected_flight_price: float
    selected_hotel_price: float

    flight_options: List[dict]
    hotel_options: List[dict]
    activities: List[str]

    messages: Annotated[List[dict], operator.add]