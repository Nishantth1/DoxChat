import streamlit as st
import requests
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from dotenv import load_dotenv
import os

load_dotenv()

# Load the API URL from environment variables
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="DoxChat")

logo_path = r"./src/ui/white_logo.png"

with st.sidebar:
    try:
        st.image(logo_path, width=200)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        
    model_choice = st.selectbox("Choose Language Model", ["Gemini", "GPT"])
    st.session_state.model_choice = model_choice
    st.title('📄 Document Processing Chatbot')
    st.markdown('''
    ## About
    This app allows you to upload a PDF document and perform various tasks such as:
    - Asking questions
    - Extracting information
    - Summarizing the document
    - Classifying the document
    - Translating text
    
    Powered by Streamlit and custom backend services.
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Nishant](https://www.linkedin.com/in/nishant-thakre/)')

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I'm here to help you with your document. Please upload a PDF to get started."}]

# Display chat messages from history on app rerun
def display_conversation():
    for message_data in st.session_state.messages:
        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])

# Add messages to the conversation
def add_message(role, content):
    with st.chat_message(role):
        st.markdown(content)
    st.session_state.messages.append({"role": role, "content": content})

if 'processed_text' not in st.session_state:
    st.session_state.processed_text = ""

# File upload
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "jpeg", "png"])

if uploaded_file:
    st.session_state.processed_text = ""
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    response = requests.post(f"{API_URL}/process-document/", files=files)
    if response.status_code == 200:
        st.session_state.processed_text = response.json().get("processed_text", "")
        with st.chat_message('user'):
            st.markdown('Uploaded document.')
        with st.chat_message('assistant'):
            st.markdown('Document processed successfully.')
    else:
        with st.chat_message('assistant'):
            st.markdown('Failed to process document. Please try again.')

# Display processed text if available
if 'processed_text' in st.session_state:
    st.text_area("Processed Text", st.session_state.processed_text, height=200)

# Display the conversation UI
display_conversation()

# Task selection and interaction
if 'processed_text' in st.session_state:
    task = st.selectbox("Choose a task", ["Chat with Doc", "Extract Information", "Summarize Document", "Classify Document", "Translate Text"])

    if task == "Chat with Doc":
        prompt = st.text_input("Enter your question about the document:", key="ask_question")
        if st.button("Submit Question"):
            response = requests.post(f"{API_URL}/ask-question/", params={"text": st.session_state.processed_text, "question": prompt, 'model': st.session_state.model_choice})
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                add_message("user", prompt)
                add_message("assistant", answer)
            else:
                add_message("assistant", "Failed to get answer.")

    elif task == "Extract Information":
        if st.button("Submit Extraction"):
            response = requests.post(f"{API_URL}/extract-information/", params={"text": st.session_state.processed_text, 'model': st.session_state.model_choice})
            if response.status_code == 200:
                extracted_info = response.json().get("extracted_information", "")
                add_message("user", "Extracting Information...")
                add_message("assistant", extracted_info)
            else:
                add_message("assistant", "Failed to extract information.")

    elif task == "Summarize Document":
        if st.button("Submit Summary"):
            response = requests.post(f"{API_URL}/summarize-document/", params={"text": st.session_state.processed_text, 'model': st.session_state.model_choice})
            if response.status_code == 200:
                summary = response.json().get("summary", "")
                add_message("user", "Summarizing Text...")
                add_message("assistant", summary)
            else:
                add_message("assistant", "Failed to summarize document.")

    elif task == "Classify Document":
        if st.button("Submit Classification"):
            response = requests.post(f"{API_URL}/classify-document/", params={"text": st.session_state.processed_text, 'model': st.session_state.model_choice})
            if response.status_code == 200:
                classification = response.json().get("classification", "")
                add_message("user", "Classifying Document...")
                add_message("assistant", classification)
            else:
                add_message("assistant", "Failed to classify document.")

    elif task == "Translate Text":
        target_language = st.text_input("Enter target language:", key="translate_text_lang")
        if st.button("Submit Translation"):
            response = requests.post(f"{API_URL}/translate-text/", params={"text": st.session_state.processed_text, "target_language": target_language, 'model': st.session_state.model_choice})
            if response.status_code == 200:
                translation = response.json().get("translation", "")
                add_message("user", f"Requested translation to: {target_language}")
                add_message("assistant", translation)
            else:
                add_message("assistant", "Failed to translate text.")
