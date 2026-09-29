import ollama


def ask_model(prompt):
    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# -------------------------------
# Version 1 — Zero-shot
# -------------------------------

zero_shot_prompt = """
Classify each statement as one of:

FACT
OPINION
UNSUPPORTED

Statement:
Generative AI will completely replace software developers
within the next five years.

Return only the classification.
"""

print("=" * 60)
print("ZERO-SHOT")
print("=" * 60)

print(ask_model(zero_shot_prompt))


# -------------------------------
# Version 2 — Few-shot
# -------------------------------

few_shot_prompt = """
You classify research statements into:

FACT
OPINION
UNSUPPORTED

Use these examples:

Example 1:
Statement:
Software developers use generative AI tools to assist with
code generation.

Classification:
FACT

Example 2:
Statement:
Generative AI is the most exciting technology ever created.

Classification:
OPINION

Example 3:
Statement:
Generative AI will eliminate all software development jobs
within five years.

Classification:
UNSUPPORTED

Now classify the following statement:

Statement:
Generative AI will completely replace software developers
within the next five years.

Return only the classification.
"""

print("\n" + "=" * 60)
print("FEW-SHOT")
print("=" * 60)

print(ask_model(few_shot_prompt))