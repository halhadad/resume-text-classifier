import streamlit as st
import PyPDF2
import requests
from io import BytesIO

def extract_text_from_pdf(uploaded_file):
    text = []
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            lines = page_text.split('\n')
            text += [line.strip() for line in lines if line.strip()]
    return text

def display_results(results, text_lines):
    results = [{"Line Number": i + 1, "Text": text_lines[i], "Label": label} for i, label in enumerate(results["labels"])]
    st.subheader("Classification Results")
    st.dataframe(
        data=results,
        column_config={
            "Line Number": "Line #",
            "Text": "Resume Text",
            "Label": st.column_config.SelectboxColumn(
                "Category",
                help="The predicted category",
                width="medium",
                options=["Exp", "Edu", "PI", "Obj", "Sum", "QC", "Skill"]
            )
        },
        use_container_width=True,
        hide_index=True
    )

st.title("PDF Resume Classifier")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    text_lines = extract_text_from_pdf(BytesIO(uploaded_file.read()))
    if st.button("Classify"):
        res = requests.post("http://127.0.0.1:8000/predict", json={"text": text_lines})
        if res.ok:
            display_results(res.json(), text_lines)
            st.success("Prediction successful")
        else:
            st.error("Error during prediction")
