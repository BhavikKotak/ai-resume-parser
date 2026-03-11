import pdfplumber
import docx


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            if page.extract_text():
                text += page.extract_text()

    return text


def extract_text_from_docx(file_path):

    doc = docx.Document(file_path)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text