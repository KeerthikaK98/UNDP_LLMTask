import os
import re
import fitz
import requests
#import pdfplumber
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from tqdm import tqdm
import time
import random
from requests.exceptions import RequestException
from langchain.schema import Document
from config import ffd4_URL, index_path, doc_path, embedding_model_, llm_model


# Scraping FFD4 Pdfs

def pdf_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    pdf_url = [link["href"] for link in links if link["href"].endswith(".pdf")]
    return list(set(pdf_url))

# Extracting text from Pdfs

def extract_text_from_pdf(url, save_dir="data/pdfs", retries=3):
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(url)
    filepath = os.path.join(save_dir, filename)

    headers={
        "User-Agent":"Mozilla/5.0"
    }

    if not os.path.exists(filepath):
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, stream=True, timeout=30)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                break
            except RequestException as e:
                print(f"Download failed for {filename}, retrying.. ({attempt+1}/{retries})")
                time.sleep(random.uniform(1.5, 4.0))
        else:
            print(f" skipping {filename}: Failed after {retries} attempts")
            return ""
        
        #with requests.get(url, stream=True) as r:
         #   with open(filepath, "wb") as f:
          #      f.write(r.content)

    try:
        with fitz.open(filepath) as pdf:
            full_text = ""
            for page in pdf:
                text = page.get_text()
                full_text += text+ "\n"
            return full_text
    except Exception as e:
        print(f"Failed to read {filename}: {e}")
        return ""
    
# Cleaning the text

def clean_text(text):
    #text = text.replace("\n"," ")
    #text = " ".join(text.split())
    #return text
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line or (line.isupper() and len(line.split())<=6):
            continue
        if re.match(r'^\d+$', line) or re.match(r'^page \d+', line.lower()):
            continue
        cleaned_lines.append(line)
    clean_text = " ".join(cleaned_lines)
    return re.sub(r'\s+', ' ', clean_text).strip()

# Embedding and Indexing

def embed_docs(texts, model_name = embedding_model_):
    model = SentenceTransformer(model_name)
    text_list = [doc.page_content for doc in texts]
    embeddings = model.encode(text_list, convert_to_numpy=True, show_progress_bar=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings, model

# Pipeline Runner

def run_pipeline(base_url, limit=100):
    pdf_l = pdf_links(base_url)
    print(f"Found {len(pdf_l)} PDFs")

    docs= []
    for url in tqdm(pdf_l[:limit], desc="Extracting PDFs"):
        text = extract_text_from_pdf(url)
        if len(text)>300:
            cleaned = clean_text(text)
            filename = os.path.basename(url)
            docs.append(Document(page_content=cleaned, metadata= {"source":filename}))

    
    print(f"{len(docs)} docs ready for indexing")
    index, embeddings, model = embed_docs(docs)

    os.makedirs(os.path.dirname(doc_path), exist_ok=True)
    faiss.write_index(index, index_path)
    with open(doc_path, "w", encoding = "utf-8") as f:
        for doc in docs:
            f.write(f"## Source: {doc.metadata['source']}\n")
            f.write(doc.page_content + "\n\n")
    print("Index and Documents saved")

if __name__ == "__main__":
    #FFD4_URL = "https://financing.desa.un.org/ffd4/elementspaperinputs"
    if not ffd4_URL:
        raise ValueError("Missing FFD4 URL in .env file")
    run_pipeline(ffd4_URL)

