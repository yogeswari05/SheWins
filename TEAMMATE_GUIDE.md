# SheWins Application Guide for New Team Members

## Overview
SheWins is a comprehensive menstrual health and wellness companion app that helps women track their cycles, receive AI-powered health guidance, and understand their body patterns with privacy-first design.

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Routing**: React Router v6
- **UI Framework**: TailwindCSS with custom glass morphism design
- **State Management**: React Context (AuthContext, ThemeContext)
- **Internationalization**: react-i18next (English, Hindi, Telugu)
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy with SQLite
- **ML Libraries**: TensorFlow, scikit-learn, numpy, pandas
- **Authentication**: Session-based with JWT tokens
- **API Documentation**: OpenAPI/Swagger

---

## 🎯 Core Features

### 1. User Authentication & Onboarding
- **Signup/Login**: Email-based authentication with secure password handling
- **Demo Accounts**: Pre-populated demo users for testing
  - `demo@eliteher.com` / `demo123456` - 17 months of realistic data
  - `sarah@eliteher.com` / `sarah123456` - Regular user data
  - `maya@eliteher.com` / `maya123456` - Minimal data for edge cases

### 2. Landing Page (Public)
- **Modern Design**: Dark/light theme support with bubble cursor effects
- **Navigation**: Features, FAQs, About Diseases sections
- **CTA**: Get Started Free and Explore Features buttons
- **Responsive**: Mobile-first design with glass morphism effects

### 3. Dashboard (Today Page)
- **Wellness Score**: Comprehensive 0-100 score based on:
  - Sleep patterns (25% weight)
  - Stress levels (25% weight) 
  - Exercise habits (20% weight)
  - Mood stability (15% weight)
  - Symptom patterns (10% weight)
  - Cycle regularity (5% weight)
- **Health Risk Score**: PCOS risk assessment with recommendations
- **Cycle Predictions**: ML-powered predictions for next 3 cycles
- **Alerts**: Personalized health alerts and reminders

### 4. Period Tracking
- **Cycle Logging**: Start/end dates, flow intensity, symptoms
- **Symptom Tracking**: 20+ symptoms with severity levels
- **Mood Tracking**: Daily mood with emotional states
- **Sleep & Exercise**: Hours of sleep and activity levels
- **Stress Levels**: 1-10 scale with contextual factors
- **Personal Notes**: Free-text journaling for each cycle

### 5. Analytics & Insights
- **Six-Month Heatmap**: Visual cycle patterns with monthly breakdown
- **Trend Analysis**: Cycle length, symptom, and mood trends
- **Pattern Recognition**: AI-identified patterns and correlations
- **Health Metrics**: Comprehensive wellness indicators
- **Export Reports**: PDF reports for healthcare providers

### 6. AI Health Assistant
- **Natural Language**: ChatGPT-like conversational interface
- **Contextual Responses**: AI responses based on user's cycle data
- **Health Guidance**: Personalized advice and recommendations
- **Pattern Insights**: AI-powered pattern explanations

### 7. Reminders System
- **Period Reminders**: Customizable notifications before expected periods
- **Symptom Check-ins**: Daily prompts for symptom tracking
- **Weekly Insights**: Summarized wellness reports
- **Health Tips**: Personalized health recommendations

### 8. Settings & Preferences
- **Language Support**: English, Hindi, Telugu
- **Theme Selection**: Dark/light mode with system preference
- **Privacy Controls**: Data sharing and analytics preferences
- **Notification Settings**: Granular control over all notifications

---

## 🤖 Machine Learning Components

### 1. Cycle Prediction Engine
- **Algorithm**: LSTM neural network with TensorFlow
- **Input Features**: 
  - Historical cycle lengths
  - Symptom patterns
  - Stress levels
  - Sleep patterns
  - Exercise data
- **Output**: Next 3 cycle predictions with confidence intervals
- **Accuracy**: 85-92% confidence based on data quality

### 2. Wellness Score Calculator
- **Multi-factor Analysis**: Weighted scoring system
- **Statistical Methods**: Standard deviation, trend analysis
- **Normalization**: Min-max scaling for consistent scoring
- **Trend Detection**: Comparative analysis over time periods

### 3. PCOS Risk Assessment
- **Heuristic Algorithm**: Rule-based risk scoring
- **Risk Factors**:
  - Cycle irregularity (>35 days)
  - Heavy periods (>7 days)
  - High stress levels
  - Symptom clusters (acne, hair growth, weight gain)
