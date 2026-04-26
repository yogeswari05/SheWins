"""
Demo data service for creating comprehensive demo users.
Showcases all features of the EliteHer application.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from typing import Any, Dict, List

from app.services import db


DEMO_USERS = [
    {
        "email": "demo@eliteher.com",
        "password_hash": "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u",  # demo123456
        "display_name": "Demo User",
        "description": "Comprehensive demo user showcasing all features"
    },
    {
        "email": "sarah@eliteher.com", 
        "password_hash": "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u",  # demo123456
        "display_name": "Sarah",
        "description": "User with regular cycles, tracking wellness"
    },
    {
        "email": "maya@eliteher.com",
        "password_hash": "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u",  # demo123456
        "display_name": "Maya", 
        "description": "User with irregular cycles and PCOD risk indicators"
    },
    {
        "email": "demo2@eliteher.com",
        "password_hash": "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u",  # demo123456
        "display_name": "Demo2 High Risk",
        "description": "User with high PCOD risk score (>60%) to test gynecologist recommendation"
    }
]


def generate_demo_cycles(user_profile: str) -> List[Dict[str, Any]]:
    """Generate realistic demo cycles based on user profile."""
    
    if user_profile == "comprehensive":
        return generate_comprehensive_cycles()
    elif user_profile == "regular":
        return generate_regular_cycles()
    elif user_profile == "irregular":
        return generate_irregular_cycles()
    elif user_profile == "high_risk":
        return generate_high_risk_cycles()
    else:
        return generate_regular_cycles()


def generate_comprehensive_cycles() -> List[Dict[str, Any]]:
    """Generate cycles showcasing all features and edge cases."""
    cycles = []
    base_date = date.today() - timedelta(days=180)
    
    # Cycle 1: Normal cycle with comprehensive data
    cycles.append({
        "start_date": (base_date + timedelta(days=0)).isoformat(),
        "end_date": (base_date + timedelta(days=4)).isoformat(),
        "flow": "medium",
        "symptoms": ["cramps", "bloating", "headache", "breast_tenderness", "fatigue"],
        "mood": "tired",
        "sleep_hours": 6.5,
        "stress": 6,
        "exercise": "light",
        "notes": "Feeling overwhelmed with work this week. Having trouble sleeping."
    })
    
    # Cycle 2: Heavy flow with more symptoms
    cycles.append({
        "start_date": (base_date + timedelta(days=28)).isoformat(),
        "end_date": (base_date + timedelta(days=33)).isoformat(),
        "flow": "heavy",
        "symptoms": ["severe_cramps", "migraine", "nausea", "back_pain", "fatigue", "mood_swings", "acne"],
        "mood": "irritable",
        "sleep_hours": 5,
        "stress": 8,
        "exercise": "none",
        "notes": "Very painful period this time. Had to take pain medication. Feeling very stressed and anxious."
    })
    
    # Cycle 3: Irregular timing (long gap)
    cycles.append({
        "start_date": (base_date + timedelta(days=45)).isoformat(),
        "end_date": (base_date + timedelta(days=48)).isoformat(),
        "flow": "light",
        "symptoms": ["spotting", "mood_swings", "acne_breakouts"],
        "mood": "anxious",
        "sleep_hours": 7,
        "stress": 7,
        "exercise": "moderate",
        "notes": "Period came late again. Starting to worry about irregularity. Trying yoga to help with stress."
    })
    
    # Cycle 4: Very long gap (PCOD risk indicator)
    cycles.append({
        "start_date": (base_date + timedelta(days=80)).isoformat(),
        "end_date": (base_date + timedelta(days=84)).isoformat(),
        "flow": "heavy",
        "symptoms": ["prolonged_bleeding", "severe_cramps", "weight_gain", "excess_hair_growth", "acne", "fatigue"],
        "mood": "overwhelmed",
        "sleep_hours": 4.5,
        "stress": 9,
        "exercise": "none",
        "notes": "35 days since last period! Very concerned. Symptoms getting worse. Making doctor appointment."
    })
    
    # Cycle 5: Post-medical consultation
    cycles.append({
        "start_date": (base_date + timedelta(days=110)).isoformat(),
        "end_date": (base_date + timedelta(days=113)).isoformat(),
        "flow": "medium",
        "symptoms": ["cramps", "bloating", "headache"],
        "mood": "hopeful",
        "sleep_hours": 8,
        "stress": 5,
        "exercise": "moderate",
        "notes": "Doctor recommended lifestyle changes. Starting new treatment plan. Feeling more optimistic."
    })
    
    # Cycle 6: Improving with treatment
    cycles.append({
        "start_date": (base_date + timedelta(days=138)).isoformat(),
        "end_date": (base_date + timedelta(days=141)).isoformat(),
        "flow": "medium",
        "symptoms": ["mild_cramps", "breast_tenderness"],
        "mood": "calm",
        "sleep_hours": 8.5,
        "stress": 3,
        "exercise": "moderate",
        "notes": "Treatment is working! More regular cycle now. Sleeping better and feeling less stressed."
    })
    
    # Cycle 7: Recent cycle - good management
    cycles.append({
        "start_date": (base_date + timedelta(days=166)).isoformat(),
        "end_date": (base_date + timedelta(days=169)).isoformat(),
        "flow": "light",
        "symptoms": ["light_cramping", "fatigue"],
        "mood": "happy",
        "sleep_hours": 7.5,
        "stress": 2,
        "exercise": "moderate",
        "notes": "Feeling great! Regular cycle and much better symptom management. Yoga and meditation helping a lot."
    })
    
    return cycles


def generate_regular_cycles() -> List[Dict[str, Any]]:
    """Generate regular, healthy cycles for wellness tracking demo."""
    cycles = []
    base_date = date.today() - timedelta(days=120)
    
    cycle_lengths = [28, 29, 27, 28, 30, 28]  # Regular cycle lengths
    
    for i, length in enumerate(cycle_lengths):
        start_date = base_date + timedelta(days=sum(cycle_lengths[:i]))
        cycles.append({
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=4)).isoformat(),
            "flow": "medium",
            "symptoms": ["cramps", "bloating", "fatigue"],
            "mood": "tired" if i % 2 == 0 else "calm",
            "sleep_hours": 7 + (i % 2),
            "stress": 3 + (i % 3),
            "exercise": "moderate",
            "notes": f"Regular cycle #{i+1}. Feeling good overall."
        })
    
    return cycles


def generate_irregular_cycles() -> List[Dict[str, Any]]:
    """Generate irregular cycles with PCOD risk indicators."""
    cycles = []
    base_date = date.today() - timedelta(days=150)
    
    # Irregular pattern: 25, 35, 45, 28, 40, 32 days
    cycle_lengths = [25, 35, 45, 28, 40, 32]
    
    pcod_symptoms = [
        ["irregular_periods", "acne", "weight_gain"],
        ["missed_periods", "hirsutism", "mood_swings"],
        ["prolonged_bleeding", "ovarian_pain", "fatigue"],
        ["heavy_periods", "insulin_resistance", "dark_skin_patches"],
        ["infrequent_periods", "male_pattern_baldness", "high_testosterone"],
        ["acne_on_face", "excess_facial_hair", "pelvic_pain"]
    ]
    
    for i, length in enumerate(cycle_lengths):
        start_date = base_date + timedelta(days=sum(cycle_lengths[:i]))
        symptoms = ["cramps", "bloating"] + pcod_symptoms[i]
        
        cycles.append({
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=6 if i % 2 == 0 else 4)).isoformat(),
            "flow": "heavy" if i % 2 == 0 else "medium",
            "symptoms": symptoms,
            "mood": "anxious",
            "sleep_hours": 5.5,
            "stress": 7 + (i % 3),
            "exercise": "light",
            "notes": f"Concerned about irregularity. Symptoms seem to be getting worse. Cycle length: {length} days."
        })
    
    return cycles


def generate_high_risk_cycles() -> List[Dict[str, Any]]:
    """Generate cycles with high PCOD risk factors to trigger >60% risk score."""
    cycles = []
    base_date = date.today() - timedelta(days=200)
    
    # High-risk pattern: Very irregular cycles with gaps >35 days and multiple risk factors
    cycle_lengths = [28, 42, 38, 65, 40, 55]  # Includes gaps >35 days and high variance
    
    # High-risk symptoms combining multiple PCOD indicators
    high_risk_symptoms = [
        ["acne", "weight_gain", "excess_hair_growth", "hirsutism"],  # Acne + weight + hair combo
        ["prolonged_bleeding", "ovarian_pain", "fatigue", "mood_swings"],  # Prolonged bleeding
        ["heavy_periods", "insulin_resistance", "dark_skin_patches", "acne"],  # Multiple symptoms
        ["missed_periods", "male_pattern_baldness", "high_testosterone", "weight_gain"],  # Missed period
        ["infrequent_periods", "excess_facial_hair", "pelvic_pain", "acne_breakouts"],  # Hair + acne
        ["severe_cramps", "prolonged_bleeding", "weight_gain", "hirsutism"]  # Prolonged + multiple
    ]
    
    for i, length in enumerate(cycle_lengths):
        start_date = base_date + timedelta(days=sum(cycle_lengths[:i]))
        symptoms = ["cramps", "bloating", "fatigue"] + high_risk_symptoms[i]
        
        # Some cycles have prolonged bleeding (>7 days) to trigger medium risk
        bleeding_days = 8 if i in [1, 3, 5] else (5 if i % 2 == 0 else 6)
        
        cycles.append({
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=bleeding_days)).isoformat(),
            "flow": "heavy" if i % 2 == 0 else "medium",
            "symptoms": symptoms,
            "mood": "overwhelmed" if i % 2 == 0 else "anxious",
            "sleep_hours": 4.5 if i % 2 == 0 else 5.0,
            "stress": 8 + (i % 2),
            "exercise": "none",
            "notes": f"Very concerned about cycle length: {length} days. Multiple PCOD symptoms present. Bleeding lasted {bleeding_days} days. Symptoms getting progressively worse."
        })
    
    return cycles


def create_demo_users() -> Dict[str, Any]:
    """Create all demo users with their data."""
    results = {}
    
    print("🔄 Starting demo user creation...")
    
    for demo_user in DEMO_USERS:
        email = demo_user["email"]
        print(f"👤 Processing user: {email}")
        
        # Check if user already exists
        try:
            existing_user = db.find_user_by_email(email)
            if existing_user:
                user_id = existing_user[0]
                print(f"⚠️ User {email} already exists")
                results[email] = {
                    "status": "already_exists",
                    "user_id": user_id,
                    "message": f"Demo user {email} already exists"
                }
                continue
        except Exception as e:
            print(f"❌ Error checking user {email}: {e}")
            results[email] = {
                "status": "error",
                "message": f"Error checking {email}: {str(e)}"
            }
            continue
        
        # Create new user
        try:
            print(f"🔨 Creating user: {email}")
            user_id = db.create_registered_user(
                email=email,
                password_hash=demo_user["password_hash"],
                display_name=demo_user["display_name"]
            )
            print(f"✅ User created: {email} -> {user_id}")
            
            # Determine user profile type
            if "comprehensive" in demo_user["description"].lower():
                profile = "comprehensive"
            elif "regular" in demo_user["description"].lower():
                profile = "regular"
            elif "irregular" in demo_user["description"].lower():
                profile = "irregular"
            elif "high risk" in demo_user["description"].lower():
                profile = "high_risk"
            else:
                profile = "regular"
            
            # Generate and add cycles
            cycles = generate_demo_cycles(profile)
            print(f"📊 Creating {len(cycles)} cycles for {email}...")
            for i, cycle_data in enumerate(cycles):
                try:
                    db.add_cycle(user_id, cycle_data)
                    print(f"  ✅ Cycle {i+1}/{len(cycles)} created")
                except Exception as e:
                    print(f"  ❌ Cycle {i+1} failed: {e}")
            
            results[email] = {
                "status": "created",
                "user_id": user_id,
                "profile": profile,
                "cycles_created": len(cycles),
                "message": f"Demo user {email} created with {len(cycles)} cycles"
            }
        except Exception as e:
            print(f"❌ Error creating user {email}: {e}")
            results[email] = {
                "status": "error", 
                "message": f"Error creating {email}: {str(e)}"
            }
            continue
    
    return results


def get_demo_user_info() -> Dict[str, Any]:
    """Get information about demo users for display."""
    return {
        "users": [
            {
                "email": user["email"],
                "password": "demo123456",
                "display_name": user["display_name"],
                "description": user["description"],
                "features": get_user_features(user["description"])
            }
            for user in DEMO_USERS
        ],
        "setup_instructions": {
            "step1": "Use any demo account to explore features",
            "step2": "demo@eliteher.com shows comprehensive features including PCOD risk",
            "step3": "sarah@eliteher.com shows regular wellness tracking",
            "step4": "maya@eliteher.com shows irregular cycles and PCOD indicators",
            "step5": "demo2@eliteher.com shows high PCOD risk (>60%) triggering gynecologist recommendation",
            "step6": "All accounts use password: demo123456"
        }
    }


def get_user_features(description: str) -> List[str]:
    """Get list of features demonstrated by each user."""
    if "comprehensive" in description.lower():
        return [
            "Complete cycle tracking",
            "Date inconsistency alerts", 
            "PCOD risk detection",
            "Stress analysis",
            "Symptom management",
            "Mood tracking",
            "All flow types",
            "Health insights",
            "Treatment progress"
        ]
    elif "regular" in description.lower():
        return [
            "Regular cycle tracking",
            "Wellness monitoring",
            "Basic symptom tracking",
            "Mood and sleep tracking",
            "Exercise logging",
            "Health maintenance"
        ]
    elif "irregular" in description.lower():
        return [
            "Irregular cycle tracking",
            "PCOD risk indicators",
            "Advanced symptom analysis",
            "Health alerts",
            "Pattern recognition",
            "Risk assessment"
        ]
    elif "high risk" in description.lower():
        return [
            "High PCOD risk score (>60%)",
            "Gynecologist recommendation trigger",
            "Multiple PCOD symptoms",
            "Irregular cycle patterns",
            "Prolonged bleeding episodes",
            "High-risk symptom combinations",
            "Advanced risk assessment"
        ]
    else:
        return ["Basic cycle tracking"]


def setup_demo_data() -> Dict[str, Any]:
    """Main function to set up all demo data."""
    results = create_demo_users()
    
    summary = {
        "total_users": len([r for r in results.values() if r["status"] == "created"]),
        "existing_users": len([r for r in results.values() if r["status"] == "already_exists"]),
        "errors": len([r for r in results.values() if r["status"] == "error"]),
        "details": results,
        "user_info": get_demo_user_info(),
        "summary": f"{len([r for r in results.values() if r['status'] == 'created'])} users created, {len([r for r in results.values() if r['status'] == 'already_exists'])} already exist"
    }
    
    return summary
