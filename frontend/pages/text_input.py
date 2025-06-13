import streamlit as st
import requests

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

st.title("Text Input")
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
