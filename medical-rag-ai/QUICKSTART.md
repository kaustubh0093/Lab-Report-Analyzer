# AI Medical Report Analyzer - Quickstart Guide

This guide will help you set up and run the AI Medical Report Analyzer locally. The project uses FastAPI for the backend, Streamlit for the frontend, and Google's Gemini models for AI analysis.

## Prerequisites

- **Python 3.9+** installed.
- **Git** installed.
- **Google API Key** for Gemini models.
- (Optional) **CUDA-capable GPU** for faster local embeddings and OCR (though CPU works too).

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd medical-rag-ai
```

### 2. Create and Activate Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dimensions

Install the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1.  Copy the example `.env` file (or create one directly).
2.  Open `.env` in a text editor.
3.  Add your **Google API Key**.

**Example `.env` file:**

```env
APP_NAME="Medical RAG AI"
API_VERSION="v1"
SECRET_KEY="supersecretkey"
HF_AUTH_TOKEN=""
OPENAI_API_KEY="" 
GOOGLE_API_KEY="your_google_ai_studio_api_key_here"
VECTOR_DB_PATH="vectorstore/index"
```

*Note: The system is configured to use `gemini-2.5-flash` by default. You can change this in `backend/config.py` if needed.*

## Running the Application

You need to run both the Backend (API) and the Frontend (UI). It is best to use two separate terminal windows/tabs.

### Step 1: Start the Backend (FastAPI)

1.  Open a new terminal.
2.  Navigate to the project root (`medical-rag-ai`).
3.  Activate your virtual environment.
4.  Run the backend server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will start at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### Step 2: Start the Frontend (Streamlit)

1.  Open a second terminal.
2.  Navigate to the project root (`medical-rag-ai`).
3.  Activate your virtual environment.
4.  Run the Streamlit app:

```bash
streamlit run frontend/app.py
```

The application will likely open automatically in your browser at `http://localhost:8501`.

## Usage

1.  **Upload**: Click on the upload area to select a Medical Lab Report (Image or PDF).
2.  **Process**: The system will automatically OCR the document to extract text.
3.  **Analyze**: Click the "Analyze Report" button.
4.  **Results**:
    *   **Summary**: A quick overview of the findings.
    *   **Detailed Analysis**: Detailed breakdown of each test result, compared against standard ranges.
    *   **Recommendations**: AI-generated follow-up suggestions (Consult your doctor!).

## Troubleshooting

-   **OCR Errors**: If you get errors related to 'trocr', ensure you have a stable internet connection for the first run as it downloads the model from HuggingFace.
-   **API Key Errors**: Double-check your `GOOGLE_API_KEY` in the `.env` file. Ensure it has permissions for `gemini-2.5-flash`.
-   **Dependencies**: If you encounter `ModuleNotFoundError`, try running `pip install -r requirements.txt` again.
