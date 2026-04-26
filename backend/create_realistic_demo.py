#!/usr/bin/env python3
"""
Create realistic, non-uniform demo data for demo@eliteher.com user
from March 2025 to present with PCOD risk indicators and irregular patterns
"""

import sys
import os
from datetime import date, datetime, timedelta
import random

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services import db

def create_realistic_demo_data():
    """Create realistic demo data with irregular patterns and risk indicators."""
    email = "demo@eliteher.com"
    password_hash = "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u"
    
    print("Creating realistic demo data from March 2025 to present...")
    
    try:
        # Check if user exists
        existing_user = db.find_user_by_email(email)
        if existing_user:
            user_id = existing_user[0]
            print(f"Demo user exists: {user_id}")
        else:
            # Create user
            user_id = db.create_registered_user(
                email=email,
                password_hash=password_hash,
                display_name="Demo User"
            )
            print(f"Created demo user: {user_id}")
        
        # Create realistic, non-uniform cycles from March 2025
        cycles = generate_realistic_cycles()
        print(f"Generated {len(cycles)} realistic cycles")
        
        # Clear existing cycles and add new ones
        try:
            # Get existing cycles to delete them
            existing_cycles = db.list_cycles(user_id)
            for cycle in existing_cycles:
                try:
                    cycle_id = cycle.get('id')
                    if cycle_id:
                        db.delete_cycle(user_id, cycle_id)
                except:
                    pass
            print("Cleared existing cycles")
        except:
            pass
        
        # Add new cycles
        for cycle in cycles:
            db.add_cycle(user_id, cycle)
        
        print(f"Added {len(cycles)} new cycles")
        
        print("\n" + "="*60)
        print("REALISTIC DEMO DATA READY!")
        print("="*60)
        print(f"📧 Email: {email}")
        print("🔑 Password: demo123456")
        print(f"👤 User ID: {user_id}")
        print(f"📊 Cycles: {len(cycles)}")
        print(f"📅 Date Range: {cycles[0]['start_date'][:10]} to {cycles[-1]['start_date'][:10]}")
        print("⚠️  Features: Irregular patterns, PCOD risks, stress patterns")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")

def generate_realistic_cycles() -> list:
    """Generate realistic, non-uniform cycles with various health scenarios."""
    cycles = []
    start_date = date(2025, 3, 15)  # March 15, 2025
    
    # Define realistic, non-uniform cycle patterns
    cycle_scenarios = [
        # Early 2025: Regular cycles
        {"days": 28, "flow": "medium", "scenario": "normal"},
        {"days": 27, "flow": "light", "scenario": "normal"},
        {"days": 29, "flow": "medium", "scenario": "normal"},
        
        # Mid 2025: Starting irregularities
        {"days": 31, "flow": "heavy", "scenario": "stress"},
        {"days": 26, "flow": "medium", "scenario": "normal"},
        {"days": 35, "flow": "heavy", "scenario": "irregular_start"},
        
        # Late 2025: More irregular patterns
        {"days": 42, "flow": "heavy", "scenario": "pcod_risk"},
        {"days": 28, "flow": "medium", "scenario": "normal_break"},
        {"days": 38, "flow": "heavy", "scenario": "pcod_worsening"},
        {"days": 45, "flow": "heavy", "scenario": "severe_irregular"},
        
        # Early 2026: Continued issues
        {"days": 32, "flow": "medium", "scenario": "treatment_start"},
        {"days": 29, "flow": "medium", "scenario": "improving"},
        {"days": 30, "flow": "light", "scenario": "better"},
        {"days": 28, "flow": "medium", "scenario": "stable"},
        
        # Recent cycles: Some improvement but still irregular
        {"days": 31, "flow": "medium", "scenario": "stable"},
        {"days": 29, "flow": "light", "scenario": "good"},
        {"days": 33, "flow": "medium", "scenario": "minor_setback"},
    ]
    
    current_date = start_date
    
    for i, scenario in enumerate(cycle_scenarios):
        cycle_data = create_cycle_data(current_date, scenario, i)
        cycles.append(cycle_data)
        current_date += timedelta(days=scenario["days"])
    
    return cycles

def create_cycle_data(start_date: date, scenario: dict, index: int) -> dict:
    """Create detailed cycle data based on scenario."""
    
    # Base cycle data
    flow = scenario["flow"]
    scenario_type = scenario["scenario"]
    
    # Period duration based on flow
    if flow == "light":
        duration = random.randint(3, 4)
    elif flow == "medium":
        duration = random.randint(4, 6)
    else:  # heavy
        duration = random.randint(5, 8)
    
    end_date = start_date + timedelta(days=duration)
    
    # Generate symptoms based on scenario
    symptoms, mood, stress, sleep, exercise, notes = generate_scenario_data(
        scenario_type, flow, index
    )
    
    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "flow": flow,
        "symptoms": symptoms,
        "mood": mood,
        "sleep_hours": sleep,
        "stress": stress,
        "exercise": exercise,
        "notes": notes
    }

