import google.generativeai as genai


# Assuming you have obtained your API key (replace with your actual key)
API_KEY = "API_KEY"

def call_llm(prompt, max_length=1000):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
