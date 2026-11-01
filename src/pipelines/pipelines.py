from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    #1st step of pipeline
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

    #2nd step of pipeline
    print("\n"+" ="*50)
    print("Step 2: Reader agent is working...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results on the '{topic}'",
            f"Pick the most relevant URL and scrap it for deeper content\n\n",
            f"Search results: \n{state['search_results']}"
            )]
    })

    state["reader_results"] = reader_results["messages"][-1].content
    print("\nReader agent results: ", state["reader_results"])