def generate_scenario_data(scenario_type: str, flow: str, index: int):
    """Generate realistic data based on health scenario."""
    
    if scenario_type == "normal":
        symptoms = ["cramps", "bloating", "fatigue"]
        mood = random.choice(["calm", "tired", "happy"])
        stress = random.randint(2, 5)
        sleep = round(random.uniform(7.0, 8.5), 1)
        exercise = random.choice(["moderate", "light"])
        notes = f"Normal cycle #{index+1}. Feeling good."
        
    elif scenario_type == "stress":
        symptoms = ["cramps", "bloating", "headache", "fatigue", "mood_swings"]
        mood = random.choice(["anxious", "irritable", "overwhelmed"])
        stress = random.randint(6, 8)
        sleep = round(random.uniform(5.5, 7.0), 1)
        exercise = random.choice(["light", "none"])
        notes = f"Stressful period. Work pressure affecting cycle #{index+1}."
        
    elif scenario_type == "irregular_start":
        symptoms = ["cramps", "bloating", "acne", "breast_tenderness", "fatigue"]
        mood = random.choice(["anxious", "worried"])
        stress = random.randint(5, 7)
        sleep = round(random.uniform(6.0, 7.5), 1)
        exercise = random.choice(["light", "moderate"])
        notes = f"Cycle #{index+1} came late. Starting to worry about irregularity."
        
    elif scenario_type == "pcod_risk":
        symptoms = [
            "severe_cramps", "heavy_bleeding", "acne", "weight_gain", 
            "excess_hair_growth", "mood_swings", "fatigue", "bloating"
        ]
        mood = random.choice(["overwhelmed", "depressed", "anxious"])
        stress = random.randint(7, 9)
        sleep = round(random.uniform(4.5, 6.5), 1)
        exercise = random.choice(["none", "light"])
        notes = f"Very concerning cycle #{index+1}. Many PCOD symptoms appearing. Considering doctor visit."
        
    elif scenario_type == "normal_break":
        symptoms = ["cramps", "bloating", "headache"]
        mood = random.choice(["calm", "hopeful"])
        stress = random.randint(3, 5)
        sleep = round(random.uniform(7.0, 8.0), 1)
        exercise = random.choice(["moderate", "light"])
        notes = f"Cycle #{index+1} seems more normal. Feeling hopeful."
        
    elif scenario_type == "pcod_worsening":
        symptoms = [
            "prolonged_bleeding", "severe_cramps", "ovarian_pain", 
            "male_pattern_hair_growth", "dark_skin_patches", "insulin_resistance"
        ]
        mood = random.choice(["depressed", "overwhelmed"])
        stress = random.randint(8, 10)
        sleep = round(random.uniform(4.0, 6.0), 1)
        exercise = "none"
        notes = f"Cycle #{index+1} is very concerning. PCOD symptoms worsening. Made doctor appointment."
        
    elif scenario_type == "severe_irregular":
        symptoms = [
            "missed_periods", "prolonged_bleeding", "severe_cramps",
            "weight_gain", "acne", "infrequent_periods", "pelvic_pain"
        ]
        mood = random.choice(["depressed", "anxious", "hopeless"])
        stress = random.randint(8, 10)
        sleep = round(random.uniform(3.5, 5.5), 1)
        exercise = "none"
        notes = f"Cycle #{index+1} - 45 days since last period! Very worried about health."
        
    elif scenario_type == "treatment_start":
        symptoms = ["cramps", "bloating", "headache", "fatigue"]
        mood = random.choice(["hopeful", "cautiously_optimistic"])
        stress = random.randint(4, 6)
        sleep = round(random.uniform(6.5, 8.0), 1)
        exercise = random.choice(["light", "moderate"])
        notes = f"Cycle #{index+1} - Started medical treatment. Feeling hopeful about improvement."
        
    elif scenario_type == "improving":
        symptoms = ["cramps", "bloating", "mood_swings"]
        mood = random.choice(["calm", "optimistic", "happy"])
        stress = random.randint(3, 5)
        sleep = round(random.uniform(7.0, 8.5), 1)
        exercise = random.choice(["moderate", "light"])
        notes = f"Cycle #{index+1} - Treatment seems to be working. Feeling better."
        
    elif scenario_type == "better":
        symptoms = ["mild_cramping", "fatigue", "breast_tenderness"]
        mood = random.choice(["happy", "calm", "energetic"])
        stress = random.randint(2, 4)
        sleep = round(random.uniform(7.5, 9.0), 1)
        exercise = random.choice(["moderate", "intense"])
        notes = f"Cycle #{index+1} - Much better! Regular and lighter symptoms."
        
    elif scenario_type == "stable":
        symptoms = ["cramps", "bloating", "fatigue"]
        mood = random.choice(["calm", "stable", "content"])
        stress = random.randint(3, 5)
        sleep = round(random.uniform(7.0, 8.0), 1)
        exercise = random.choice(["moderate", "light"])
        notes = f"Cycle #{index+1} - Stable and manageable."
        
    elif scenario_type == "good":
        symptoms = ["mild_cramping", "light_fatigue"]
        mood = random.choice(["happy", "energetic", "positive"])
        stress = random.randint(1, 3)
        sleep = round(random.uniform(8.0, 9.0), 1)
        exercise = random.choice(["moderate", "intense"])
        notes = f"Cycle #{index+1} - Feeling great! Treatment working well."
        
    else:  # minor_setback
        symptoms = ["cramps", "bloating", "headache", "fatigue"]
        mood = random.choice(["tired", "slightly_anxious"])
        stress = random.randint(4, 6)
        sleep = round(random.uniform(6.5, 7.5), 1)
        exercise = random.choice(["light", "moderate"])
        notes = f"Cycle #{index+1} - Minor setback but still much better than before."
    
    return symptoms, mood, stress, sleep, exercise, notes

if __name__ == "__main__":
    create_realistic_demo_data()
