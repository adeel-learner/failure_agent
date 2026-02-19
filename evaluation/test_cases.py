TEST_CASES = [
    {
        "event": "Missed sprint deadline due to unclear requirements.",
        "expected_failure_detected": True,
        "expected_category": "planning_error"
    },
    {
        "event": "Team members misunderstood instructions and delivered wrong feature.",
        "expected_failure_detected": True,
        "expected_category": "communication_failure"
    },
    {
        "event": "Finished all assigned tasks successfully ahead of schedule.",
        "expected_failure_detected": False,
        "expected_category": None
    },
    {
        "event": "Production server crashed because monitoring alerts were ignored.",
        "expected_failure_detected": True,
        "expected_category": "systemic_issue"
    }
]
