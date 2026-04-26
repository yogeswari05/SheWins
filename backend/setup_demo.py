#!/usr/bin/env python3
"""
Simple demo data setup for demo@eliteher.com user
"""

import sys
import os
from datetime import date, datetime, timedelta
import random

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services import db

def create_demo_data():
    """Create demo user with realistic cycle data."""
    email = "demo@eliteher.com"
    password_hash = "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u"
    
    print("Creating demo user with 1 year of data...")
    
    try:
        # Check if user exists
        existing_user = db.find_user_by_email(email)
        if existing_user:
            user_id = existing_user[0]
            print(f"Demo user already exists: {user_id}")
        else:
            # Create user
            user_id = db.create_registered_user(
                email=email,
                password_hash=password_hash,
                display_name="Demo User"
            )
            print(f"Created demo user: {user_id}")
        
        # Generate 1 year of cycles
        cycles = []
        start_date = date.today() - timedelta(days=365)
        
        for i in range(13):  # About 13 cycles in a year
            cycle_start = start_date + timedelta(days=i*28)
            cycle_length = random.randint(26, 32)
            flow = random.choice(["light", "medium", "heavy"])
            
            cycles.append({
                "start_date": cycle_start.isoformat(),
                "end_date": (cycle_start + timedelta(days=5)).isoformat(),
                "flow": flow,
                "symptoms": ["cramps", "bloating"] + random.sample(["headache", "fatigue", "mood_swings", "breast_tenderness"], 2),
                "mood": random.choice(["tired", "calm", "anxious", "happy"]),
                "sleep_hours": round(random.uniform(6.0, 9.0), 1),
                "stress": random.randint(2, 8),
                "exercise": random.choice(["none", "light", "moderate"]),
                "notes": f"Cycle {i+1} - {flow} flow"
            })
        
        # Add cycles to database
        for cycle in cycles:
            db.add_cycle(user_id, cycle)
        
        print(f"Created {len(cycles)} cycles for demo user")
        
        print("\n" + "="*50)
        print("DEMO DATA READY!")
        print("="*50)
        print(f"Email: {email}")
        print("Password: demo123456")
        print(f"User ID: {user_id}")
        print(f"Cycles: {len(cycles)}")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_demo_data()
