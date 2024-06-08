import streamlit as st
import requests

st.title("Document Processing Chatbot")

# Initialize conversation history in session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = {'User': [], 'System': []}

# Function to display conversation history
def display_conversation():
    # Find the maximum number of messages in either list to avoid index errors
    max_length = max(len(st.session_state.conversation['User']), len(st.session_state.conversation['System']))
    
    # Interleave messages from User and System
    for i in range(max_length):
        if i < len(st.session_state.conversation['User']):
            st.write(f"**User**: {st.session_state.conversation['User'][i]}")
        if i < len(st.session_state.conversation['System']):
            st.write(f"**System**: {st.session_state.conversation['System'][i]}")
            

# Function to add messages to the conversation
def add_message(role, content):
    st.write(role, content)
    st.session_state.conversation[role].append(content)
    # display_conversation()

# File upload
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
if uploaded_file and 'processed_text' not in st.session_state:
    files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
    response = requests.post("http://127.0.0.1:8000/process-document/", files=files)
    if response.status_code == 200:
        st.session_state.processed_text = response.json().get("processed_text", "")
        st.write("User", "Uploaded document.")
        st.write("System", "Document processed successfully.")
        
    else:
        st.write("System", "Failed to process document. Please try again.")

# Display processed text if available
if 'processed_text' in st.session_state:
    st.text_area("Processed Text", st.session_state.processed_text, height=200)

# Display the conversation UI
display_conversation()

# Task selection
if 'processed_text' in st.session_state:
    task = st.selectbox("Choose a task", ["Ask Question", "Extract Information", "Summarize Document", "Classify Document", "Translate Text"])

    if task == "Ask Question":
        question = st.text_input("Enter your question about the document:")
        if st.button("Ask"):
            response = requests.post("http://127.0.0.1:8000/ask-question/", params={"text": st.session_state.processed_text, "question": question})
            if response.status_code == 200:
                answer = response.json().get("answer", "")
                add_message("User", question)
                add_message("System", answer)
            else:
                add_message("System", "Failed to get answer.")

    elif task == "Extract Information":
        if st.button("Extract Information"):
            response = requests.post("http://127.0.0.1:8000/extract-information/", params={"text": st.session_state.processed_text})
            if response.status_code == 200:
                extracted_info = response.json().get("extracted_information", "")
                add_message("User", "Requested extraction of information.")
                add_message("System", extracted_info)
            else:
                add_message("System", "Failed to extract information.")

    elif task == "Summarize Document":
        if st.button("Summarize Document"):
            response = requests.post("http://127.0.0.1:8000/summarize-document/", params={"text": st.session_state.processed_text})
            if response.status_code == 200:
                summary = response.json().get("summary", "")
                add_message("User", "Requested document summary.")
                add_message("System", summary)
            else:
                add_message("System", "Failed to summarize document.")

    elif task == "Classify Document":
        # categories = st.text_input("Enter categories (comma-separated):")
        if st.button("Classify Document"):
            response = requests.post("http://127.0.0.1:8000/classify-document/", params={"text": st.session_state.processed_text})
            if response.status_code == 200:
                classification = response.json().get("classification", "")
                add_message("User", f"Classified Document.")
                add_message("System", classification)
            else:
                add_message("System", "Failed to classify document.")

    elif task == "Translate Text":
        target_language = st.text_input("Enter target language:")
        if st.button("Translate Text"):
            response = requests.post("http://127.0.0.1:8000/translate-text/", params={"text": st.session_state.processed_text, "target_language": target_language})
            if response.status_code == 200:
                translation = response.json().get("translation", "")
                add_message("User", f"Requested translation to: {target_language}")
                add_message("System", translation)
            else:
                add_message("System", "Failed to translate text.")
