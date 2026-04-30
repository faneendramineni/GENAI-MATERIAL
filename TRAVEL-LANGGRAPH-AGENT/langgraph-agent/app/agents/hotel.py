from langchain_community.utilities import SerpAPIWrapper

search = SerpAPIWrapper()

def hotel_agent(state):
    result = search.run(f"best hotels in {state['destination']} 2026")
    return {"hotel_options": [{"info": result[:300]}]}