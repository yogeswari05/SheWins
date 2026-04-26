from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.config import get_settings
from app.dependencies import get_user_id
from app.models.schemas import ChatMessageIn
from app.services import db
from app.services.free_ai_chat import free_ai_chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

SYSTEM = """You are a supportive menstrual health and PCOS/PCOD awareness assistant for a privacy-first app.
Give general education only — never diagnose. Encourage users to see qualified clinicians.
Be concise, empathetic, and clear. If asked for medical treatment, say you cannot provide diagnosis or prescriptions."""


@router.post("/message")
async def chat_message(
    body: ChatMessageIn, user_id: str = Depends(get_user_id)
):
    db.ensure_user(user_id)
    s = get_settings()
    
    # Try free AI services first
    try:
        response = await free_ai_chat_service.chat(body.message, body.language)
        if response:
            return {
                "reply": response["response"],
                "model": response.get("model", "free_ai"),
                "source": response.get("source", "free_ai_service")
            }
    except Exception as e:
        print(f"Free AI service failed: {e}")
    
    # Fallback to paid services if configured
    if s.anthropic_api_key:
        return await _anthropic(body, s)
    if s.openai_api_key:
        return await _openai(body, s)
    
    # Final fallback
    return {
        "reply": (
            "The AI service is not configured. Set GROQ_API_KEY or HUGGINGFACE_API_KEY "
            "for free AI service, or ANTHROPIC_API_KEY/OPENAI_API_KEY for paid services. "
            "For now: consider tracking cycle length, symptoms, and "
            "discussing persistent irregularity with a gynecologist."
        ),
        "model": "local_fallback",
        "source": "rule_based"
    }


async def _anthropic(body: ChatMessageIn, s) -> dict:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": s.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    language_note = f" Prefer responding in the user's language/locale: {body.language!r} if appropriate."
    payload = {
        "model": s.anthropic_model,
        "max_tokens": 800,
        "system": SYSTEM + language_note,
        "messages": [{"role": "user", "content": body.message}],
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, headers=headers, json=payload)
    if r.status_code >= 400:
        raise HTTPException(502, r.text)
    data = r.json()
    text = ""
    for b in data.get("content", []):
        if b.get("type") == "text":
            text += b.get("text", "")
    return {"reply": text.strip(), "model": s.anthropic_model}


async def _openai(body: ChatMessageIn, s) -> dict:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {s.openai_api_key}",
        "Content-Type": "application/json",
    }
    language_note = f" Prefer responding in locale: {body.language!r} if appropriate."
    payload = {
        "model": s.openai_model,
        "messages": [
            {"role": "system", "content": SYSTEM + language_note},
            {"role": "user", "content": body.message},
        ],
        "max_tokens": 800,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, headers=headers, json=payload)
    if r.status_code >= 400:
        raise HTTPException(502, r.text)
    data = r.json()
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        text = str(data)
    return {"reply": text.strip(), "model": s.openai_model}
