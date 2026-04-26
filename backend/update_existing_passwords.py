"""
Force update existing demo user passwords in Firebase.
"""
from __future__ import annotations

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.firebase_db import _get_firestore_client
from app.services import auth_password

def update_existing_demo_passwords():
    """Force update existing demo users with correct password hash."""
    print("🔧 Force updating existing demo user passwords...")
    
    # Correct password hash for demo123456
    correct_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO."
    
    demo_emails = [
        "demo@eliteher.com",
        "sarah@eliteher.com", 
        "maya@eliteher.com"
    ]
    
    try:
        client = _get_firestore_client()
        
        for email in demo_emails:
            print(f"👤 Updating password for: {email}")
            
            # Find user by email in Firebase
            users_ref = client.collection("users")
            query = users_ref.where("email", "==", email).limit(1)
            docs = list(query.stream())
            
            if docs:
                user_doc = docs[0]
                user_id = user_doc.id
                print(f"  📝 Found user ID: {user_id}")
                
                # Update password hash
                user_ref = client.collection("users").document(user_id)
                user_ref.update({"password_hash": correct_hash})
                print(f"  ✅ Password updated for {email}")
                
                # Test the new password
                stored_hash = user_doc.to_dict().get("password_hash", "")
                is_valid = auth_password.verify_password("demo123456", stored_hash)
                print(f"  🔍 Test with old hash: {is_valid}")
                
                # Verify update worked
                updated_doc = user_ref.get()
                updated_hash = updated_doc.to_dict().get("password_hash", "")
                is_new_valid = auth_password.verify_password("demo123456", updated_hash)
                print(f"  🔍 Test with new hash: {is_new_valid}")
                
            else:
                print(f"  ❌ User {email} not found in Firebase!")
        
        print("\n🎉 Demo passwords updated!")
        
        # Final login test
        print("\n🔍 Final login test...")
        from app.services.db import find_user_by_email
        test_user = find_user_by_email("demo@eliteher.com")
        if test_user:
            user_id, stored_hash = test_user
            is_valid = auth_password.verify_password("demo123456", stored_hash)
            print(f"✅ Final login test result: {is_valid}")
            if is_valid:
                print("🎉 Login should work now!")
            else:
                print("❌ Still not working!")
        else:
            print("❌ Demo user not found!")
        
    except Exception as e:
        print(f"❌ Error updating passwords: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_existing_demo_passwords()
