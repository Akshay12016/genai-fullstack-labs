from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama

# State definition
class PoemState(dict):
    topic: str
    poem: str

# Local LLM
llm = ChatOllama(model="llama3")

def generate_poem(state: PoemState):
    prompt = f"Write a 4-line poem about {state['topic']}"
    response = llm.invoke(prompt)
    state["poem"] = response.content
    return state

# Build LangGraph
graph = StateGraph(PoemState)
graph.add_node("poem_generator", generate_poem)
graph.set_entry_point("poem_generator")
graph.set_finish_point("poem_generator")

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"topic": "Nature"})
    print("\n🌸 Generated Poem:\n")
    print(result["poem"])
