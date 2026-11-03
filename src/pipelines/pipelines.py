from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    #1st step of pipeline
    state = {}

    print("\n"+" ="*50)
    print("Step 1: Search agent is working...")
    print("="*50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user", f"Search for relevant, current and detailed information on: {topic}")]
    })
    state["search_results"] = search_results["messages"][-1].content

    print(f"\n search results\n", state['search_results'])

    #2nd step of pipeline
    print("\n"+" ="*50)
    print("Step 2: Reader agent is working...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results on the '{topic}'\n"
            f"Pick the most relevant URL and scrap it for deeper content\n"
            f"Search results: \n{state['search_results'][:800]}"
            )]
    })

    state["scrapped_content"] = reader_results["messages"][-1].content
    print("\nReader agent results: ", state["scrapped_content"])


    #3rd step: Writer chain
    print("\n"+" ="*50)
    print("Step 3: Writer chain is working...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS: \n{state['search_results']}\n\n"
        f"SCRAPPED CONTENT: \n{state['scrapped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print(f"\n Final Report: \n{state['report']}" )


    #4th step: Critic Chain
    print("\n"+" ="*50)
    print("Step 4: Critic chain is working...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic report: \n", state['feedback'])

    return state

