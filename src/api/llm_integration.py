from .models.gpt import call_gpt
from .models.gemini import call_gemini


def extract_information(text, model_type):
    prompt = f"Extract key-value pairs from the following text:\n\n{text}"
    return call_llm(prompt, model=model_type)

def get_answer(text, question, model_type):
    prompt = f"Based on the following text, answer the question:\n\nText:\n{text}\n\nQuestion:\n{question}"
    return call_llm(prompt, model=model_type)

def summarize_document(text, model_type):
    prompt = f"Summarize the key points from the following document:\n\n{text}"
    return call_llm(prompt, model=model_type)

def classify_document(text, model_type):
    prompt = f"Classify the following text based on its content and infer the appropriate categories:\n\n{text}"
    return call_llm(prompt, model=model_type)

def translate_text(text, target_language, model_type):
    prompt = f"Translate the following text into {target_language}:\n\n{text}"
    return call_llm(prompt, model=model_type)

def call_llm(prompt, model="default_model"):
    if model == "GPT":
        return call_gpt(prompt)
    elif model == "Gemini":
        return call_gemini(prompt)
    else:
        return "Unknown model type"
