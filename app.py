from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Deep Research Maker",
    page_icon="🔎",
    layout="wide"
)

# -------------------------------------------------
# Sidebar - Author Info
# -------------------------------------------------
with st.sidebar:
    st.title("🔎 Deep Research Maker")
    st.markdown("An AI agent pipeline that searches, reads, writes, and critiques research reports on any topic.")
    st.divider()
    st.subheader("👤 Author")
    st.markdown("**Gaurav Gupta**")
    st.markdown("[🔗 LinkedIn Profile](https://www.linkedin.com/in/gaurav-gupta-79754a377)")
    st.divider()
    st.caption("Pipeline: Search Agent → Reader Agent → Writer Chain → Critic Chain")


# -------------------------------------------------
# Core pipeline function (SAME LOGIC, unchanged)
# -------------------------------------------------
def run_research_pipeline(topic: str) -> dict:
    state = {}

    # ---------------- Step 1: Search Agent ----------------
    with st.status("Step 1: Search Agent is working...", expanded=True) as status:
        search_agent = build_search_agent()
        search_results = search_agent.invoke({
            'messages': [("user", f"Find the recent and Reliable information about:{topic}")]
        })
        state['search_results'] = search_results['messages'][-1].content
        status.update(label="Step 1: Search Agent — done ✅", state="complete")

    with st.expander("🔍 Search Results (raw)", expanded=False):
        st.write(state['search_results'])

    # ---------------- Step 2: Reader Agent ----------------
    with st.status("Step 2: Reader Agent is working...", expanded=True) as status:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['reader_results'] = reader_result['messages'][-1].content
        status.update(label="Step 2: Reader Agent — done ✅", state="complete")

    with st.expander("📖 Reader Results (raw)", expanded=False):
        st.write(state['reader_results'])

    # ---------------- Step 3: Structuring the Report ----------------
    with st.status("Step 3: Structuring the Report...", expanded=True) as status:
        combined_research = (
            "Search Results\n" + state['search_results'] +
            "\n\nReader Results\n".join(state["reader_results"])
        )
        report = writer_chain.invoke({
            'topic': topic,
            'research': combined_research
        })
        status.update(label="Step 3: Report structured — done ✅", state="complete")

    # ---------------- Step 4: Critic Analysis ----------------
    with st.status("Step 4: Analysing Report...", expanded=True) as status:
        critics = critic_chain.invoke({
            'report': report
        })
        status.update(label="Step 4: Analysis complete ✅", state="complete")

    state['report'] = report
    state['critics'] = critics
    return state


# -------------------------------------------------
# Main UI
# -------------------------------------------------
st.title("🔎 Deep Research Maker")
st.markdown("Enter a topic below and let the multi-agent pipeline **search → read → write → critique** a research report for you.")

topic = st.text_input("Enter topic to be Researched:", placeholder="e.g. Impact of AI on the job market in 2026")

col1, col2 = st.columns([1, 5])
with col1:
    run_clicked = st.button("🚀 Run Research", type="primary", use_container_width=True)

if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        result_state = run_research_pipeline(topic=topic)

        st.divider()
        st.subheader("📄 Final Report")
        st.markdown(result_state['report'])

        st.divider()
        st.subheader("🧐 Analysis of Report")
        st.markdown(result_state['critics'])

        st.divider()
        st.success("Research pipeline completed successfully!")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center'>Made by <b>Gaurav Gupta</b> | "
    "<a href='https://www.linkedin.com/in/gaurav-gupta-79754a377' target='_blank'>LinkedIn</a></div>",
    unsafe_allow_html=True
)
