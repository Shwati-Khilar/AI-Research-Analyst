import json
import ollama

from schemas import ResearchAnalysis


response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "system",
            "content": """
You are an expert research analyst.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
    "definition": "string",
    "how_it_works": "string",
    "examples": ["string", "string", "string"],
    "limitations": ["string", "string"],
    "key_takeaway": "string"
}

Do not include Markdown.
Do not include explanations outside the JSON.
"""
        },
        {
            "role": "user",
            "content": "Explain Generative AI."
        }
    ]
)

text = response["message"]["content"]

data = json.loads(text)

research = ResearchAnalysis.model_validate(data)

print("Definition:")
print(research.definition)

print("\nHow It Works:")
print(research.how_it_works)

print("\nExamples:")
for example in research.examples:
    print("-", example)

print("\nLimitations:")
for limitation in research.limitations:
    print("-", limitation)

print("\nKey Takeaway:")
print(research.key_takeaway)