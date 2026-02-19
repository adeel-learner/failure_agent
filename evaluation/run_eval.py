from dotenv import load_dotenv
load_dotenv()

from .test_cases import TEST_CASES
from .evaluator import evaluate_all


if __name__ == "__main__":
    results, summary = evaluate_all(TEST_CASES)

    print("\n--- Evaluation Results ---\n")

    for r in results:
        print(f"Event: {r['event']}")
        print(f"Detection Correct: {r['detection_correct']}")
        print(f"Category Correct: {r['category_correct']}")
        print(f"Predicted Detection: {r['predicted_detection']}")
        print(f"Predicted Category: {r['predicted_category']}")
        print("-" * 50)

    print("\n--- Summary ---")
    print(f"Detection Accuracy: {summary['detection_accuracy']}")
    print(f"Category Accuracy: {summary['category_accuracy']}")
