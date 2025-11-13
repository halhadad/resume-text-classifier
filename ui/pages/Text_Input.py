import streamlit as st
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

st.title("Text Input")
text_input = st.text_area("Paste your resume text here", height=300)

if text_input:
    text_lines = [line.strip() for line in text_input.split('\n') if line.strip()]
    if st.button("Classify"):
        rows = classify_lines(text_lines)
        if rows:
            display_results(rows)
            st.success("Prediction successful")
        else:
            st.warning("No lines to classify.")
