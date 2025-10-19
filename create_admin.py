"""Create an admin user for the AI Product Management System"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import User
import mongoengine
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        mongoengine.connect(host=app.config['MONGO_URI'])
        
        # Admin 
        admin_email = "admin@example.com"
        admin_password = "admin123"
        
        try:
            # Checking if admin already exists
            existing_admin = User.objects(email=admin_email).first()
            if existing_admin:
                print(f"⚠️  Admin user already exists: {admin_email}")
                # Updating existing user to have proper hashed password
                existing_admin.password = generate_password_hash(admin_password, method="pbkdf2:sha256")
                existing_admin.roles = ["admin", "client"]
                existing_admin.save()
                print("✅ Updated existing admin with proper password hash")
                print(f"🔑 Password: {admin_password}")
                print("🚀 You can now login at: http://127.0.0.1:5000/auth/login")
                return
            
            # Creating new admin user with hashed password
            hashed_password = generate_password_hash(admin_password, method="pbkdf2:sha256")
            admin_user = User(
                email=admin_email,
                password=hashed_password,
                roles=["admin", "client"]
            )
            admin_user.save()
            
            print("✅ Admin user created successfully!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Password: {admin_password}")
            print("\n🚀 Now you can:")
            print("1. Login at: http://127.0.0.1:5000/auth/login")
            print("2. Go to products: http://127.0.0.1:5000/products/")
            print("3. You'll see ADD, EDIT, DELETE buttons!")
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_admin_user()