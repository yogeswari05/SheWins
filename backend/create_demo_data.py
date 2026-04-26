#!/usr/bin/env python3
"""
Create comprehensive demo data for demo@eliteher.com user covering the last year.
Showcases all EliteHer features with realistic patterns.
"""

import sys
import os
from datetime import date, datetime, timedelta
import random

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services import db
from app.services.demo_data import generate_demo_cycles

def generate_yearly_cycles() -> list:
    """Generate 1 year of realistic menstrual cycle data."""
    cycles = []
    base_date = date.today() - timedelta(days=365)
    
    # Create a realistic pattern for the year
    cycle_lengths = []
    current_date = base_date
    
    while current_date < date.today():
        # Generate realistic cycle length (25-35 days, with some variation)
        base_length = 28
        variation = random.randint(-3, 7)
        cycle_length = base_length + variation
        cycle_length = max(25, min(35, cycle_length))  # Keep within realistic range
        
        cycle_lengths.append(cycle_length)
        current_date += timedelta(days=cycle_length)
    
    # Generate cycle data for each cycle
    for i, cycle_length in enumerate(cycle_lengths):
        start_date = base_date + timedelta(days=sum(cycle_lengths[:i]))
        
        # Vary flow intensity realistically
        flow_options = ["light", "medium", "heavy"]
        flow_weights = [0.3, 0.5, 0.2]  # Most cycles are medium
        flow = random.choices(flow_options, weights=flow_weights)[0]
        
        # Generate period duration based on flow
        if flow == "light":
            period_duration = random.randint(3, 5)
        elif flow == "medium":
            period_duration = random.randint(4, 6)
        else:  # heavy
            period_duration = random.randint(5, 7)
        
        end_date = start_date + timedelta(days=period_duration)
        
        # Generate realistic symptoms based on flow and cycle position
        symptoms = generate_symptoms(flow, i)
        mood = generate_mood(flow, i)
        sleep_hours = generate_sleep_hours(flow, i)
        stress_level = generate_stress_level(i)
        exercise = generate_exercise(stress_level)
        notes = generate_notes(i, cycle_length, flow, symptoms)
        
        cycles.append({
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "flow": flow,
            "symptoms": symptoms,
            "mood": mood,
            "sleep_hours": sleep_hours,
            "stress": stress_level,
            "exercise": exercise,
            "notes": notes
        })
    
    return cycles

def generate_symptoms(flow: str, cycle_index: int) -> list:
    """Generate realistic symptoms based on flow and cycle position."""
    base_symptoms = ["cramps", "bloating"]  # Always include these
    
    # Add symptoms based on flow intensity
    if flow == "heavy":
        heavy_symptoms = ["severe_cramps", "migraine", "back_pain", "fatigue", "nausea"]
        base_symptoms.extend(random.sample(heavy_symptoms, random.randint(3, 5)))
    elif flow == "medium":
        medium_symptoms = ["headache", "breast_tenderness", "fatigue", "mood_swings"]
        base_symptoms.extend(random.sample(medium_symptoms, random.randint(2, 3)))
    else:  # light
        light_symptoms = ["mild_cramping", "breast_tenderness"]
        base_symptoms.extend(random.sample(light_symptoms, random.randint(1, 2)))
    
    # Add occasional symptoms for realism
    if cycle_index % 4 == 0:  # Every 4th cycle has acne
        base_symptoms.append("acne")
    if cycle_index % 6 == 0:  # Every 6th cycle has food cravings
        base_symptoms.append("food_cravings")
    
    return base_symptoms

def generate_mood(flow: str, cycle_index: int) -> str:
    """Generate realistic mood based on symptoms and cycle."""
    moods = ["tired", "calm", "anxious", "irritable", "happy", "overwhelmed", "hopeful"]
    
    # Weight moods based on flow
    if flow == "heavy":
        mood_weights = [0.3, 0.1, 0.2, 0.2, 0.05, 0.1, 0.05]
    elif flow == "medium":
        mood_weights = [0.2, 0.2, 0.15, 0.15, 0.15, 0.1, 0.05]
    else:  # light
        mood_weights = [0.1, 0.3, 0.1, 0.1, 0.3, 0.05, 0.05]
    
    return random.choices(moods, weights=mood_weights)[0]

