"""
Firebase-only database service for EliteHer.
Firebase is mandatory - no in-memory fallbacks.
"""
from __future__ import annotations

# Import all functions from the Firebase-only implementation
from app.services.firebase_db import (
    # User functions
    ensure_user,
    get_user,
    find_user_by_email,
    create_registered_user,
    update_user_settings,
    merge_user_data,
    
    # Cycle functions
    list_cycles,
    create_cycle,
    update_cycle,
    delete_cycle,
    
    # Reminder functions
    list_reminders,
    set_reminders,
    
    # Analytics functions
    anon_record_opt_in_delta,
    anon_record_cycle_event,
    
    # Internal functions
    _sanitize_user_dict,
    _sanitize_cycle_dict,
    _prepare_cycle_payload,
    _is_opted_in_analytics,
    _anon_bins_label,
)

# Firebase client is always required
from app.services.firebase_db import _get_firestore_client

# Legacy compatibility
def use_firestore() -> bool:
    """Always True - Firebase is mandatory."""
    return True

# Add backward compatibility for add_cycle (maps to create_cycle)
def add_cycle(user_id: str, payload: Dict[str, Any]) -> str:
    """Backward compatibility wrapper for create_cycle."""
    return create_cycle(user_id, payload)
