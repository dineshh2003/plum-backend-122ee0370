# AI-powered Backend with OCR and Text Processing

## 📌 Overview
This project provides a backend system that can process both **text** and **image** inputs:

- **Text input** → Analyze, transform (extract keywords), and validate.  
- **Image input** → Extract text with OCR (Tesseract), then analyze, transform, and validate.  
- **Chain-run** → Run a sequence of AI-inspired steps (`analysis → transform → validate`).  
- **Validation** → Enforce JSON schemas and guardrails.  

It includes:
- **FastAPI backend** with multiple endpoints (`/v1/process/text`, `/v1/process/image`, `/v1/chain-run`, `/v1/validate`).  
- **OCR integration** via Tesseract.  
- **Guardrails**: API key auth, input validation, structured error responses.  
- **Streamlit frontend** for demo (upload image, type text, view JSON responses).  

---

## 🚀 Live Demo

### Backend (FastAPI)
Primary API:  
👉 [https://plum-backend-122ee0370.onrender.com](https://plum-backend-122ee0370.onrender.com)

Interactive Docs:  
👉 [https://plum-backend-122ee0370.onrender.com/docs](https://plum-backend-122ee0370.onrender.com/docs)

### Frontend (Streamlit UI)
👉 [https://plum-streamlit-xxxxxx.onrender.com](https://plum-streamlit-xxxxxx.onrender.com)  
*(Replace with your actual Render URL)*

---

## ⚡ Features
- **OCR**: Extracts text from PNG/JPG using Tesseract.  
- **Text analysis**: Produces summaries.  
- **Keyword extraction**: Splits text into keywords.  
- **Validation**: JSON schema validation of input/output.  
- **Guardrails**: API key auth, PII masking (optional), structured logging.  
- **Streamlit UI**: Upload images, paste text, and view JSON outputs.

---

## 🔑 Authentication
Every request must include a header:

(You can change this via environment variables.)

---

## 📚 API Endpoints

### 1. Process Text
```bash
curl -s -X POST "https://plum-backend-122ee0370.onrender.com/v1/process/text" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-secret-key" \
  -d '{"input_id":"demo-1","text":"Hello from deployed backend"}'


curl -v -X POST "https://plum-backend-122ee0370.onrender.com/v1/process/image" \
  -H "X-API-KEY: demo-secret-key" \
  -F "input_id=img-1" \
  -F "image=@sample_requests/sample.jpg"


curl -s -X POST "https://plum-backend-122ee0370.onrender.com/v1/validate" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-secret-key" \
  -d '{"schema_name":"default","payload":{"a":1}}'


curl -s -X POST "https://plum-backend-122ee0370.onrender.com/v1/chain-run" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo-secret-key" \
  -d '{"chain":["analysis","transform","validate"],"input":{"text":"Quick test chain","input_id":"cr-1"}}'


🛠️ Local Setup
Prerequisites

Python 3.11+

pip & virtualenv

Tesseract OCR installed (apt-get install tesseract-ocr on Ubuntu/Debian)

Setup
git clone https://github.com/<your-username>/<your-repo>.git
cd backend-problems-5-8

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


🌐 Streamlit Frontend (local)

Run:

streamlit run streamlit_app.py --server.port 8501


🧪 Testing

Run tests with:

pytest -q


📝 Project Structure
.
├── app/
│   ├── api/
│   │   └── v1.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   └── ocr.py
│   └── main.py
├── sample_requests/
│   └── sample.jpg
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
└── README.md


👤 Author

Dinesh Jangid
Backend Assignment Problems 


---