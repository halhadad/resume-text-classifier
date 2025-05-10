import streamlit as st
import PyPDF2
from io import BytesIO
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_model_manually(model_path):
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=True  # Force local loading
        )
        
        # Load model
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            local_files_only=True
        )
        
        return model, tokenizer
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

# Load your pre-trained model and tokenizer
@st.cache_resource
def load_model():
    # Update this path to your model directory
    model_path = "model/scratch/checkpoint-11802"  
    #model_path = "model/resume_text_classifier_model"  
    return load_model_manually(model_path)

def extract_text_from_pdf(uploaded_file):
    text = []
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            lines = page_text.split('\n')
            text += [line.strip() for line in lines if line.strip()]
    return text

def predict_label(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return model.config.id2label[predicted_class_id]

def main():
    st.title("Resume Sentence Classifier")
    st.markdown("Upload a PDF resume to classify each line into categories")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Process PDF
        text_lines = extract_text_from_pdf(BytesIO(uploaded_file.read()))
        
        # Load model
        model, tokenizer = load_model()
        
        # Make predictions
        results = []
        for i, line in enumerate(text_lines):
            label = predict_label(line, model, tokenizer)
            results.append({
                "Line Number": i+1,
                "Text": line,
                "Label": label
            })

        # Display results
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

if __name__ == "__main__":
    main()