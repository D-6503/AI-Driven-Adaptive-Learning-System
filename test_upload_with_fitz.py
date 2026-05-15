import os
import fitz  # PyMuPDF
from app.services.pdf_processor import process_pdf
from app.services.embeddings import embed_texts

def create_dummy_pdf(path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "OptiLearn AI Physics Dummy Document.")
    page.insert_text((50, 70), "Chapter: Gravitation.")
    page.insert_text((50, 90), "Newton's law of universal gravitation states that every particle attracts every other particle.")
    doc.save(path)
    doc.close()

if __name__ == "__main__":
    pdf_path = "dummy_physics.pdf"
    create_dummy_pdf(pdf_path)
    print("Testing process_pdf...")
    try:
        res = process_pdf(pdf_path)
        print("process_pdf success:", res["chapter"], res["chunk_count"])
        chunks = res["chunks"]
        print("Testing embed_texts...")
        emb = embed_texts(chunks)
        print("embed_texts success. shape:", emb.shape)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERROR:", e)