- **Output**: Risk score (0-100) with severity levels

### 4. Stress Analysis Engine
- **Multi-dimensional Scoring**: Sleep, exercise, mood, cycle factors
- **Pattern Recognition**: Identify stress triggers
- **Recommendation Engine**: Personalized stress management tips

### 5. Symptom Pattern Analysis
- **Clustering**: K-means for symptom grouping
- **Correlation Analysis**: Pearson correlation between symptoms
- **Predictive Modeling**: Forecast symptom severity

---

## 🏗️ Application Architecture

### Frontend Structure
```
src/
├── components/          # Reusable UI components
│   ├── GlassCard.tsx   # Glass morphism card component
│   ├── BubbleCursor.tsx # Interactive bubble effects
│   ├── LoadingSkeleton.tsx # Loading states
│   └── ...
├── context/            # React contexts
│   ├── AuthContext.tsx # Authentication state
│   └── ThemeContext.tsx # Theme management
├── pages/              # Page components
│   ├── Home.tsx        # Dashboard
│   ├── Analytics.tsx   # Analytics page
│   ├── Track.tsx       # Period tracking
│   ├── Chat.tsx        # AI assistant
│   └── Settings.tsx    # User settings
├── lib/                # Utilities
│   ├── api.ts          # API client
│   └── report.ts       # PDF generation
└── translations/       # i18n files
```

### Backend Structure
```
backend/
├── app/
│   ├── routers/        # API endpoints
│   │   ├── auth.py     # Authentication
│   │   ├── cycles.py   # Cycle management
│   │   ├── analytics.py # Analytics data
│   │   ├── wellness.py # Wellness scoring
│   │   └── insights.py # AI insights
│   ├── services/       # Business logic
│   │   ├── wellness_predictor.py # Wellness scoring
│   │   ├── stress_analyzer.py # Stress analysis
│   │   ├── mood_predictor.py # Mood patterns
│   │   └── symptom_manager.py # Symptom tracking
│   ├── models/         # Database models
│   └── dependencies.py # Dependency injection
└── ml_models/          # Trained ML models
```

---

## 🔄 User Flow

### New User Journey
1. **Landing Page** → Learn about features
2. **Signup** → Create account with email
3. **Onboarding** → Set preferences and language
4. **Dashboard** → View wellness overview
5. **First Cycle** → Log initial period data
6. **Analytics** → Explore patterns over time
7. **AI Chat** → Get personalized guidance

### Daily User Flow
1. **Dashboard Check** → Review wellness score and alerts
2. **Symptom Logging** → Track daily symptoms and mood
3. **Analytics Review** → Check patterns and trends
4. **AI Interaction** → Ask questions and get insights
5. **Settings Management** → Adjust preferences as needed

---

