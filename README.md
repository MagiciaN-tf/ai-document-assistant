# 📄 Streamlit AI Document Assistant

An interactive web application built with Python, Streamlit, and Google's Gemini 3.6 Flash model. Upload multi-page PDFs or `.txt` files to ask contextual questions directly against source documents.

## ⚡ Features
- **Document Ingestion:** Processes `.txt` and `.pdf` files using `pypdf`.
- **Session Memory:** Retains full conversational context across turns.
- **Stateless LLM Integration:** Uses the modern `google-genai` SDK.

## 🛠️ Tech Stack
- **Frontend/UI:** Streamlit
- **AI Model:** Google Gemini 3.6 Flash (`google-genai` SDK)
- **Document Parsing:** `pypdf`

## 🚀 Getting Started

1. Clone the repository:
git clone https://github.com/MagiciaN-tf/ai-document-assistant.git
cd ai-document-assistant

2. Install dependencies:
pip install -r requirements.txt

3. Run the application:
streamlit run app.py
