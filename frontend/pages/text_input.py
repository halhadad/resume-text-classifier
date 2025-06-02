import streamlit as st
import requests

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

st.title("Text Resume Classifier")
text_input = st.text_area("Paste your resume text here", height=300)

if text_input:
    text_lines = [line.strip() for line in text_input.split('\n') if line.strip()]
    if st.button("Classify"):
        res = requests.post("http://127.0.0.1:8000/predict", json={"text": text_lines})
        if res.ok:
            display_results(res.json(), text_lines)
            st.success("Prediction successful")
        else:
            st.error("Error during prediction")
