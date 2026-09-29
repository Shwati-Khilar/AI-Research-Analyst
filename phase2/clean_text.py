import pymupdf
import re


def extract_pdf_text(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page in document:
        text = page.get_text()
        pages.append(text)

    document.close()

    return "\n".join(pages)


def clean_text(text):

    # 1. Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 2. Fix hyphenated words split across lines
    # Example:
    # organi-
    # zation
    # becomes:
    # organization
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # 3. Replace remaining single line breaks with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # 4. Normalize multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # 5. Normalize multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # 6. Remove repeated page header
    text = re.sub(
        r"BONIN ET AL\. EXPLORING THE IMPACT OF GENERATIVE ARTIFICIAL INTELLIGENCE\.\.\.",
        "",
        text
    )

    # 7. Remove PREPRINT when it appears as a standalone line
    text = re.sub(r"\n?PREPRINT\s*\n?", "\n", text)

    # 8. Remove unnecessary spaces around punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # 9. Clean leading/trailing whitespace
    text = text.strip()

    return text


pdf_path = "data/documents/research_paper.pdf"

raw_text = extract_pdf_text(pdf_path)

cleaned_text = clean_text(raw_text)


print("=" * 60)
print("CLEANED TEXT")
print("=" * 60)

print(cleaned_text[:5000])