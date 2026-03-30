# Document AI for Financial Quotations

### Intelligent Information Extraction from Scanned Documents

---

##  Problem Statement

Financial institutions receive large volumes of scanned quotation documents (PDFs/images) for loan processing.  
These documents are unstructured, noisy, and vary widely in layout, making manual verification slow and error-prone.

##  Objective

Build an end-to-end **Document AI pipeline** that automatically extracts key financial fields from scanned quotation images and produces **structured JSON output with confidence scores**.

---

##  System Overview

The system processes raw document images and extracts:

- Dealer Name
- Model Name
- Horse Power (HP)
- Asset Cost
- Stamp Presence
- Signature Presence
- Overall Confidence Score

Final output is saved as a machine-readable JSON file.

---

##  Design Philosophy

> **Design once. Scale everywhere.**

The solution avoids hardcoding for specific documents and instead uses **generic OCR + rule-based extraction**, making it scalable across hundreds of document variations.

---

##  Architecture

```
Document Images
↓
OCR (Tesseract)
↓
Text Cleaning & Normalization
↓
Rule-Based Field Extraction
↓
Vision-Based Stamp/Signature Detection
↓
Confidence Scoring
↓
Structured JSON Output
```

---

##  Tech Stack

- Python 3.13
- Tesseract OCR
- Pillow (PIL)
- Regex-based NLP
- Lightweight Computer Vision heuristics

---

##  Project Structure

```
document_ai_idfc/
│
├── dataset/ # Input images
├── sample_output/
│ └── result.json # Final output
│
├── utils/
│ ├── ocr_utils.py # OCR handling
│ ├── field_extractors.py # Dealer, model, HP, cost extraction
│ ├── vision_utils.py # Stamp & signature detection
│ └── confidence.py # Confidence scoring
│
├── config.py
├── executable.py # Main pipeline
└── README.md

```

---

##  Field Extraction Logic

### Dealer Name

- Keyword matching with normalization
- Handles spelling variants (Odisha / Orissa)

### Model Name

- Regex-based model pattern detection
- Robust to OCR noise

### Horse Power

- Extracted from contextual numeric patterns (e.g., `50 HP`)

### Asset Cost

- Supports Indian numbering format (e.g., `9,11,769`)
- Converts to clean integers

### Stamp & Signature

- Detected using bounding-box heuristics
- Independent detection for higher reliability

---

##  Confidence Scoring

Confidence score (0–1) is computed using:

- Number of extracted core fields
- Presence of stamp/signature
- Data completeness

This makes the output suitable for downstream automation.

---

##  Dataset Usage Explanation

Although the dataset contains ~500 images, a **small representative subset** was initially used for:

- Faster iteration
- Easier debugging
- Rule validation

Once validated, the **same pipeline was run on the entire dataset** without any code changes.

---

##  PDF Support

The current pipeline processes scanned document images (PNG/JPG).

Support for PDF documents can be seamlessly enabled by adding a lightweight PDF-to-image conversion
step using tools such as `pdf2image`. Once converted, each page is processed by the same OCR,
NLP, and Computer Vision pipeline **without any code changes**.

This design mirrors real-world Document AI systems where PDFs are normalized into images before
information extraction.

---

##  Installation & Setup

### Option A: Using the submitted ZIP file (Recommended)

1. Extract the submitted ZIP file.
2. Navigate to the project root directory:

```bash
cd document_ai_idfc
```

### Option B: Using GitHub

Clone the repository

```bash
git clone https://github.com/pritmehta/document-AI-for-financial-solution-
cd document_ai_idfc
```

### 1️⃣ Install Python dependencies

```bash
pip install pytesseract pillow
```

### 2️⃣ Install Tesseract OCR

Windows

- Download installer from:
  https://github.com/UB-Mannheim/tesseract/wiki

- Default installation path:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

Linux

```
sudo apt install tesseract-ocr
```

macOS

```
brew install tesseract
```

### 3️⃣ Configure Tesseract path (Windows only)

Update `utils/ocr_utils.py:`

```
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### 4️⃣ Run the pipeline

```
python executable.py
```

Output will be generated at:

```
sample_output/result.json
```

---

##  How to Run

1. Place images in the `dataset/` folder
2. Execute:

```bash
python executable.py
```

3. View results in:

```bash
sample_output/result.json
```

##  Sample Output

```
json
{
"doc_id": "172561841_pg1.png",
"fields": {
"dealer_name": "Odisha Agro Industries Corporation Ltd",
"model_name": "DI-745",
"horse_power": 50,
"asset_cost": 911769,
"signature": { "present": true },
"stamp": { "present": false }
},
"confidence": 1.0
}
```

##  Analysis & Insights

- Processing time per document is logged to enable performance benchmarking.
- Confidence scores expose extraction reliability and act as a proxy for error rate.
- Most extraction failures occur due to OCR noise, extreme layout variance, or missing fields.
- The modular design enables easy extension to visualization, EDA, and dashboards if metadata is available.

---

##  Error Analysis

Observed error categories include:

- OCR-induced spelling noise
- Missing or ambiguous fields
- Non-standard document layouts
- Poor scan quality

These are reflected in lowered confidence scores and null field outputs.

---

## Key Highlights

- Scales to hundreds of scanned documents
- Robust against OCR noise
- Produces clean structured output
- Confidence-aware extraction
- Hackathon and industry ready

---

## 🏁 Conclusion

This project demonstrates a practical, scalable, and production-oriented Document AI pipeline for financial document processing.
It bridges the gap between raw scanned data and trustworthy, machine-readable structured information.
