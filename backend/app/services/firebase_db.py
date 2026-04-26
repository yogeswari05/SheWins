"""
Firebase-only database service for EliteHer.
No in-memory fallbacks - Firebase is mandatory.
"""
from __future__ import annotations

import hashlib
import uuid as _uuid_module
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.config import get_settings
from app.services import encryption

try:
    import firebase_admin  # type: ignore
    from firebase_admin import credentials, firestore  # type: ignore
except Exception as e:
    raise RuntimeError("Firebase SDK not installed. Run: pip install firebase-admin") from e


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class UserDoc:
    id: str
    email: str = ""
    email_hash: str = ""
    password_hash: str = ""
    display_name_enc: str = ""
    created_at: str = field(default_factory=_now_iso)
    locale: str = "en"
    settings: Dict[str, Any] = field(default_factory=dict)
    opt_in_analytics: bool = False


# Global Firebase client
_fs_client: Any = None


def _get_firestore_client():
    """Get Firebase client (mandatory)."""
    global _fs_client
    if _fs_client is not None:
        return _fs_client
    
    path = get_settings().firebase_credentials_path
    if not path or not str(path).strip():
        raise RuntimeError("Firebase credentials not configured. Set FIREBASE_CREDENTIALS_PATH in .env")
    
    try:
        firebase_admin.get_app()  # type: ignore
    except ValueError:
        cred = credentials.Certificate(path)  # type: ignore
        firebase_admin.initialize_app(cred)  # type: ignore
    
    _fs_client = firestore.client()  # type: ignore
    return _fs_client


# --- User Functions ---

def ensure_user(
    user_id: Optional[str], email: Optional[str] = None, locale: str = "en"
) -> str:
    """Create or ensure user exists in Firebase."""
    uid = user_id or str(_uuid_module.uuid4())
    em = (email or "").lower().encode()
    h = hashlib.sha256(em).hexdigest() if em else ""
    
    client = _get_firestore_client()
    ref = client.collection("users").document(uid)
    snap = ref.get()
    if not snap.exists:
        ref.set(
            {
                "email_hash": h,
                "created_at": _now_iso(),
                "locale": locale,
                "settings": {},
                "opt_in_analytics": False,
            }
        )
    return uid


