# SheWins - Smart Women's Health Platform

AI-powered menstrual health tracking with PCOD risk detection, stress analysis, and gamification.

## Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
copy .env.example .env
python run_dev.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Backend runs at `http://127.0.0.1:8000`
Frontend runs at `http://127.0.0.1:5173`

## Production Setup

## ✨ Features

### Core Health Tracking
- Smart cycle tracking with date validation alerts
- Custom symptom management (150+ symptoms)
- Enhanced mood tracking with emojis
- AI-powered stress analysis
- Free AI health chatbot
- Advanced LSTM-based cycle predictions
- PCOD risk detection and insights

### Advanced Features
- Gamification (wellness score)
- Anonymous community insights and comparisons
- Doctor-friendly PDF reports
- Smart reminders and notifications
- Multi-language support

### Production Features
- Secure authentication (JWT)
- Data encryption (AES-256)
- Firebase persistent database
- Production-ready deployment

## Train LSTM model
```bash
python train_lstm.py
```

## Project Structure

```text
SheWins/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── services/        # AI, analytics, gamification
│   │   ├── routers/         # API endpoints
│   │   └── models/          # Data models
│   ├── models/              # LSTM model files
│   └── firebase-credentials.json
├── frontend/                # React frontend
│   └── src/
│       ├── pages/           # React components
│       └── components/      # UI components
├── API_KEYS_SETUP.md        # Production setup guide
└── test_free_ai.py          # AI testing script
```

## 🤖 AI Features

- **Free AI Chatbot**: Groq or HuggingFace (no credit card required)
- **LSTM Predictions**: Advanced cycle pattern analysis
- **Stress Analysis**: Multi-factor stress scoring
- **Health Insights**: Personalized recommendations

### Advanced Features
- **Ensemble Prediction System:** 6 algorithms combined with intelligent voting
- **Advanced Feature Engineering:** 11 features extracted for pattern recognition
- **Adaptive Confidence Scoring:** 6 factors for reliability assessment
- **Enhanced LSTM Architecture:** Multi-feature input with improved training

### Novel Features
- **Multi-factor AI Analysis:** Comprehensive health scoring
- **Gamification System:** Points, badges, achievements, leaderboard
- **Community Insights:** Anonymous peer comparisons
- **Intelligent Symptom Management:** 150+ symptoms with PCOD risk correlation
- **Enhanced Predictions:** LSTM with pattern recognition and confidence scoring

---

**SheWins - Empowering Women's Health Through AI** 💪✨
