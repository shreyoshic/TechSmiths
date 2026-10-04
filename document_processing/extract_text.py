import pymupdf
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


for file in os.listdir(OUTPUT_DIR):

    if file.endswith(".json"):

        os.remove(os.path.join(OUTPUT_DIR, file))



def extract_text(pdf_path):

    doc = pymupdf.open(pdf_path)

    document_name = os.path.basename(pdf_path)

    pages = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text().strip()
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        pages.append({
            "document": document_name,
            "page": page_number,
            "text": text
        })

    doc.close()

    return pages

def extract_all_documents():

    pdf_files = [
        file for file in os.listdir(DOCUMENTS_DIR)
        if file.lower().endswith(".pdf")
    ]

    all_documents = []

    for pdf_file in pdf_files:

        try:
            result = extract_text(os.path.join(DOCUMENTS_DIR, pdf_file))

            all_documents.extend(result)

            output_name = os.path.splitext(pdf_file)[0] + ".json"

            with open(os.path.join(OUTPUT_DIR, output_name), "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

            print("Extracted:", pdf_file)

        except Exception as e:
            print("Failed to extract:", pdf_file)
            print("Error:", e)
            continue

    with open(os.path.join(OUTPUT_DIR, "all_documents.json"), "w", encoding="utf-8") as file:
        json.dump(all_documents, file, indent=4, ensure_ascii=False)

    print("Combined output saved to output/all_documents.json")

    return all_documents


if __name__ == "__main__":
    extract_all_documents()