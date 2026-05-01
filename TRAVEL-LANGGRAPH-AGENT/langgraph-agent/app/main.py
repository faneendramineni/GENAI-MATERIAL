from fastapi import FastAPI, Body, HTTPException
from app.graph import graph
from app.config import logger

app = FastAPI(title="Travel Agent API")

@app.post("/chat")
async def chat(payload: dict = Body(...)):
    thread_id = payload.get("thread_id", "session_1")
    config = {"configurable": {"thread_id": thread_id}}
    action = payload.get("action")
    data = payload.get("data", {})

    try:
        if action == "start":
            graph.invoke(data, config)
        
        elif action == "select_prices":
            # Update price and trigger budget_check node
            graph.update_state(config, data)
            graph.invoke(None, config)

        elif action == "confirm_booking":
            # Moves graph from breakpoint to END
            graph.invoke(None, config)

        elif action == "retrieve":
            pass 

        elif action == "fix_budget":
            # Update total_budget and re-run supervisor/route logic
            graph.update_state(config, data)
            graph.invoke(None, config)
            
        else:
            raise HTTPException(status_code=400, detail="Invalid action")

        # Get the latest values from the checkpointer
        state_values = graph.get_state(config).values
        return state_values

    except Exception as e:
        logger.error(f"Backend Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}