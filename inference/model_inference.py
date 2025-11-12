"""Model inference functionality using globals from models.__init__"""
import torch
from typing import List, Dict
from . import MODEL, TOKENIZER, DEVICE, LABEL_MAP

@torch.no_grad()
def classify_lines(lines: List[str]) -> List[Dict]:
    if not lines:
        return []
    inputs = TOKENIZER(lines, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    logits = MODEL(**inputs).logits
    pred_ids = logits.argmax(dim=-1)
    results = []
    for idx, line in enumerate(lines):
        class_id = pred_ids[idx].item()
        code = MODEL.config.id2label[class_id]
        label = LABEL_MAP.get(code, code)
        results.append({
            "text": line,
            "label": label,
        })
    return results
