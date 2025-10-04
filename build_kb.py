
"""
build_haw_kb_from_pdf.py

Reads the HAW_Hamburg_Online_Services.xlsx, extracts all URLs from the Excel file,
cleans/validates them, fetches page content, and builds a JSON knowledge base.

Run:
    python build_haw_kb_from_excel.py
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse


EXCEL_PATH = "HAW_Hamburg_Online_Services.xlsx"
OUTPUT_JSON = "haw_kb.json"


# ------------------- URL Handling -------------------
def extract_urls_from_excel(excel_path):
    """Extract all http(s) URLs from the Excel file."""
    df = pd.read_excel(excel_path)
    urls = []
    for _, row in df.iterrows():
        label = str(row.get("Label", "")).strip()
        url = str(row.get("URL", "")).strip()
        if url:
            urls.append((label, url))
    return urls


def is_valid_url(url):
    """Check if URL has a valid scheme and netloc."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


# ------------------- Fetching -------------------
def fetch_page_text(url):
    """Fetch a web page and return cleaned visible text."""
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()  ## checks the HTTP status code
    except Exception as e:
        return None, f"Error fetching {url}: {e}"

    soup = BeautifulSoup(resp.text, "html.parser")  ## using html.parser to extract the response text

    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)  ## using regex sub method to clean the response text 
    return text, None


def split_text_into_chunks(text, chunk_size=500):
    """Split text into chunks of approximately `chunk_size` words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


# ------------------- Build KB -------------------
def build_kb(excel_path, output_path):
    raw_data = extract_urls_from_excel(excel_path)
    cleaned = [(label, u) for label, u in raw_data]
    unique_urls = list(dict.fromkeys([u for _, u in cleaned]))  # deduplicate while keeping order

    kb = []
    for label, url in cleaned:
        if not is_valid_url(url):
            print(f"Skipping invalid URL: {url}")
            kb.append({
                "url": url,
                "title": label,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "status": "invalid",
                "chunk_id": None,
                "text": "",
                "error": "Invalid URL"
            })
            continue

        print(f"Fetching {url} ...")
        text, error = fetch_page_text(url)

        if text:
            chunks = split_text_into_chunks(text, chunk_size=500)
            for idx, chunk in enumerate(chunks):
                entry = {
                    "url": url,
                    "title": label,
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success",
                    "chunk_id": idx,
                    "text": chunk,
                    "error": "",
                }
                kb.append(entry)
        else:
            entry = {
                "url": url,
                "title": label,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "status": "error",
                "chunk_id": None,
                "text": "",
                "error": error if error else "",
            }
            kb.append(entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Knowledge base saved to {output_path} with {len(kb)} entries.")


if __name__ == "__main__":
    build_kb(EXCEL_PATH, OUTPUT_JSON)
