import os
import docx
import requests

# === CONFIGURATION ===
# Insert your API keys here as environment variables or directly in the script
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-claude-key")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "your-cohere-key")

# === HELPER: Load .docx prompt ===
def load_docx(filename):
    doc = docx.Document(filename)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# === AI QUERIES ===
def query_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {
        "model": "gpt-4o-mini",  # try gpt-4o or gpt-3.5-turbo if needed
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()

    if "error" in result:
        return f"OpenAI API error: {result['error']['message']}"
    elif "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"Unexpected response: {result}"

def query_claude(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {"x-api-key": ANTHROPIC_API_KEY, "Content-Type": "application/json"}
    data = {
        "model": "claude-3-haiku-20240307",  # or claude-3-opus if available
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()

    if "error" in result:
        return f"Claude API error: {result['error']['message']}"
    elif "content" in result:
        return result["content"][0]["text"]
    else:
        return f"Unexpected response: {result}"

def query_cohere(prompt):
    url = "https://api.cohere.ai/v1/chat"
    headers = {"Authorization": f"Bearer {COHERE_API_KEY}"}
    data = {"model": "command-r", "message": prompt}
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()

    if "error" in result:
        return f"Cohere API error: {result['error']['message']}"
    elif "text" in result:
        return result["text"]
    else:
        return f"Unexpected response: {result}"

# === MAIN ===
def main():
    prompt = load_docx("My AI Prompt.docx")
    print("Prompt loaded from My AI Prompt.docx\n")

    print("=== OpenAI (ChatGPT) Response ===")
    print(query_openai(prompt))
    print("\n=== Anthropic (Claude) Response ===")
    print(query_claude(prompt))
    print("\n=== Cohere Response ===")
    print(query_cohere(prompt))

if __name__ == "__main__":
    main()

