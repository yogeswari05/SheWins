#!/usr/bin/env python3
"""
Test script to verify demo2 user gets >60% risk score and gynecologist recommendation.
"""

from app.services import db
from app.services.pcod_risk import compute_pcod_risk

def test_demo2_risk():
    """Test demo2 user risk assessment."""
    try:
        # Test demo2 user risk assessment
        user_id = db.find_user_by_email('demo2@eliteher.com')[0]
        cycles = db.list_cycles(user_id)
        risk_result = compute_pcod_risk(cycles)

        print('=== DEMO2 USER RISK ASSESSMENT ===')
        print(f'Email: demo2@eliteher.com')
        print(f'User ID: {user_id}')
        print(f'Number of Cycles: {len(cycles)}')
        print(f'Risk Score: {risk_result["risk_score"]}%')
        print(f'Risk Level: {risk_result["level"]}')
        print(f'Recommendation: {risk_result["recommendation"]}')
        print()
        print('Risk Factors:')
        for factor in risk_result['factors']:
            print(f'  - {factor["label"]} ({factor["tier"]} risk)')
        print()
        
        if risk_result['risk_score'] >= 60:
            print('✅ SUCCESS: User will be recommended to see a gynecologist!')
            return True
        else:
            print('❌ FAILED: User will NOT be recommended to see a gynecologist')
            return False
            
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == "__main__":
    test_demo2_risk()
