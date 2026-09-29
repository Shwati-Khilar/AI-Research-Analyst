import pymupdf

pdf_path = "data/documents/research_paper.pdf"

document = pymupdf.open(pdf_path)

print("Number of pages:", len(document))

for page_number, page in enumerate(document):
    text = page.get_text()

    print("\n" + "=" * 60)
    print(f"PAGE {page_number + 1}")
    print("=" * 60)

    print(text[:2000])