# ✅ extract_text_and_tables.py
# Extracts text, tables, and images from manuals for semantic embedding and part lookup

import os
import json
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
from bs4 import BeautifulSoup

from tqdm import tqdm
from pdfminer.high_level import extract_text as extract_pdfminer_text

# ---------------------------
# ⚙️ Configuration
# ---------------------------
PDF_DIR = "./Manuals"
OUTPUT_CHUNKS = "chunks.jsonl"
OUTPUT_TABLES = "tables.json"
IMAGE_DIR = "images"
IMAGE_ANNOTATIONS = "image_metadata.json"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------------------------
# 🧠 Utility: Clean lines
# ---------------------------
def clean_text(text):
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(lines)

# ---------------------------
# 📦 Table Parser (simple heuristic for part tables)
# ---------------------------
def extract_tables_from_text(page_text):
    tables = []
    lines = page_text.splitlines()
    part_row_pattern = re.compile(r"^(\d+)\s+([A-Z0-9-]+)\s+(\d+)\s+(.*)$")

    for line in lines:
        match = part_row_pattern.match(line)
        if match:
            tables.append({
                "ref_number": match.group(1),
                "part_number": match.group(2),
                "qty": match.group(3),
                "description": match.group(4)
            })
    return tables

# ---------------------------
# 📸 OCR helper for images
# ---------------------------
def ocr_image(image):
    text = pytesseract.image_to_string(image)
    return text.strip()

# ---------------------------
# 🚀 Main Extraction Loop
# ---------------------------
all_chunks = []
all_tables = []
image_annotations = []

pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]

for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
    pdf_path = os.path.join(PDF_DIR, pdf_file)
    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            continue

        cleaned = clean_text(text)

        # Store full text chunks for semantic search
        all_chunks.append({
            "source_file": pdf_file,
            "chunk_id": f"{pdf_file}::page_{page_num+1}",
            "text": cleaned,
            "page": page_num + 1
        })

        # Detect and extract table rows
        part_table = extract_tables_from_text(cleaned)
        if part_table:
            all_tables.append({
                "source_file": pdf_file,
                "page": page_num + 1,
                "rows": part_table
            })

        # Extract image blocks and OCR their content
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image = Image.open(io.BytesIO(image_bytes))
            image_path = os.path.join(IMAGE_DIR, f"{pdf_file}_p{page_num+1}_{img_index}.{image_ext}")
            image.save(image_path)

            # OCR the image for possible labels or diagram callouts
            description = ocr_image(image)
            image_annotations.append({
                "file": image_path,
                "source_file": pdf_file,
                "page": page_num + 1,
                "ocr_text": description.strip()
            })

# ---------------------------
# 💾 Save outputs
# ---------------------------
with open(OUTPUT_CHUNKS, "w", encoding="utf-8") as f:
    for chunk in all_chunks:
        json.dump(chunk, f)
        f.write("\n")

with open(OUTPUT_TABLES, "w", encoding="utf-8") as f:
    json.dump(all_tables, f, indent=2)

with open(IMAGE_ANNOTATIONS, "w", encoding="utf-8") as f:
    json.dump(image_annotations, f, indent=2)

print(f"\n✅ Done! Extracted {len(all_chunks)} chunks, {len(all_tables)} tables, {len(image_annotations)} images with OCR.")
