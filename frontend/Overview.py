import streamlit as st

st.set_page_config(page_title="Overview", page_icon="https://i.ibb.co/j9pDZwkb/resumate-logo.png")
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

st.title("Resumate: Classification of Resume Content")


# st.title("Resumate: Classification of Resume Content")
st.markdown("Navigate from the sidebar to choose how to classify resume content:")
st.markdown("- **PDF Upload**: Upload and classify resumes from PDF files.")
st.markdown("- **Text Input**: Paste raw resume text for classification.")
