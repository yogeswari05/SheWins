"""Run API with host/port from .env (avoids Windows reserved ranges like 8000)."""
from __future__ import annotations

import uvicorn

from app.config import get_settings

if __name__ == "__main__":
    s = get_settings()
    uvicorn.run(
        "app.main:app",
        host=s.api_host,
        port=s.api_port,
        reload=True,
    )
