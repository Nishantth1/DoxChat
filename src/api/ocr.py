# src/api/ocr.py

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

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
