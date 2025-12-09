# 🚀 Deployment Guide for LegalEagle

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

### Prerequisites
1. GitHub repository (already done ✅)
2. Streamlit Cloud account (free at https://share.streamlit.io/)

### Steps:

1. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Deploy your app:**
   - Click "New app"
   - Select your repository: `jaswanth-tiruvee/LegalEagle`
   - Branch: `main`
   - Main file path: `app.py`

3. **Configure Secrets:**
   - In the app settings, go to "Secrets"
   - Add your Groq API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

4. **Advanced Settings (Optional):**
   - Python version: 3.11
   - Dependencies: `requirements.txt`

5. **Deploy:**
   - Click "Deploy"
   - Wait for the build to complete (first time may take 5-10 minutes for model downloads)

### Important Notes:
- ⚠️ HuggingFace models will be downloaded on first run (~100MB)
- ⚠️ FAISS indices are stored in memory (not persistent between sessions)
- ✅ Free tier includes 1GB RAM and unlimited apps

---

## Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Then deploy to:
- **Railway**: https://railway.app/
- **Render**: https://render.com/
- **Fly.io**: https://fly.io/
- **AWS/GCP/Azure**: Using container services

---

## Option 3: Local Deployment with ngrok (Testing)

For testing before cloud deployment:

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Run your app
streamlit run app.py

# In another terminal
ngrok http 8501
```

---

## Environment Variables for Cloud Deployment

Add these as secrets/environment variables:

```env
GROQ_API_KEY=gsk_your_key_here
VECTOR_STORE_TYPE=faiss
LLM_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## Troubleshooting Cloud Deployment

### Issue: App crashes on startup
- Check that all dependencies are in `requirements.txt`
- Verify API keys are set in secrets
- Check logs in Streamlit Cloud dashboard

### Issue: Model download timeout
- HuggingFace models download on first run
- Consider using smaller models or pre-downloading

### Issue: Memory errors
- FAISS stores vectors in memory
- Consider using Pinecone for production (has free tier)
- Reduce CHUNK_SIZE or TOP_K_RESULTS in config

---

## Recommended: Streamlit Cloud

✅ **Easiest deployment**
✅ **Free tier available**
✅ **Automatic HTTPS**
✅ **GitHub integration**
✅ **One-click deployment**

Get started: https://share.streamlit.io/

