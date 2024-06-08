from .models.llm_model import call_llm

def extract_information(text):
    prompt = f"Extract key-value pairs from the following text:\n\n{text}"
    return call_llm(prompt)

def get_answer(text, question):
    prompt = f"Based on the following text, answer the question:\n\nText:\n{text}\n\nQuestion:\n{question}"
    return call_llm(prompt)

def summarize_document(text):
    prompt = f"Summarize the key points from the following document:\n\n{text}"
    return call_llm(prompt)

def classify_document(text):
    prompt = f"Classify the following text based on its content and infer the appropriate categories:\n\n{text}"
    return call_llm(prompt)

def translate_text(text, target_language):
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    return call_llm(prompt)
