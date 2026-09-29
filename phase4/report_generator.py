import ollama
import json

from qdrant_client import QdrantClient
from schemas import ResearchReport


# --------------------------------------------------
# 1. Connect to persistent Qdrant
# --------------------------------------------------

client = QdrantClient(path="data/qdrant")

collection_name = "research_documents"


# --------------------------------------------------
# 2. Get research topic
# --------------------------------------------------

topic = input("\nEnter your research topic: ")


# --------------------------------------------------
# 3. Embed research topic
# --------------------------------------------------

response = ollama.embed(
    model="nomic-embed-text",
    input=topic
)

query_vector = response["embeddings"][0]


# --------------------------------------------------
# 4. Retrieve relevant research chunks
# --------------------------------------------------

search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=5
).points


# --------------------------------------------------
# 5. Build research context
# --------------------------------------------------

context_parts = []

for i, result in enumerate(search_results, start=1):

    page = result.payload["page"]
    text = result.payload["text"]

    context_parts.append(
        f"[Source {i} - Page {page}]\n{text}"
    )

context = "\n\n".join(context_parts)


# --------------------------------------------------
# 6. Research report prompt
# --------------------------------------------------

system_prompt = """
You are an expert research analyst.

Your task is to generate a structured research report
using ONLY the research context provided.

IMPORTANT RULES:

1. Do not use information outside the provided context.
2. Do not invent facts, statistics, or sources.
3. Do not strengthen claims beyond what the research says.
4. Clearly distinguish research findings from claims
   discussed in the literature.
5. Preserve uncertainty when the research expresses
   uncertainty.
6. If the provided context does not contain enough
   information for a section, say:
   "Insufficient information in the retrieved research."
7. Include the source page number when making claims.
8. The research source is a preliminary study, so do not
   present its findings as universally established facts.

Return ONLY valid JSON.

Use exactly this structure:

{
    "executive_summary": "string",
    "background": "string",
    "key_findings": [
        "string",
        "string",
        "string"
    ],
    "benefits": [
        "string"
    ],
    "challenges": [
        "string"
    ],
    "evidence": [
        {
            "claim": "string",
            "source_page": "string"
        }
    ],
    "conclusion": "string",
    "limitations": [
        "string"
    ]
}
"""


user_prompt = f"""
Research Topic:

{topic}


Retrieved Research Context:

{context}
"""


# --------------------------------------------------
# 7. Generate report
# --------------------------------------------------

response = ollama.chat(
    model="qwen3:4b",
    format="json",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
)


# --------------------------------------------------
# 8. Parse JSON
# --------------------------------------------------

content = response["message"]["content"]

try:

    raw_report = json.loads(content)

    report = ResearchReport.model_validate(raw_report)

except json.JSONDecodeError:

    print("\nModel did not return valid JSON.")
    print("\nRaw response:")
    print(content)

    client.close()
    exit()

except Exception as e:

    print("\nModel returned JSON, but it does not match our schema.")
    print("\nValidation error:")
    print(e)

    print("\nRaw response:")
    print(content)

    client.close()
    exit()

# --------------------------------------------------
# 9. Display report
# --------------------------------------------------

print("\n" + "=" * 70)
print("AI RESEARCH REPORT")
print("=" * 70)

print("\nEXECUTIVE SUMMARY")
print(report.executive_summary)

print("\nBACKGROUND")
print(report.background)

print("\nKEY FINDINGS")

for finding in report.key_findings:
    print(f"- {finding}")

print("\nBENEFITS")

for benefit in report.benefits:
    print(f"- {benefit}")

print("\nCHALLENGES")

for challenge in report.challenges:
    print(f"- {challenge}")

print("\nEVIDENCE")

for evidence in report.evidence:
    print(
        f"- {evidence.claim} "
        f"(Page {evidence.source_page})"
    )

print("\nCONCLUSION")
print(report.conclusion)

print("\nLIMITATIONS")

for limitation in report.limitations:
    print(f"- {limitation}")


# --------------------------------------------------
# 10. Close Qdrant
# --------------------------------------------------

client.close()