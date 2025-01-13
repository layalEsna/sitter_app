from app import app  # Import the Flask app
from models import db, PetOwner  # Import the database and PetOwner model

def test_password_handling():
    user = PetOwner(user_name="testuser")

    # Test invalid password
    try:
        user.password = "Invalid"  # Should raise a ValueError
    except ValueError as e:
        print(f"Validation failed as expected: {e}")

    # Test valid password
    user.password = "ValidPass1!"
    print(f"Hashed Password: {user._hash_password}")  # Should display the hashed password
    print(f"Password Check: {user.check_password('ValidPass1!')}")  # Should return True

if __name__ == "__main__":
    with app.app_context():  # If using Flask
        db.create_all()  # Ensure the database is initialized
        test_password_handling()