def generate_sleep_hours(flow: str, cycle_index: int) -> float:
    """Generate realistic sleep hours."""
    base_sleep = 7.5
    
    # Adjust based on flow
    if flow == "heavy":
        base_sleep -= random.uniform(1.5, 2.5)  # Poor sleep with heavy flow
    elif flow == "medium":
        base_sleep -= random.uniform(0.5, 1.5)
    else:  # light
        base_sleep -= random.uniform(0, 1)
    
    # Add some random variation
    base_sleep += random.uniform(-1, 1)
    
    return round(max(4.0, min(10.0, base_sleep), 1)

def generate_stress_level(cycle_index: int) -> int:
    """Generate realistic stress levels (1-10 scale)."""
    # Base stress with some seasonal variation
    base_stress = 4
    
    # Add some variation based on cycle position
    if cycle_index % 3 == 0:  # Every 3rd cycle is more stressful
        base_stress += 3
    
    # Add random variation
    stress = base_stress + random.randint(-2, 3)
    
    return max(1, min(10, stress))

def generate_exercise(stress_level: int) -> str:
    """Generate exercise based on stress level."""
    if stress_level >= 7:
        return random.choice(["none", "light"])
    elif stress_level >= 5:
        return random.choice(["light", "moderate"])
    else:
        return random.choice(["moderate", "intense"])

def generate_notes(cycle_index: int, cycle_length: int, flow: str, symptoms: list) -> str:
    """Generate realistic notes for each cycle."""
    notes_templates = [
        f"Cycle #{cycle_index + 1}. Feeling {('good' if flow == 'light' else 'okay' if flow == 'medium' else 'tired')}.",
        f"Cycle length was {cycle_length} days. {'Regular' if 25 <= cycle_length <= 32 else 'A bit irregular'}.",
        f"{'Painful' if 'severe_cramps' in symptoms else 'Mild'} period this time. Took {'pain medication' if flow == 'heavy' else 'no medication'}.",
        f"Trying to {'exercise more' if stress_level > 6 else 'maintain routine'}. Sleep has been {'poor' if flow == 'heavy' else 'decent'}.",
        f"{'Stressful week at work' if cycle_index % 4 == 0 else 'Calm week'}. Focusing on self-care.",
        f"{'Starting to worry about irregularity' if cycle_length > 35 else 'Cycle seems normal'}. Maybe {'see doctor' if cycle_length > 40 else 'keep tracking'}.",
        f"{'New symptoms appeared' if len(symptoms) > 5 else 'Usual symptoms'}. {'Managing well' if flow != 'heavy' else 'Difficult to manage'}."
    ]
    
    return random.choice(notes_templates)

def create_demo_user_with_year_data():
    """Create demo user with a full year of cycle data."""
    email = "demo@eliteher.com"
    password_hash = "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u"  # demo123456
    
    print("🔄 Creating demo@eliteher.com user with 1 year of data...")
    
    try:
        # Check if user already exists
        existing_user = db.find_user_by_email(email)
        if existing_user:
            user_id = existing_user[0]
            print(f"⚠️ Demo user {email} already exists (ID: {user_id})")
        else:
            # Create new user
            user_id = db.create_registered_user(
                email=email,
                password_hash=password_hash,
                display_name="Demo User"
            )
            print(f"✅ Demo user created: {email} -> {user_id}")
        
        # Generate yearly cycles
        cycles = generate_yearly_cycles()
        print(f"📊 Generated {len(cycles)} cycles covering the last year")
        
        # Add cycles to database
        success_count = 0
        for i, cycle_data in enumerate(cycles):
            try:
                db.add_cycle(user_id, cycle_data)
                success_count += 1
                if (i + 1) % 10 == 0:
                    print(f"  ✅ Processed {i + 1}/{len(cycles)} cycles...")
            except Exception as e:
                print(f"  ❌ Failed to add cycle {i + 1}: {e}")
        
        print(f"🎉 Successfully created {success_count}/{len(cycles)} cycles for demo user")
        
        # Generate some wellness data
        create_wellness_data(user_id, cycles)
        
        return {
            "status": "success",
            "user_id": user_id,
            "email": email,
            "cycles_created": success_count,
            "date_range": f"{cycles[0]['start_date'][:10]} to {cycles[-1]['start_date'][:10]}",
            "password": "demo123456"
        }
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

def create_wellness_data(user_id: str, cycles: list):
    """Create additional wellness data for demo user."""
    print("🧘 Creating wellness data...")
    
    wellness_entries = []
    for i, cycle in enumerate(cycles):
        # Create some wellness entries between cycles
        if i < len(cycles) - 1:
            next_cycle = cycles[i + 1]
            days_between = (datetime.fromisoformat(next_cycle['start_date']) - 
                          datetime.fromisoformat(cycle['end_date'])).days
            
            # Add wellness entries for some days
            for day in range(1, min(days_between, 10)):
                entry_date = (datetime.fromisoformat(cycle['end_date']) + timedelta(days=day)).date()
                
                wellness_entries.append({
                    "date": entry_date.isoformat(),
                    "mood": random.choice(["happy", "calm", "energetic", "tired", "stressed"]),
                    "energy": random.randint(3, 8),
                    "stress": random.randint(1, 7),
                    "sleep_hours": round(random.uniform(6.0, 9.0), 1),
                    "exercise": random.choice(["none", "light", "moderate", "intense"]),
                    "meditation": random.choice([True, False]),
                    "water_intake": random.randint(4, 10),
                    "notes": f"Wellness check-in day {day}"
                })
    
    # Add wellness entries to database
    success_count = 0
    for entry in wellness_entries:
        try:
            db.add_wellness_entry(user_id, entry)
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed to add wellness entry: {e}")
    
    print(f"  ✅ Created {success_count} wellness entries")

if __name__ == "__main__":
    result = create_demo_user_with_year_data()
    
    if result["status"] == "success":
        print("\n" + "="*50)
        print("🎉 DEMO DATA CREATION COMPLETED!")
        print("="*50)
        print(f"📧 Email: {result['email']}")
        print(f"🔑 Password: {result['password']}")
        print(f"👤 User ID: {result['user_id']}")
        print(f"📊 Cycles Created: {result['cycles_created']}")
        print(f"📅 Date Range: {result['date_range']}")
        print("="*50)
        print("✨ You can now login and test all features!")
        print("="*50)
    else:
        print("\n❌ DEMO DATA CREATION FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")
