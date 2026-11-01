from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("\n"+" ="*50)
    print("Step 1: Search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user", f"Find detailed, relevant and current information about {topic}")]
    })
    state["search_results"] = search_results["messages"][-1].content

    print("\n search results", state['search_results'])