# 🚀 How to Run LegalEagle

## Quick Start (Easiest Method)

### Option 1: Using Setup Script (Recommended)

```bash
# Step 1: Run the setup script
./setup.sh

# Step 2: Edit .env file and add your OpenAI API key
# Open .env in a text editor and replace:
# OPENAI_API_KEY=your_openai_api_key_here
# with your actual API key

# Step 3: Run the app
./run.sh
```

### Option 2: Manual Setup

```bash
# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Step 3: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Create .env file
cp env_template.txt .env

# Step 5: Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-key-here

# Step 6: Run the app
streamlit run app.py
```

## Detailed Instructions

### 1. Prerequisites

- **Python 3.8 or higher** - Check with: `python3 --version`
- **OpenAI API Key** - Get one from: https://platform.openai.com/api-keys
- **Internet connection** (for API calls)

### 2. Get Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)
6. **Important:** Save it somewhere safe - the key is free with generous limits!

### 3. Configure Environment Variables

Edit the `.env` file and add your API key:

```env
GROQ_API_KEY=gsk-your-actual-key-here
VECTOR_STORE_TYPE=faiss
LLM_MODEL=llama-3.3-70b-versatile
```

**Note:** For local testing, use `faiss` (default). For production or cloud storage, you can use `pinecone` (requires additional setup).

### 4. Install Dependencies

The setup script does this automatically, but if you're doing it manually:

```bash
pip install -r requirements.txt
```

This installs:
- LangChain (RAG framework)
- OpenAI (LLM and embeddings)
- FAISS (local vector store)
- Streamlit (web UI)
- PyPDF2 (PDF processing)
- Other dependencies

### 5. Run the Application

```bash
streamlit run app.py
```

You should see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

The app will automatically open in your browser, or you can manually visit http://localhost:8501

## Using the App

1. **Upload Documents:**
   - Click "Browse files" in the sidebar
   - Select one or more PDF contract files
   - Click "Process Documents"
   - Wait for processing to complete (may take 30-60 seconds)

2. **Ask Questions:**
   - Type your question in the search box
   - Click "Search" or press Enter
   - View the answer with page citations
   - Expand "View Source Excerpts" to see the source material

## Troubleshooting

### ❌ "Groq API key not found"
**Solution:**
- Make sure `.env` file exists
- Check that `GROQ_API_KEY=gsk-...` is in the file
- Ensure no extra spaces or quotes around the key
- Restart the app after editing `.env`
- Get your free key from: https://console.groq.com/

### ❌ "ModuleNotFoundError" or Import Errors
**Solution:**
```bash
source venv/bin/activate  # Make sure venv is activated
pip install -r requirements.txt  # Reinstall dependencies
```

### ❌ "streamlit: command not found"
**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment first
pip install streamlit
```

### ❌ Port 8501 already in use
**Solution:**
```bash
# Option 1: Use a different port
streamlit run app.py --server.port 8502

# Option 2: Kill the process using port 8501
lsof -ti:8501 | xargs kill
```

### ❌ PDF processing fails
**Solution:**
- Make sure the PDF is not password-protected
- Check that the PDF contains readable text (not just images)
- Try a different PDF file

### ❌ "Error reading PDF"
**Solution:**
- Ensure the PDF file is not corrupted
- Try opening the PDF in a PDF viewer first
- Some scanned PDFs may need OCR processing

## System Requirements

- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** ~500MB for dependencies
- **Internet:** Required for OpenAI API calls
- **Browser:** Modern browser (Chrome, Firefox, Safari, Edge)

## What Happens When You Run the App?

1. **Startup:** Streamlit loads the web interface
2. **Initialization:** The app checks for API keys and configuration
3. **Ready:** You can upload PDFs and start querying

## Next Steps After Running

1. Upload a sample NDA or contract PDF
2. Ask questions like:
   - "What is the termination clause?"
   - "What are the confidentiality obligations?"
   - "What is the dispute resolution process?"

## Need Help?

- Check the `README.md` for more details
- Review the `QUICKSTART.md` for condensed instructions
- Verify your `.env` file has the correct API key

---

**Happy querying! ⚖️**

