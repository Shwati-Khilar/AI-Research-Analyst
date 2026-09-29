import ollama
import json


def evaluate_faithfulness(question, context, answer):

    system_prompt = """
You are a research answer evaluator.

Your task is to evaluate whether the generated answer
is supported by the provided research context.

Do NOT use outside knowledge.

For each factual claim in the answer:

1. Determine whether the context supports it.
2. Identify unsupported claims.
3. Give an overall faithfulness score from 0 to 1.

Scoring:
1.0 = All factual claims are supported.
0.8 = Most claims are supported, with minor unsupported details.
0.5 = Some important claims are unsupported.
0.2 = Most claims are unsupported.
0.0 = The answer is completely unsupported.

Return ONLY valid JSON in this format:

{
    "score": 0.0,
    "supported_claims": [],
    "unsupported_claims": [],
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

    print("\nRAW MODEL OUTPUT:")
    print(raw_output)

    result = json.loads(raw_output)

    return result


question = """
What are the challenges of Generative AI adoption?
"""

context = """
The study identifies inaccurate outputs as a major challenge,
reported by 64.2% of respondents. Regulatory compliance issues
were reported by 58.2% of respondents, while ethical concerns
were reported by 52.2% of respondents.
"""

answer = """
The study identifies inaccurate outputs, regulatory compliance,
and ethical concerns as major challenges of Generative AI adoption.
Inaccurate outputs were reported by 64.2% of respondents.
Generative AI reduced software development time by 50%.
"""

result = evaluate_faithfulness(
    question,
    context,
    answer
)

print("\n" + "=" * 60)
print("FAITHFULNESS EVALUATION")
print("=" * 60)

print("\nScore:", result["score"])

print("\nSupported Claims:")
for claim in result["supported_claims"]:
    print("-", claim)

print("\nUnsupported Claims:")
for claim in result["unsupported_claims"]:
    print("-", claim)

print("\nReason:")
print(result["reason"])