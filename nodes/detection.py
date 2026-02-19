import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import FailureState
from prompts.detection_prompt import DETECTION_SYSTEM_PROMPT

from utils.logger import logger

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # fast & cheap
    temperature=0
)


def detect_failure_node(state: FailureState) -> FailureState:
    """
    LLM-based failure detection and classification.
    """
    logger.info("Running Detection Node")

    event_description = state["event_description"]

    response = llm.invoke([
        SystemMessage(content=DETECTION_SYSTEM_PROMPT),
        HumanMessage(content=f"Event:\n{event_description}")
    ])

    logger.info(f"Detection Raw LLM Output: {response.content}")

    try:
        result = json.loads(response.content)
    except Exception:
        # Fallback if LLM returns non-JSON
        result = {
            "failure_detected": False,
            "failure_category": None,
            "severity": None
        }

    state["failure_detected"] = result.get("failure_detected", False)
    state["failure_category"] = result.get("failure_category")
    state["severity"] = result.get("severity")

    logger.info(
        f"Detection Result → "
        f"Detected: {state['failure_detected']} | "
        f"Category: {state['failure_category']} | "
        f"Severity: {state['severity']}"
    )

    return state
