from datetime import datetime
from graph.state import FailureState

from memory.database import save_failure_event
from memory.vector_store import store_failure_embedding

from utils.logger import logger

# -------------------------
# LangGraph Node
# -------------------------

def memory_node(state: FailureState) -> FailureState:
    """
    Persists failure data into memory systems
    """
    logger.info("Running Memory Update Node")

    if not state.get("failure_detected"):
        return state

    # -------------------------
    # Build Memory Record
    # -------------------------

    logger.info("Saving failure to SQLite")

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_description": state.get("event_description"),
        "metadata": state.get("metadata"),
        "failure_category": state.get("failure_category"),
        "severity": state.get("severity"),
        "root_causes": state.get("root_causes"),
        "failure_type": state.get("failure_type"),
        "pattern_summary": state.get("pattern_summary"),
        "prevention_strategies": state.get("prevention_strategies")
    }

    # -------------------------
    # Store in SQL / Structured DB
    # -------------------------

    event_id = save_failure_event(record)

    # -------------------------
    # Store Semantic Embedding
    # -------------------------

    logger.info("Storing embedding in FAISS")
    store_failure_embedding(event_id, record)

    return state
