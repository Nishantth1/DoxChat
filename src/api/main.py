from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from .ocr import extract_text_from_pdf, convert_docx_to_pdf, convert_images_to_pdf
from .preprocessing import preprocess_text
from .llm_integration import extract_information, summarize_document, classify_document, translate_text, get_answer
from PIL import Image
import os


app = FastAPI()

@app.post("/process-document/")
async def process_document(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ['application/pdf', 'image/jpeg', 'image/png', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        raise HTTPException(status_code=400, detail="Invalid document type. Only PDFs, images (JPEG, PNG), and DOCX are supported.")
    
    try:
        file_extension = file.filename.split('.')[-1].lower()
        file_location = f"./data/{file.filename}"
        
        # Save uploaded file
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        if file_extension == 'docx':
            pdf_path = f"./data/{file.filename.split('.')[0]}.pdf"
            convert_docx_to_pdf(file_location, pdf_path)
            file_location = pdf_path

        elif file_extension in ['jpeg', 'png']:
            images = Image.open(file_location)
            pdf_path = f"./data/{file.filename.split('.')[0]}.pdf"
            convert_images_to_pdf(images, pdf_path)
            file_location = pdf_path
        
        # Process the file
        extracted_text = extract_text_from_pdf(file_location)
        processed_text = preprocess_text(extracted_text)
        os.remove(file_location)
        
        return JSONResponse(content={"processed_text": processed_text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/extract-information/")
async def extract_info(text: str, model: str ):
    try:
        extracted_info = extract_information(text, model)
        return {"extracted_information": extracted_info}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/ask-question/")
async def ask_question(text: str, question: str, model: str ):
    try:
        answer = get_answer(text, question, model)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/summarize-document/")
async def summarize_doc(text: str, model: str):
    try:
        summary = summarize_document(text, model)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/classify-document/")
async def classify_doc(text: str, model: str):
    try:
        classification = classify_document(text, model)
        return {"classification": classification}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/translate-text/")
async def translate_txt(text: str, target_language: str, model: str):
    try:
        translation = translate_text(text, target_language, model)
        return {"translation": translation}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
