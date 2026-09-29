import ollama

from qdrant_client import QdrantClient


# --------------------------------------------------
# 1. Connect to persistent Qdrant
# --------------------------------------------------

client = QdrantClient(path="data/qdrant")

collection_name = "research_documents"


# --------------------------------------------------
# 2. Get user question
# --------------------------------------------------

query = input("\nEnter your research question: ")


# --------------------------------------------------
# 3. Convert question into embedding
# --------------------------------------------------

response = ollama.embed(
    model="nomic-embed-text",
    input=query
)

query_vector = response["embeddings"][0]


# --------------------------------------------------
# 4. Search Qdrant
# --------------------------------------------------

search_results = client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=3
).points


# --------------------------------------------------
# 5. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for i, result in enumerate(search_results, start=1):

    print(f"\nRESULT {i}")
    print("-" * 60)

    print("Similarity score:", result.score)
    print("Page:", result.payload["page"])

    print("\nText:")
    print(result.payload["text"])


# --------------------------------------------------
# 6. Close Qdrant
# --------------------------------------------------

client.close()