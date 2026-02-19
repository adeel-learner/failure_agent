from graph.workflow import app
from graph.state import FailureState


def run_single_test(test_case):
    state: FailureState = {
        "event_description": test_case["event"],
        "metadata": {},
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

    result = app.invoke(state)

    detection_correct = (
        result["failure_detected"] == test_case["expected_failure_detected"]
    )

    category_correct = (
        result["failure_category"] == test_case["expected_category"]
    )

    return {
        "event": test_case["event"],
        "detection_correct": detection_correct,
        "category_correct": category_correct,
        "predicted_category": result["failure_category"],
        "predicted_detection": result["failure_detected"]
    }


def evaluate_all(test_cases):
    results = []
    detection_score = 0
    category_score = 0

    for case in test_cases:
        res = run_single_test(case)
        results.append(res)

        if res["detection_correct"]:
            detection_score += 1

        if res["category_correct"]:
            category_score += 1

    total = len(test_cases)

    summary = {
        "detection_accuracy": detection_score / total,
        "category_accuracy": category_score / total
    }

    return results, summary
