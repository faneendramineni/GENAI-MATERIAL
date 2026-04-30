from fastapi import FastAPI
from app.graph import build_graph

app = FastAPI()
graph = build_graph()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/plan")
def plan_trip(payload: dict):
    config = {
        "configurable": {
            "thread_id": payload.get("session_id", "default")
        }
    }

    result = graph.invoke({
        "origin": payload["origin"],
        "destination": payload["destination"],
        "travel_date_input": payload["date"],
        "total_budget": payload["budget"],
        "messages": []
    }, config)

    return result