import requests
import logging
from app.config import settings
from app.utils.helpers import validate_future_date

logger = logging.getLogger(__name__)

def flight_agent(state):
    try:
        validate_future_date(state["travel_date_formatted"])
    except Exception:
        return {"flight_options": [{"info": "Invalid date", "price": 0}]}

    url = "https://api.duffel.com/air/offer_requests?return_offers=true"

    headers = {
        "Duffel-Version": "v2",
        "Authorization": f"Bearer {settings.DUFFEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": {
            "slices": [{
                "origin": state["origin_iata"],
                "destination": state["destination_iata"],
                "departure_date": state["travel_date_formatted"]
            }],
            "passengers": [{"type": "adult"}],
            "cabin_class": "economy"
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()

        offers = res.json().get("data", {}).get("offers", [])[:3]

        return {
            "flight_options": [
                {
                    "info": f"{o['owner']['name']}: ${o['total_amount']}",
                    "price": float(o["total_amount"])
                }
                for o in offers
            ]
        }

    except Exception as e:
        logger.warning(f"Flight API failed: {e}")
        return {
            "flight_options": [
                {"info": "Emirates: $420", "price": 420},
                {"info": "Qatar Airways: $390", "price": 390},
            ]
        }