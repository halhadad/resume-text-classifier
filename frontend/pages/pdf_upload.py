import streamlit as st
import PyPDF2
import requests
from io import BytesIO

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
                options=["Experience", "Education", "Personal Information", "Objective", "Summary", "Qualifications and Certificates", "Skills"]
            )
        },
        use_container_width=True,
        hide_index=True
    )

st.title("PDF Upload")
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
