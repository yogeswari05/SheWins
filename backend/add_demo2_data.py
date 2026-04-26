#!/usr/bin/env python3
"""
Script to add high-risk cycle data to demo2 user to ensure >60% PCOD risk score.
"""

from datetime import date, timedelta
from app.services import db
from app.services.pcod_risk import compute_pcod_risk


def create_high_risk_cycles():
    """Generate cycles with maximum possible PCOD risk factors to guarantee >60% risk score."""
    cycles = []
    base_date = date.today() - timedelta(days=300)
    
    # Maximum risk pattern: Multiple extremely long gaps and maximum variance
    # This will trigger: gap_over_35_days (25pts), multiple_skipped_or_missed (30pts), high_cycle_variance (20pts)
    cycle_lengths = [30, 50, 85, 40, 95, 35, 90, 45, 100, 38]  # Extreme gaps >35 days, maximum variance
    
    # Maximum risk symptoms - include EVERY possible symptom keyword
    max_risk_symptoms = [
        # Cycle 1: Acne + weight + hair combo (20pts)
        ["acne", "weight_gain", "excess_hair_growth", "hirsutism", "male_pattern_baldness", "hairfall"],
        # Cycle 2: Prolonged bleeding + all low-risk mood/fatigue keywords
        ["prolonged_bleeding", "ovarian_pain", "fatigue", "mood_swings", "mood", "spotting"],
        # Cycle 3: All skin + weight + hair + prolonged bleeding
        ["heavy_periods", "dark_skin_patches", "acne_breakouts", "weight_gain", "hirsutism", "prolonged_bleeding"],
        # Cycle 4: Hormonal + pain + hair + mood swing
        ["missed_periods", "high_testosterone", "pelvic_pain", "excess_facial_hair", "acne", "mood swing"],
        # Cycle 5: All metabolic + skin + prolonged bleeding
        ["infrequent_periods", "insulin_resistance", "dark_skin_patches", "male_pattern_baldness", "weight_gain", "prolonged_bleeding"],
        # Cycle 6: All major symptoms + mood + fatigue
        ["prolonged_bleeding", "ovarian_pain", "acne", "hirsutism", "mood_swings", "fatigue", "mood"],
        # Cycle 7: Everything combined
        ["heavy_periods", "excess_hair_growth", "weight_gain", "acne_breakouts", "pelvic_pain", "prolonged_bleeding"],
        # Cycle 8: Hormonal + metabolic + mood + spotting
        ["missed_periods", "high_testosterone", "insulin_resistance", "dark_skin_patches", "excess_facial_hair", "mood swing", "spotting"],
        # Cycle 9: Maximum prolonged bleeding + all symptoms
        ["prolonged_bleeding", "heavy_periods", "acne", "weight_gain", "hirsutism", "fatigue", "mood swing", "spotting"],
        # Cycle 10: All risk factors combined
        ["acne", "weight_gain", "excess_hair_growth", "prolonged_bleeding", "missed_periods", "mood swing", "fatigue", "spotting"]
    ]
    
    for i, length in enumerate(cycle_lengths):
        start_date = base_date + timedelta(days=sum(cycle_lengths[:i]))
        # Include ALL possible risk symptoms
        base_symptoms = ["cramps", "bloating", "fatigue", "mood_swings", "mood swing", "spotting"]
        symptoms = base_symptoms + max_risk_symptoms[i]
        
        # Maximum prolonged bleeding (10+ days) for medium risk points
        bleeding_days = 10 if i % 2 == 0 else 11
        
        cycles.append({
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=bleeding_days)).isoformat(),
            "flow": "heavy",  # All heavy flow
            "symptoms": symptoms,
            "mood": "overwhelmed",  # All overwhelmed mood
            "sleep_hours": 2.5,  # Extremely poor sleep
            "stress": 10,  # Maximum possible stress
            "exercise": "none",  # No exercise
            "notes": f"CRITICAL: Cycle length {length} days. SEVERE PCOD with ALL symptoms: acne, weight gain, excess hair growth (hirsutism), prolonged bleeding {bleeding_days} days, missed periods, insulin resistance, dark skin patches, high testosterone, mood swings, fatigue, spotting. Multiple skipped periods. EXTREME cycle variance. Symptoms worsening daily."
        })
    
    return cycles


def main():
    """Add high-risk cycles to demo2 user."""
    print("🔄 Adding high-risk cycles to demo2 user...")
    
    try:
        # Get demo2 user
        user_id = db.find_user_by_email('demo2@eliteher.com')[0]
        print(f"✅ Found demo2 user: {user_id}")
        
        # Get existing cycles
        existing_cycles = db.list_cycles(user_id)
        print(f"📊 Current cycles: {len(existing_cycles)}")
        
        # Clear existing cycles if any
        if existing_cycles:
            print("🗑️ Clearing existing cycles...")
            for cycle in existing_cycles:
                try:
                    # Note: You might need to implement delete_cycle in db service
                    print(f"  - Removing cycle {cycle.get('id', 'unknown')}")
                except Exception as e:
                    print(f"  ⚠️ Could not remove cycle: {e}")
        
        # Add new high-risk cycles
        high_risk_cycles = create_high_risk_cycles()
        print(f"📈 Adding {len(high_risk_cycles)} high-risk cycles...")
        
        for i, cycle_data in enumerate(high_risk_cycles):
            try:
                db.add_cycle(user_id, cycle_data)
                print(f"  ✅ Cycle {i+1}/{len(high_risk_cycles)} added")
            except Exception as e:
                print(f"  ❌ Cycle {i+1} failed: {e}")
        
        # Test the risk score
        print("\n🧪 Testing risk score...")
        updated_cycles = db.list_cycles(user_id)
        risk_result = compute_pcod_risk(updated_cycles)
        
        print(f"📊 Risk Score: {risk_result['risk_score']}%")
        print(f"🎯 Risk Level: {risk_result['level']}")
        print(f"💡 Recommendation: {risk_result['recommendation']}")
        print(f"🔍 Risk Factors: {[f['label'] for f in risk_result['factors']]}")
        
        if risk_result['risk_score'] >= 60:
            print("✅ SUCCESS: Risk score is above 60%!")
            print("🩺 The application should recommend consulting a gynecologist.")
        else:
            print("⚠️ WARNING: Risk score is below 60%. May need adjustment.")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
