"""Model package globals: MODEL, TOKENIZER, DEVICE, LABEL_MAP"""
import os
import torch
from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer

load_dotenv()

LABEL_MAP = {
    "Edu": "Education",
    "Exp": "Experience",
    "Skill": "Skills",
    "Obj": "Objective",
    "QC": "Qualifications and Certificates",
    "PI": "Personal Information",
    "Sum": "Summary",
}

# Configuration
import json

# Find project root and load config
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(root_dir, "config.json")

def load_config():
    default_config = {
        "hf_repo_id": "halhadad/DistilBERT-NLP-Resume-TextClassifer-Lines",
        "use_local_model": False,
        "hf_token_env_var": "HF_TOKEN"
    }
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return {**default_config, **json.load(f)}
    return default_config

config = load_config()

HF_REPO_ID = config["hf_repo_id"]
# Environment variable overrides config if present, otherwise use config value
USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", str(config["use_local_model"])).lower() == "true"
token_env_var = config["hf_token_env_var"]
HF_TOKEN = os.getenv(token_env_var)

model_path = None
load_kwargs = {}

if USE_LOCAL_MODEL:
    # Find local model path
    print("Attempting to load model locally...")
    root = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(root, "model_90"),  # preferred
        os.path.join(root, "..", "models", "model_90"),  # legacy
    ]
    for p in possible_paths:
        if os.path.isdir(p):
            model_path = p
            break
    
    if not model_path:
        # Fallback handling or error
        print("Local model not found. Falling back to Hugging Face Hub.")
        model_path = HF_REPO_ID
        load_kwargs = {"token": HF_TOKEN}
    else:
        print(f"Found local model at: {model_path}")
        load_kwargs = {"local_files_only": True}
else:
    # Use Hugging Face Hub
    print(f"Loading model from Hugging Face Hub: {HF_REPO_ID}")
    model_path = HF_REPO_ID
    load_kwargs = {"token": HF_TOKEN}
    
    if not HF_TOKEN:
        print("Warning: HF_TOKEN not found. Access to private repositories might fail.")

# Load globals
try:
    TOKENIZER = AutoTokenizer.from_pretrained(model_path, **load_kwargs)
    MODEL = AutoModelForSequenceClassification.from_pretrained(model_path, **load_kwargs)
except Exception as e:
    print(f"Error loading model from {model_path}: {e}")
    # Critical failure if model cannot be loaded
    raise e

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL.to(DEVICE)