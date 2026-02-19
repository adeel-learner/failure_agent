import json
from typing import List
from graph.state import FailureState

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from prompts.strategy_prompt import STRATEGY_SYSTEM_PROMPT

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

def build_strategy_prompt(root_causes: List[str], pattern_summary: str):

    user_prompt = f"""
Root Causes:
{root_causes}

Pattern Insight:
{pattern_summary}
"""

    return [
        SystemMessage(content=STRATEGY_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]


# -------------------------
# JSON Parser
# -------------------------

def parse_llm_json(response_text: str) -> dict:

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        cleaned = response_text[start:end]
        return json.loads(cleaned)


# -------------------------
# LangGraph Node
# -------------------------

def prevention_node(state: FailureState) -> FailureState:

    root_causes = state.get("root_causes", [])
    pattern_summary = state.get("pattern_summary", "")

    if not root_causes:
        state["prevention_strategies"] = ["Insufficient data to generate strategies."]
        state["insight_summary"] = "Not enough information to provide recommendations."
        return state

    messages = build_strategy_prompt(root_causes, pattern_summary)

    response = llm.invoke(messages)

    parsed = parse_llm_json(response.content)

    state["prevention_strategies"] = parsed.get("prevention_strategies", [])
    state["insight_summary"] = parsed.get("insight_summary")

    return state
