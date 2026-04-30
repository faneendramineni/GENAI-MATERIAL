import json
import re
import logging
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.models.state import TravelState
from app.utils.helpers import normalize_date, fallback_iata
from app.agents.flight import flight_agent
from app.agents.hotel import hotel_agent
from app.agents.activity import activity_agent
from app.config import settings

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=settings.OPENAI_API_KEY
)


def input_processor_node(state: TravelState):
    formatted_date = normalize_date(state["travel_date_input"])

    prompt = f"""
    Return ONLY JSON:
    {{
      "origin_iata": "...",
      "destination_iata": "..."
    }}
    Origin: {state['origin']}
    Destination: {state['destination']}
    """

    try:
        raw = llm.invoke(prompt).content.strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)

        if match:
            data = json.loads(match.group(0))
            origin_iata = data["origin_iata"].upper()
            dest_iata = data["destination_iata"].upper()
        else:
            raise ValueError()

    except Exception:
        origin_iata = fallback_iata(state["origin"])
        dest_iata = fallback_iata(state["destination"])

    return {
        "origin_iata": origin_iata,
        "destination_iata": dest_iata,
        "travel_date_formatted": formatted_date
    }


def supervisor_node(state: TravelState):
    total = state.get("total_budget", 0)
    spent = state.get("selected_flight_price", 0) + state.get("selected_hotel_price", 0)
    return {"remaining_budget": total - spent}


def budget_warning_node(state: TravelState):
    return {}


def route(state: TravelState):
    return "warn" if state["remaining_budget"] < 0 else "proceed"


def build_graph():
    builder = StateGraph(TravelState)

    builder.add_node("processor", input_processor_node)
    builder.add_node("flights", flight_agent)
    builder.add_node("hotels", hotel_agent)
    builder.add_node("activities", activity_agent)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("budget_warning", budget_warning_node)

    builder.set_entry_point("processor")

    builder.add_edge("processor", "flights")
    builder.add_edge("flights", "hotels")
    builder.add_edge("hotels", "supervisor")

    builder.add_conditional_edges(
        "supervisor",
        route,
        {
            "warn": "budget_warning",
            "proceed": "activities"
        }
    )

    builder.add_edge("activities", END)
    builder.add_edge("budget_warning", END)

    return builder.compile(checkpointer=MemorySaver())