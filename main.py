from dotenv import load_dotenv
load_dotenv()

from graph.workflow import app
from graph.state import FailureState

from utils.logger import logger

def run_failure_agent(event_description: str, metadata: dict = None):
    if metadata is None:
        metadata = {}

    # Initialize state
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

    # Run LangGraph pipeline
    final_state = app.invoke(state)

    logger.info("Workflow Complete")
    logger.info(f"Final State Snapshot:\n{final_state}")


    return final_state


# -------------------------
# Example Interactive Run
# -------------------------

if __name__ == "__main__":
    event_desc = input("Enter failure description: ")
    result = run_failure_agent(event_desc)

    print("\n--- Failure Post-Mortem Result ---\n")
    print(f"Detected Failure: {result['failure_detected']}")
    print(f"Category: {result['failure_category']}")
    print(f"Root Causes: {result['root_causes']}")
    print(f"Failure Type: {result['failure_type']}")
    print(f"Pattern Summary: {result['pattern_summary']}")
    print(f"Prevention Strategies: {result['prevention_strategies']}")
    print(f"Insight Summary: {result['insight_summary']}")
