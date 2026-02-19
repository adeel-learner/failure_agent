from typing import List, Dict
from graph.state import FailureState

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from memory.vector_store import search_similar_failures

from prompts.pattern_prompt import PATTERN_SYSTEM_PROMPT

from utils.logger import logger

# -------------------------
# LLM Setup
# -------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # fast & cheap
    temperature=0
)

# -------------------------
# Prompt Builder
# -------------------------

def build_pattern_prompt(root_causes: List[str], similar_failures: List[Dict]):

    logger.info("Running Pattern Match Node")

    user_prompt = f"""
Current Root Causes:
{root_causes}

Similar Past Failures:
{similar_failures}
"""

    return [
        SystemMessage(content=PATTERN_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]


# -------------------------
# LangGraph Node
# -------------------------

def pattern_match_node(state: FailureState) -> FailureState:

    root_causes = state.get("root_causes", [])

    if not root_causes:
        state["pattern_summary"] = "No root causes identified."
        return state

    # -------------------------
    # Vector Similarity Search
    # -------------------------

    similar_failures = search_similar_failures(root_causes)

    state["similar_failures"] = similar_failures

    # If no history exists
    if not similar_failures:
        state["pattern_summary"] = "No similar historical failures found."
        return state

    # -------------------------
    # Pattern Insight Generation
    # -------------------------

    messages = build_pattern_prompt(root_causes, similar_failures)

    response = llm.invoke(messages)

    state["pattern_summary"] = response.content

    logger.info(f"Similar Failures Found: {len(similar_failures)}")
    logger.info(f"Pattern Summary: {state['pattern_summary']}")

    return state
