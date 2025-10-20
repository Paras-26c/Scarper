import json
import requests

def save_json(data, filename):
    """Save results to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"📁 Saved results to {filename}")

def download_pdf(url, filename):
    """Download PDF file from URL."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"📥 PDF downloaded: {filename}")
    else:
        print("⚠️ PDF not available or link broken.")
