"""
Generate correct password hash for demo123456.
"""
from __future__ import annotations

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import auth_password

def generate_and_test_hash():
    """Generate and test correct hash for demo123456."""
    print("🔐 Generating correct hash for demo123456...")
    
    password = "demo123456"
    correct_hash = auth_password.hash_password(password)
    
    print(f"🔐 Password: {password}")
    print(f"🔐 Correct hash: {correct_hash}")
    
    # Test the hash
    is_valid = auth_password.verify_password(password, correct_hash)
    print(f"✅ Verification result: {is_valid}")
    
    if is_valid:
        print("\n🎉 This is the correct hash!")
        print("📝 Update demo_data.py with this hash:")
        print(f'"password_hash": "{correct_hash}",  # demo123456')
    else:
        print("❌ Hash verification failed!")
    
    return correct_hash if is_valid else None

if __name__ == "__main__":
    generate_and_test_hash()
