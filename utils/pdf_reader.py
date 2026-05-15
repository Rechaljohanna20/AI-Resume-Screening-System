import pdfplumber
import io

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Accepts a Streamlit UploadedFile object and returns
    the full extracted text as a single string.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()