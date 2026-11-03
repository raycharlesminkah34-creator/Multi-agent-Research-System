
import streamlit as st
from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.title("🔎 AI Research Assistant")
st.markdown(
    "An AI-powered research pipeline that searches, reads, "
    "writes, and evaluates research reports."
)

st.divider()

# -----------------------------
# RESEARCH PIPELINE
# -----------------------------
def run_research_pipeline(topic: str):

    state = {}

    # STEP 1: SEARCH AGENT
    with st.status("Step 1: Searching for relevant information...", expanded=True) as status:

        search_agent = build_search_agent()

        search_results = search_agent.invoke({
            "messages": [
                ("user", f"Search for relevant, current and detailed information on: {topic}")
            ]
        })

        state["search_results"] = search_results["messages"][-1].content

        st.write("Search completed successfully.")
        status.update(label="Step 1: Search completed", state="complete")

    # STEP 2: READER AGENT
    with st.status("Step 2: Reading and extracting information...", expanded=True) as status:

        reader_agent = build_reader_agent()

        reader_results = reader_agent.invoke({
            "messages": [
                ("user",
                 f"Based on the following search results on '{topic}', "
                 f"pick the most relevant URL and scrape it for deeper content.\n"
                 f"Search results:\n{state['search_results'][:800]}")
            ]
        })

        state["scrapped_content"] = reader_results["messages"][-1].content

        st.write("Content extraction completed.")
        status.update(label="Step 2: Reading completed", state="complete")

    # STEP 3: WRITER CHAIN
    with st.status("Step 3: Writing research report...", expanded=True) as status:

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SCRAPPED CONTENT:\n{state['scrapped_content']}"
        )

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })

        st.write("Research report generated.")
        status.update(label="Step 3: Report generated", state="complete")

    # STEP 4: CRITIC CHAIN
    with st.status("Step 4: Evaluating research report...", expanded=True) as status:

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        st.write("Report evaluation completed.")
        status.update(label="Step 4: Evaluation completed", state="complete")

    return state


# -----------------------------
# USER INPUT
# -----------------------------
st.subheader("Start your research")

topic = st.text_area(
    "What would you like to research?",
    placeholder="e.g. The impact of artificial intelligence on healthcare...",
    height=120
)

run_button = st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True
)

# -----------------------------
# EXECUTE PIPELINE
# -----------------------------
if run_button:

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:

        try:
            with st.spinner("Your research pipeline is running..."):

                results = run_research_pipeline(topic)

            st.success("Research pipeline completed successfully!")

            st.divider()
            st.header("Research Results")

            # SEARCH RESULTS
            with st.expander("🔍 Search Agent Results"):
                st.markdown(results["search_results"])

            # READER RESULTS
            with st.expander("📖 Reader Agent Results"):
                st.markdown(results["scrapped_content"])

            # WRITER RESULTS
            st.subheader("📝 Final Research Report")
            st.markdown(results["report"])

            # CRITIC RESULTS
            st.subheader("🧠 Critic Evaluation")
            st.markdown(results["feedback"])

            # DOWNLOAD REPORT
            st.download_button(
                label="⬇️ Download Research Report",
                data=str(results["report"]),
                file_name="research_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)
