import ollama

from qdrant_client import QdrantClient


# --------------------------------------------------
# 1. Connect to persistent Qdrant
# --------------------------------------------------

client = QdrantClient(path="data/qdrant")

collection_name = "research_documents"


# --------------------------------------------------
# 2. Get user's question
# --------------------------------------------------

query = input("\nEnter your research question: ")


# --------------------------------------------------
# 3. Convert question into an embedding
# --------------------------------------------------

response = ollama.embed(
    model="nomic-embed-text",
    input=query
)

query_vector = response["embeddings"][0]


# --------------------------------------------------
# 4. Retrieve relevant chunks
# --------------------------------------------------

search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
).points


# --------------------------------------------------
# 5. Build context from retrieved chunks
# --------------------------------------------------

context_parts = []

for i, result in enumerate(search_results, start=1):

    text = result.payload["text"]
    page = result.payload["page"]

    context_parts.append(
        f"[Source {i} - Page {page}]\n{text}"
    )


context = "\n\n".join(context_parts)


# --------------------------------------------------
# 6. Create RAG prompt
# --------------------------------------------------

system_prompt = """
You are an expert research assistant.

Answer the user's question using ONLY the research
context provided below.

Rules:
- Use only information supported by the context.
- Do not invent facts.
- If the context does not contain enough information,
  clearly say that the available research context
  is insufficient.
- Give a clear and concise answer.
- Mention the relevant source page numbers when
  making claims from the research.
"""


user_prompt = f"""
Research Context:

{context}


User Question:

{query}
"""


# --------------------------------------------------
# 7. Generate answer using Qwen
# --------------------------------------------------

answer = ollama.chat(
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
    ]
)


# --------------------------------------------------
# 8. Display answer
# --------------------------------------------------

print("\n" + "=" * 60)
print("RAG ANSWER")
print("=" * 60)

print(answer["message"]["content"])


# --------------------------------------------------
# 9. Close Qdrant
# --------------------------------------------------

client.close()
