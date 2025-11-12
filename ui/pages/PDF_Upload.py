import streamlit as st
import PyPDF2
from io import BytesIO
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from inference.model_inference import classify_lines

st.set_page_config(page_icon="https://i.ibb.co/j9pDZwkb/resumate-logo.png")
st.logo(
    "https://i.ibb.co/j9pDZwkb/resumate-logo.png",
    link="https://i.ibb.co/j9pDZwkb/resumate-logo.png",
    size="large",
)
st.sidebar.markdown("<div style='height:45vh;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("""
<hr style="margin-top: 0;">
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://i.ibb.co/j9pDZwkb/resumate-logo.png" width="25">
    <span style="font-size: 16px; font-weight: 600;">Resumate</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 10px; font-weight: 300;">Made by github.com/halhadad</span>
</div>
""", unsafe_allow_html=True)

def extract_text_from_pdf(uploaded_file):
    text = []
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            lines = page_text.split('\n')
            text += [line.strip() for line in lines if line.strip()]
    return text

def display_results(rows):
    st.subheader("Classification Results")
    table = [
        {
            "Line #": i + 1,
            "Text": r["text"],
            "Label": r["label"],
        }
        for i, r in enumerate(rows)
    ]
    st.dataframe(
        data=table,
        column_config={
            "Line #": "Line #",
            "Text": "Resume Text",
            "Label": st.column_config.SelectboxColumn(
                "Category",
                help="Predicted category (editable for manual correction)",
                width="medium",
                options=[
                    "Experience",
                    "Education",
                    "Personal Information",
                    "Objective",
                    "Summary",
                    "Qualifications and Certificates",
                    "Skills"
                ]
            ),
        },
        use_container_width=True,
        hide_index=True
    )

st.title("PDF Upload")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    text_lines = extract_text_from_pdf(BytesIO(uploaded_file.read()))
    if st.button("Classify"):
        rows = classify_lines(text_lines)
        if rows:
            display_results(rows)
            st.success("Prediction successful")
        else:
            st.warning("No text extracted to classify.")
