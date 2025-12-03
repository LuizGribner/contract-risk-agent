import io
import pdfplumber

def extract_text_from_file(content, content_type):
    if content_type == "application/pdf":
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text
        except Exception as e:
            return f"PDF extraction error: {str(e)}"

    if content_type == "text/plain":
        return content.decode("utf-8", errors="ignore")

    return ""