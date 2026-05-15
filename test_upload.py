import os
from reportlab.pdfgen import canvas
from app.services.pdf_processor import process_pdf
from app.services.embeddings import embed_texts

def create_dummy_pdf(path):
    c = canvas.Canvas(path)
    c.drawString(100, 750, "This is a test PDF for OptiLearn AI.")
    c.drawString(100, 730, "NCERT Physics Gravitation Newton Law.")
    c.save()

if __name__ == "__main__":
    pdf_path = "test_dummy.pdf"
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
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
