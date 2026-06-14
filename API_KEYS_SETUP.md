# 🔑 API Keys Setup

### 1. Firebase Database (Required for Production)
```bash
# 1. Go to https://console.firebase.google.com/
# 2. Create project → Enable Firestore → Production mode
# 3. Get service account key → Save as backend/firebase-credentials.json
```

### 2. Free AI Chatbot (Choose ONE - No Credit Card!)

#### Groq (Recommended)
```bash
# 1. Go to https://console.groq.com/
# 2. Sign up → Get API key
# 3. Add to backend/.env: GROQ_API_KEY=gsk_your_key_here
```

#### HuggingFace (Also Free)
```bash
# 1. Go to https://huggingface.co/settings/tokens
# 2. Sign up → Create token
# 3. Add to backend/.env: HUGGINGFACE_API_KEY=hf_your_token_here
```

### 3. Complete Environment (`backend/.env`)
```env
# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
JWT_SECRET=your_jwt_secret_32_chars_minimum
ENCRYPTION_KEY=your_encryption_key_here

# Free AI (choose one)
GROQ_API_KEY=gsk_your_actual_api_key_here
# OR
# HUGGINGFACE_API_KEY=hf_your_actual_token_here

# Production
DEBUG=false
ENVIRONMENT=production
```

### 4. Test Setup
```bash
python test_free_ai.py
```

### 5. Frontend (`frontend/.env.production`)
```env
VITE_API_PROXY=https://your-backend-url.com
```

🚀 Ready to deploy!
