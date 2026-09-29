import pymupdf
import re


def clean_text(text):

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Fix words split across lines with a hyphen
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Replace single line breaks with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove repeated page header
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

for i, chunk in enumerate(all_chunks[:10]):

    print("\n" + "=" * 60)
    print(f"CHUNK {i + 1}")
    print("=" * 60)

    print("Page:", chunk["page"])

    print("\nText:")
    print(chunk["text"])