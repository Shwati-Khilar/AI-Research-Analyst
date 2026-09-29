import ollama
import json


def generate_report(topic, context, prompt_version):

    if prompt_version == "baseline":

        system_prompt = """
You are a research analyst.

Answer the user's research question using the provided context.

Generate a concise research answer.

Return only valid JSON:

{
    "answer": "",
    "sources": []
}
"""

    else:

        system_prompt = """
You are an evidence-grounded research analyst.

Your task is to answer the research question using ONLY
the provided research context.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts, statistics, or sources.
3. Every factual claim must be supported by the context.
4. Preserve the uncertainty and wording of the research.
5. Do not turn correlations into causal claims.
6. Do not exaggerate research findings.
7. If the context does not contain enough information,
   explicitly state that the information is insufficient.
8. Include the relevant source page for factual claims.

Return ONLY valid JSON:

{
    "answer": "",
    "sources": []
}
"""

    user_prompt = f"""
Research Question:
{topic}

Research Context:
{context}
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

    return json.loads(response["message"]["content"])


if __name__ == "__main__":

    topic = "What challenges of Generative AI adoption were identified?"

    context = """
    The study identifies inaccurate outputs (64.2%),
    regulatory compliance issues (58.2%), and ethical concerns
    (52.2%) as adoption challenges.
    """

    print("\n" + "=" * 60)
    print("BASELINE PROMPT")
    print("=" * 60)

    baseline = generate_report(
        topic,
        context,
        "baseline"
    )

    print(json.dumps(baseline, indent=2))

    print("\n" + "=" * 60)
    print("OPTIMIZED PROMPT")
    print("=" * 60)

    optimized = generate_report(
        topic,
        context,
        "optimized"
    )

    print(json.dumps(optimized, indent=2))