## 🔧 Development Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- SQLite

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### Environment Variables
```env
# Backend (.env)
DATABASE_URL=sqlite:///./eliteher.db
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Frontend (.env)
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Testing & Demo Data

### Demo Users
The application includes pre-populated demo data for comprehensive testing:

1. **demo@eliteher.com** - 17 months of realistic data including:
   - Progressive health journey (normal → concerning → improving)
   - PCOS risk indicators
   - Various symptom patterns
   - Treatment response patterns

2. **sarah@eliteher.com** - Regular user with stable patterns

3. **maya@eliteher.com** - Minimal data for edge case testing

### Test Scenarios
- **New Users**: Empty data handling
- **Regular Users**: Pattern recognition
- **High-Risk Users**: PCOS detection
- **Edge Cases**: Division by zero, missing data
- **Performance**: Large datasets, concurrent users

---

## 🎨 Design System

### Visual Identity
- **Primary Colors**: Rose-to-violet gradient
- **Design Language**: Glass morphism with backdrop blur
- **Typography**: Modern sans-serif with gradient text
- **Animations**: Smooth transitions and micro-interactions

### Component Library
- **GlassCard**: Reusable glass morphism container
- **LoadingSkeleton**: Animated loading states
- **BubbleCursor**: Interactive visual effects
- **AmbientBackground**: Dynamic background gradients

### Responsive Design
- **Mobile First**: 320px breakpoint
- **Tablet**: 768px breakpoint
- **Desktop**: 1024px breakpoint
- **Large Desktop**: 1440px+ breakpoint

---

## 🔒 Security & Privacy

### Data Protection
- **Encryption**: All sensitive data encrypted at rest
- **Authentication**: JWT tokens with expiration
- **Session Management**: Secure session handling
- **Privacy Controls**: User-controlled data sharing

### HIPAA Considerations
- **No Medical Diagnosis**: Clear disclaimer about non-medical nature
- **Data Anonymization**: Optional data sharing without personal info
- **User Consent**: Explicit consent for data usage
- **Export Rights**: Users can export and delete their data

---

## 📊 Analytics & Monitoring

### User Analytics
- **Wellness Trends**: Population-level wellness patterns
- **Feature Usage**: Most used features and workflows
- **Retention Metrics**: User engagement over time
- **Error Tracking**: Frontend and backend error monitoring

### Performance Metrics
- **API Response Times**: <200ms average
- **ML Model Inference**: <100ms for predictions
- **Database Queries**: Optimized with indexing
- **Frontend Performance**: <2s initial load

---

## 🚀 Deployment

### Development Environment
- **Frontend**: Vite dev server with HMR
- **Backend**: Uvicorn with auto-reload
- **Database**: SQLite for local development

### Production Environment
- **Frontend**: Static hosting (Vercel/Netlify)
- **Backend**: Docker containers
- **Database**: PostgreSQL for production
- **ML Models**: Pre-trained models loaded at startup

---

## 🤝 Contributing Guidelines

### Code Standards
- **TypeScript**: Strict mode enabled
- **ESLint**: Airbnb configuration
- **Prettier**: Consistent formatting
- **Git Hooks**: Pre-commit linting and testing

### Feature Development
1. **Create Feature Branch**: `git checkout -b feature/new-feature`
2. **Frontend First**: Build UI components
3. **Backend Integration**: Add API endpoints
4. **Testing**: Unit and integration tests
5. **Documentation**: Update README and comments
6. **PR Review**: Code review before merge

### Testing Strategy
- **Unit Tests**: Jest for frontend, pytest for backend
- **Integration Tests**: API endpoint testing
- **E2E Tests**: Critical user journeys
- **ML Testing**: Model accuracy and performance

---

## 📚 Key Resources

### Documentation
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Component Library**: Storybook (if available)
- **Database Schema**: SQLAlchemy models documentation

### Communication
- **Daily Standups**: Progress and blockers
- **Sprint Planning**: Feature prioritization
- **Retrospectives**: Process improvements

### Learning Resources
- **React Documentation**: https://react.dev
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **TailwindCSS**: https://tailwindcss.com
- **TensorFlow**: https://tensorflow.org

---

## 🎯 Quick Start Tasks for New Team Member

### Day 1: Setup & Exploration
1. Set up development environment
2. Run the application locally
3. Explore demo user accounts
4. Review the codebase structure

### Day 2: Feature Deep Dive
1. Understand the wellness scoring algorithm
2. Review the ML prediction models
3. Test the analytics dashboard
4. Explore the AI chat functionality

### Day 3: Code Contribution
1. Fix a small bug or improvement
2. Add a new feature or enhancement
3. Write tests for your changes
4. Submit your first pull request

### Week 1: Integration
1. Understand the deployment pipeline
2. Review monitoring and analytics
3. Learn about the ML model training process
4. Contribute to documentation

---

## 🆘 Common Issues & Solutions

### Frontend Issues
- **Object Rendering Error**: Check data structure matches TypeScript types
- **API Errors**: Verify backend is running and CORS is configured
- **Theme Issues**: Check ThemeContext provider wrapping
- **Translation Issues**: Verify i18n configuration

### Backend Issues
- **Database Errors**: Check migration status and connection
- **ML Model Errors**: Verify model files exist and are loaded
- **Authentication Issues**: Check JWT configuration
- **Performance Issues**: Monitor database query performance

### Development Tips
- **Hot Reload**: Both frontend and backend support hot reload
- **Demo Data**: Use demo accounts for comprehensive testing
- **API Testing**: Use Swagger UI for endpoint testing
- **Error Handling**: Check browser console and backend logs

---

Welcome to the SheWins team! 🎉 We're excited to have you contribute to this important women's health platform. Don't hesitate to ask questions and suggest improvements!
