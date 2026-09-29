import json

from evaluator import evaluate_faithfulness
from relevance_evaluator import evaluate_relevance
from completeness_evaluator import evaluate_completeness


def evaluate_report(topic, context, report):
    """
    Evaluate the generated research report using the
    Phase 5 LLM-based evaluators.
    """

    try:
        print("Evaluating report quality...")

        # Convert report to text
        report_text = json.dumps(report, indent=2)

        # -----------------------------------------
        # 1. FAITHFULNESS
        # -----------------------------------------

        print("Checking faithfulness...")

        faithfulness_result = evaluate_faithfulness(
            context,
            report_text
        )

        # -----------------------------------------
        # 2. RELEVANCE
        # -----------------------------------------

        print("Checking relevance...")

        relevance_result = evaluate_relevance(
            topic,
            report_text
        )

        # -----------------------------------------
        # 3. COMPLETENESS
        # -----------------------------------------

        print("Checking completeness...")

        completeness_result = evaluate_completeness(
            topic,
            context,
            report_text
        )

        print("\nRAW EVALUATION RESULTS:")
        print("Faithfulness:", faithfulness_result)
        print("Relevance:", relevance_result)
        print("Completeness:", completeness_result)

        # -----------------------------------------
        # Extract scores
        # -----------------------------------------

        faithfulness_score = float(
            faithfulness_result["score"]
        )

        relevance_score = float(
            relevance_result["score"]
        )

        completeness_score = float(
            completeness_result["score"]
        )

        # -----------------------------------------
        # Overall score
        # -----------------------------------------

        overall_score = (
            faithfulness_score
            + relevance_score
            + completeness_score
        ) / 3

        quality = {
            "faithfulness": {
                "score": faithfulness_score,
                "reason": faithfulness_result.get(
                    "reason",
                    "Evaluation completed."
                )
            },

            "relevance": {
                "score": relevance_score,
                "reason": relevance_result.get(
                    "reason",
                    "Evaluation completed."
                )
            },

            "completeness": {
                "score": completeness_score,
                "reason": completeness_result.get(
                    "reason",
                    "Evaluation completed."
                )
            },

            "overall_score": round(overall_score, 2)
        }

        print("\nQUALITY RESULT:")
        print(json.dumps(quality, indent=2))

        return quality

    except Exception as e:
        print(f"Quality evaluation failed: {e}")
        return None