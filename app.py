"""
DeepSearch — Research Report Generator
A Streamlit front-end for the multi-agent research pipeline in pipeline.py

Made by Gaurav Gupta
LinkedIn: https://www.linkedin.com/in/gaurav-gupta-79754a377
"""

import time
import traceback
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------------------------
# The pipeline itself is untouched. We only import the function it exposes.
# ---------------------------------------------------------------------------
from pipeline import run_research_pipline


# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="DeepSearch | Research Report Generator",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# DESIGN SYSTEM — fonts, colors, component styling
# ============================================================================
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <style>
        :root {
            --ink:        #0F1620;   /* background */
            --panel:      #171F2B;   /* card / panel surface */
            --panel-line: #263041;   /* hairline borders */
            --paper:      #E8ECF1;   /* primary text */
            --fog:        #8A93A3;   /* muted / secondary text */
            --signal:     #D4A24C;   /* amber accent — insight */
            --depth:      #4C8BD4;   /* blue accent — search/depth */
            --good:       #5FB88A;   /* success green */
        }

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: var(--ink);
            color: var(--paper);
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: var(--panel);
            border-right: 1px solid var(--panel-line);
        }
        section[data-testid="stSidebar"] * {
            color: var(--paper);
        }

        /* ---------- Headline block ---------- */
        .ds-hero {
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 28px 0 20px 0;
            border-bottom: 1px solid var(--panel-line);
            margin-bottom: 28px;
        }
        .ds-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--signal);
        }
        .ds-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 40px;
            line-height: 1.1;
            color: var(--paper);
            margin: 0;
        }
        .ds-title span {
            color: var(--signal);
        }
        .ds-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            color: var(--fog);
            max-width: 640px;
        }

        /* ---------- Pipeline stepper (signature element) ---------- */
        .ds-stepper {
            display: flex;
            align-items: stretch;
            gap: 0;
            margin: 6px 0 30px 0;
        }
        .ds-step {
            flex: 1;
            position: relative;
            padding: 14px 18px 14px 44px;
            background: var(--panel);
            border: 1px solid var(--panel-line);
            border-radius: 10px;
            margin-right: 10px;
        }
        .ds-step:last-child { margin-right: 0; }
        .ds-step-num {
            position: absolute;
            left: 14px;
            top: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: var(--ink);
            background: var(--fog);
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 500;
        }
        .ds-step.active .ds-step-num {
            background: var(--signal);
            color: var(--ink);
        }
        .ds-step.done .ds-step-num {
            background: var(--good);
            color: var(--ink);
        }
        .ds-step-label {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--paper);
        }
        .ds-step-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            color: var(--fog);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .ds-step.active {
            border-color: var(--signal);
        }
        .ds-step.done {
            border-color: var(--good);
        }

        /* ---------- Content panels ---------- */
        .ds-panel {
            background: var(--panel);
            border: 1px solid var(--panel-line);
            border-radius: 12px;
            padding: 22px 24px;
            margin-bottom: 18px;
        }
        .ds-panel-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--depth);
            margin-bottom: 10px;
        }
        .ds-panel-title.amber { color: var(--signal); }
        .ds-panel-title.green { color: var(--good); }

        /* ---------- Buttons ---------- */
        .stButton > button {
            background: var(--signal);
            color: var(--ink);
            border: none;
            border-radius: 8px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            padding: 10px 22px;
            transition: opacity 0.15s ease;
        }
        .stButton > button:hover {
            opacity: 0.88;
            color: var(--ink);
        }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: 1px solid var(--panel-line);
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 13.5px;
            color: var(--fog);
            padding: 10px 16px;
        }
        .stTabs [aria-selected="true"] {
            color: var(--signal) !important;
            border-bottom: 2px solid var(--signal) !important;
        }

        /* ---------- Text input ---------- */
        .stTextInput input {
            background: var(--ink);
            color: var(--paper);
            border: 1px solid var(--panel-line);
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
        }

        /* ---------- Footer ---------- */
        .ds-footer {
            margin-top: 48px;
            padding-top: 18px;
            border-top: 1px solid var(--panel-line);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .ds-footer-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11.5px;
            color: var(--fog);
        }
        .ds-footer-text a {
            color: var(--depth);
            text-decoration: none;
            font-weight: 500;
        }
        .ds-footer-text a:hover {
            color: var(--signal);
        }

        /* misc cleanup */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stStatusWidget"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;
                    font-size:22px;color:#E8ECF1;margin-bottom:2px;">
            ◆ DeepSearch
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:10.5px;
                    letter-spacing:0.08em;color:#D4A24C;text-transform:uppercase;
                    margin-bottom:22px;">
            Autonomous Research Pipeline
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='color:#8A93A3;font-size:13px;line-height:1.6;margin-bottom:18px;'>"
        "Four agents work in sequence to research any topic: a "
        "<b style='color:#E8ECF1;'>Search Agent</b> gathers current sources, "
        "a <b style='color:#E8ECF1;'>Reader Agent</b> scrapes the most relevant page, "
        "a <b style='color:#E8ECF1;'>Writer</b> drafts a structured report, and a "
        "<b style='color:#E8ECF1;'>Critic</b> reviews it for quality."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if "history" in st.session_state and st.session_state.history:
        st.markdown(
            "<div style='font-family:JetBrains Mono,monospace;font-size:11px;"
            "letter-spacing:0.08em;text-transform:uppercase;color:#8A93A3;"
            "margin-bottom:8px;'>Past Runs</div>",
            unsafe_allow_html=True,
        )
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(
                f"<div style='font-size:12.5px;color:#E8ECF1;padding:6px 0;"
                f"border-bottom:1px solid #263041;'>🔹 {item['topic']}"
                f"<br><span style='color:#8A93A3;font-size:10.5px;'>{item['time']}</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        "<div style='color:#8A93A3;font-size:11.5px;'>"
        "Built on LangGraph-style agents defined in "
        "<code style='color:#D4A24C;'>agents.py</code> and "
        "<code style='color:#D4A24C;'>tool.py</code>."
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================================
# HERO
# ============================================================================
st.markdown(
    """
    <div class="ds-hero">
        <div class="ds-eyebrow">Multi-Agent Research Assistant</div>
        <h1 class="ds-title">Deep<span>Search</span> Report Generator</h1>
        <div class="ds-subtitle">
            Enter any topic. Watch the pipeline search the web, read the most
            relevant source in depth, draft a structured report, and critique
            its own work — end to end, in one run.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# SESSION STATE
# ============================================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None


# ============================================================================
# INPUT ROW
# ============================================================================
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. The impact of quantum computing on cybersecurity",
        label_visibility="collapsed",
    )
with col2:
    run_clicked = st.button("Run Research", use_container_width=True)


# ============================================================================
# STEPPER (renders current progress through the 4 pipeline stages)
# ============================================================================
def render_stepper(active_index: int):
    """active_index: 0..3 currently running, 4 = all done, -1 = idle"""
    labels = [
        ("01", "Search Agent", "Gathering sources"),
        ("02", "Reader Agent", "Deep-scraping content"),
        ("03", "Writer Chain", "Structuring report"),
        ("04", "Critic Chain", "Reviewing quality"),
    ]
    html = "<div class='ds-stepper'>"
    for i, (num, label, sub) in enumerate(labels):
        state = ""
        if active_index > i or active_index == 4:
            state = "done"
        elif active_index == i:
            state = "active"
        html += f"""
        <div class="ds-step {state}">
            <div class="ds-step-num">{"✓" if state == "done" else num}</div>
            <div class="ds-step-label">{label}</div>
            <div class="ds-step-sub">{sub}</div>
        </div>
        """
    html += "</div>"
    return html


stepper_placeholder = st.empty()
if not run_clicked and st.session_state.result is None:
    stepper_placeholder.markdown(render_stepper(-1), unsafe_allow_html=True)


# ============================================================================
# RUN PIPELINE
# ============================================================================
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a topic to research before running the pipeline.")
    else:
        st.session_state.error = None
        try:
            # Stage 1 & 2 happen inside run_research_pipline itself; since the
            # underlying function is a single blocking call, we show a staged
            # visual progression around it without altering its logic.
            stepper_placeholder.markdown(render_stepper(0), unsafe_allow_html=True)
            with st.spinner("Search agent is gathering recent, reliable sources..."):
                time.sleep(0.4)
                stepper_placeholder.markdown(render_stepper(1), unsafe_allow_html=True)

                # This single call runs the full, unmodified pipeline
                # (search -> read -> write -> critique).
                result = run_research_pipline(topic=topic.strip())

            stepper_placeholder.markdown(render_stepper(4), unsafe_allow_html=True)
            st.session_state.result = result
            st.session_state.history.append(
                {"topic": topic.strip(), "time": datetime.now().strftime("%b %d, %H:%M")}
            )
            st.success("Research pipeline completed successfully.")

        except Exception as e:
            st.session_state.error = f"{e}\n\n{traceback.format_exc()}"
            stepper_placeholder.markdown(render_stepper(-1), unsafe_allow_html=True)


# ============================================================================
# ERROR DISPLAY
# ============================================================================
if st.session_state.error:
    st.markdown(
        f"""
        <div class="ds-panel" style="border-color:#B5544C;">
            <div class="ds-panel-title" style="color:#E38178;">Pipeline Error</div>
            <pre style="white-space:pre-wrap;color:#E8ECF1;font-size:12.5px;
                        font-family:'JetBrains Mono',monospace;">{st.session_state.error}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# RESULTS DISPLAY
# ============================================================================
if st.session_state.result:
    state = st.session_state.result

    tab_report, tab_critique, tab_search, tab_reader = st.tabs(
        ["📄 Final Report", "🧠 Critic Analysis", "🔎 Search Results", "📖 Reader Content"]
    )

    with tab_report:
        st.markdown(
            "<div class='ds-panel'><div class='ds-panel-title amber'>Structured Report</div>",
            unsafe_allow_html=True,
        )
        st.markdown(str(state.get("report", "")))
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇ Download Report (.md)",
            data=str(state.get("report", "")),
            file_name=f"deepsearch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    with tab_critique:
        st.markdown(
            "<div class='ds-panel'><div class='ds-panel-title green'>Critic Feedback</div>",
            unsafe_allow_html=True,
        )
        st.markdown(str(state.get("critics", "")))
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown(
            "<div class='ds-panel'><div class='ds-panel-title'>Raw Search Agent Output</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<pre style='white-space:pre-wrap;font-family:Inter,sans-serif;"
            f"font-size:13.5px;color:#E8ECF1;'>{state.get('search_results', '')}</pre>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_reader:
        st.markdown(
            "<div class='ds-panel'><div class='ds-panel-title'>Raw Reader Agent Output</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<pre style='white-space:pre-wrap;font-family:Inter,sans-serif;"
            f"font-size:13.5px;color:#E8ECF1;'>{state.get('reader_results', '')}</pre>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

elif not run_clicked and not st.session_state.error:
    st.markdown(
        """
        <div class="ds-panel" style="text-align:center;padding:48px 24px;">
            <div style="font-size:32px;margin-bottom:8px;">🧭</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;
                        color:#E8ECF1;margin-bottom:4px;">
                No report generated yet
            </div>
            <div style="color:#8A93A3;font-size:13px;">
                Enter a topic above and click <b style="color:#D4A24C;">Run Research</b>
                to start the pipeline.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# FOOTER
# ============================================================================
st.markdown(
    """
    <div class="ds-footer">
        <div class="ds-footer-text">DeepSearch Research Pipeline · Powered by LangGraph Agents</div>
        <div class="ds-footer-text">
            Made by <b style="color:#E8ECF1;">Gaurav Gupta</b> ·
            <a href="https://www.linkedin.com/in/gaurav-gupta-79754a377" target="_blank">LinkedIn Profile</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
