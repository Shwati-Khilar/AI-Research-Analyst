import ollama


def create_research_prompt(topic, audience="general"):
    return f"""
You are an expert research analyst.

Research Topic:
{topic}

Target Audience:
{audience}

Task:
Analyze the research topic and produce a balanced overview.

Include:
1. Definition / Background
2. Key Findings
3. Benefits or Positive Impacts
4. Challenges or Risks
5. Conclusion

Requirements:
- Use clear language appropriate for the target audience.
- Avoid unnecessary jargon.
- Do not make unsupported claims.
- Clearly distinguish facts from observations.
- Keep the response under 500 words.
"""


topic = "Impact of Generative AI on software development"

prompt = create_research_prompt(
    topic,
    audience="third-year computer science student"
)

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response["message"]["content"])