"""
build_haw_kb_from_pdf.py

Reads the HAW_Hamburg_Online_Services.pdf, extracts all URLs,
cleans/validates them, fetches page content, and builds a JSON knowledge base.

Run:
    python build_haw_kb_from_pdf.py
"""

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse


PDF_PATH = "HAW_Hamburg_Online_Services.pdf"
OUTPUT_JSON = "haw_kb.json"
