"""
Date inconsistency detection and validation for menstrual cycles.
Provides smart alerts for potential data entry errors and health patterns.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


def _parse_date(s: str) -> date:
    """Parse date string to date object."""
    if isinstance(s, date) and not isinstance(s, datetime):
        return s
    return date.fromisoformat(str(s)[:10])


def detect_date_inconsistencies(
    cycle_data: Dict[str, Any], existing_cycles: List[Dict[str, Any]]
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Detect potential date inconsistencies in cycle data.
    Returns (warnings, suggestions)
    """
    warnings: List[str] = []
    suggestions: List[Dict[str, Any]] = []
    
    try:
        start_date = _parse_date(cycle_data.get("start_date", ""))
        end_date = None
        if cycle_data.get("end_date"):
            end_date = _parse_date(cycle_data["end_date"])
    except ValueError:
        warnings.append("invalid_date_format")
        suggestions.append({
            "type": "error",
            "message": "Please use valid date format (YYYY-MM-DD)",
            "field": "start_date"
        })
        return warnings, suggestions
    
    # Check 1: End date before start date
    if end_date and end_date < start_date:
        warnings.append("end_before_start")
        suggestions.append({
            "type": "warning",
            "message": "End date is before start date. This might be an entry error.",
            "field": "end_date",
            "auto_fix": "swap_dates"
        })
    
    # Check 2: Very long duration (> 15 days)
    if end_date:
        duration = (end_date - start_date).days + 1
        if duration > 15:
            warnings.append("very_long_period")
            suggestions.append({
                "type": "info",
                "message": f"Period duration is {duration} days. This is unusual and might indicate spotting or entry error.",
                "field": "end_date"
            })
    
    # Check 3: Very short duration (< 2 days)
    if end_date:
        duration = (end_date - start_date).days + 1
        if duration < 2:
            warnings.append("very_short_period")
            suggestions.append({
                "type": "info",
                "message": "Period duration is very short. This might be spotting.",
                "field": "end_date"
            })
    
    # Check 4: Overlapping with existing cycles
    for existing in existing_cycles:
        try:
            existing_start = _parse_date(existing["start_date"])
            existing_end = None
            if existing.get("end_date"):
                existing_end = _parse_date(existing["end_date"])
            
            # Check for overlapping periods
            if existing_end and start_date <= existing_end:
                warnings.append("overlapping_cycles")
                suggestions.append({
                    "type": "warning",
                    "message": "This cycle overlaps with an existing cycle entry.",
                    "field": "start_date",
                    "conflict_cycle_id": existing.get("id")
                })
                break
            
            # Check for duplicate dates
            if start_date == existing_start:
                warnings.append("duplicate_start_date")
                suggestions.append({
                    "type": "warning",
                    "message": "You already have a cycle starting on this date.",
                    "field": "start_date",
                    "conflict_cycle_id": existing.get("id")
                })
                break
                
        except (ValueError, KeyError):
            continue
    
    # Check 5: Unusual gaps from previous cycle
    if existing_cycles:
        try:
            sorted_cycles = sorted(existing_cycles, key=lambda c: c["start_date"])
            last_cycle = sorted_cycles[-1]
            last_start = _parse_date(last_cycle["start_date"])
            
            gap = (start_date - last_start).days
            
            # Very short gap (< 15 days)
            if gap < 15:
                warnings.append("very_short_gap")
                suggestions.append({
                    "type": "info",
                    "message": f"Only {gap} days since last period. This might be the same cycle.",
                    "field": "start_date"
                })
            
            # Very long gap (> 90 days)
            elif gap > 90:
                warnings.append("very_long_gap")
                suggestions.append({
                    "type": "health_alert",
                    "message": f"{gap} days since last period. Consider consulting a healthcare provider.",
                    "field": "start_date",
                    "health_importance": "high"
                })
                
        except (ValueError, KeyError):
            pass
    
    return warnings, suggestions


def get_health_insights_from_dates(
    cycle_data: Dict[str, Any], existing_cycles: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate health insights based on date patterns."""
    insights: List[Dict[str, Any]] = []
    
    try:
        start_date = _parse_date(cycle_data.get("start_date", ""))
        end_date = None
        if cycle_data.get("end_date"):
            end_date = _parse_date(cycle_data["end_date"])
    except ValueError:
        return insights
    
    # Analyze cycle patterns if we have enough data
    if len(existing_cycles) >= 2:
        try:
            sorted_cycles = sorted(existing_cycles + [cycle_data], key=lambda c: c["start_date"])
            cycle_lengths = []
            
            for i in range(1, len(sorted_cycles)):
                prev_start = _parse_date(sorted_cycles[i-1]["start_date"])
                curr_start = _parse_date(sorted_cycles[i]["start_date"])
                cycle_lengths.append((curr_start - prev_start).days)
            
            if len(cycle_lengths) >= 3:
                avg_length = sum(cycle_lengths) / len(cycle_lengths)
                current_length = cycle_lengths[-1]
                
                # Significant deviation from average
                if abs(current_length - avg_length) > 10:
                    insights.append({
                        "type": "pattern_change",
                        "message": f"Current cycle length ({current_length} days) differs from your average ({avg_length:.1f} days).",
                        "importance": "medium"
                    })
                    
        except (ValueError, KeyError):
            pass
    
    return insights


def validate_cycle_completeness(cycle_data: Dict[str, Any]) -> List[str]:
    """Check if cycle data has all recommended fields."""
    missing_fields: List[str] = []
    
    required_fields = ["start_date"]
    recommended_fields = ["end_date", "flow", "symptoms", "mood", "sleep_hours", "stress"]
    
    for field in required_fields:
        if not cycle_data.get(field):
            missing_fields.append(field)
    
    for field in recommended_fields:
        if field not in cycle_data or not cycle_data.get(field):
            missing_fields.append(f"optional_{field}")
    
    return missing_fields
