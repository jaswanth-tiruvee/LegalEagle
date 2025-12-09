# Quick Start Guide

## 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configure API Keys

```bash
# Copy the environment template
cp env_template.txt .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk-your-key-here
```

**Get your free Groq API key:** https://console.groq.com/

**Minimum required:** Groq API key (free)

**Optional:** Pinecone credentials (if using cloud vector store instead of FAISS)

## 3. Run the Application

```bash
streamlit run app.py
```

Or use the quick launcher:
```bash
./run.sh
```

## 4. Use the Application

1. Upload PDF contract(s) in the sidebar
2. Click "Process Documents"
3. Ask questions about the contracts
4. Get answers with page citations!

## Example Questions

- "What is the termination clause?"
- "What are the confidentiality obligations?"
- "What is the dispute resolution process?"
- "What are the payment terms?"

## Troubleshooting

### Issue: "Groq API key not found"
- Make sure you created a `.env` file with `GROQ_API_KEY=your_key`
- Get your key from: https://console.groq.com/

### Issue: "ModuleNotFoundError"
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using Python 3.8+

### Issue: "Model not found" or "Model decommissioned"
- Check available models at: https://console.groq.com/docs/models
- Update `LLM_MODEL` in `.env` to a current model like `llama-3.3-70b-versatile`

## System Information

- **LLM:** Groq (Free & Fast)
- **Embeddings:** HuggingFace Sentence Transformers (Free, Local)
- **Vector Store:** FAISS (Local, Free)
- **No costs required!**
