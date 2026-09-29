import ollama

prompt = """
Explain the impact of Generative AI on software development
in approximately 100 words.
"""

for temperature in [0.0, 0.5, 1.0]:

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": temperature
        }
    )

    print("\n" + "=" * 60)
    print(f"TEMPERATURE: {temperature}")
    print("=" * 60)
    print(response["message"]["content"])