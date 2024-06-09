import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import docx2pdf


pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract\tesseract.exe'

def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

def ocr_image(image):
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path):
    images = pdf_to_images(pdf_path)
    text = ""
    for image in images:
        text += ocr_image(image)
    return text

def convert_docx_to_pdf(docx_path, pdf_path):
  """Converts a DOCX file to PDF using docx2pdf."""
  try:
    docx2pdf.convert(docx_path, pdf_path)
    print(f"Successfully converted DOCX to PDF: {docx_path} -> {pdf_path}")
  except Exception as e:
    print(f"An error occurred during conversion: {e}")

def convert_images_to_pdf(images, pdf_path):
    if isinstance(images, Image.Image):
        images = [images] 
    images[0].save(pdf_path, save_all=True, append_images=images[1:], format='PDF')