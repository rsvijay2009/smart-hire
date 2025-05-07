import PyPDF2
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_file(file_path):
    """
    Extract text from a PDF or text file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Extracted text.
    """
    try:
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted
                logger.info(f"Extracted text from PDF: {file_path}")
                return text
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                text = file.read()
                logger.info(f"Extracted text from TXT: {file_path}")
                return text
        else:
            logger.error(f"Unsupported file type: {file_path}")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return ""