import ollama
import json


def evaluate_relevance(question, answer):

    system_prompt = """
You are an evaluator of research answers.

Your task is to determine whether the generated answer
directly addresses the research question.

Do NOT judge whether the answer is factually correct.
Only judge relevance to the question.

Scoring:

1.0 = Directly and completely answers the question.
0.8 = Mostly answers the question but misses a minor point.
0.5 = Partially relevant but misses important information.
0.2 = Mostly irrelevant to the question.
0.0 = Completely irrelevant.

Return ONLY valid JSON in this format:

{
    "score": 0.0,
    "reason": ""
}
"""

    user_prompt = f"""
Research Question:
{question}

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

answer = """
The study reports that 97% of IT workers use Generative AI tools,
primarily ChatGPT.
"""

result = evaluate_relevance(question, answer)

print("\n" + "=" * 60)
print("RELEVANCE EVALUATION")
print("=" * 60)

print("\nScore:", result["score"])
print("\nReason:")
print(result["reason"])