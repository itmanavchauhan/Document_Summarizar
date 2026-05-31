import os
from pypdf import PdfReader
from docx import Document
import pytesseract
from PIL import Image
import pdfplumber


# OPTIONAL:
# Add this ONLY if Windows OCR not working
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        # Normal PDF Text Extraction
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # OCR fallback for scanned PDFs
        if len(text.strip()) < 50:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    image = page.to_image(resolution=300)
                    pil_image = image.original

                    ocr_text = pytesseract.image_to_string(pil_image)

                    text += ocr_text + "\n"

    except Exception as e:
        text = f"Error reading PDF: {e}"

    return text


def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return f"Error reading TXT: {e}"


def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)

        text = "\n".join([para.text for para in doc.paragraphs])

        return text

    except Exception as e:
        return f"Error reading DOCX: {e}"


def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:
        return f"Error reading image: {e}"


def process_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)

    else:
        return "Unsupported file format"