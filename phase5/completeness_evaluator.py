import ollama
import json


def evaluate_completeness(question, context, answer):

    system_prompt = """
You are an evaluator of research answers.

Your task is to determine whether the generated answer
covers the important information contained in the provided
research context that is relevant to the question.

Evaluate coverage, NOT whether the answer is factually correct.

Identify:
1. Important points from the context that are relevant to the question.
2. Which of those points are covered by the answer.
3. Which important points are missing.

Scoring:

1.0 = Covers all important relevant points.
0.8 = Covers most important points with minor omissions.
0.5 = Covers some important points but misses significant information.
0.2 = Covers very little of the important information.
0.0 = Does not cover the relevant information.

Return ONLY valid JSON in this format:

{
    "score": 0.0,
    "covered_points": [],
    "missing_points": [],
    "reason": ""
}
"""

    user_prompt = f"""
Research Question:
{question}

Research Context:
{context}

Generated Answer:
{answer}
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        format="json"
    )

    raw_output = response["message"]["content"]

    result = json.loads(raw_output)

    return result


# Test case

question = """
What challenges of Generative AI adoption were identified?
"""

context = """
The study identifies inaccurate outputs (64.2%),
regulatory compliance issues (58.2%), and ethical concerns
(52.2%) as adoption challenges.
"""

answer = """
The study identifies inaccurate outputs as a challenge.
"""


result = evaluate_completeness(
    question,
    context,
    answer
)

print("\n" + "=" * 60)
print("COMPLETENESS EVALUATION")
print("=" * 60)

print("\nScore:", result["score"])

print("\nCovered Points:")
for point in result["covered_points"]:
    print("-", point)

print("\nMissing Points:")
for point in result["missing_points"]:
    print("-", point)

print("\nReason:")
print(result["reason"])