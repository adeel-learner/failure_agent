import json
from typing import List
from graph.state import FailureState

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from prompts.postmortem_prompt import POSTMORTEM_SYSTEM_PROMPT
from utils.logger import logger


# -------------------------
# LLM Initialization
# -------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # fast & cheap
    temperature=0
)


# -------------------------
# Prompt Builder
# -------------------------

def build_postmortem_prompt(description: str, category: str) -> List:
    """
    Creates structured prompt for root cause analysis
    """
    logger.info("Running Postmortem Node")

    user_prompt = f"""
Failure Description:
{description}

Failure Category:
{category}
"""

    return [
        SystemMessage(content=POSTMORTEM_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]


# -------------------------
# JSON Safe Parser
# -------------------------

def parse_llm_json(response_text: str) -> dict:
    """
    Safely parse LLM JSON output
    """

    if not response_text:
        return {}

    # First, try a normal parse
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Remove common code-fence wrappers
    cleaned = response_text.strip()
    if cleaned.startswith("```") and cleaned.endswith("```"):
        parts = cleaned.splitlines()
        if len(parts) >= 3:
            cleaned = "\n".join(parts[1:-1]).strip()

    # Helper to extract balanced JSON blocks (objects or arrays)
    def _extract_blocks(text: str, open_ch: str, close_ch: str):
        blocks = []
        start = None
        depth = 0
        for i, ch in enumerate(text):
            if ch == open_ch:
                if depth == 0:
                    start = i
                depth += 1
            elif ch == close_ch and depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    blocks.append(text[start:i + 1])
                    start = None
        return blocks

    # Try to extract JSON objects first
    obj_blocks = _extract_blocks(cleaned, "{", "}")
    for blk in obj_blocks:
        try:
            return json.loads(blk)
        except json.JSONDecodeError:
            continue

    # Then try JSON arrays
    arr_blocks = _extract_blocks(cleaned, "[", "]")
    for blk in arr_blocks:
        try:
            parsed = json.loads(blk)
            # wrap array into object if caller expects dict
            if isinstance(parsed, dict):
                return parsed
            return {"result": parsed}
        except json.JSONDecodeError:
            continue

    # As a last resort, return empty dict so caller can handle defaults
    return {}


# -------------------------
# LangGraph Node
# -------------------------

def post_mortem_node(state: FailureState) -> FailureState:

    if not state.get("failure_detected"):
        return state

    description = state["event_description"]
    category = state.get("failure_category", "general_failure")

    messages = build_postmortem_prompt(description, category)

    # LLM Call
    response = llm.invoke(messages)

    # Parse structured output
    parsed = parse_llm_json(response.content)

    # Update state
    state["root_causes"] = parsed.get("root_causes", [])
    state["failure_type"] = parsed.get("failure_type")

    logger.info(f"Root Causes: {state['root_causes']}")
    logger.info(f"Failure Type: {state['failure_type']}")


    return state
