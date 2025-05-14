import fitz  
from keybert import KeyBERT
import spacy
import os

# Load models
print("Loading models")
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()
print("Models loaded.\n")

# Extract text from PDF
pdf_path = "/Users/aaravtiwari/fidhacks/example.pdf"  # replace with filename

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f" File not found: {pdf_path}")

print(f"Reading PDF: {pdf_path}")
doc = fitz.open(pdf_path)
text = ""
for page_num, page in enumerate(doc, start=1):
    page_text = page.get_text().strip()
    print(f"--- Page {page_num} ---")
    print(page_text[:300])  # show first 300 characters of each page
    text += page_text + "\n"

if not text.strip():
    raise ValueError(" No text could be extracted from the PDF. Is it a scanned image or empty?")

# Named Entity Recognition (NER) 
doc_nlp = nlp(text)
ner_keywords = list(set(
    ent.text.strip() for ent in doc_nlp.ents
    if ent.label_ in ("ORG", "GPE", "PERSON", "NORP", "FAC", "WORK_OF_ART", "PRODUCT", "EVENT")
))

print("\n=== NER Keywords ===")
print(ner_keywords if ner_keywords else " No keywords found by spaCy NER.")

# KeyBERT keyword extraction 
keybert_results = kw_model.extract_keywords(
    text,
    keyphrase_ngram_range=(1, 2),
    stop_words='english',
    top_n=10
)
keybert_keywords = [kw[0] for kw in keybert_results]

print("\n=== KeyBERT Keywords ===")
print(keybert_keywords if keybert_keywords else " No keywords found by KeyBERT.")

# Write to output file 
with open("output.txt", "w") as f:
    f.write("KEYWORDS FROM NER:\n")
    f.write(", ".join(ner_keywords) + "\n\n" if ner_keywords else "None found.\n\n")
    f.write("KEYWORDS FROM KeyBERT:\n")
    f.write(", ".join(keybert_keywords) if keybert_keywords else "None found.")

print("\n Keyword extraction complete. See 'output.txt'.")
