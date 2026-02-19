from langgraph.graph import StateGraph, END
from graph.state import FailureState

from nodes.detection import detect_failure_node
from nodes.postmortem import post_mortem_node
from nodes.pattern import pattern_match_node
from nodes.strategy import prevention_node
from nodes.memory import memory_node


# -------------------------
# Conditional Router
# -------------------------

def route_after_detection(state: FailureState):
    """
    If no failure detected, end workflow early.
    """
    if not state.get("failure_detected"):
        return END
    return "post_mortem"


# -------------------------
# Define Workflow
# -------------------------

workflow = StateGraph(FailureState)

# Add nodes
workflow.add_node("detect_failure", detect_failure_node)
workflow.add_node("post_mortem", post_mortem_node)
workflow.add_node("pattern_match", pattern_match_node)
workflow.add_node("strategy", prevention_node)
workflow.add_node("memory_update", memory_node)

# Entry point
workflow.set_entry_point("detect_failure")

# Conditional routing
workflow.add_conditional_edges(
    "detect_failure",
    route_after_detection,
    {
        "post_mortem": "post_mortem",
        END: END
    }
)

# Sequential edges after detection
workflow.add_edge("post_mortem", "pattern_match")
workflow.add_edge("pattern_match", "strategy")
workflow.add_edge("strategy", "memory_update")
workflow.add_edge("memory_update", END)

# Compile app
app = workflow.compile()
