from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import (
    analytics,
    auth,
    chat,
    cycles,
    demo,
    insights,
    predict,
    reminders,
    reports,
    user,
    wellness,
)

app = FastAPI(
    title="Elite Her — Smart Period & PCOD API",
    version="1.0.0",
    description="Privacy-first cycle tracking, PCOD/PCOS risk heuristics, LSTM-style predictions, and AI chat.",
)
s = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=s.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(cycles.router)
app.include_router(predict.router)
app.include_router(analytics.router)
app.include_router(chat.router)
app.include_router(reports.router)
app.include_router(reminders.router)
app.include_router(user.router)
app.include_router(insights.router)
app.include_router(demo.router)
app.include_router(wellness.router)


# Auto-setup demo data on startup
@app.on_event("startup")
async def startup_event():
    """Set up demo data automatically on startup."""
    try:
        from app.services.demo_data import setup_demo_data
        print("🔄 Starting demo data setup...")
        result = setup_demo_data()
        print(f"🎉 Demo data setup complete: {result['summary']}")
        
        # Show detailed results
        total_users = result.get('total_users', 0)
        total_cycles = sum(r.get('cycles_created', 0) for r in result.get('details', {}).values())
        print(f"📊 Created {total_users} users with {total_cycles} cycles")
        
    except Exception as e:
        print(f"⚠️ Demo data setup failed: {e}")
        import traceback
        print("🔍 Full error details:")
        traceback.print_exc()


@app.get("/api/health")
def health():
    return {"ok": True, "service": "elite-her"}


@app.get("/api/insights/summary")
def insights_summary():
    return {
        "app": "Elite Her",
        "privacy": [
            "Field-level optional AES-256 (Fernet) for sensitive user strings when ENCRYPTION_KEY is set",
            "Firestore or local in-memory store; no data selling (configure your own project)",
        ],
    }
