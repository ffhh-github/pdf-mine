#!/usr/bin/env python3
import os
import sys
import requests
from docx import Document
import json

# === YOUR POE API KEY ===
POE_API_KEY = "UZkBIjfV7DWCDbEar0r6QvMTERL1v88hi2sOR6YoxQ"

# === Model map (add/remove as needed) ===
MODELS = {
    "Claude":   "claude-3-5-sonnet",
    "ChatGPT":  "gpt-4o",
    "Gemini":   "gemini-1.5-pro",
    "Llama":    "llama-3-70b-instruct",
    "Mixtral":  "mixtral-8x22b",
    # Full list: https://poe.com/api/models
}

# Poe Official API
BASE_URL = "https://api.poe.com/v1/chat/completions"

def get_response(model_name, prompt):
    if not POE_API_KEY:
        return "Error: API key missing."
    
    headers = {
        "Authorization": f"Bearer {POE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Network Error: {str(e)[:100]}"
    except Exception as e:
        return f"API Error: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_poe.py <your_document.docx>")
        sys.exit(1)

    doc_path = sys.argv[1]
    doc = Document(doc_path)
    text = "\n".join(p.text for p in doc.paragraphs)

    # Extract [A] and [AI] sections
    try:
        prompt = text.split("[A]")[1].split("[/A]")[0].strip()
        ai_names = [l.strip() for l in text.split("[AI]")[1].split("[/AI]")[0].split("\n") if l.strip()]
    except Exception:
        print("Error: Missing [A]...[/A] or [AI]...[/AI] in document")
        sys.exit(1)

    print(f"Running {len(ai_names)} models...")
    responses = {}
    for name in ai_names:
        model = MODELS.get(name)
        if not model:
            responses[name] = "Model not in MODELS"
            print(f"{name}: skipped")
            continue
        print(f"{name}...", end=" ", flush=True)
        responses[name] = get_response(model, prompt)
        print("Done")

    # Write results after [B]
    output = "\n\n[B]\n"
    for n, r in responses.items():
        output += f"{n}:\n{r}\n\n---\n\n"

    doc = Document(doc_path)
    doc.add_paragraph(output)
    doc.save(doc_path)

    print(f"\nSuccess! Open: {doc_path}")

if __name__ == "__main__":
    main()
