import pymupdf
import re
import ollama

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


# --------------------------------------------------
# 1. Clean text
# --------------------------------------------------

def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Join words broken by PDF line wrapping
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Convert single line breaks into spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize paragraph breaks
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove repeated header
    text = re.sub(
        r"BONIN ET AL\. EXPLORING THE IMPACT OF GENERATIVE ARTIFICIAL INTELLIGENCE\.\.\.",
        "",
        text
    )

    # Remove PREPRINT
    text = re.sub(r"\n?PREPRINT\s*\n?", "\n", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    return text.strip()


# --------------------------------------------------
# 2. Create chunks
# --------------------------------------------------

def create_chunks(page_text, page_number, chunk_size=1500):

    paragraphs = page_text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= chunk_size:

            current_chunk += paragraph + "\n\n"

        else:

            if current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "page": page_number
                })

            current_chunk = paragraph + "\n\n"

    if current_chunk:
        chunks.append({
            "text": current_chunk.strip(),
            "page": page_number
        })

    return chunks


# --------------------------------------------------
# 3. Read PDF and create all chunks
# --------------------------------------------------

pdf_path = "data/documents/research_paper.pdf"

document = pymupdf.open(pdf_path)

all_chunks = []

for page_number, page in enumerate(document, start=1):

    raw_text = page.get_text()

    cleaned_text = clean_text(raw_text)

    page_chunks = create_chunks(
        cleaned_text,
        page_number
    )

    all_chunks.extend(page_chunks)

document.close()

print("Total chunks:", len(all_chunks))


# --------------------------------------------------
# 4. Create embeddings
# --------------------------------------------------

embeddings = []

for i, chunk in enumerate(all_chunks):

    response = ollama.embed(
        model="nomic-embed-text",
        input=chunk["text"]
    )

    embedding = response["embeddings"][0]

    embeddings.append(embedding)

    print(f"Embedded chunk {i + 1}/{len(all_chunks)}")


# --------------------------------------------------
# 5. Create Qdrant client
# --------------------------------------------------

client = QdrantClient(path="data/qdrant")


# --------------------------------------------------
# 6. Create collection
# --------------------------------------------------

collection_name = "research_documents"

if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )
    print("Qdrant collection created!")
else:
    print("Qdrant collection already exists.")




# --------------------------------------------------
# 7. Insert chunks into Qdrant
# --------------------------------------------------

points = []

for i, chunk in enumerate(all_chunks):

    point = PointStruct(
        id=i,
        vector=embeddings[i],
        payload={
            "text": chunk["text"],
            "page": chunk["page"]
        }
    )

    points.append(point)


client.upsert(
    collection_name=collection_name,
    points=points
)

print("Documents indexed successfully!")
print(
    "Number of stored points:",
    client.count(collection_name=collection_name).count
)

client.close()