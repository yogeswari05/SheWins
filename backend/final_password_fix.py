"""
Final fix: Update existing demo users with correct password hash.
"""
from __future__ import annotations

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.firebase_db import _get_firestore_client
from app.services import auth_password

def final_password_fix():
    """Update existing demo users with correct password hash."""
    print("🔧 Final password fix for demo users...")
    
    # Correct password hash for demo123456 (from generate_correct_hash.py)
    correct_hash = "$2b$12$iKhaQEI5ZG1Qrgs2NeBAKehKO40ZOdsrWxE/4wJaCgLqcPjnEKI/u"
    
    demo_emails = [
        "demo@eliteher.com",
        "sarah@eliteher.com", 
        "maya@eliteher.com"
    ]
    
    try:
        client = _get_firestore_client()
        
        for email in demo_emails:
            print(f"👤 Final update for: {email}")
            
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
                
                # Verify the update worked
                updated_doc = user_ref.get()
                updated_hash = updated_doc.to_dict().get("password_hash", "")
                is_valid = auth_password.verify_password("demo123456", updated_hash)
                print(f"  🔍 Final verification: {is_valid}")
                
                if is_valid:
                    print(f"  🎉 {email} login should work now!")
                else:
                    print(f"  ❌ {email} still not working!")
                
            else:
                print(f"  ❌ User {email} not found in Firebase!")
        
        print("\n🎉 Final password fix complete!")
        
        # Test login with db.find_user_by_email
        print("\n🔍 Testing login with db.find_user_by_email...")
        from app.services.db import find_user_by_email
        test_user = find_user_by_email("demo@eliteher.com")
        if test_user:
            user_id, stored_hash = test_user
            is_valid = auth_password.verify_password("demo123456", stored_hash)
            print(f"✅ Login test result: {is_valid}")
            if is_valid:
                print("🎉 LOGIN SHOULD WORK NOW!")
                print("📝 Try logging in with:")
                print("   Email: demo@eliteher.com")
                print("   Password: demo123456")
            else:
                print("❌ Login test still failed!")
        else:
            print("❌ Demo user not found!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_password_fix()
