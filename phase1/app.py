import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "system",
            "content": """
You are an expert research analyst who explains technical
concepts accurately and clearly.

Your task is to explain Generative AI.

Audience:
A third-year computer science student who is new to
advanced AI concepts.

Requirements:
- Start with a simple definition.
- Explain how Generative AI works at a high level.
- Give 3 real-world examples.
- Explain how it differs from traditional AI.
- Mention two limitations.
- Avoid unnecessary mathematical details.
- Do not make unsupported claims.

Output format:

1. Definition
2. How It Works
3. Real-World Examples
4. Generative AI vs Traditional AI
5. Limitations
6. Key Takeaway

Keep the explanation under 500 words.
"""
        },
        {
            "role": "user",
            "content": "Explain Generative AI."
        }
    ]
)

print(response["message"]["content"])