from langchain_community.utilities import SerpAPIWrapper

search = SerpAPIWrapper()

def activity_agent(state):
    result = search.run(f"top attractions in {state['destination']}")
    return {"activities": [result]}