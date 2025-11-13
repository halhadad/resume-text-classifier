"""Model package globals: MODEL, TOKENIZER, DEVICE, LABEL_MAP"""
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

LABEL_MAP = {
    "Edu": "Education",
    "Exp": "Experience",
    "Skill": "Skills",
    "Obj": "Objective",
    "QC": "Qualifications and Certificates",
    "PI": "Personal Information",
    "Sum": "Summary",
}

# Find model path
root = os.path.dirname(os.path.abspath(__file__))
model_paths = [
    os.path.join(root, "model_90"),  # preferred
    os.path.join(root, "..", "models", "model_90"),  # legacy
]
model_path = None
for p in model_paths:
    if os.path.isdir(p):
        model_path = p
        break
if not model_path:
    raise FileNotFoundError("Could not locate model_90 in models/ or legacy backend path.")

# Load globals
TOKENIZER = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
MODEL = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL.to(DEVICE)