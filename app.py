import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Talha's AI Document Assistant", page_icon="📄")
st.title("📄 Talha's AI Document Assistant")
st.caption("Powered by Gemini 3.6 Flash, Streamlit & PyPDF")

API_KEY = st.sidebar.text_input("Enter your Gemini API Key", type="password")
client = genai.Client(api_key=API_KEY)

# 2. Sidebar File Uploader (Supports TXT & PDF)
st.sidebar.header("📁 Document Upload")
uploaded_file = st.sidebar.file_uploader("Upload a file (.txt or .pdf)", type=["txt", "pdf"])

file_text = ""
if uploaded_file is not None:
    # PDF Parsing Logic
    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            extracted_page_text = page.extract_text()
            if extracted_page_text:
                file_text += extracted_page_text + "\n"
    # Plain Text Parsing Logic
    else:
        file_text = uploaded_file.read().decode("utf-8")
        
    st.sidebar.success(f"Loaded '{uploaded_file.name}' successfully!")

# 3. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Render Conversation History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle Prompt Submission
if prompt := st.chat_input("Ask anything about the document or a general question..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Attach document text as context if available
    if file_text:
        final_prompt = f"Read the following document carefully and answer the user's question:\n\n--- DOCUMENT START ---\n{file_text}\n--- DOCUMENT END ---\n\nUser Question: {prompt}"
    else:
        final_prompt = prompt

    # Package History for Gemini
    formatted_contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        formatted_contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )

    formatted_contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=final_prompt)]
        )
    )

    config = types.GenerateContentConfig(
        system_instruction="You are an expert AI document analyzer helping Talha extract facts accurately."
    )

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=formatted_contents,
            config=config
        )
        st.markdown(response.text)

    # Save Turn to Session State
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response.text})