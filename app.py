import os
import streamlit as st
import google.genai as genai
import fitz  # PyMuPDF
import json

# --- CONFIG ---
st.set_page_config(page_title="Lazarus AI | Pharma Insights", layout="wide")
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
MODEL_ID = 'models/gemini-2.5-flash'

# --- LOGIC ---
def pdf_to_text(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# --- UI ---
st.title("🧬 Project Lazarus: Agentic Trial Matching")
st.markdown("### Accelerating Clinical Recruitment via Automated Protocol Logic")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Protocol")
    uploaded_pdf = st.file_uploader("Upload Phase III PDF", type="pdf")
    
with col2:
    st.header("2. Patient Context")
    patient_note = st.text_area("Paste Anonymized Doctor's Note", height=200, placeholder="e.g. 55yo Male, Stage IV SCLC...")

if st.button("Run Intelligence Audit"):
    if uploaded_pdf and patient_note:
        with st.spinner("Extracting Protocol Logic & Auditing Patient..."):
            # A. Process PDF
            context = pdf_to_text(uploaded_pdf)
            
            # B. Agentic Analysis
            prompt = f"""
            MISSION: Extract Inclusion/Exclusion from this protocol AND Audit this patient note: {patient_note}
            PROTOCOL TEXT: {context}
            
            OUTPUT: Provide a JSON Matching Report with 'Status', 'Matched_Criteria', and 'Critical_Conflicts'.
            """
            
            response = client.models.generate_content(model=MODEL_ID, contents=prompt)
            
            st.success("Audit Complete")
            st.json(response.text)
    else:
        st.error("Please provide both a PDF and a Patient Note.")