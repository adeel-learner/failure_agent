from typing import TypedDict, List, Optional, Dict, Any


class FailureState(TypedDict):
    """
    Global shared state across all LangGraph nodes
    """

    # --------------------
    # Raw Input
    # --------------------
    event_description: str
    metadata: Dict[str, Any]

    # --------------------
    # Detection Output
    # --------------------
    failure_detected: Optional[bool]
    failure_category: Optional[str]
    severity: Optional[str]

    # --------------------
    # Post Mortem Output
    # --------------------
    root_causes: List[str]
    failure_type: Optional[str]

    # --------------------
    # Pattern Matching Output
    # --------------------
    similar_failures: List[Dict]
    pattern_summary: Optional[str]

    # --------------------
    # Prevention Output
    # --------------------
    prevention_strategies: List[str]

    # --------------------
    # Final Output
    # --------------------
    insight_summary: Optional[str]
