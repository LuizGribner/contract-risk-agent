import pdfplumber
import io

def extract_text_from_file(content, content_type):
    if content_type == "application/pdf":
        return extract_from_pdf(content)
    return content.decode(errors="ignore")

def extract_from_pdf(content):
    data = io.BytesIO(content)
    text = ""
    with pdfplumber.open(data) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text