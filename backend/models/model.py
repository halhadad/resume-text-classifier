from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F
from io import BytesIO
import os


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
# def load_model():
#     # Update this path to your model directory
#     model_path = "./model_84"  
#     return load_model_manually(model_path)
def load_model():
    # Get absolute path to model directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "model_84")
    return load_model_manually(model_path)
model, tokenizer = load_model()

def predict_label(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return model.config.id2label[predicted_class_id]



# Load model and tokenizer
def classify_text(text: str) -> str:
    label = predict_label(text, model, tokenizer)
    return label