def _sanitize_user_dict(d: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    out = {**d, "id": user_id}
    out.pop("password_hash", None)
    # Return decrypted display name for UI; keep encrypted value private.
    dn = out.pop("display_name_enc", "")
    if isinstance(dn, str) and dn:
        out["display_name"] = encryption.maybe_decrypt_str(dn) or dn
    return out


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user from Firebase."""
    client = _get_firestore_client()
    snap = client.collection("users").document(user_id).get()
    if not snap.exists:
        return None
    d = snap.to_dict() or {}
    return _sanitize_user_dict(dict(d), user_id)


def find_user_by_email(email: str) -> Optional[tuple[str, str]]:
    """Return (user_id, password_hash) for login, or None."""
    em = email.strip().lower()
    client = _get_firestore_client()
    col = client.collection("users")
    for doc in col.where("email", "==", em).limit(1).stream():
        d = doc.to_dict() or {}
        return (doc.id, str(d.get("password_hash") or ""))
    return None


def create_registered_user(
    email: str, password_hash: str, display_name: str = "", locale: str = "en"
) -> str:
    em = email.strip().lower()
    if find_user_by_email(em):
        raise ValueError("email_taken")
    uid = str(_uuid_module.uuid4())
    h = hashlib.sha256(em.encode()).hexdigest()
    client = _get_firestore_client()
    client.collection("users").document(uid).set(
        {
            "email": em,
            "email_hash": h,
            "password_hash": password_hash,
            "display_name_enc": encryption.maybe_encrypt_str(display_name) if display_name else "",
            "created_at": _now_iso(),
            "locale": locale,
            "settings": {},
            "opt_in_analytics": False,
        }
    )
    return uid


def update_user_settings(user_id: str, settings: Dict[str, Any]) -> None:
    client = _get_firestore_client()
    client.collection("users").document(user_id).set(
        {"settings": settings}, merge=True
    )


def merge_user_data(user_id: str, data: Dict[str, Any]) -> None:
    client = _get_firestore_client()
    client.collection("users").document(user_id).set(data, merge=True)


# --- Cycle Functions ---

def _sanitize_cycle_dict(c: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(c)
    notes = out.get("notes")
    if isinstance(notes, str) and notes:
        out["notes"] = encryption.maybe_decrypt_str(notes) or notes
    return out


def _prepare_cycle_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(payload)
    n = out.get("notes")
    if isinstance(n, str) and n:
        out["notes"] = encryption.maybe_encrypt_str(n)
    return out


def list_cycles(user_id: str) -> List[Dict[str, Any]]:
    client = _get_firestore_client()
    col = (
        client.collection("users")
        .document(user_id)
        .collection("cycles")
        .order_by("start_date", direction=firestore.Query.DESCENDING)
    )
    return [_sanitize_cycle_dict({**c.to_dict(), "id": c.id}) for c in col.stream()]


def create_cycle(user_id: str, payload: Dict[str, Any]) -> str:
    cid = str(_uuid_module.uuid4())
    prev_start = payload.get("previous_cycle_start")
    body = {
        **_prepare_cycle_payload(payload),
        "id": cid,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    client = _get_firestore_client()
    (
        client.collection("users")
        .document(user_id)
        .collection("cycles")
        .document(cid)
    ).set(body)
    return cid


def update_cycle(user_id: str, cycle_id: str, payload: Dict[str, Any]) -> bool:
    payload = {**_prepare_cycle_payload(payload), "updated_at": _now_iso()}
    client = _get_firestore_client()
    ref = (
        client.collection("users")
        .document(user_id)
        .collection("cycles")
        .document(cycle_id)
    )
    snap = ref.get()
    if not snap.exists:
        return False
    ref.set(payload, merge=True)
    return True


def delete_cycle(user_id: str, cycle_id: str) -> bool:
    client = _get_firestore_client()
    ref = (
        client.collection("users")
        .document(user_id)
        .collection("cycles")
        .document(cycle_id)
    )
    snap = ref.get()
    if not snap.exists:
        return False
    ref.delete()
    return True


# --- Reminder Functions ---

def list_reminders(user_id: str) -> List[Dict[str, Any]]:
    client = _get_firestore_client()
    col = (
        client.collection("users")
        .document(user_id)
        .collection("reminders")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
    )
    return [{**c.to_dict(), "id": c.id} for c in col.stream()]


def set_reminders(user_id: str, items: List[Dict[str, Any]]) -> None:
    client = _get_firestore_client()
    uref = client.collection("users").document(user_id)
    # Delete existing reminders
    for old in uref.collection("reminders").stream():
        old.reference.delete()
    # Create new reminders
    for it in items:
        iid = str(_uuid_module.uuid4())
        uref.collection("reminders").document(iid).set(
            {**it, "id": iid, "updated_at": _now_iso()}
        )


# --- Analytics Functions ---

def _is_opted_in_analytics(user_id: str) -> bool:
    user = get_user(user_id)
    return bool(user and user.get("opt_in_analytics"))


def anon_record_opt_in_delta(delta: int) -> None:
    if not delta:
        return
    try:
        client = _get_firestore_client()
        doc = client.collection("anon_analytics").document("global")
        inc = getattr(firestore, "Increment", None)
        if inc is not None:
            doc.update({"opt_in_user_count": inc(delta), "updated_at": _now_iso()})
        else:
            # Fallback
            snap = doc.get()
            current = snap.to_dict() or {}
            doc.set({
                "opt_in_user_count": int(current.get("opt_in_user_count", 0)) + delta,
                "updated_at": _now_iso()
            }, merge=True)
    except Exception:
        pass


def _anon_bins_label(length_days: int) -> str:
    if length_days <= 0:
        return "unknown"
    if length_days <= 21:
        return "21_or_less"
    if length_days <= 35:
        return "22_to_35"
    if length_days <= 45:
        return "36_to_45"
    return "46_or_more"


def anon_record_cycle_event(user_id: str, cycle_payload: Dict[str, Any], prev_start_date: Optional[str]) -> None:
    if not _is_opted_in_analytics(user_id):
        return
    
    flow = str(cycle_payload.get("flow") or "unknown")
    symptoms = cycle_payload.get("symptoms") or []
    if not isinstance(symptoms, list):
        symptoms = []

    length_days: Optional[int] = None
    try:
        if prev_start_date and cycle_payload.get("start_date"):
            a = str(prev_start_date)[:10]
            b = str(cycle_payload.get("start_date"))[:10]
            length_days = (datetime.fromisoformat(b) - datetime.fromisoformat(a)).days
    except Exception:
        length_days = None

    try:
        client = _get_firestore_client()
        doc = client.collection("anon_analytics").document("global")
        inc = getattr(firestore, "Increment", None)
        
        if inc is not None:
            updates: Dict[str, Any] = {
                "total_cycles": inc(1),
                f"flow_counts.{flow}": inc(1),
                "updated_at": _now_iso(),
            }
            for s in symptoms:
                if isinstance(s, str) and s.strip():
                    k = s.strip().lower()[:48]
                    updates[f"symptom_counts.{k}"] = inc(1)
            if isinstance(length_days, int) and length_days > 0:
                b = _anon_bins_label(length_days)
                updates[f"cycle_length_bins.{b}"] = inc(1)
            doc.set(updates, merge=True)
    except Exception:
        pass
