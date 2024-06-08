from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .ocr import extract_text_from_pdf
from .preprocessing import preprocess_text
from .llm_integration import extract_information, summarize_document, classify_document, translate_text, get_answer

app = FastAPI()

@app.post("/process-document/")
async def process_document(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid document type. Only PDFs are supported.")
    
    try:
        file_location = f"./data/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process the file
        extracted_text = extract_text_from_pdf(file_location)
        processed_text = preprocess_text(extracted_text)
        return JSONResponse(content={"processed_text": processed_text})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/extract-information/")
async def extract_info(text: str):
    try:
        extracted_info = extract_information(text)
        return {"extracted_information": extracted_info}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
@app.post("/ask-question/")
async def extract_info(text: str, question: str):
    try:
        answer = get_answer(text, question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/summarize-document/")
async def summarize_doc(text: str):
    try:
        summary = summarize_document(text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/classify-document/")
async def classify_doc(text: str):
    try:
        classification = classify_document(text)
        return {"classification": classification}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/translate-text/")
async def translate_txt(text: str, target_language: str):
    try:
        translation = translate_text(text, target_language)
        return {"translation": translation}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
