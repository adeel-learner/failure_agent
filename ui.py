from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import json
from graph.workflow import app
from graph.state import FailureState
from memory.database import get_connection


# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Failure Post-Mortem Agent",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Failure Post-Mortem Agent")
st.markdown("Analyze failures, detect patterns, and generate prevention strategies.")

# -------------------------
# User Input Section
# -------------------------

st.subheader("Enter Failure Event")

event_description = st.text_area(
    "Failure Description",
    height=150,
    placeholder="Describe what went wrong..."
)

metadata_input = st.text_area(
    "Optional Metadata (JSON format)",
    height=100,
    placeholder='{"project": "AI Agent", "sprint": "Sprint 5"}'
)

run_button = st.button("Run Analysis")

# -------------------------
# Run Agent
# -------------------------

if run_button and event_description.strip():

    # Parse metadata safely
    try:
        metadata = json.loads(metadata_input) if metadata_input else {}
    except:
        st.error("Invalid JSON in metadata.")
        metadata = {}

    state: FailureState = {
        "event_description": event_description,
        "metadata": metadata,
        "failure_detected": None,
        "failure_category": None,
        "severity": None,
        "root_causes": [],
        "failure_type": None,
        "similar_failures": [],
        "pattern_summary": None,
        "prevention_strategies": [],
        "insight_summary": None
    }

    with st.spinner("Analyzing failure..."):
        result = app.invoke(state)

    # -------------------------
    # Display Results
    # -------------------------

    st.divider()
    st.subheader("Analysis Result")

    if not result["failure_detected"]:
        st.success("No failure detected.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Classification")
            st.write("**Category:**", result["failure_category"])
            st.write("**Severity:**", result["severity"])
            st.write("**Failure Type:**", result["failure_type"])

            st.markdown("### Root Causes")
            for cause in result["root_causes"]:
                st.write("•", cause)

        with col2:
            st.markdown("### Pattern Summary")
            st.write(result["pattern_summary"])

            st.markdown("### Prevention Strategies")
            for strategy in result["prevention_strategies"]:
                st.write("•", strategy)

        st.markdown("### Insight Summary")
        st.info(result["insight_summary"])

# -------------------------
# History Section
# -------------------------

st.divider()
st.subheader("Failure History")

if st.button("Load Past Failures"):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM failures ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        with st.expander(f"Event #{row['id']} — {row['event_description'][:50]}"):
            st.write("Category:", row["failure_category"])
            st.write("Severity:", row["severity"])
            st.write("Failure Type:", row["failure_type"])
            st.write("Pattern Summary:", row["pattern_summary"])
